# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

- Add durable project-specific notes here as they are discovered through real work.

## Agent skills

### Acceptance gates

Every implementation ticket is gated by `gates/<issue-number>-<slug>.py`, written by a validator before the build and never edited by the builder. `sh gates/run.sh` runs them all. See `docs/agents/gates.md`.

### Issue tracker

Issues, specs and Wayfinder maps live in this repository's GitHub Issues, driven with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: one `CONTEXT.md` glossary and `docs/adr/` at the repo root, both created lazily by real sessions. See `docs/agents/domain.md`.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
