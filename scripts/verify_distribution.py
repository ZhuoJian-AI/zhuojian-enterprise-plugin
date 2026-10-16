"""Verify the unchanged distribution against its original receipt (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archives", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    receipt = json.loads((root / "release/build-receipt.json").read_text("utf-8"))
    files = receipt["files"]
    actual = {
        path.relative_to(root).as_posix()
        for folder in ("zhuojian-enterprise", "workbuddy-zhuojian-enterprise", ".agents")
        for path in (root / folder).rglob("*") if path.is_file()
    }
    require(actual == set(files), "Package file whitelist mismatch")
    for name, expected in files.items():
        path = root / name
        require(not path.is_symlink(), f"Symlink forbidden: {name}")
        require(digest(path.read_bytes()) == expected, f"File hash mismatch: {name}")
    market = json.loads((root / ".agents/plugins/marketplace.json").read_text("utf-8"))
    require(market["name"] == "zhuojian-enterprise-pilot", "Marketplace name mismatch")
    require(market["plugins"][0]["source"]["path"] == "./zhuojian-enterprise", "Marketplace path mismatch")
    manifest = json.loads((root / "zhuojian-enterprise/plugin.json").read_text("utf-8"))
    require(manifest["version"] == receipt["version"], "Plugin version mismatch")
    checksums = (root / "release/SHA256SUMS").read_text("utf-8").splitlines()
    require(set(checksums) == {f"{h}  {n}" for n, h in receipt["archives"].items()}, "Checksum list mismatch")
    if args.archives:
        for name, expected in receipt["archives"].items():
            archive = args.archives / name
            require(digest(archive.read_bytes()) == expected, f"Archive hash mismatch: {name}")
            if "marketplace" in name:
                members = {n: root / n for n in files if not n.startswith("workbuddy-")}
            else:
                prefix = "workbuddy-zhuojian-enterprise/" if name.startswith("workbuddy-") else "zhuojian-enterprise/"
                members = {n[len(prefix):]: root / n for n in files if n.startswith(prefix)}
            with zipfile.ZipFile(archive) as zf:
                require(len(zf.namelist()) == len(set(zf.namelist())), f"Duplicate ZIP members: {name}")
                require(set(zf.namelist()) == set(members), f"ZIP whitelist mismatch: {name}")
                for member, source in members.items():
                    require(zf.read(member) == source.read_bytes(), f"ZIP content mismatch: {name}/{member}")
    print(f"PASS: {len(files)} distribution files; version {receipt['version']}; archives={'verified' if args.archives else 'not requested'}")


if __name__ == "__main__":
    main()
