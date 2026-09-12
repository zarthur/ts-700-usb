#!/usr/bin/env python3
"""Read-only discovery of the KiCad commands required by Rev A."""
import os
from pathlib import Path
import shutil
import subprocess

candidate = os.environ.get('KICAD_CLI') or shutil.which('kicad-cli')
if not candidate:
    candidate = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
if not Path(candidate).is_file():
    raise SystemExit('KiCad CLI not found; set KICAD_CLI to its executable path')
print('CLI:', candidate, flush=True)
subprocess.run([candidate, 'version'], check=True)
for args in [('sch', 'erc'), ('sch', 'export', 'pdf'),
             ('sch', 'export', 'bom'), ('sch', 'export', 'netlist'),
             ('pcb', 'drc'), ('pcb', 'export', 'gerbers'),
             ('pcb', 'export', 'drill'), ('pcb', 'export', 'pos'),
             ('pcb', 'export', 'step')]:
    subprocess.run([candidate, *args, '--help'], check=True, stdout=subprocess.DEVNULL)
    print('Available:', ' '.join(args))
