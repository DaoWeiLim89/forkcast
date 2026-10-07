import csv
import json
from pathlib import Path
from urllib.request import urlopen

# IDs and URL templates come from https://nd.api.nutrislice.com/menu/api/schools/
base = "https://nd.api.nutrislice.com"  # Notre Dame's Nutrislice API
school_id = 58415  # North Dining Hall (South: 58414)
meal_id = 28583  # Lunch (Breakfast: 28582, Dinner: 28863)
date = "2026/10/7"  # Year/month/day; the endpoint returns the containing week
url = f"{base}/menu/api/weeks/school/{school_id}/menu-type/{meal_id}/{date}"


def save_json(data, path):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def save_csv(data, path):
    rows = []
    for day in data["days"]:
        for item in day["menu_items"]:
            food = item.get("food")
            if not food:
                continue
            rows.append({
                "date": day["date"],
                "food_id": food["id"],
                "name": food["name"],
                "ingredients": food.get("ingredients"),
                **(food.get("serving_size_info") or {}),
                **(food.get("rounded_nutrition_info") or {}),
                "source_url": url,
            })
    columns = list(dict.fromkeys(key for row in rows for key in row)) or ["date", "name"]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)  # Missing values become blank cells, not zero.


if __name__ == "__main__":
    with urlopen(url, timeout=30) as response:
        data = json.load(response) 

    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    filename = f"{school_id}_{meal_id}_week-of-{date.replace('/', '-')}"
    json_path = output / f"{filename}.json"
    csv_path = output / f"{filename}.csv"
    save_json(data, json_path)
    save_csv(data, csv_path)
    print(f"JSON saved to {json_path}\nCSV saved to {csv_path}")
