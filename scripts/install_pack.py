#!/usr/bin/env python3
"""Explicit, local copied-skill transactions. Plans are read-only; --apply writes.

Removal quarantines owned trees; it never deletes them. A stopped transaction is
retained for manual review. Records are private local data, not signed authority.
The lock coordinates this helper, not unrelated processes. Close editors/hosts
that write these trees; hostile concurrent filesystem changes are not supported.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata
import uuid

SCHEMA = "i-have-neurodivergence-install/1"
STORE = ".i-have-neurodivergence-records"
HOST_ROOTS = {"codex": "platforms/codex/skills", "hermes": "platforms/hermes/skills/accessibility"}
HEX = re.compile(r"[0-9a-f]{64}\Z")


class Refusal(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Refusal(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def name_key(value):
    return unicodedata.normalize("NFC", value).casefold()


def path_key(path):
    return tuple(name_key(part) for part in path.parts)


def same_location(left, right):
    if path_key(left) == path_key(right):
        return True
    if left.exists() and right.exists() and left.samefile(right):
        return True
    return (left.parent.exists() and right.parent.exists()
            and left.parent.samefile(right.parent) and name_key(left.name) == name_key(right.name))


def absolute(value):
    expanded = os.path.expanduser(str(value))
    require(".." not in Path(expanded).parts, "Parent '..' path components are refused; supply an explicit path")
    path = Path(os.path.abspath(expanded))
    check_ancestors(path)
    return path


def check_ancestors(path):
    for item in reversed((path, *path.parents)):
        if os.path.lexists(item):
            require(not linklike(item.lstat()), f"Symlink/reparse point refused: {item}")
            if item != path:
                require(item.is_dir(), f"Non-directory ancestor: {item}")


def linklike(info):
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0)
                                           & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def safe_relative(name):
    require(isinstance(name, str) and name and "\\" not in name and ":" not in name
            and not any(ord(c) < 32 for c in name),
            "Invalid relative inventory path")
    p = PurePosixPath(name)
    require(not p.is_absolute() and all(x not in (".", "..", "") for x in name.split("/")),
            f"Unsafe relative path: {name}")


def inventory(root, exclude_git=False):
    check_ancestors(root)
    require(root.is_dir(), f"Missing directory: {root}")
    entries = {}
    folded = set()
    def walk(folder):
        for p in sorted(folder.iterdir()):
            rel = p.relative_to(root).as_posix()
            safe_relative(rel)
            info = p.lstat()
            mode = info.st_mode
            require(not linklike(info), f"Symlink/reparse point refused: {p}")
            if exclude_git and rel == ".git":
                require(stat.S_ISDIR(mode) or stat.S_ISREG(mode), "Unsupported .git entry")
                continue
            require(name_key(rel) not in folded, f"Case/Unicode-normalized path collision: {rel}")
            folded.add(name_key(rel))
            if stat.S_ISDIR(mode):
                entries[rel] = {"type": "directory"}
                walk(p)
            elif stat.S_ISREG(mode):
                require(p.stat().st_nlink == 1, f"Hard-linked file refused: {p}")
                data = p.read_bytes()
                entries[rel] = {"type": "file", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            else:
                raise Refusal(f"Unsupported entry: {p}")
    walk(root)
    return entries


def validate_inventory(entries):
    require(isinstance(entries, dict) and entries, "Empty or invalid inventory")
    folded = set()
    for name, item in entries.items():
        safe_relative(name)
        require(name_key(name) not in folded, "Case/Unicode-normalized inventory collision")
        folded.add(name_key(name))
        require(isinstance(item, dict), "Invalid inventory entry")
        if item.get("type") == "directory":
            require(set(item) == {"type"}, "Unexpected directory metadata")
        else:
            require(set(item) == {"type", "bytes", "sha256"} and item.get("type") == "file"
                    and type(item["bytes"]) is int and item["bytes"] >= 0
                    and isinstance(item["sha256"], str) and HEX.fullmatch(item["sha256"]), "Invalid file metadata")
        parent = PurePosixPath(name).parent
        if str(parent) != ".":
            require(entries.get(str(parent)) == {"type": "directory"}, "Missing inventory parent")


def read_json(path):
    check_ancestors(path)
    require(path.is_file() and path.stat().st_nlink == 1, f"Missing or unsafe JSON file: {path}")
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, f"Duplicate JSON key: {k}")
            result[k] = v
        return result
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    except (ValueError, UnicodeError) as exc:
        raise Refusal(f"Invalid JSON: {path}") from exc


def source_plan(source, host, source_id):
    require(source_id and source_id.strip(), "An externally verified --source-id is required")
    inv = inventory(source, exclude_git=True)
    manifest_hash = None
    if "BUNDLE_MANIFEST.json" in inv:
        manifest = read_json(source / "BUNDLE_MANIFEST.json")
        require(isinstance(manifest, dict) and manifest.get("format") == 1, "Unsupported bundle manifest")
        files = manifest.get("files")
        require(isinstance(files, dict), "Invalid bundle manifest")
        actual = {p: {"bytes": e["bytes"], "sha256": e["sha256"]} for p, e in inv.items()
                  if e["type"] == "file" and p != "BUNDLE_MANIFEST.json"}
        for p in files:
            safe_relative(p)
        require(files == actual, "Bundle manifest membership or hashes do not match")
        manifest_hash = inv["BUNDLE_MANIFEST.json"]["sha256"]
    plugin = read_json(source / ".claude-plugin/plugin.json")
    require(isinstance(plugin, dict), "Invalid plugin manifest")
    version = plugin.get("version")
    require(isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", version), "Invalid source version")
    if manifest_hash:
        require(manifest.get("release") == version, "Manifest release differs from plugin version")
    skill_root = source / HOST_ROOTS[host]
    skills = {}
    require(skill_root.is_dir(), "Missing platform skills")
    for p in sorted(skill_root.iterdir()):
        require(p.is_dir() and not p.is_symlink(), f"Unexpected platform entry: {p}")
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", p.name), "Invalid skill folder name")
        tree = inventory(p)
        require(tree.get("SKILL.md", {}).get("type") == "file", f"Missing SKILL.md: {p}")
        skills[p.name] = tree
    require(len(skills) == 31, f"Expected 31 skills; found {len(skills)}")
    return {"path": str(source), "identity_asserted_by_caller": source_id, "version": version,
            "manifest_sha256": manifest_hash, "inventory": inv, "inventory_sha256": digest(inv)}, skills


def store_for(destination):
    return destination.parent / STORE


def validate_destination_location(destination):
    require(all(name_key(p.name) != name_key(STORE) for p in (destination, *destination.parents)),
            "Destination cannot be the record store or inside a record store")
    require(not same_location(destination, store_for(destination)), "Destination aliases record store")


def record_integrity(record):
    return digest({k: v for k, v in record.items() if k != "integrity_sha256"})


def load_record(path):
    r = read_json(path)
    required = {"schema", "run_id", "record_path", "destination", "host", "scope", "source",
                "skills", "state", "created", "quarantined", "history", "integrity_sha256"}
    require(isinstance(r, dict) and set(r) == required and r["schema"] == SCHEMA, "Unsupported or incomplete record")
    require(isinstance(r["run_id"], str) and re.fullmatch(r"[0-9a-f]{32}", r["run_id"]), "Invalid run ID")
    require(r["host"] in HOST_ROOTS and r["scope"] in ("project", "personal"), "Invalid host or scope")
    require(isinstance(r["destination"], str) and os.path.isabs(r["destination"]), "Invalid destination path")
    destination = absolute(r["destination"])
    validate_destination_location(destination)
    require(str(destination) == r["destination"], "Noncanonical destination path")
    expected = store_for(destination) / r["run_id"] / "record.json"
    require(path == expected and str(path) == r["record_path"], "Record moved or location ambiguous; refusing recovery/search")
    require(record_integrity(r) == r["integrity_sha256"], "Record integrity mismatch")
    require(r["state"] in ("installing", "installed", "removing", "removed", "incomplete"), "Invalid record state")
    source = r["source"]
    require(isinstance(source, dict) and set(source) == {"path", "identity_asserted_by_caller", "version", "manifest_sha256", "inventory", "inventory_sha256"}, "Incomplete source provenance")
    require(all(isinstance(source[k], str) and source[k] for k in ("path", "identity_asserted_by_caller", "version")), "Invalid provenance")
    require(os.path.isabs(source["path"]) and re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][\w.-]+)?", source["version"]), "Invalid source path/version")
    validate_inventory(source["inventory"])
    require(digest(source["inventory"]) == source["inventory_sha256"], "Source inventory digest mismatch")
    manifest_entry = source["inventory"].get("BUNDLE_MANIFEST.json")
    require((manifest_entry is None and source["manifest_sha256"] is None)
            or (isinstance(manifest_entry, dict) and manifest_entry.get("type") == "file"
                and manifest_entry["sha256"] == source["manifest_sha256"]), "Invalid manifest provenance")
    require(isinstance(r["skills"], dict) and len(r["skills"]) == 31, "Incomplete skill list")
    prefix = HOST_ROOTS[r["host"]] + "/"
    for name, item in r["skills"].items():
        require(isinstance(name, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name), "Invalid skill name")
        require(isinstance(item, dict) and set(item) == {"ownership", "inventory"}
                and item["ownership"] in ("new", "pre-existing-identical"), "Invalid ownership")
        validate_inventory(item["inventory"])
        sub = prefix + name + "/"
        expected_tree = {p[len(sub):]: e for p, e in source["inventory"].items() if p.startswith(sub)}
        require(item["inventory"] == expected_tree and "SKILL.md" in expected_tree, "Skill/source inventory mismatch")
    owned = {n for n, e in r["skills"].items() if e["ownership"] == "new"}
    for key in ("created", "quarantined"):
        require(isinstance(r[key], list) and all(isinstance(n, str) for n in r[key])
                and len(r[key]) == len(set(r[key])) and set(r[key]) <= owned, "Invalid transaction progress")
    require(set(r["quarantined"]) <= set(r["created"]), "Invalid removal progress")
    if r["state"] in ("installed", "removing", "removed"):
        require(set(r["created"]) == owned, "Incomplete installation")
    if r["state"] == "installed":
        require(not r["quarantined"], "Ambiguous installed state")
    if r["state"] == "removed":
        require(set(r["quarantined"]) == owned, "Incomplete removal")
    require(isinstance(r["history"], list) and r["history"], "Missing retained history")
    for e in r["history"]:
        require(isinstance(e, dict) and set(e) == {"time", "event"}
                and all(isinstance(v, str) for v in e.values()), "Invalid history")
    return r


def history(record, event):
    record["history"].append({"time": datetime.now(timezone.utc).isoformat(), "event": event})


def save_record(path, record, first=False):
    check_ancestors(path)
    record["integrity_sha256"] = record_integrity(record)
    data = canonical(record) + b"\n"
    if first:
        with path.open("xb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
    else:
        require(path.is_file() and not path.is_symlink() and path.stat().st_nlink == 1, "Record replaced during transaction")
        temp = path.parent / (".record-" + uuid.uuid4().hex + ".tmp")
        with temp.open("xb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, path)


def check_store(destination, lock_owned=False):
    store = store_for(destination)
    check_ancestors(store)
    if not store.exists():
        return
    require(store.is_dir(), "Record store is not a directory")
    owners = {}
    for p in store.iterdir():
        if p.name == ".lock":
            if lock_owned:
                continue
            raise Refusal("Another transaction or stale lock exists; stop for manual review")
        require(p.is_dir() and not p.is_symlink() and re.fullmatch(r"[0-9a-f]{32}", p.name), "Unexpected record-store entry; stop for review")
        r = load_record(p / "record.json")
        recorded_destination = Path(r["destination"])
        if same_location(recorded_destination, destination):
            require(r["destination"] == str(destination),
                    "Destination spelling aliases a recorded location; use its exact recorded path")
            require(r["state"] in ("installed", "removed"), f"Incomplete prior transaction: {p}")
            if r["state"] == "installed":
                for name, entry in r["skills"].items():
                    if entry["ownership"] == "new":
                        require(name not in owners, f"Ambiguous ownership across runs: {name}")
                        owners[name] = r["run_id"]
                        require(inventory(destination / name) == entry["inventory"],
                                f"Earlier owned tree changed/missing: {name}; review its retained record")


@contextmanager
def locked(store):
    lock = store / ".lock"
    lock.mkdir()
    try:
        yield
    finally:
        lock.rmdir()


def destination_check(destination, skills):
    check_ancestors(destination)
    validate_destination_location(destination)
    require(not destination.exists() or destination.is_dir(), "Destination is not a directory")
    # Inspect unrelated trees too: no destination symlinks or unsupported entries.
    if destination.exists():
        inventory(destination)
        existing = {name_key(p.name): p.name for p in destination.iterdir()}
        for name in skills:
            require(existing.get(name_key(name), name) == name,
                    f"Case-insensitive skill name collision: {name}")
    classified = {}
    for name, tree in skills.items():
        target = destination / name
        exists = target.exists() or target.is_symlink()
        if exists:
            require(inventory(target) == tree, f"Conflicting skill; no changes made: {name}")
        classified[name] = {"ownership": "pre-existing-identical" if exists else "new", "inventory": tree}
    return classified


def copy_tree(source, target, expected):
    for rel, entry in sorted(expected.items(), key=lambda x: (len(PurePosixPath(x[0]).parts), x[0])):
        p = target / rel
        check_ancestors(p)
        if entry["type"] == "directory":
            p.mkdir()
        else:
            origin = source / rel
            check_ancestors(origin)
            require(origin.is_file() and origin.stat().st_nlink == 1, "Source file changed type")
            data = origin.read_bytes()
            require(len(data) == entry["bytes"] and hashlib.sha256(data).hexdigest() == entry["sha256"], "Source changed during copy")
            with p.open("xb") as out:
                out.write(data)
    require(inventory(target) == expected, "Installed tree verification failed")


def install(source, destination, host, scope, source_id, apply=False):
    source, destination = absolute(source), absolute(destination)
    validate_destination_location(destination)
    require(not same_location(source, destination)
            and not any(same_location(source, p) for p in destination.parents)
            and not any(same_location(destination, p) for p in source.parents),
            "Source and destination must be separate trees")
    require(destination.parent.is_dir(), "Destination parent must already exist; choose/create it explicitly")
    provenance, skills = source_plan(source, host, source_id)
    check_store(destination)
    classified = destination_check(destination, skills)
    result = {"action": "install", "applied": apply, "version": provenance["version"],
              "new": [n for n, e in classified.items() if e["ownership"] == "new"],
              "pre_existing_identical": [n for n, e in classified.items() if e["ownership"] != "new"]}
    if not apply:
        return result
    store = store_for(destination)
    store.mkdir(exist_ok=True, mode=0o700)
    with locked(store):
        check_store(destination, lock_owned=True)
        require(destination_check(destination, skills) == classified, "Destination changed after preflight")
        run = uuid.uuid4().hex
        run_dir = store / run
        run_dir.mkdir(mode=0o700)
        path = run_dir / "record.json"
        record = {"schema": SCHEMA, "run_id": run, "record_path": str(path), "destination": str(destination),
                  "host": host, "scope": scope, "source": provenance, "skills": classified,
                  "state": "installing", "created": [], "quarantined": [], "history": []}
        history(record, "Installation started; source identity is caller-asserted, not a signature")
        save_record(path, record, first=True)
        try:
            destination.mkdir(exist_ok=True)
            for name in result["new"]:
                check_ancestors(destination)
                target = destination / name
                target.mkdir()  # Exclusive reservation; never merge or replace.
                record["created"].append(name)
                save_record(path, record)
                copy_tree(source / HOST_ROOTS[host] / name, target, skills[name])
            require(inventory(source, exclude_git=True) == provenance["inventory"], "Source changed during installation")
            for name, entry in classified.items():
                require(inventory(destination / name) == entry["inventory"], "Destination changed during installation")
            record["state"] = "installed"
            history(record, "Installation verified; pre-existing identical trees are not owned by this run")
            save_record(path, record)
            load_record(path)
        except BaseException as exc:
            record["state"] = "incomplete"
            history(record, f"Stopped: {type(exc).__name__}; additions retained for manual review")
            save_record(path, record)
            raise Refusal(f"Incomplete installation; inspect retained record {path}: {exc}") from exc
    result.update(record=str(path), run_id=run, host_discovery="not checked")
    return result


def removal_preflight(record):
    destination = absolute(record["destination"])
    require(destination.is_dir(), "Destination missing")
    inventory(destination)
    require(record["state"] == "installed", "Only a complete installed run can be removed; manual review required")
    owned = [n for n, e in record["skills"].items() if e["ownership"] == "new"]
    for name in owned:
        require(inventory(destination / name) == record["skills"][name]["inventory"],
                f"Owned tree changed or missing: {name}; nothing removed")
    quarantine = Path(record["record_path"]).parent / "quarantine"
    require(not quarantine.exists() and not quarantine.is_symlink(), "Existing quarantine; manual review required")
    return destination, owned, quarantine


def remove(record_path, apply=False):
    path = absolute(record_path)
    record = load_record(path)
    destination, owned, quarantine = removal_preflight(record)
    check_store(destination)
    result = {"action": "remove", "applied": apply, "run_id": record["run_id"],
              "record": str(path), "owned": owned, "quarantine": str(quarantine)}
    if not apply:
        return result
    with locked(store_for(destination)):
        check_store(destination, lock_owned=True)
        require(load_record(path) == record, "Record changed after preflight")
        removal_preflight(record)
        record["state"] = "removing"
        history(record, "Removal started: move only owned trees to retained quarantine")
        save_record(path, record)
        try:
            quarantine.mkdir(mode=0o700)
            for name in owned:
                target = destination / name
                require(inventory(target) == record["skills"][name]["inventory"], f"Tree changed before move: {name}")
                check_ancestors(quarantine)
                held = quarantine / name
                require(not held.exists() and not held.is_symlink(), "Quarantine target exists")
                target.rename(held)
                record["quarantined"].append(name)
                save_record(path, record)
                require(inventory(held) == record["skills"][name]["inventory"], "Tree changed during move; retained for review")
            record["state"] = "removed"
            history(record, "Removal verified; owned trees retained in quarantine; record retained")
            save_record(path, record)
            load_record(path)
        except BaseException as exc:
            record["state"] = "incomplete"
            history(record, f"Stopped: {type(exc).__name__}; moved and remaining trees retained for manual review")
            save_record(path, record)
            raise Refusal(f"Incomplete removal; inspect {path}; no quarantined data deleted: {exc}") from exc
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("install", help="Plan or apply a copied-skill installation")
    p.add_argument("--source", required=True)
    p.add_argument("--destination", required=True, help="Exact host skill root; its parent must exist")
    p.add_argument("--host", required=True, choices=HOST_ROOTS)
    p.add_argument("--scope", required=True, choices=("project", "personal"))
    p.add_argument("--source-id", required=True, help="Externally verified commit/release identity; this tool does not authenticate it")
    p.add_argument("--apply", action="store_true")
    p = sub.add_parser("remove", help="Plan or quarantine one exact run's owned trees")
    p.add_argument("--record", required=True)
    p.add_argument("--apply", action="store_true")
    args = vars(parser.parse_args(argv))
    action = args.pop("action")
    if action == "remove":
        args["record_path"] = args.pop("record")
    try:
        result = (install if action == "install" else remove)(**args)
        print(json.dumps(result, indent=2))
        return 0
    except (Refusal, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "STOP", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
