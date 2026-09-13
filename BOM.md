# Rev A BOM policy

This file is not a release BOM. JLCPCB/LCSC is a **provisional formatting target**, not a selected or approved provider. The release BOM must name the actual chosen provider and contain exact MPN, provider SKU, reference, quantity, value, footprint, populated/DNP state, dated lifecycle/stock snapshot, and approved-substitute policy. Do not substitute an LCSC part number for manufacturer qualification or a provider-capability review.

Through-hole or mechanically inaccessible parts are permitted only when explicitly marked for manual installation in both BOM and assembly drawing. The schematic, PCB, BOM, and CPL must agree on each populated reference.

## Provisional component register

The entries below are research candidates from [component verification](docs/component-verification.md), not release lines. `TBD` is intentional where endpoint measurements, a drawing audit, or provider selection is missing. No reference designators, quantities, footprints, or substitution permissions are approved by this table.

| Function | Proposed manufacturer MPN | Provider SKU | Population state | Release blocker |
|---|---|---|---|---|
| USB bridge | CP2102N-A02-GQFN24-R | TBD | proposed | QFN land/paste/mask overlay, provider process and sourcing evidence |
| USB-C receptacle | GCT USB4105-GF-A | TBD | proposed | exact drawing/suffix, footprint and cable-envelope review |
| USB data ESD | TPD2EUSB30DRTR | TBD | proposed | land audit, final protection context and provider capability |
| PTT gates | SN74LVC1G04DBVR; SN74LVC1G08DBVR | TBD | proposed | #12 state/margin decision and footprint audit |
| PTT LED driver | MMBT3904,215 | TBD | proposed | #12 drive calculation and footprint audit |
| Isolated PTT switch | AQY212GS | TBD | proposed | #12 current/leakage/drive proof, SOP4 audit and assembly policy |
| Audio transformers | Bourns LM-NP-1001-B1L | TBD | proposed (2) | #13 loading calculation, pin/drill/dimension audit and installation policy |
| Radio TRRS | Same Sky SJ-43514 | TBD | proposed | cable continuity, measured PTT rating check, pad/dimension/mating review |
| Audio trimmers | Bourns 3296W-1-102LF | TBD | proposed (2) | #13 value choice, terminal/dimension audit and access review |

Unselected audio connectors, passives, USB VBUS/CC protection, and timeout/arming parts must remain absent from any release or procurement export until their governing measurements and design decisions are recorded. A release BOM may include a part only after its manufacturer evidence, provider-specific availability/process record, schematic/PCB mapping, and populated/DNP policy agree.
