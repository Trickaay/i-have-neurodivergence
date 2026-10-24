#!/usr/bin/env python3
"""Filesystem regression tests. No host configuration or installed skills touched."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_pack", ROOT / "scripts/install_pack.py")
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


def snapshot(root):
    result = {}
    for p in sorted(root.rglob("*")):
        name = p.relative_to(root).as_posix()
        if p.is_symlink():
            result[name] = ("link", os.readlink(p))
        elif p.is_file():
            result[name] = ("file", hashlib.sha256(p.read_bytes()).hexdigest())
        elif p.is_dir():
            result[name] = ("directory",)
    return result


class InstallationTests(unittest.TestCase):
    def setUp(self):
        # /tmp can be a symlink on macOS. The helper intentionally rejects it.
        base = "/private/tmp" if Path("/private/tmp").is_dir() else None
        self.temp = tempfile.TemporaryDirectory(prefix="pack test ", dir=base)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "Downloaded pack"
        self.source.mkdir()
        (self.source / ".claude-plugin").mkdir()
        (self.source / ".claude-plugin/plugin.json").write_text('{"version":"0.4.7"}')
        for host in ("codex", "hermes"):
            hostroot = self.source / pack.HOST_ROOTS[host]
            for i in range(31):
                skill = hostroot / f"skill-{i:02}"
                (skill / "references/empty").mkdir(parents=True)
                (skill / "SKILL.md").write_text(f"---\nname: skill-{i:02}\n---\nFixture {host} {i}\n")
                (skill / "references/.hidden").write_text("hidden metadata\n")
        self.project = self.root / "My Project/.agents"
        self.project.mkdir(parents=True)
        self.destination = self.project / "skills"

    def tearDown(self):
        self.temp.cleanup()

    def install(self, apply=True, host="codex"):
        return pack.install(self.source, self.destination, host, "project", "fixture:independent-test", apply)

    def record(self):
        return Path(self.install()["record"])

    def refusal_unchanged(self, call):
        before = snapshot(self.root)
        with self.assertRaises((pack.Refusal, OSError)):
            call()
        self.assertEqual(snapshot(self.root), before)

    def make_manifest(self):
        inv = pack.inventory(self.source)
        files = {n: {"bytes": e["bytes"], "sha256": e["sha256"]} for n, e in inv.items() if e["type"] == "file"}
        (self.source / "BUNDLE_MANIFEST.json").write_text(json.dumps({"format": 1, "release": "0.4.7", "files": files}))

    def test_plan_writes_nothing(self):
        before = snapshot(self.root)
        plan = self.install(apply=False)
        self.assertEqual(len(plan["new"]), 31)
        self.assertEqual(snapshot(self.root), before)

    def test_parent_components_refused_before_symlink_normalization(self):
        alias = self.project / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        ambiguous = alias / ".." / "skills"
        self.refusal_unchanged(lambda: pack.install(self.source, ambiguous, "codex", "project", "fixture", True))
        source_alias = self.source / ".." / self.source.name
        self.refusal_unchanged(lambda: pack.install(source_alias, self.destination, "codex", "project", "fixture", True))
        record = self.record()
        ambiguous_record = record.parent / ".." / record.parent.name / "record.json"
        self.refusal_unchanged(lambda: pack.remove(ambiguous_record, True))

    def test_dot_source_remains_supported(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/install_pack.py"),
                                 "install", "--source", ".", "--destination", str(self.destination),
                                 "--host", "codex", "--scope", "project", "--source-id", "fixture"],
                                cwd=self.source, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.destination.exists())

    def test_windows_reparse_predicate_is_fail_closed(self):
        flag = 0x400
        with patch.object(pack.stat, "FILE_ATTRIBUTE_REPARSE_POINT", flag, create=True):
            self.assertTrue(pack.linklike(SimpleNamespace(st_mode=0o040755, st_file_attributes=flag)))
            self.assertFalse(pack.linklike(SimpleNamespace(st_mode=0o040755, st_file_attributes=0)))

    def test_real_pack_plan_has_31_skills_for_both_hosts(self):
        for host in ("codex", "hermes"):
            result = pack.install(ROOT, self.destination, host, "project", "local-working-copy-test", False)
            self.assertEqual(len(result["new"]), 31)

    def test_install_complete_and_private_record(self):
        result = self.install()
        path = Path(result["record"])
        r = pack.load_record(path)
        self.assertEqual(r["state"], "installed")
        self.assertEqual(len(r["created"]), 31)
        self.assertEqual(pack.inventory(self.source), r["source"]["inventory"])
        self.assertEqual(pack.inventory(self.destination), pack.inventory(self.source / pack.HOST_ROOTS["codex"]))
        self.assertTrue(path.is_relative_to(self.destination.parent))
        self.assertFalse(path.is_relative_to(self.destination))

    def test_hermes_install_and_source_independent_remove(self):
        path = Path(self.install(host="hermes")["record"])
        shutil.rmtree(self.source)
        pack.remove(path, True)
        self.assertEqual(pack.load_record(path)["state"], "removed")

    def test_remove_retains_exact_quarantine_and_history(self):
        path = self.record()
        before = snapshot(self.destination)
        old_history = pack.load_record(path)["history"]
        dry_before = snapshot(self.root)
        self.assertEqual(len(pack.remove(path)["owned"]), 31)
        self.assertEqual(snapshot(self.root), dry_before)
        result = pack.remove(path, True)
        self.assertEqual(snapshot(Path(result["quarantine"])), before)
        self.assertEqual(list(self.destination.iterdir()), [])
        r = pack.load_record(path)
        self.assertEqual(r["history"][:len(old_history)], old_history)
        self.assertEqual(r["state"], "removed")
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_latest_noop_run_cannot_remove_prior_install(self):
        old_path = self.record()
        before_skills = snapshot(self.destination)
        new = self.install()
        new_path = Path(new["record"])
        self.assertNotEqual(old_path, new_path)
        self.assertEqual(new["new"], [])
        self.assertEqual(len(new["pre_existing_identical"]), 31)
        pack.remove(new_path, True)
        self.assertEqual(snapshot(self.destination), before_skills)
        self.assertEqual(pack.load_record(old_path)["state"], "installed")

    def test_reinstall_cannot_take_over_missing_earlier_owned_tree(self):
        self.record()
        shutil.rmtree(self.destination / "skill-30")
        self.refusal_unchanged(self.install)

    def test_case_alias_cannot_bypass_prior_ownership(self):
        old = self.record()
        (self.destination / "skill-30").rename(self.project / "held-skill-30")
        alias = self.project / "Skills"
        if alias.exists():
            self.assertTrue(alias.samefile(self.destination))
        self.refusal_unchanged(lambda: pack.install(self.source, alias, "codex", "project", "fixture", True))
        self.refusal_unchanged(lambda: pack.remove(old, True))

    def test_case_alias_refused_even_with_intact_prior_run(self):
        self.record()
        alias = self.project / "Skills"
        self.refusal_unchanged(lambda: pack.install(self.source, alias, "codex", "project", "fixture", True))

    def test_unicode_alias_cannot_bypass_prior_ownership(self):
        self.destination = self.project / "skills-\u00e9"
        self.record()
        (self.destination / "skill-30").rename(self.project / "held-skill-30")
        alias = self.project / "skills-e\u0301"
        if alias.exists():
            self.assertTrue(alias.samefile(self.destination))
        self.refusal_unchanged(lambda: pack.install(self.source, alias, "codex", "project", "fixture", True))

    def test_different_destinations_in_same_parent_are_independent(self):
        old = self.record()
        different = self.project / "other-skills"
        result = pack.install(self.source, different, "codex", "project", "fixture", True)
        self.assertEqual(len(result["new"]), 31)
        before = snapshot(self.destination)
        pack.remove(result["record"], True)
        self.assertEqual(snapshot(self.destination), before)
        self.assertEqual(pack.load_record(old)["state"], "installed")

    def test_reinstall_after_verified_removal_owns_new_trees(self):
        old = self.record()
        pack.remove(old, True)
        new = self.install()
        self.assertEqual(len(new["new"]), 31)
        self.assertNotEqual(new["record"], str(old))
        pack.remove(new["record"], True)
        self.assertTrue((old.parent / "quarantine/skill-00/SKILL.md").is_file())

    def test_preexisting_identical_and_unrelated_are_preserved(self):
        self.destination.mkdir()
        shutil.copytree(self.source / pack.HOST_ROOTS["codex"] / "skill-00", self.destination / "skill-00")
        unrelated = self.destination / "unrelated"
        unrelated.mkdir()
        (unrelated / "keep.txt").write_text("user content")
        before = snapshot(self.destination)
        path = self.record()
        self.assertEqual(len(pack.load_record(path)["created"]), 30)
        pack.remove(path, True)
        self.assertEqual(snapshot(self.destination), before)

    def test_conflict_stops_before_any_mutation(self):
        p = self.destination / "skill-30"
        p.mkdir(parents=True)
        (p / "SKILL.md").write_text("custom")
        self.refusal_unchanged(self.install)

    def test_record_store_cannot_be_destination(self):
        for name in (pack.STORE, pack.STORE.upper()):
            destination = self.project / name
            self.refusal_unchanged(lambda: pack.install(self.source, destination, "codex", "project", "fixture", True))

    def test_nested_record_store_cannot_be_destination(self):
        parent = self.project / pack.STORE / "nested"
        parent.mkdir(parents=True)
        self.refusal_unchanged(lambda: pack.install(self.source, parent / "skills", "codex", "project", "fixture", True))

    def test_existing_case_variant_does_not_create_duplicate_skill(self):
        self.destination.mkdir()
        shutil.copytree(self.source / pack.HOST_ROOTS["codex"] / "skill-00", self.destination / "SKILL-00")
        self.refusal_unchanged(self.install)

    def test_manifest_exact_and_tamper(self):
        self.make_manifest()
        self.assertEqual(len(self.install(apply=False)["new"]), 31)
        (self.source / "extra.txt").write_text("unexpected")
        self.refusal_unchanged(self.install)
        (self.source / "extra.txt").unlink()
        (self.source / pack.HOST_ROOTS["codex"] / "skill-01/SKILL.md").write_text("changed")
        self.refusal_unchanged(self.install)

    def test_manifest_traversal_rejected_without_writes(self):
        self.make_manifest()
        path = self.source / "BUNDLE_MANIFEST.json"
        manifest = json.loads(path.read_text())
        manifest["files"]["../outside"] = {"bytes": 1, "sha256": "0" * 64}
        path.write_text(json.dumps(manifest))
        self.refusal_unchanged(self.install)

    def test_malformed_source_manifests_refused_without_writes(self):
        p = self.source / "BUNDLE_MANIFEST.json"
        p.write_text("[]")
        self.refusal_unchanged(self.install)
        p.unlink()
        (self.source / ".claude-plugin/plugin.json").write_text("[]")
        self.refusal_unchanged(self.install)

    def test_record_missing_inventory_is_not_reconstructed(self):
        path = self.record()
        r = pack.load_record(path)
        del r["source"]["inventory"]
        pack.save_record(path, r)
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_record_symlink_is_refused(self):
        path = self.record()
        held = self.project / "held.json"
        path.rename(held)
        path.symlink_to(held)
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_no_source_identity_and_missing_parent_refused(self):
        self.refusal_unchanged(lambda: pack.install(self.source, self.destination, "codex", "project", "", True))
        self.refusal_unchanged(lambda: pack.install(self.source, self.project / "not created/skills", "codex", "project", "fixture", True))

    def test_missing_file_stops_entire_removal(self):
        path = self.record()
        (self.destination / "skill-30/references/.hidden").unlink()
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_missing_tree_stops_entire_removal(self):
        path = self.record()
        shutil.rmtree(self.destination / "skill-30")
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_extra_file_stops_entire_removal(self):
        path = self.record()
        (self.destination / "skill-30/new.txt").write_text("custom")
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_extra_empty_directory_stops_entire_removal(self):
        path = self.record()
        (self.destination / "skill-30/new empty directory").mkdir()
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_edited_file_stops_entire_removal(self):
        path = self.record()
        (self.destination / "skill-30/SKILL.md").write_text("custom")
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_symlink_tree_stops_entire_removal(self):
        path = self.record()
        (self.destination / "skill-30/linked").symlink_to(self.source)
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_symlink_source_destination_and_ancestor(self):
        (self.source / "linked").symlink_to(self.project)
        self.refusal_unchanged(self.install)
        (self.source / "linked").unlink()
        self.destination.symlink_to(self.source, target_is_directory=True)
        self.refusal_unchanged(self.install)
        self.destination.unlink()
        alias = self.root / "project alias"
        alias.symlink_to(self.project, target_is_directory=True)
        self.refusal_unchanged(lambda: pack.install(self.source, alias / "skills", "codex", "project", "fixture", True))

    def test_moved_record_is_not_recovered(self):
        path = self.record()
        moved = self.project / "moved-record.json"
        path.rename(moved)
        self.refusal_unchanged(lambda: pack.remove(moved, True))
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_deleted_record_is_not_reconstructed(self):
        path = self.record()
        path.unlink()
        self.refusal_unchanged(lambda: pack.remove(path, True))
        self.refusal_unchanged(self.install)

    def test_truncated_and_modified_record_refused(self):
        path = self.record()
        original = path.read_bytes()
        path.write_bytes(original[:100])
        self.refusal_unchanged(lambda: pack.remove(path, True))
        path.write_bytes(original)
        r = json.loads(original)
        r["skills"]["skill-00"]["ownership"] = "pre-existing-identical"
        path.write_text(json.dumps(r))
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_duplicate_json_keys_refused(self):
        path = self.record()
        path.write_text('{"schema":"x","schema":"y"}')
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_strict_schema_even_with_recomputed_checksum(self):
        path = self.record()
        r = pack.load_record(path)
        r["skills"]["skill-00"]["inventory"]["../escape"] = {"type": "directory"}
        pack.save_record(path, r)
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_lock_stops_install_and_remove(self):
        path = self.record()
        (pack.store_for(self.destination) / ".lock").mkdir()
        self.refusal_unchanged(self.install)
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_install_failure_retains_record_and_blocks_retry(self):
        with patch.object(pack, "copy_tree", side_effect=OSError("test disk error")):
            with self.assertRaises(pack.Refusal):
                self.install()
        paths = list(pack.store_for(self.destination).glob("*/record.json"))
        self.assertEqual(len(paths), 1)
        record = pack.load_record(paths[0])
        self.assertEqual(record["state"], "incomplete")
        self.assertEqual(record["created"], ["skill-00"])
        self.assertTrue((self.destination / "skill-00").is_dir())
        self.refusal_unchanged(self.install)
        self.refusal_unchanged(lambda: pack.remove(paths[0], True))

    def test_remove_failure_preserves_moved_and_remaining_data(self):
        path = self.record()
        original = Path.rename
        count = 0
        def fail_second(p, target):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("test I/O failure")
            return original(p, target)
        with patch.object(Path, "rename", fail_second):
            with self.assertRaises(pack.Refusal):
                pack.remove(path, True)
        record = pack.load_record(path)
        self.assertEqual(record["state"], "incomplete")
        self.assertEqual(record["quarantined"], ["skill-00"])
        self.assertEqual(len(list(self.destination.iterdir())), 30)
        self.assertEqual(pack.inventory(path.parent / "quarantine/skill-00"), record["skills"]["skill-00"]["inventory"])
        self.refusal_unchanged(lambda: pack.remove(path, True))

    def test_concurrent_new_target_not_overwritten(self):
        original = Path.mkdir
        def race(p, *args, **kwargs):
            if p == self.destination / "skill-00" and not p.exists():
                original(p)
                (p / "user.txt").write_text("concurrent user data")
            return original(p, *args, **kwargs)
        with patch.object(Path, "mkdir", race):
            with self.assertRaises(pack.Refusal):
                self.install()
        self.assertEqual((self.destination / "skill-00/user.txt").read_text(), "concurrent user data")
        self.assertEqual(len(list(self.destination.iterdir())), 1)

    def test_source_change_during_copy_retains_incomplete(self):
        original = pack.copy_tree
        count = 0
        def changed(source, target, expected):
            nonlocal count
            count += 1
            if count == 2:
                (source / "SKILL.md").write_text("changed during operation")
            return original(source, target, expected)
        with patch.object(pack, "copy_tree", changed):
            with self.assertRaises(pack.Refusal):
                self.install()
        path = next(pack.store_for(self.destination).glob("*/record.json"))
        self.assertEqual(pack.load_record(path)["state"], "incomplete")

    def test_hardlink_and_special_file_source_refused(self):
        origin = self.source / pack.HOST_ROOTS["codex"] / "skill-00/SKILL.md"
        os.link(origin, self.source / "hardlink")
        self.refusal_unchanged(self.install)
        (self.source / "hardlink").unlink()
        if hasattr(os, "mkfifo"):
            os.mkfifo(self.source / "fifo")
            with self.assertRaises(pack.Refusal):
                self.install()
            (self.source / "fifo").unlink()

    def test_cli_plan_apply_remove_and_refusal_exit_codes(self):
        command = [sys.executable, "-B", str(ROOT / "scripts/install_pack.py")]
        args = ["install", "--source", str(self.source), "--destination", str(self.destination),
                "--host", "codex", "--scope", "project", "--source-id", "fixture"]
        plan = subprocess.run(command + args, capture_output=True, text=True)
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertFalse(self.destination.exists())
        installed = subprocess.run(command + args + ["--apply"], capture_output=True, text=True)
        self.assertEqual(installed.returncode, 0, installed.stderr)
        record = json.loads(installed.stdout)["record"]
        removed = subprocess.run(command + ["remove", "--record", record, "--apply"], capture_output=True, text=True)
        self.assertEqual(removed.returncode, 0, removed.stderr)
        again = subprocess.run(command + ["remove", "--record", record, "--apply"], capture_output=True, text=True)
        self.assertEqual(again.returncode, 2)
        self.assertEqual(json.loads(again.stderr)["status"], "STOP")


if __name__ == "__main__":
    unittest.main(verbosity=2)
