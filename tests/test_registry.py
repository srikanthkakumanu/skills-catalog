#!/usr/bin/env python3
"""
Unit tests for registry.json, model tiering, scope boundaries, and context window optimization configurations.
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
        required_fields = ["name", "version", "compatibility", "context_standards", "skills"]
        for field in required_fields:
            self.assertIn(field, self.registry, f"Missing required top-level field '{field}' in registry.json")

    def test_context_standards(self):
        standards = self.registry.get("context_standards", {})
        self.assertTrue(standards.get("progressive_loading"), "context_standards.progressive_loading should be true")
        self.assertTrue(standards.get("subagent_isolation"), "context_standards.subagent_isolation should be true")
        self.assertTrue(standards.get("targeted_file_slicing"), "context_standards.targeted_file_slicing should be true")

    def test_skills_metadata_and_files(self):
        skills = self.registry.get("skills", [])
        self.assertGreater(len(skills), 0, "No skills registered in registry.json")

        for skill in skills:
            skill_name = skill.get("name")
            self.assertIsNotNone(skill_name, "Skill entry missing 'name'")

            # Check required fields
            for field in ["name", "version", "path", "entrypoint", "readme", "triggers", "runtimes", "scopes", "models", "context_optimization"]:
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

    def test_scope_configuration(self):
        skills = self.registry.get("skills", [])
        for skill in skills:
            skill_name = skill.get("name")
            scopes = skill.get("scopes", {})
            self.assertIn("supported", scopes, f"Skill '{skill_name}' missing scopes.supported")
            self.assertIn("default", scopes, f"Skill '{skill_name}' missing scopes.default")
            self.assertEqual(scopes["default"], "mvp")
            for expected_scope in ["prototype", "mvp", "full"]:
                self.assertIn(expected_scope, scopes["supported"])

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

    def test_skill_md_frontmatter_and_directives(self):
        skills = self.registry.get("skills", [])
        for skill in skills:
            entrypoint_path = REPO_ROOT / skill["path"] / skill["entrypoint"]
            content = entrypoint_path.read_text(encoding="utf-8")

            # Check that frontmatter exists and contains models, context, and scopes definitions
            self.assertTrue(content.startswith("---"), f"{entrypoint_path} does not start with YAML frontmatter")
            self.assertIn("models:", content, f"{entrypoint_path} frontmatter missing 'models:' section")
            self.assertIn("reasoning_tier:", content, f"{entrypoint_path} frontmatter missing 'reasoning_tier:'")
            self.assertIn("lightweight_tier:", content, f"{entrypoint_path} frontmatter missing 'lightweight_tier:'")
            self.assertIn("context_optimization:", content, f"{entrypoint_path} frontmatter missing 'context_optimization:'")
            self.assertIn("scopes:", content, f"{entrypoint_path} frontmatter missing 'scopes:' section")
            self.assertIn("Directive 4: Strict Context Window Optimization", content, f"{entrypoint_path} missing Directive 4")
            self.assertIn("Directive 5: Strict Scope Boundary Control", content, f"{entrypoint_path} missing Directive 5")


if __name__ == "__main__":
    unittest.main()
