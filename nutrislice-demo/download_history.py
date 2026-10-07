import csv
import gzip
import hashlib
import json
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output' / 'history'
CACHE = ROOT / '.cache' / 'history'
BASE = 'https://nd.api.nutrislice.com'
START, END = date(2026, 8, 16), date(2026, 10, 7)
HALLS = {58415: 'North Dining Hall', 58414: 'South Dining Hall'}
MEALS = {28582: 'Breakfast', 28583: 'Lunch', 28863: 'Dinner', 28865: 'Brunch'}


def get(url):
    digest = hashlib.sha256(url.encode()).hexdigest()
    cached = CACHE / (digest + '.json.gz')
    previous = ROOT / '.cache' / (digest + '.json')
    if cached.exists():
        with gzip.open(cached, 'rt') as f:
            return json.load(f)
    if previous.exists():
        return json.loads(previous.read_text())
    time.sleep(1)
    with urlopen(Request(url, headers={'User-Agent': 'ND-class-menu-archive/1.0'}), timeout=60) as response:
        data = json.load(response)
    with gzip.open(cached, 'wt') as f:
        json.dump(data, f)
    return data


def write_csv(name, rows):
    columns = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    foods, occurrences, coverage = {}, {}, []
    week = START
    while week <= END:
        for hall_id, hall in HALLS.items():
            for meal_id, meal in MEALS.items():
                url = f'{BASE}/menu/api/weeks/school/{hall_id}/menu-type/{meal_id}/{week.year}/{week.month}/{week.day}'
                data = get(url)
                count = 0
                for day in data['days']:
                    if not START.isoformat() <= day['date'] <= END.isoformat():
                        continue
                    stations = {i.get('station_id'): i.get('text', '') for i in day['menu_items'] if i.get('is_station_header')}
                    daily = 0
                    for item in day['menu_items']:
                        food = item.get('food')
                        if not food:
                            continue
                        # Preserve distinct source versions rather than overwrite historical nutrition.
                        version = hashlib.sha256(json.dumps(food, sort_keys=True).encode()).hexdigest()
                        if version not in foods:
                            foods[version] = {
                                'food_version_id': version, 'food_id': food['id'],
                                'name': food['name'], 'description': food.get('description'),
                                'ingredients': food.get('ingredients'),
                                **(food.get('serving_size_info') or {}),
                                **(food.get('rounded_nutrition_info') or {}),
                                'diet_and_allergen_labels': '; '.join(i['name'] for i in (food.get('icons') or {}).get('food_icons', []) if i.get('enabled')),
                                'has_nutrition_info': food.get('has_nutrition_info'),
                                'source_food_json': json.dumps(food, ensure_ascii=False, separators=(',', ':')),
                            }
                        key = (hall_id, meal_id, day['date'], item['id'])
                        row = {
                            'date': day['date'], 'hall_id': hall_id, 'hall': hall,
                            'meal_id': meal_id, 'meal': meal, 'menu_item_id': item['id'],
                            'station_id': item.get('station_id'), 'station': stations.get(item.get('station_id'), ''),
                            'food_id': food['id'], 'food_version_id': version, 'name': food['name'],
                            'source_last_updated': data.get('last_updated'), 'source_url': url,
                            'source_item_json': json.dumps({k: v for k, v in item.items() if k != 'food'}, ensure_ascii=False, separators=(',', ':')),
                        }
                        if key in occurrences and occurrences[key]['food_version_id'] != version:
                            raise ValueError(f'Conflicting occurrence: {key}')
                        occurrences[key] = row
                        daily += 1
                    coverage.append({'date': day['date'], 'hall': hall, 'meal': meal, 'food_entries': daily, 'source_url': url})
                    count += daily
                print(f'{week} | {hall} | {meal}: {count}', flush=True)
        week += timedelta(days=7)
    write_csv('foods.csv', list(foods.values()))
    write_csv('menu_occurrences.csv', sorted(occurrences.values(), key=lambda r: (r['date'], r['hall'], r['meal'], r['menu_item_id'])))
    write_csv('coverage.csv', coverage)
    summary = {
        'requested_start': str(START), 'requested_end': str(END),
        'earliest_populated_date': min(r['date'] for r in occurrences.values()),
        'latest_populated_date': max(r['date'] for r in occurrences.values()),
        'distinct_food_ids': len({f['food_id'] for f in foods.values()}),
        'food_versions': len(foods), 'menu_occurrences': len(occurrences),
        'csv_bytes': {p.name: p.stat().st_size for p in OUT.glob('*.csv')},
    }
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
