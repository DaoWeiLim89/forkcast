# Forkcast

Notre Dame dining menu archive and plans for a student dining review and recommendation app. The stack is PostgreSQL, Django/Python, and Expo/React. This checkout currently contains the project documents and the Nutrislice data collector; it does not yet contain a database migration, database importer, or application backend.

- [Project proposal](project.html)
- [Development plan and proposed SQL schema](devplan.html)
- [Project review, October 28, 2026](REVIEW.md)
- [Menu archive and data dictionary](nutrislice-demo/output/history/README.md)
- [Archive coverage and counts](nutrislice-demo/output/history/summary.json)

From this directory, extend the existing archive through today in South Bend:

```sh
python3 nutrislice-demo/download_history.py
```

To choose an explicit cutoff:

```sh
python3 nutrislice-demo/download_history.py --end-date 2026-10-28
```

The collector preserves exported dates and food versions, downloads newly requested days for both dining halls and all four meal types, and checks complete daily coverage before updating the exports. Newly requested weeks are fetched again even when cached, since previously unpublished days may now be available. Repeating the same cutoff makes no changes; this command extends a historical snapshot rather than revising previously exported menus.

Run the collector's regression tests:

```sh
cd nutrislice-demo
python3 -m unittest -v test_download_history.py
```
