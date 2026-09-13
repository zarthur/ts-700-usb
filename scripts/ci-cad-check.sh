#!/bin/sh
# Produce CAD reports when KiCad is available.  A report is CAD consistency
# evidence only; it never substitutes for visual, mechanical, or bench review.
set -eu

report_dir="${REPORT_DIR:-reports}"
mkdir -p "$report_dir"
cli="${KICAD_CLI:-$(command -v kicad-cli || true)}"
if [ -z "$cli" ]; then
  printf '%s\n' 'SKIPPED: kicad-cli is unavailable on this runner.' > "$report_dir/kicad-cli.txt"
  exit 0
fi

"$cli" version | tee "$report_dir/kicad-cli.txt"
for schematic in hardware/*.kicad_sch; do
  [ -f "$schematic" ] || continue
  name=$(basename "$schematic" .kicad_sch)
  "$cli" sch erc "$schematic" --format json --output "$report_dir/${name}-erc.json" --exit-code-violations
done
for board in hardware/*.kicad_pcb; do
  [ -f "$board" ] || continue
  name=$(basename "$board" .kicad_pcb)
  "$cli" pcb drc "$board" --format json --output "$report_dir/${name}-drc.json" --exit-code-violations
done
