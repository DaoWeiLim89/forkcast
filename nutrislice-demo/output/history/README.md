# Notre Dame menu archive

Requested coverage: August 16 through October 28, 2026, inclusive. North and South Dining Halls; breakfast, lunch, dinner, and brunch. The October 28 refresh added October 8–28 while preserving all previously exported rows. Requests are paced and compressed source responses are cached. Empty responses are recorded in coverage.csv; they do not prove a hall was closed.

- `menu_occurrences.csv`: One source food entry on a dated hall/meal menu. Distinct station appearances remain separate. Repeat retrievals do not add copies. Contains names for browsing, source URLs, station information, and the source item's remaining fields in `source_item_json`.
- `foods.csv`: Shared food details, nutrition, ingredients, serving sizes, and diet/allergen labels. Join to occurrences on `food_version_id`. A source food ID may have multiple versions if its source details differ; historical details are never silently overwritten. `source_food_json` preserves the complete food object, including fields not flattened into columns.
- `coverage.csv`: Every requested date/hall/meal and its food-entry count, including empty menus.
- `summary.json`: Actual coverage, counts, and CSV sizes.

Nutritional units are in column names (g, mg, mcg, etc.). Blank nutrient values mean unavailable, not zero. Serving size must be considered: some source portions are entire pizzas or bulk containers. An empty allergen-label list does not establish that a food is allergen-free.

The archive stops at October 28 even when the weekly response includes later dates. It now contains 57,199 menu occurrences, 1,568 distinct source food IDs, and 1,766 food versions; the refresh added 17,142 occurrences and 140 distinct food IDs. Actual populated dates run from August 30 through October 28. There are 592 date/hall/meal coverage rows, including empty menus.

Compressed source responses are cached in ../../.cache/history. Earlier data and all future availability have not been exhaustively surveyed. The small fetch_menu.py manager demonstration remains an October 7 example; download_history.py performs this larger export.

Run `python3 download_history.py` from the nutrislice-demo directory to extend through today in South Bend, or specify `--end-date YYYY-MM-DD`. The command loads the existing archive and adds only later dates. Newly requested weeks bypass cached responses, including a partly archived boundary week. Existing dated occurrences and food versions remain unchanged. Repeating the same cutoff makes no changes; previously exported menus are snapshots and are not automatically revised for later source edits. An earlier cutoff is rejected rather than truncating the archive. Missing or duplicate daily coverage aborts the export.
