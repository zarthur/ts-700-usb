#!/bin/sh
set -eu

KICAD_CLI="${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}"
"$KICAD_CLI" version

if [ -f hardware/ts700sp-interface.kicad_sch ]; then
  mkdir -p reports
  "$KICAD_CLI" sch erc hardware/ts700sp-interface.kicad_sch --output reports/erc.json
fi

if [ -f hardware/ts700sp-interface.kicad_pcb ]; then
  mkdir -p reports
  "$KICAD_CLI" pcb drc hardware/ts700sp-interface.kicad_pcb --output reports/drc.json
fi
