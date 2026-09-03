# fm-scratch

## Purpose

This is a public scratch repository with no product code. It exists so an AI agent fleet has a safe, low-stakes place to exercise and verify its software-delivery workflow end to end: creating repositories, dispatching workers, validating changes, opening pull requests, and merging them. Everything here is disposable and carries no guarantees of stability, correctness, or continued existence.

## How the fleet uses it

- A coordinating agent registers this repository as a project the fleet can work on.
- Worker agents are dispatched into isolated git worktrees, each on its own branch, so they never touch the default branch or each other's work.
- Every change goes through an automated validation pipeline covering code review, tests, lint, and docs before a pull request is opened.
- Pull requests are merged only with the repository owner's explicit approval.
- The repository may be reset or discarded at any time.

## Tools

- `firstmate` - the coordinating agent that registers projects, dispatches workers into isolated worktrees, and supervises their work.
- `no-mistakes` - the automated validation pipeline that runs code review, tests, lint, and docs checks, then pushes and opens the pull request.
- `tasks-axi` - the fleet's task backlog: queued work, dependencies, holds, and completion history.
- `gh-axi` - GitHub operations such as pull requests, issues, and CI runs through an agent-friendly wrapper.
- `chrome-devtools-axi` - browser control for visual checks and web-based verification.
- `lavish-axi` - turns HTML artifacts into review surfaces the repository owner can annotate and send feedback on.
- `quota-axi` - reports model and provider quota so dispatch decisions account for remaining capacity.
- `markdownlint-cli2` - the Markdown linter the CI workflow runs on every pull request.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the tools a contributor works with here and the ground rules.

## Continuous integration

Every pull request runs the CI workflow in `.github/workflows/ci.yml`, which lints every Markdown file not listed under `ignores` in `.markdownlint-cli2.yaml`. It exists so the fleet's validation pipeline has a real check to wait on before a pull request can be merged.
