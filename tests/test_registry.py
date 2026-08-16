#!/usr/bin/env python3
"""
Unit tests for registry.json and skill model tier configurations.
"""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "registry.json"


class TestRegistryAndSkillConfiguration(unittest.TestCase):
    def setUp(self):
        self.assertTrue(REGISTRY_PATH.exists(), f"registry.json not found at {REGISTRY_PATH}")
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

    def test_registry_top_level_fields(self):
        required_fields = ["name", "version", "compatibility", "skills"]
        for field in required_fields:
            self.assertIn(field, self.registry, f"Missing required top-level field '{field}' in registry.json")

    def test_skills_metadata_and_files(self):
        skills = self.registry.get("skills", [])
        self.assertGreater(len(skills), 0, "No skills registered in registry.json")

        for skill in skills:
            skill_name = skill.get("name")
            self.assertIsNotNone(skill_name, "Skill entry missing 'name'")

            # Check required fields
            for field in ["name", "version", "path", "entrypoint", "readme", "triggers", "runtimes", "models"]:
                self.assertIn(field, skill, f"Skill '{skill_name}' missing field '{field}'")

            # Check paths exist
            skill_dir = REPO_ROOT / skill["path"]
            self.assertTrue(skill_dir.is_dir(), f"Skill directory not found: {skill_dir}")

            entrypoint = skill_dir / skill["entrypoint"]
            self.assertTrue(entrypoint.is_file(), f"Skill entrypoint not found: {entrypoint}")

            readme = skill_dir / skill["readme"]
            self.assertTrue(readme.is_file(), f"Skill README not found: {readme}")

            if "schema" in skill:
                schema_path = skill_dir / skill["schema"]
                self.assertTrue(schema_path.is_file(), f"Skill schema not found: {schema_path}")

            if "validator" in skill:
                validator_path = skill_dir / skill["validator"]
                self.assertTrue(validator_path.is_file(), f"Skill validator not found: {validator_path}")

    def test_model_tiering_configuration(self):
        skills = self.registry.get("skills", [])
        for skill in skills:
            skill_name = skill.get("name")
            models = skill.get("models", {})

            self.assertIn("reasoning_tier", models, f"Skill '{skill_name}' missing models.reasoning_tier")
            self.assertIn("lightweight_tier", models, f"Skill '{skill_name}' missing models.lightweight_tier")

            for tier in ["reasoning_tier", "lightweight_tier"]:
                tier_data = models[tier]
                self.assertIn("recommended", tier_data, f"Skill '{skill_name}' {tier} missing 'recommended'")
                recommended = tier_data["recommended"]
                self.assertIn("gemini", recommended, f"Skill '{skill_name}' {tier} missing gemini model")
                self.assertIn("claude", recommended, f"Skill '{skill_name}' {tier} missing claude model")
                self.assertIn("codex", recommended, f"Skill '{skill_name}' {tier} missing codex model")

    def test_skill_md_frontmatter_models(self):
        skills = self.registry.get("skills", [])
        for skill in skills:
            entrypoint_path = REPO_ROOT / skill["path"] / skill["entrypoint"]
            content = entrypoint_path.read_text(encoding="utf-8")

            # Check that frontmatter exists and contains models definitions
            self.assertTrue(content.startswith("---"), f"{entrypoint_path} does not start with YAML frontmatter")
            self.assertIn("models:", content, f"{entrypoint_path} frontmatter missing 'models:' section")
            self.assertIn("reasoning_tier:", content, f"{entrypoint_path} frontmatter missing 'reasoning_tier:'")
            self.assertIn("lightweight_tier:", content, f"{entrypoint_path} frontmatter missing 'lightweight_tier:'")


if __name__ == "__main__":
    unittest.main()
