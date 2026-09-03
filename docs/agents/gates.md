# Acceptance gates

Every implementation ticket in this repository is gated by a script written before the build. Seeded by `ancilli-install`; the full contracts are the `gate-validator` and `gate-builder` skills in the Ancilli plugin.

- **Validator** writes `gates/<issue-number>-<slug>.py`: a PEP 723 `uv` script that prints one `PASS:` or `FAIL:` line per requirement and exits 0 only when the ticket is complete. It inspects the repo read-only, maps every explicit requirement to a check and nothing more, runs the gate once to prove it is red, and commits only the gate file.
- **Builder** never creates, edits or deletes anything under `gates/`. It runs `sh gates/run.sh` until green, at most five rounds, taking each `FAIL` line verbatim as the next instruction, then hands to no-mistakes with the ticket body plus spec link as intent and the final gate output as evidence. Still red after five rounds escalates to the captain.
- **Gates stay.** `commands.test` in `.no-mistakes.yaml` runs `sh gates/run.sh` on every pipeline test step, so gates are the regression suite. A gate is removed only by an explicit ticket. `gates/runs/` is gitignored; evidence lives in the PR body.
- **Review guard.** A change that edits an existing gate while implementing the ticket it gates is an error finding.
