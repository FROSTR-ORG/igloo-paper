from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from .generated import manifest_path, prune_stale_generated_files


class GeneratedFilePruningTest(unittest.TestCase):
    def test_prunes_previous_manifest_entries_that_are_no_longer_generated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            stale = repo_root / "screens" / "create" / "old-screen" / "screen.html"
            current = repo_root / "screens" / "create" / "new-screen" / "screen.html"
            manual = repo_root / "screens" / "create" / "old-screen" / "notes.txt"
            stale.parent.mkdir(parents=True)
            current.parent.mkdir(parents=True)
            stale.write_text("stale\n")
            current.write_text("current\n")
            manual.write_text("manual\n")
            manifest_path(repo_root).write_text(
                json.dumps(
                    {
                        "version": 1,
                        "files": [
                            {"path": "screens/create/old-screen/screen.html", "kind": "html"},
                            {"path": "screens/create/new-screen/screen.html", "kind": "html"},
                        ],
                    },
                ),
            )

            pruned = prune_stale_generated_files(repo_root, [current])

            self.assertEqual(pruned, ["screens/create/old-screen/screen.html"])
            self.assertFalse(stale.exists())
            self.assertTrue(current.exists())
            self.assertTrue(manual.exists())
            self.assertTrue(stale.parent.exists())

    def test_removes_empty_directories_after_pruning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            stale = repo_root / "screens" / "shared" / "old-screen" / "screen.html"
            stale.parent.mkdir(parents=True)
            stale.write_text("stale\n")
            manifest_path(repo_root).write_text(
                json.dumps(
                    {
                        "version": 1,
                        "files": [
                            {"path": "screens/shared/old-screen/screen.html", "kind": "html"},
                        ],
                    },
                ),
            )

            pruned = prune_stale_generated_files(repo_root, [])

            self.assertEqual(pruned, ["screens/shared/old-screen/screen.html"])
            self.assertFalse(stale.parent.exists())


if __name__ == "__main__":
    unittest.main()
