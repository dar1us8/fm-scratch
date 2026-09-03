#!/bin/sh
# Runs every acceptance gate under gates/ with uv and exits non-zero if any fails.
# Gates are PEP 723 single-file Python scripts named gates/<issue-number>-<slug>.py.
# With no gates present it prints "no gates yet" and exits 0, so a freshly seeded
# project is never blocked. Seeded by ancilli-install; owned by the project.
set -u
cd "$(dirname "$0")/.." || exit 2
status=0
count=0
for gate in gates/*.py; do
  [ -e "$gate" ] || continue
  count=$((count + 1))
  printf '== %s\n' "$gate"
  if ! uv run --quiet "$gate"; then
    status=1
  fi
done
if [ "$count" -eq 0 ]; then
  echo "no gates yet"
fi
exit $status
