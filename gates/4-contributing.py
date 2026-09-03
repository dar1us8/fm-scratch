# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Acceptance gate for issue #4: Add CONTRIBUTING.md to fm-scratch.

Checks, one line each:
  1. CONTRIBUTING.md exists at the repository root.
  2. It names firstmate, no-mistakes and gh-axi, each with a description line.
  3. README.md carries a real Markdown link that resolves to CONTRIBUTING.md.
  4. The CI markdownlint command passes from the repository root.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
README = ROOT / "README.md"
TOOLS = ("firstmate", "no-mistakes", "gh-axi")
LINT_CMD = ["npx", "--yes", "markdownlint-cli2", "**/*.md"]

results: list[bool] = []


def report(ok: bool, passed: str, failed: str) -> bool:
    print(f"PASS: {passed}" if ok else f"FAIL: {failed}")
    results.append(ok)
    return ok


def contributing_exists() -> bool:
    return report(
        CONTRIBUTING.is_file(),
        "CONTRIBUTING.md exists at the repository root",
        f"expected a file, found nothing at {CONTRIBUTING.relative_to(ROOT)} "
        "- create CONTRIBUTING.md at the repository root",
    )


def description_for(tool: str, lines: list[str]) -> str | None:
    """Return the description text accompanying the first mention of `tool`.

    The description is the rest of the line that names the tool (after the
    name and any list marker, backticks, colon or dash) or, when the tool is
    named on its own or as a heading, the next non-blank line.
    """
    name_re = re.compile(rf"(?<![\w-])`?{re.escape(tool)}`?(?![\w-])", re.IGNORECASE)
    for idx, line in enumerate(lines):
        if not name_re.search(line):
            continue
        rest = clean(name_re.sub(" ", line, count=1))
        if is_description(rest):
            return rest
        for nxt in lines[idx + 1 :]:
            if nxt.strip():
                nxt = clean(nxt)
                return nxt if is_description(nxt) else None
        return None
    return None


def clean(line: str) -> str:
    """Strip list / heading markers and surrounding punctuation from a line."""
    return re.sub(r"^[\s#>*+\-\d.]*", "", line).strip(" \t:-*_`")


def is_description(text: str) -> bool:
    """At least three real words that are not just the tool names themselves."""
    for tool in TOOLS:
        text = re.sub(rf"`?{re.escape(tool)}`?", " ", text, flags=re.IGNORECASE)
    words = [w for w in text.split() if re.search(r"[A-Za-z]", w)]
    return len(words) >= 3


def tools_described() -> bool:
    if not CONTRIBUTING.is_file():
        return report(
            False,
            "",
            f"expected {TOOLS} each described in CONTRIBUTING.md, found no file at "
            f"{CONTRIBUTING.relative_to(ROOT)} - create it first",
        )
    lines = CONTRIBUTING.read_text(encoding="utf-8").splitlines()
    ok = True
    for tool in TOOLS:
        desc = description_for(tool, lines)
        if desc is None:
            ok = False
            report(
                False,
                "",
                f"expected `{tool}` named with one line saying what it is for in "
                f"this repo, found no such description at CONTRIBUTING.md - add a "
                f"line such as '- `{tool}` - <what it is for here>'",
            )
        else:
            report(True, f"CONTRIBUTING.md names `{tool}` with a description line: {desc!r}", "")
    return ok


LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^\s)>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)", re.MULTILINE)


def link_targets(text: str) -> list[str]:
    return LINK_RE.findall(text) + REF_DEF_RE.findall(text)


def resolves_to_contributing(target: str) -> bool:
    target = target.split("#", 1)[0]
    if not target:
        return False
    if re.match(r"^https?://", target):
        return target.rstrip("/").endswith("/CONTRIBUTING.md")
    try:
        return (README.parent / target).resolve() == CONTRIBUTING.resolve()
    except OSError:
        return False


def readme_links() -> bool:
    if not README.is_file():
        return report(False, "", f"expected README.md at {ROOT}, found none - restore README.md")
    targets = link_targets(README.read_text(encoding="utf-8"))
    hits = [t for t in targets if resolves_to_contributing(t)]
    return report(
        bool(hits),
        f"README.md links to CONTRIBUTING.md via {hits[0]!r}" if hits else "",
        "expected a Markdown link in README.md whose target resolves to "
        f"CONTRIBUTING.md, found link targets {targets!r} at README.md - add a "
        "link such as 'See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute.'",
    )


def lint_passes() -> bool:
    cmd = " ".join(LINT_CMD)
    try:
        proc = subprocess.run(
            LINT_CMD, cwd=ROOT, capture_output=True, text=True, timeout=50
        )
    except FileNotFoundError:
        return report(False, "", f"expected `{cmd}` to run, found npx missing - install Node.js/npx")
    except subprocess.TimeoutExpired:
        return report(False, "", f"expected `{cmd}` to finish within 50s, found a timeout - rerun")
    output = (proc.stdout + proc.stderr).strip().splitlines()
    tail = " | ".join(line for line in output if line.strip())[-600:]
    return report(
        proc.returncode == 0,
        f"markdownlint passes: `{cmd}` exited 0",
        f"expected `{cmd}` to exit 0, found exit {proc.returncode}: {tail} "
        "- fix the reported Markdown lint findings",
    )


def main() -> int:
    contributing_exists()
    tools_described()
    readme_links()
    lint_passes()
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
