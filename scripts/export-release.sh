#!/bin/sh
# Create a review-only candidate package. This is intentionally not a
# fabrication or procurement release command.
set -eu

usage() {
  cat <<'EOF'
Usage: scripts/export-release.sh --source-sha <40-hex SHA> --output-dir <absolute path>

Creates a source-pinned, review-only candidate package outside this checkout.
The command refuses incomplete CAD, a dirty checkout, an output directory
inside the repository, or a pre-existing output directory. It never writes
editable CAD source or a fabrication/release directory.
EOF
}

source_sha=''
output_dir=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    --source-sha) source_sha=${2-}; shift 2 ;;
    --output-dir) output_dir=${2-}; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage >&2; exit 64 ;;
  esac
done
[ -n "$source_sha" ] && [ -n "$output_dir" ] || { usage >&2; exit 64; }
[ "${#source_sha}" -eq 40 ] || { printf '%s\n' 'ERROR: --source-sha must be a 40-character lowercase hexadecimal commit SHA.' >&2; exit 64; }
case "$source_sha" in *[!0123456789abcdef]*) printf '%s\n' 'ERROR: --source-sha must be a 40-character lowercase hexadecimal commit SHA.' >&2; exit 64 ;; esac
case "$output_dir" in /*) ;; *) printf '%s\n' 'ERROR: --output-dir must be an absolute path outside the repository.' >&2; exit 64 ;; esac

repo_root=$(git rev-parse --show-toplevel) || exit 2
cd "$repo_root"
head_sha=$(git rev-parse HEAD)
[ "$source_sha" = "$head_sha" ] || { printf 'ERROR: source SHA %s is not the checked-out HEAD %s.\n' "$source_sha" "$head_sha" >&2; exit 2; }
git diff --quiet && git diff --cached --quiet || { printf '%s\n' 'ERROR: checkout has tracked changes; export only from a clean source revision.' >&2; exit 2; }
[ ! -e "$output_dir" ] || { printf 'ERROR: output directory already exists: %s\n' "$output_dir" >&2; exit 2; }
python3 - "$repo_root" "$output_dir" <<'PY'
import os
import sys
root, output = map(os.path.realpath, sys.argv[1:])
if os.path.commonpath((root, output)) == root:
    raise SystemExit("ERROR: output directory must be outside the source checkout.")
PY

root_sch=hardware/ts700sp-interface.kicad_sch
usb_sch=hardware/usb-ptt.kicad_sch
audio_sch=hardware/audio.kicad_sch
board=hardware/ts700sp-interface.kicad_pcb
for source in "$root_sch" "$usb_sch" "$audio_sch" "$board"; do
  [ -s "$source" ] || { printf 'ERROR: required CAD input is absent: %s\n' "$source" >&2; exit 2; }
done
grep -q '(sheet' "$root_sch" || { printf '%s\n' 'ERROR: root schematic has no child sheets.' >&2; exit 2; }
for schematic in "$usb_sch" "$audio_sch"; do
  grep -q '(symbol' "$schematic" || { printf 'ERROR: child schematic is still a scaffold: %s\n' "$schematic" >&2; exit 2; }
done
grep -q '(footprint' "$board" || { printf '%s\n' 'ERROR: PCB has no footprints.' >&2; exit 2; }
grep -q 'Edge.Cuts' "$board" || { printf '%s\n' 'ERROR: PCB has no Edge.Cuts definition.' >&2; exit 2; }

cli=${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
[ -x "$cli" ] || cli=$(command -v kicad-cli || true)
[ -n "$cli" ] || { printf '%s\n' 'ERROR: kicad-cli is unavailable.' >&2; exit 2; }
cli_version=$($cli version)
case "$cli_version" in 10.*) ;; *) printf 'ERROR: candidate export requires KiCad 10.x; found %s.\n' "$cli_version" >&2; exit 2 ;; esac

mkdir -p "$output_dir"
trap 'rm -rf "$output_dir"' HUP INT TERM EXIT
mkdir -p "$output_dir"/source "$output_dir"/reports "$output_dir"/review "$output_dir"/manufacturing-candidate
cat > "$output_dir"/README.txt <<EOF
TS-700SP Rev A candidate package
SOURCE SHA: $source_sha
STATUS: PROVISIONAL — NOT FOR FABRICATION, PROCUREMENT, ASSEMBLY, OR RADIO OPERATION

This package is a reproducible CAD-review artifact only. It contains no
provider selection, sourcing authorization, mechanical-fit certification, or
hardware-validation claim. See source/cad-completion.md for assumptions and
the later physical-finalization gate.
EOF
cp "$root_sch" "$usb_sch" "$audio_sch" "$board" hardware/ts700sp-interface.kicad_pro "$output_dir"/source/
cp docs/cad-completion.md "$output_dir"/source/cad-completion.md
for schematic in "$root_sch" "$usb_sch" "$audio_sch"; do
  name=$(basename "$schematic" .kicad_sch)
  "$cli" sch erc "$schematic" --format json --output "$output_dir/reports/${name}-erc.json" --exit-code-violations
done
"$cli" pcb drc "$board" --format json --output "$output_dir/reports/drc.json" --exit-code-violations
"$cli" sch export pdf "$root_sch" --output "$output_dir/review/schematic.pdf"
"$cli" sch export svg "$root_sch" --output "$output_dir/review/schematic.svg"
"$cli" sch export netlist "$root_sch" --output "$output_dir/review/schematic.net"
"$cli" sch export bom "$root_sch" --output "$output_dir/manufacturing-candidate/bom.csv"
"$cli" pcb export gerbers --output "$output_dir/manufacturing-candidate/gerbers" "$board"
"$cli" pcb export drill --output "$output_dir/manufacturing-candidate/drill" "$board"
"$cli" pcb export pos --output "$output_dir/manufacturing-candidate/placement.csv" "$board"
"$cli" pcb export step --output "$output_dir/review/board.step" "$board"
"$cli" pcb export svg --layers F.Cu,B.Cu,Edge.Cuts --output "$output_dir/review/board.svg" "$board"
python3 scripts/validate-candidate-release.py --package "$output_dir" --source-sha "$source_sha" --tool-version "$cli_version" --write-manifest
trap - HUP INT TERM EXIT
printf 'Candidate review package created: %s\n' "$output_dir"
