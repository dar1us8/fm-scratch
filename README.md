# fm-scratch

## Purpose

This is a public scratch repository with no product code. It exists so an AI agent fleet has a safe, low-stakes place to exercise and verify its software-delivery workflow end to end: creating repositories, dispatching workers, validating changes, opening pull requests, and merging them. Everything here is disposable and carries no guarantees of stability, correctness, or continued existence.

## How the fleet uses it

- A coordinating agent registers this repository as a project the fleet can work on.
- Worker agents are dispatched into isolated git worktrees, each on its own branch, so they never touch the default branch or each other's work.
- Every change goes through an automated validation pipeline covering code review, tests, lint, and docs before a pull request is opened.
- Pull requests are merged only with the repository owner's explicit approval.
- The repository may be reset or discarded at any time.

## Continuous integration

Every pull request runs the CI workflow in `.github/workflows/ci.yml`, which lints all Markdown files. It exists so the fleet's validation pipeline has a real check to wait on before a pull request can be merged.
