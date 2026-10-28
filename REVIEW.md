# Project review — October 28, 2026

The checkout contains a proposal, a development plan with PostgreSQL DDL, an ER diagram, and working public Nutrislice menu collectors. There is no executable database migration/import pipeline or Flask/Expo application in this checkout. The CSV export is collected source data; refreshing it does not populate a running PostgreSQL database.

The archive has useful source provenance: separate food versions, dated menu appearances, station information, complete source food JSON, and explicit empty-menu coverage. Preserve these distinctions when importing it.

Findings, in priority order:

1. **Ratings can refer to a dish that was not on the selected menu.** In `devplan.html`, the `Rating` definition references `Dish` and `Menu` independently. Add a composite foreign key from `(menu_id, dish_id)` to `MenuDish(menu_id, dish_id)` for menu-specific ratings. Also add a score check once the rating scale is chosen; `NUMERIC(3,1)` alone allows negative and out-of-scale scores.

2. **General dish ratings can repeat for the same student.** `Rating.menu_id` is nullable, so `UNIQUE (student_id, dish_id, menu_id)` does not prevent multiple rows with a null menu. Decide whether general dish ratings are supported; if so, add a unique partial index on `(student_id, dish_id) WHERE menu_id IS NULL`, while retaining the constraint for menu-specific ratings.

3. **The comments schema cannot implement the proposed discussion model.** `project.html` promises nested replies and comments attached to a meal period, but `Comment` in `devplan.html` has neither a parent-comment reference nor a menu reference. Add those relationships and define valid comment targets before implementing the feature.

4. **The source-to-database mapping is still missing.** `Dish` has no Nutrislice source ID or food-version relationship, and `MenuDish` collapses multiple station appearances of a dish into one pair. Add explicit source identity/version and occurrence mappings before building an idempotent importer. Keep station appearances available even if the app also exposes a distinct-dishes-per-menu view. The archive joins occurrences to food details using `food_version_id`, not food name.

The development plan also says twelve relations but defines eleven `CREATE TABLE` statements. Reconcile the plan with the executable schema when migrations are added.

The collector's fixed October 7 cutoff and stale boundary-week cache behavior were addressed during this refresh. Regression tests cover extending a partially archived week, retaining previous food details, repeat-run idempotency, missing coverage, empty menus, and rejecting an earlier cutoff. The schema findings above are review items; the proposed DDL has not been changed or executed.
