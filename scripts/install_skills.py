#!/usr/bin/env python3
"""Install the skill suite into a skills directory for common agent hosts."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILLS = ("refactoring-legacy-code", "gsd-legacy-refactor")


def destination_for_platform(platform: str) -> Path:
    if platform == "codex":
        codex_home = os.environ.get("CODEX_HOME")
        if codex_home:
            return Path(codex_home) / "skills"
        return Path.home() / ".codex" / "skills"
    if platform == "claude":
        return Path.home() / ".claude" / "skills"
    if platform == "agents":
        return Path.cwd() / ".agents" / "skills"
    raise ValueError(f"Unsupported platform: {platform}")


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
        "--platform",
        choices=("codex", "claude", "agents", "custom"),
        default="codex",
        help=(
            "Choose a preset destination: codex -> $CODEX_HOME/skills or ~/.codex/skills, "
            "claude -> ~/.claude/skills, agents -> ./.agents/skills, custom -> requires --dest."
        ),
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Destination skill directory. Overrides --platform when provided.",
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
    if args.dest is not None:
        destination = args.dest.expanduser().resolve()
    elif args.platform == "custom":
        print("[ERROR] --platform custom requires --dest", file=sys.stderr)
        return 1
    else:
        destination = destination_for_platform(args.platform).expanduser().resolve()

    try:
        installed = install(
            repo_root=repo_root,
            destination=destination,
            mode=args.mode,
            force=args.force,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    action = "Would install" if args.dry_run else "Installed"
    print(f"{action} {len(installed)} skills for {args.platform}:")
    for src, dest in installed:
        print(f"- {src.name}: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
