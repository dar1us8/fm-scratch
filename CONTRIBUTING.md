# Contributing to fm-scratch

This repository has no product code, so contributing here means exercising the fleet's software-delivery workflow rather than building a product. Read the [README](README.md) first for what the repository is for and how the fleet uses it.

## Tools the fleet uses here

Three tools carry a change from ticket to merged pull request. The README's Tools section lists the wider fleet toolset; these are the ones a contributor works with directly.

- `firstmate` - the coordinating agent that registers this repository as a project, dispatches workers into isolated worktrees on their own branches, and supervises their work.
- `no-mistakes` - the automated validation pipeline every change goes through: code review, tests, lint, and docs checks, then the push and the pull request.
- `gh-axi` - the agent-friendly wrapper for GitHub operations here, such as issues, pull requests, and CI runs.

## Ground rules

- Never push to the default branch and never merge a pull request yourself. Pull requests are merged only with the repository owner's explicit approval.
- Every Markdown file must pass the CI workflow's Markdown lint, configured in `.markdownlint-cli2.yaml`.
- The repository may be reset or discarded at any time, so do not rely on anything here persisting.
