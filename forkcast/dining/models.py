from django.db import models

# Create your models here.
    
class Dish(models.Model):
    food_version_id = models.CharField(max_length=255, unique=True)
    food_id = models.CharField(max_length=255, db_index=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)

    serving_size_amount = models.FloatField(null=True, blank=True)
    serving_size_unit = models.CharField(max_length=100, blank=True)

    calories = models.FloatField(null=True, blank=True)

    g_fat = models.FloatField(null=True, blank=True)
    g_saturated_fat = models.FloatField(null=True, blank=True)
    g_trans_fat = models.FloatField(null=True, blank=True)
    g_carbs = models.FloatField(null=True, blank=True)
    g_added_sugar = models.FloatField(null=True, blank=True)
    g_sugar = models.FloatField(null=True, blank=True)
    g_fiber = models.FloatField(null=True, blank=True)
    g_protein = models.FloatField(null=True, blank=True)

    mg_cholesterol = models.FloatField(null=True, blank=True)
    mg_potassium = models.FloatField(null=True, blank=True)
    mg_sodium = models.FloatField(null=True, blank=True)
    mg_iron = models.FloatField(null=True, blank=True)
    mg_calcium = models.FloatField(null=True, blank=True)
    mg_vitamin_c = models.FloatField(null=True, blank=True)

    iu_vitamin_a = models.FloatField(null=True, blank=True)
    re_vitamin_a = models.FloatField(null=True, blank=True)
    mcg_vitamin_a = models.FloatField(null=True, blank=True)
    mg_vitamin_d = models.FloatField(null=True, blank=True)
    mcg_vitamin_d = models.FloatField(null=True, blank=True)

    diet_and_allergen_labels = models.JSONField(default=list, blank=True)
    has_nutrition_info = models.BooleanField(null=True, blank=True)
    source_food_json = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
    
class DiningHall(models.Model):
    hall_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Menu(models.Model):
    date = models.DateField()
    dining_hall = models.ForeignKey(DiningHall, on_delete=models.CASCADE, related_name="menus")
    meal_id = models.CharField(max_length=255)
    meal = models.CharField(max_length=255)

    dishes = models.ManyToManyField(Dish, through="MenuItem", related_name="menus")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "dining_hall", "meal_id"],
                name="unique_hall_date_meal",
            )
        ]

    def __str__(self):
        return f"{self.dining_hall.name} - {self.date} - {self.meal_period}"

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey("Dish", on_delete=models.PROJECT, related_name="menu_items")
    
    menu_item_id = models.CharField(max_length=255)
    station_id = models.CharField(max_length=255, blank=True)
    station = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)

    source_last_updated = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(max_length=2000, blank=True)
    source_item_json = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["menu", "dish", "station_id"],
                name="unique_menu_item_station",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.station})"