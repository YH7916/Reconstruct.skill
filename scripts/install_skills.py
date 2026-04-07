#!/usr/bin/env python3
"""Install the skill suite into a Codex-compatible skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILLS = ("refactoring-legacy-code", "gsd-legacy-refactor")


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def copy_tree(src: Path, dest: Path, force: bool) -> None:
    if dest.exists():
        if not force:
            raise FileExistsError(f"Destination already exists: {dest}")
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def link_tree(src: Path, dest: Path, force: bool) -> None:
    if dest.exists() or dest.is_symlink():
        if not force:
            raise FileExistsError(f"Destination already exists: {dest}")
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    dest.symlink_to(src, target_is_directory=True)


def install(repo_root: Path, destination: Path, mode: str, force: bool, dry_run: bool) -> list[tuple[Path, Path]]:
    source_root = repo_root / "skills"
    destination.mkdir(parents=True, exist_ok=True)
    installed: list[tuple[Path, Path]] = []

    for name in SKILLS:
        src = source_root / name
        dest = destination / name
        if not src.exists():
            raise FileNotFoundError(f"Skill source not found: {src}")
        installed.append((src, dest))
        if dry_run:
            continue
        if mode == "copy":
            copy_tree(src, dest, force=force)
        else:
            link_tree(src, dest, force=force)

    return installed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the Reconstruct skill suite.")
    parser.add_argument(
        "--dest",
        type=Path,
        default=default_destination(),
        help="Destination skill directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--mode",
        choices=("copy", "link"),
        default="copy",
        help="Install by copying files or creating symlinks.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing destination folders if present.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be installed without writing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    try:
        installed = install(
            repo_root=repo_root,
            destination=args.dest.expanduser().resolve(),
            mode=args.mode,
            force=args.force,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    action = "Would install" if args.dry_run else "Installed"
    print(f"{action} {len(installed)} skills:")
    for src, dest in installed:
        print(f"- {src.name}: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
