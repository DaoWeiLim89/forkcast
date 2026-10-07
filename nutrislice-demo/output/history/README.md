# Notre Dame menu archive

Requested coverage: August 16 through October 7, 2026, inclusive. North and South Dining Halls; breakfast, lunch, dinner, and brunch. Each hall/meal/week is retrieved once, with local caching and paced requests. Empty responses are recorded in coverage.csv; they do not prove a hall was closed.

- `menu_occurrences.csv`: One source food entry on a dated hall/meal menu. Distinct station appearances remain separate. Repeat retrievals do not add copies. Contains names for browsing, source URLs, station information, and the source item's remaining fields in `source_item_json`.
- `foods.csv`: Shared food details, nutrition, ingredients, serving sizes, and diet/allergen labels. Join to occurrences on `food_version_id`. A source food ID may have multiple versions if its source details differ; historical details are never silently overwritten. `source_food_json` preserves the complete food object, including fields not flattened into columns.
- `coverage.csv`: Every requested date/hall/meal and its food-entry count, including empty menus.
- `summary.json`: Actual coverage, counts, and CSV sizes.

Nutritional units are in column names (g, mg, mcg, etc.). Blank nutrient values mean unavailable, not zero. Serving size must be considered: some source portions are entire pizzas or bulk containers. An empty allergen-label list does not establish that a food is allergen-free.

The archive stops at October 7 even when the weekly response includes later dates. Compressed source responses are cached in ../../.cache/history. Earlier data and all future availability have not been exhaustively surveyed. The small fetch_menu.py manager demonstration is unchanged; download_history.py performs this larger export.
