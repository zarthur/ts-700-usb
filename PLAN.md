# TS-700SP interface — model-file creation plan

Status: planning only; no schematic, PCB, or manufacturing files created.

Source: [shared design conversation](https://chatgpt.com/share/6aa473c3-1e1c-83ea-b59f-4cb476cc613d), reviewed September 11, 2026. The final specification is the planning baseline; prototype results reported there are historical evidence, not measurements independently repeated here.

“Model files” means editable KiCad electrical and PCB designs, their verified component libraries, and a board STEP model for mechanical review. A custom enclosure is optional later work.

## Scope and starting point

The repository began empty apart from Git metadata; it now includes this plan and the linked research report. KiCad is present under `/Applications/KiCad`, but its version and bundled CLI still need checking; `kicad-cli` was not found on PATH.

Revision A retains an external USB sound card, integrates USB-C serial/PTT control, and provides adjustable transformer-coupled transmit and receive audio with detachable radio cables. Frequency/mode remain manual. Integrated USB audio, a USB hub, CAT, and RF power circuitry are outside this revision.

## Research outcome and remaining decisions

See [research findings and proposed solutions](docs/research-solutions.md) for manufacturer sources, radio manual evidence, circuit recommendations and validation requirements.

1. Use inverted RTS qualified by USB-active state; verify startup, suspend and host behavior.
2. Prefer an isolated PhotoMOS PTT closure to remove the computer/radio ground connection. This is a proposed improvement to the earlier NPN arrangement, pending schematic and bench validation.
3. Consider an optional approximately 20-second FT8 transmit window to bound stuck RTS. It does not detect application health or external sound-card loss.
4. Retain TRRS per the user's instruction. Connect before radio power-on and disconnect with the radio off. Hot-plug redesign is no longer a blocker; exact jack pad and cable verification remain required.
5. The original manual confirms microphone audio on pin 1 and return on pin 4, with the PTT switch across 2/3. Check the actual adapter. Final audio values still depend on the actual sound card and radio levels.

## Planned files

| Files | Purpose |
|---|---|
| `README.md`, `DESIGN.md` | Scope, setup, reconciled requirements, status and open decisions |
| `PINOUT.md`, `docs/cables.svg` | Connector views, numbering, adapter wiring, continuity checks |
| `docs/component-verification.md` | Exact MPNs, datasheet revisions/pages, symbol/pad mapping, package dimensions, supplier evidence |
| `docs/measurements.md`, `docs/design-decisions.md` | Measured values, outstanding inputs, calculations and resolved contradictions |
| `hardware/ts700sp-interface.kicad_pro` | Project settings, net classes and electrical/physical rules |
| `hardware/ts700sp-interface.kicad_sch` | Root schematic with functional overview and sheet connections |
| `hardware/usb-ptt.kicad_sch` | USB-C, bridge, protection, power, PTT logic and indicators |
| `hardware/audio.kicad_sch` | TX/RX conditioning, transformers, connectors, filters and test points |
| `hardware/ts700sp-interface.kicad_pcb` | Placed and routed board, outline, mounting and labels |
| `hardware/lib/ts700sp.kicad_sym`, `hardware/lib/ts700sp.pretty/` | Verified custom symbols/footprints only where standard libraries are insufficient |
| `hardware/sym-lib-table`, `hardware/fp-lib-table` | Portable project-relative library references |
| `hardware/3d/`, `mechanical/ts700sp-interface.step` | Component mechanical models as needed and exported board assembly |
| `BOM.md`, `TESTING.md` | Assembly options, DNP policy, staged bring-up and acceptance procedure |
| `scripts/`, `reports/` | Reproducible export/check commands and review evidence |
| `fabrication/rev-a/` | Released Gerbers, drill files, BOM, placement files and assembly drawings |

Use one root schematic and two functional child sheets unless readability justifies another split. Do not create empty custom libraries or invented component models just to fill the proposed tree. Keep generated outputs separate from editable sources.

## Execution sequence

### 1. Establish a traceable design baseline

Check the installed KiCad version, CLI location and standard libraries. Record tool versions and export commands. Translate the conversation into requirements labeled reported, verified, proposed, or unresolved. Maintain links to source evidence rather than treating every statement in the chat as verified.

Prepare a measurement worksheet for PTT voltage/current; microphone bias and usable signal level; receive output level and loading; connector orientation/dimensions; and sound-card behavior. The operating manual now documents microphone pins 1/4 and the PTT switch pair 2/3; confirm actual cable continuity. The assignment of 2 as PTT and 3 as its return also agrees with reported prototype findings.

**Exit:** requirements and unknowns are explicit, with each unknown tied to the design choice it blocks.

### 2. Verify components and resolve circuit choices

Use the exact TS-700SP manual/service information and manufacturer datasheets. Select full orderable MPNs for the CP2102N package, USB receptacle, audio jacks, radio connector, transformers, trimmers, transistor and protection parts. Verify symbol pins, physical pads, ratings, assembly process and current sourcing. Record footprint dimensions and connector mating direction.

Calculate PTT drive margin using measured radio current; resolve inversion and default-off behavior. Calculate TX/RX attenuation at adjustment extremes and through the intended audio band, including transformer loading and DC blocking. Identify host behavior that must be tested on the intended computer. Mark unmeasured values provisional.

**Exit:** component evidence, circuit calculations, ground map, PTT state table and connector proposal are reviewable. Resolve measurement-dependent values before freezing the schematic.

### 3. Create the electrical models

Build the project and schematics with stable designators and named nets. Include verified USB support circuitry, radio-side isolated PTT closure (preferred research proposal), adjustable audio paths, optional RF components, indicators, test points and explicit ground connections. Annotate DNP options and unresolved parameters visibly.

Open the project in KiCad, inspect every sheet, run ERC, and export a schematic review PDF plus BOM and reports. Check intended connectivity separately from ERC: no computer supply driven onto radio signals, no direct headphone-channel short, correct transistor/diode orientation, and no accidental ground bypass.

**Exit:** zero unexplained ERC errors; warnings resolved or justified; schematic package ready for review. This is the first implementation milestone.

### 4. Create and review the physical model

Assign verified footprints and matching 3D models. Start placement around connector access, cable clearance, transformer size and trimmer access. Test the approximately 70 × 50 mm target against actual parts; document any necessary increase. Add mounting holes and enclosure clearances.

Export the preliminary board STEP model and top/bottom views. Check insertion envelopes, solder access, mounting hardware, component heights and pin-one alignment. Generic visual models must not be used as dimensional proof.

**Exit:** placement and mechanical arrangement reviewed before routing.

### 5. Route and validate the PCB

Use the proposed two-layer stackup after confirming fabricator rules. Set trace/clearance rules from actual manufacturing capability and current requirements. Keep USB routing short with an appropriate return path, decoupling local, and cable-entry protection close to connectors. Respect the documented ground domains when filling copper.

Run DRC after final zone fill; verify no unrouted nets, schematic/PCB consistency, connector pad mapping, courtyard/edge clearances and silkscreen legibility. Review a fresh STEP export and board renders.

**Exit:** zero unexplained DRC errors, documented warnings and a complete board review package.

### 6. Prepare the manufacturing release

After design review, generate versioned Gerbers, Excellon drills, assembler-specific BOM/CPL, schematic PDF and assembly drawings from the same source revision. Reopen Gerbers in a viewer. Cross-check BOM references, populated/DNP parts, placement origin, rotations, board side, and through-hole assembly responsibilities. Record tool versions and release checksums.

The conversation proposes review checkpoints for pin mapping, transformers, final attenuation, connector assignment and production release. Bundle these around concrete schematic and board packages. This plan does not place an order.

**Exit:** reproducible fabrication package with traceable source revision and explicit assembly instructions.

### 7. Validate the assembled prototype

Document inspection and USB-only power checks, enumeration, simulated-load PTT testing, startup/reset/suspend/unplug and application-close behavior, then audio gain/response/clipping checks. Verify TRRS adapter continuity with radio power off; live insertion is outside the accepted operating procedure. Only after bench checks, connect the radio for staged RX, TX and FT8/RF-immunity testing with an appropriate RF load.

Set quantitative limits from the confirmed radio/component data before testing; record actual results. Passing ERC/DRC establishes CAD consistency, not proof of correct analog behavior or RF immunity. Feed prototype findings back into the editable models before declaring the revision validated.

## Inputs needed during implementation

- Exact USB sound-card model and intended computer/OS for WSJT-X.
- Actual radio/cable measurements or access to the working cable for verification.
- Exact TRRS jack selection and enclosure dimensions; TRRS itself is settled.
- Assembly provider selection before final BOM/CPL formatting and sourcing freeze.

These inputs do not prevent repository setup, evidence collection or a clearly provisional schematic. They do prevent claiming the corresponding electrical or production decisions are final.
