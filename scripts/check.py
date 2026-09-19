"""Offline structural checks for this repository, not a consumer-repo linter."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlsplit

REQUIRED = {"README.md", "AGENTS.md", "AGENT_DOCS_CONVENTION.md", "ADOPTION.md"}
ENTRIES = {"README.md", "AGENTS.md"}
GENRES = {"contract", "map", "manual", "state", "entry"}
LINK = re.compile(r"!?\[[^\]\n]+\]\(([^\s)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
CONFLICT = re.compile(r"^(?:<{7} |={7}$|>{7} )", re.MULTILINE)


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    documents: int = 0
    external_links: int = 0


def prose(text: str) -> str:
    lines: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    return "\n".join(lines)


def anchors(text: str) -> set[str]:
    used: set[str] = set()
    for line in prose(text).splitlines():
        match = HEADING.match(line)
        if not match:
            continue
        base = re.sub(r"[^\w\- ]", "", match[1].lower()).replace(" ", "-")
        slug, suffix = base, 0
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
    return used


def inventory(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=root, capture_output=True, check=False,
    )
    if proc.returncode:
        raise RuntimeError("Git inventory failed; use a Git checkout, not a source ZIP")
    names = set(proc.stdout.decode("utf-8").split("\0")) - {""}
    # Deleted worktree files are absent; required files and live links still fail.
    return sorted(name for name in names if (root / name).exists())


def exact_file(root: Path, target: Path) -> bool:
    current = root
    for part in target.relative_to(root).parts:
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current = current / part
    return current.is_file()


def check(root: Path, names: list[str]) -> Result:
    root = root.resolve()
    result = Result()
    texts: dict[str, str] = {}
    for name in sorted(set(names)):
        try:
            target = root / name
            if not target.resolve().is_relative_to(root):
                raise ValueError("document escapes repository")
            text = target.read_text(encoding="utf-8")
            if not text.strip() or not text.startswith("# "):
                raise ValueError("empty document or missing top-level title")
            if CONFLICT.search(text):
                result.errors.append(f"{name}: unresolved conflict marker")
            texts[name] = text
            if name not in ENTRIES:
                header = text.splitlines()[:12]
                genres = [line[6:].strip() for line in header if line.startswith("Genre:")]
                owners = [line[14:].strip() for line in header if line.startswith("Canonical for:")]
                if len(genres) != 1 or genres[0] not in GENRES:
                    result.errors.append(f"{name}: expected one valid Genre header")
                if len(owners) != 1 or not owners[0]:
                    result.errors.append(f"{name}: expected one nonempty Canonical for header")
        except (OSError, UnicodeError, ValueError) as exc:
            result.errors.append(f"{name}: cannot read document: {exc}")
    result.documents = len(texts)
    for name in sorted(REQUIRED - texts.keys()):
        result.errors.append(f"{name}: required document missing or unreadable")
    graph: dict[str, set[str]] = {name: set() for name in texts}
    for name, text in texts.items():
        for raw in LINK.findall(prose(text)):
            try:
                url = urlsplit(raw)
                if url.scheme in {"http", "https"} and url.netloc:
                    result.external_links += 1
                    continue
                if url.scheme or url.netloc or url.query or "\\" in raw:
                    raise ValueError("unsupported link form")
                relative = unquote(url.path)
                if relative.startswith("/"):
                    raise ValueError("absolute local link")
                target = (root / name).parent / relative if relative else root / name
                # Keep lexical spelling for case checks, resolve for containment.
                if not target.resolve().is_relative_to(root):
                    raise ValueError("link escapes repository")
                target = Path(os.path.abspath(target))
                if not exact_file(root, target):
                    raise ValueError("missing file or incorrect filename case")
                destination = target.relative_to(root).as_posix()
                if url.fragment:
                    if destination not in texts:
                        raise ValueError("anchor target is not an active Markdown document")
                    if unquote(url.fragment) not in anchors(texts[destination]):
                        raise ValueError("missing heading anchor")
                if destination in texts:
                    graph[name].add(destination)
            except (OSError, ValueError) as exc:
                result.errors.append(f"{name}: {raw}: {exc}")
    reachable: set[str] = set()
    pending = ["AGENTS.md"] if "AGENTS.md" in texts else []
    while pending:
        node = pending.pop()
        if node not in reachable:
            reachable.add(node)
            pending.extend(graph[node] - reachable)
    for name in sorted(texts.keys() - reachable):
        result.errors.append(f"{name}: unreachable from AGENTS.md")
    return result


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        result = check(root, inventory(root))
    except (OSError, UnicodeError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for error in result.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"documents={result.documents}; external_links_unchecked={result.external_links}; errors={len(result.errors)}")
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
