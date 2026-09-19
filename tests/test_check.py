from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.check import REQUIRED, anchors, check, inventory, main, prose


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.files = {
            "AGENTS.md": "# Entry\n[README](README.md)\n[Policy](AGENT_DOCS_CONVENTION.md)\n[Adopt](ADOPTION.md)\n",
            "README.md": "# Readme\n",
            "AGENT_DOCS_CONVENTION.md": "# Policy\n\nGenre: contract\nCanonical for: policy\n\n## Rules\n",
            "ADOPTION.md": "# Adoption\n\nGenre: manual\nCanonical for: adoption\n",
        }
        for name, text in self.files.items():
            self.write(name, text)

    def write(self, name, text):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def result(self, extra=()):
        return check(self.root, list(self.files) + list(extra))

    def add(self, text):
        self.write("README.md", self.files["README.md"] + text)

    def test_valid(self):
        self.assertEqual(self.result().errors, [])
        self.assertEqual(self.result().documents, len(REQUIRED))

    def test_empty_inventory_fails(self):
        self.assertEqual(len(check(self.root, []).errors), len(REQUIRED))

    def test_missing_required(self):
        (self.root / "ADOPTION.md").unlink()
        self.assertTrue(any("required document" in e for e in self.result().errors))

    def test_empty_document_fails(self):
        self.write("ADOPTION.md", "")
        self.assertTrue(any("empty document" in e for e in self.result().errors))

    def test_invalid_utf8_fails(self):
        (self.root / "ADOPTION.md").write_bytes(b"\xff")
        self.assertTrue(any("cannot read" in e for e in self.result().errors))

    def test_bad_genre_fails(self):
        self.write("ADOPTION.md", self.files["ADOPTION.md"].replace("Genre: manual", "Genre: unknown"))
        self.assertTrue(any("Genre header" in e for e in self.result().errors))

    def test_empty_owner_fails(self):
        self.write("ADOPTION.md", self.files["ADOPTION.md"].replace("Canonical for: adoption", "Canonical for: "))
        self.assertTrue(any("Canonical for" in e for e in self.result().errors))

    def test_duplicate_header_fails(self):
        self.write("ADOPTION.md", self.files["ADOPTION.md"] + "Genre: contract\n")
        self.assertTrue(any("Genre header" in e for e in self.result().errors))

    def test_missing_link_fails(self):
        self.add("[Broken](missing.md)\n")
        self.assertTrue(any("missing file" in e for e in self.result().errors))

    def test_wrong_case_fails_on_all_platforms(self):
        self.add("[Bad case](agents.md)\n")
        self.assertTrue(any("filename case" in e for e in self.result().errors))

    def test_parent_escape_fails(self):
        self.add("[Outside](../outside.md)\n")
        self.assertTrue(any("escapes repository" in e for e in self.result().errors))

    def test_encoded_escape_fails(self):
        self.add("[Outside](%2E%2E/outside.md)\n")
        self.assertTrue(any("escapes repository" in e for e in self.result().errors))

    def test_valid_anchor(self):
        self.add("[Rules](AGENT_DOCS_CONVENTION.md#rules)\n")
        self.assertEqual(self.result().errors, [])

    def test_invalid_anchor_fails(self):
        self.add("[Bad](AGENT_DOCS_CONVENTION.md#absent)\n")
        self.assertTrue(any("missing heading" in e for e in self.result().errors))

    def test_unicode_and_duplicate_anchors(self):
        self.assertEqual(anchors("# 계약\n## 계약\n## 계약-1\n"), {"계약", "계약-1", "계약-1-1"})

    def test_external_links_are_not_verified(self):
        self.add("[External](https://example.invalid/missing.md)\n")
        result = self.result()
        self.assertEqual(result.errors, [])
        self.assertEqual(result.external_links, 1)

    def test_fenced_examples_are_not_links(self):
        self.add("```text\n[Not a link](missing.md)\n```\n")
        self.assertEqual(self.result().errors, [])
        self.assertNotIn("Not a link", prose("~~~\nNot a link\n~~~\n"))

    def test_fence_does_not_close_early(self):
        self.add("````text\n```\n[Example](missing.md)\n````\n")
        self.assertEqual(self.result().errors, [])

    def test_unreachable_document_fails(self):
        self.write("extra.md", "# Extra\nGenre: contract\nCanonical for: extra\n")
        self.assertTrue(any("unreachable" in e for e in self.result(["extra.md"]).errors))

    def test_transitive_document_is_reachable(self):
        self.write("extra.md", "# Extra\nGenre: contract\nCanonical for: extra\n")
        self.add("[Extra](extra.md)\n")
        self.assertEqual(self.result(["extra.md"]).errors, [])

    def test_conflict_marker_fails(self):
        self.add("<<<<<<< HEAD\nold\n=======\nnew\n>>>>>>> branch\n")
        self.assertTrue(any("conflict marker" in e for e in self.result().errors))

    def test_non_markdown_file_link(self):
        self.write("scripts/run.py", "print('ok')\n")
        self.add("[Script](scripts/run.py)\n")
        self.assertEqual(self.result().errors, [])

    def test_git_failure_is_not_empty_success(self):
        failed = subprocess.CompletedProcess([], 128, b"", b"not a repository")
        with patch("scripts.check.subprocess.run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "Git inventory failed"):
                inventory(self.root)

    def test_main_inventory_failure_exit(self):
        with patch("scripts.check.inventory", side_effect=RuntimeError("inventory unavailable")):
            self.assertEqual(main(), 2)

    def test_inventory_excludes_ignored_files(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        self.write(".gitignore", ".local/\n")
        self.write(".local/task.md", "# Temporary\n")
        self.assertEqual(set(inventory(self.root)), REQUIRED)


if __name__ == "__main__":
    unittest.main()
