import contextlib
import io
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import download_history as archive


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        for name, value in {
            'OUT': root / 'output', 'CACHE': root / 'cache',
            'START': date(2026, 10, 4), 'HALLS': {1: 'Hall'}, 'MEALS': {2: 'Lunch'},
        }.items():
            mocked = patch.object(archive, name, value)
            mocked.start()
            self.addCleanup(mocked.stop)

    def response(self, calories=100, empty=False):
        return {'days': [
            {'date': str(archive.START + timedelta(days=i)), 'menu_items': [] if empty else [
                {'id': 10 + i, 'food': {'id': 42, 'name': 'Food',
                                      'rounded_nutrition_info': {'calories': calories}}},
            ]} for i in range(7)
        ]}

    def run_archive(self, end, response):
        with patch.object(archive, 'get', return_value=response) as fetch:
            with contextlib.redirect_stdout(io.StringIO()):
                archive.main(date.fromisoformat(end))
        return fetch

    def snapshot(self):
        return {p.name: p.read_bytes() for p in archive.OUT.iterdir() if p.is_file()}

    def test_extension_refreshes_boundary_and_preserves_historical_versions(self):
        self.run_archive('2026-10-07', self.response())
        old_foods = archive.read_csv('foods.csv')
        old_rows = archive.read_csv('menu_occurrences.csv')
        fetch = self.run_archive('2026-10-08', self.response(calories=200))
        fetch.assert_called_once()
        self.assertTrue(fetch.call_args.kwargs['refresh'])
        rows = archive.read_csv('menu_occurrences.csv')
        self.assertEqual(rows[:4], old_rows)
        self.assertEqual(archive.read_csv('foods.csv')[0], old_foods[0])
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[-1]['date'], '2026-10-08')
        self.assertNotEqual(rows[-1]['food_version_id'], rows[0]['food_version_id'])
        summary = json.loads((archive.OUT / 'summary.json').read_text())
        self.assertEqual(summary['distinct_food_ids'], 1)
        self.assertEqual(summary['food_versions'], 2)
        self.assertEqual(len(archive.read_csv('coverage.csv')), 5)
        before = self.snapshot()
        fetch = self.run_archive('2026-10-08', self.response())
        fetch.assert_not_called()
        self.assertEqual(self.snapshot(), before)

    def test_missing_response_day_leaves_exports_unchanged(self):
        self.run_archive('2026-10-07', self.response())
        before = self.snapshot()
        response = self.response()
        response['days'] = response['days'][:4]
        with self.assertRaisesRegex(ValueError, 'coverage'):
            self.run_archive('2026-10-08', response)
        self.assertEqual(self.snapshot(), before)

    def test_empty_menus_are_recorded(self):
        self.run_archive('2026-10-07', self.response(empty=True))
        summary = json.loads((archive.OUT / 'summary.json').read_text())
        self.assertEqual(summary['menu_occurrences'], 0)
        self.assertIsNone(summary['latest_populated_date'])
        self.assertEqual(len(archive.read_csv('coverage.csv')), 4)

    def test_archive_cannot_be_shortened(self):
        self.run_archive('2026-10-07', self.response())
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'shorten'):
            self.run_archive('2026-10-06', self.response())
        self.assertEqual(self.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
