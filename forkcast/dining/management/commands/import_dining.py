import csv
from pathlib import Path
from datetime import date
from decimal import Decimal
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from dining.models import Dish, Menu, DiningHall, MenuItem

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Path(__file__).resolve().parents[4] / "db.sqlite3",
    }
}

foods_csv_path = (
    Path(__file__).resolve().parents[4]
    / "nutrislice-demo" / "output" / "history" / "foods.csv"
)

menus_occurrences_csv_path = (
    Path(__file__).resolve().parents[4]
    / "nutrislice-demo" / "output" / "history" / "menu_occurrences.csv"
)

def parse_number(value):
    return float(value) if value and value.strip() else None

def parse_boolean(value):
    value = (value or "").strip().lower()
    if not value:
        return None
    if value in ("true", "1"):
        return True
    if value in ("false", "0"):
        return False
    raise ValueError(f"Invalid boolean: {value!r}")

numeric_fields = [
    "serving_size_amount",
    "calories",
    "g_fat",
    "g_saturated_fat",
    "g_trans_fat",
    "mg_cholesterol",
    "g_carbs",
    "g_added_sugar",
    "g_sugar",
    "mg_potassium",
    "mg_sodium",
    "g_fiber",
    "g_protein",
    "mg_iron",
    "mg_calcium",
    "mg_vitamin_c",
    "iu_vitamin_a",
    "re_vitamin_a",
    "mcg_vitamin_a",
    "mg_vitamin_d",
    "mcg_vitamin_d",
]

csv.field_size_limit(10_000_000)

class Command(BaseCommand):
    help = "Import dining data from Nutrislice demo"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Importing dining data from Nutrislice demo...")
        self.import_foods()
        self.import_menus()
        self.stdout.write("Done!")



    def import_foods(self):

        with Path(foods_csv_path).open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                defaults = {
                    "food_id": row["food_id"],
                    "name": row["name"],
                    "ingredients": row["ingredients"],
                    "description": row["description"],
                    "serving_size_unit": row["serving_size_unit"],
                    "diet_and_allergen_labels": [
                        label.strip()
                        for label in row["diet_and_allergen_labels"].split(";")
                        if label.strip()
                    ],
                    "has_nutrition_info": parse_boolean(row["has_nutrition_info"]),
                    "source_food_json": json.loads(row["source_food_json"] or "{}"),
                }

                defaults.update({
                    field: parse_number(row[field])
                    for field in numeric_fields
                })

                Dish.objects.update_or_create(
                    food_version_id=row["food_version_id"],
                    defaults=defaults,
                )


    def import_menus(self):
        with Path(menus_occurrences_csv_path).open(newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                hall, _ = DiningHall.objects.update_or_create(
                    hall_id = row["hall_id"],
                    defaults = {
                        "name": row["hall"],
                    },
                )
                menu, _ = Menu.objects.update_or_create(
                    date = date.fromisoformat(row["date"]),
                    dining_hall=hall,
                    meal_id=row["meal_id"],
                    defaults={
                        "meal": row["meal"],
                    },
                )

                dish = Dish.objects.get(
                    food_version_id=row["food_version_id"],
                )

                MenuItem.objects.update_or_create(
                    menu=menu,
                    menu_item_id=row["menu_item_id"],
                    station_id=row["station_id"],
                    defaults={
                        "dish": dish,
                        "station": row["station"],
                        "name": row["name"],
                        "source_last_updated": row["source_last_updated"],
                        "source_url": row["source_url"],
                        "source_item_json": json.loads(
                            row["source_item_json"] or "{}"
                        ),
                    },
                )
        