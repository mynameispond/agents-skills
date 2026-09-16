"""Dependency-free checks of this repository's skill discovery contracts.

The frontmatter checks cover the single-line name/description fields used here;
they are not a general YAML parser or a test of agent behavior.
"""

from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest


repo_root = Path(__file__).resolve().parents[1]
skills_root = repo_root / ".agents" / "skills"


class SkillStructureTests(unittest.TestCase):
    def setUp(self):
        self.skill_paths = sorted(skills_root.glob("*/SKILL.md"))
        self.assertTrue(self.skill_paths, "No discoverable skills found")

    def read_fields(self, path):
        content = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
        self.assertIsNotNone(match, f"Missing frontmatter: {path}")
        fields = {}
        for key in ("name", "description"):
            values = re.findall(rf"^{key}:[ \t]*([^\n]+)$", match.group(1), re.MULTILINE)
            self.assertEqual(len(values), 1, f"Expected one {key}: {path}")
            value = values[0].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            self.assertTrue(value, f"Empty {key}: {path}")
            fields[key] = value
        return fields

    def test_skill_names_are_valid_and_match_discovery_directories(self):
        seen = set()
        for path in self.skill_paths:
            with self.subTest(skill=path.parent.name):
                name = self.read_fields(path)["name"]
                self.assertRegex(name, r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
                self.assertLessEqual(len(name), 64)
                self.assertEqual(name, path.parent.name)
                self.assertNotIn(name, seen, "Duplicate skill name")
                seen.add(name)

    def test_descriptions_fit_discovery_limits(self):
        for path in self.skill_paths:
            with self.subTest(skill=path.parent.name):
                self.assertLessEqual(len(self.read_fields(path)["description"]), 1024)

    def test_empty_metadata_does_not_consume_the_following_field(self):
        samples = {
            "name": "---\nname:\ndescription: Use when testing.\nlicense: MIT\n---\n",
            "description": "---\nname: sample\ndescription:\nlicense: MIT\n---\n",
        }
        with TemporaryDirectory(prefix="skill-frontmatter-test-") as folder:
            path = Path(folder) / "SKILL.md"
            for field, content in samples.items():
                with self.subTest(field=field):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises(AssertionError):
                        self.read_fields(path)

    def test_skill_markdown_reference_targets_exist(self):
        for path in sorted(skills_root.rglob("*.md")):
            content = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                with self.subTest(file=path.relative_to(repo_root), target=target):
                    self.assertTrue((path.parent / target.split("#", 1)[0]).is_file())

    def test_checkpoint_requires_explicit_invocation(self):
        metadata = skills_root / "agent-checkpoint" / "agents" / "openai.yaml"
        self.assertTrue(metadata.is_file(), "Checkpoint invocation policy is missing")
        policies = re.findall(
            r"^policy:[ \t]*\n((?:[ \t]+[^\n]*(?:\n|$)|\n)*)",
            metadata.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        self.assertEqual(len(policies), 1, "Expected one checkpoint policy block")
        settings = re.findall(
            r"^[ \t]+allow_implicit_invocation:[ \t]*([^\n]*)$",
            policies[0],
            re.MULTILINE,
        )
        self.assertEqual(settings, ["false"], "Checkpoint must remain explicit-only")

    def test_ui_default_prompts_invoke_the_discoverable_skill(self):
        for path in self.skill_paths:
            metadata = path.parent / "agents" / "openai.yaml"
            if not metadata.exists():
                continue
            with self.subTest(skill=path.parent.name):
                match = re.search(
                    r"^[ \t]*default_prompt:[ \t]*(.+)$",
                    metadata.read_text(encoding="utf-8"),
                    re.MULTILINE,
                )
                self.assertIsNotNone(match, f"Missing default_prompt: {metadata}")
                mentions = re.findall(r"\$([a-z0-9]+(?:-[a-z0-9]+)*)", match.group(1))
                self.assertIn(self.read_fields(path)["name"], mentions)


if __name__ == "__main__":
    unittest.main()
