from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from . import verify


class VerifyMapConfigurationTest(unittest.TestCase):
    def test_map_total_is_derived_from_category_counts(self) -> None:
        self.assertEqual(
            verify.EXPECTED_MAP_TOTAL,
            sum(verify.EXPECTED_MAP_CATEGORY_COUNTS.values()),
        )


if __name__ == "__main__":
    unittest.main()
