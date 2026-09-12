# TS-700SP USB interface — Rev A

Work in progress: requirements and evidence baseline; no validated circuit or production release.

The interface retains an external USB sound card, adds USB-C serial/PTT control, and uses adjustable transformer-coupled TX/RX audio. Radio frequency and mode remain manual. TRRS radio cables must be connected and disconnected with the radio off.

Start with [design requirements](DESIGN.md), the [implementation playbook](docs/implementation-plan.md), [task status](docs/status.md), and the original [plan](PLAN.md). [Research](docs/research-solutions.md) contains source-linked proposals, not fresh bench measurements.

## Toolchain

KiCad 10.0.6 was observed on September 12, 2026. Run `python3 scripts/check-toolchain.py` to locate KiCad and inspect required CLI capabilities. Set `KICAD_CLI` to an executable path if automatic discovery fails. The macOS fallback is `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`; this is discovery documentation, not a CAD library reference.

Standard symbols, footprints and 3D models are bundled in the app's `Contents/SharedSupport` on this installation. Future project library/model paths must use project-relative paths or KiCad's versioned library variables.

## Current gates

Actual radio/cable and sound-card measurements, exact connector selection, timeout policy and manufacturing-provider inputs remain unresolved. Documentation/provisional models can progress; dependent freezes cannot. CAD consistency is not proof of analog behavior or RF immunity.
