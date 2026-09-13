# Component evidence register — provisional Rev A

Issue: [#11](https://github.com/zarthur/ts-700-usb/issues/11). Evidence checked September 13, 2026. This is a selection and library-audit record, not a released BOM. `Verified` below applies only to the stated documentary fact; no hardware, supplier inventory, assembly process, or complete footprint has been independently validated.

The external sound card came with Hyper-X headphones; exact model remains unknown. The user reports working operation with an Apple Silicon MacBook Pro and WSJT-X. That does not establish microphone contact assignment, bias, impedances, maximum levels, or the serial bridge driver behavior.

## Evidence interpretation and selection ledger

An **exact candidate** is an orderable manufacturer part number that is sufficiently identified to investigate; it is not an approved populated component. Manufacturer documents establish only the cited electrical or mechanical fact. A distributor or assembly-provider record is a separate, time-sensitive sourcing fact and must include provider, retrieval date, stock/lead-time, orderable SKU, substitute policy, and evidence URL or quotation. No such provider record is currently attached to this issue.

| Function | Exact candidate / quantity where known | Manufacturer evidence captured | Footprint/pad and mechanical evidence still required | Mating / provider gate |
|---|---|---|---|---|
| USB bridge | CP2102N-A02-GQFN24-R / 1 | Ordering page and Rev. 1.5 datasheet pp. 2, 29–30, 37–40 | Full QFN land, paste, mask, exposed-pad, and pin-1 overlay | Reflow capability and live provider SKU/stock |
| USB-C receptacle | GCT USB4105-GF-A / 1 proposed | Family drawing/specification identified, not fully audited | Exact suffix drawing revision, all SMT and shell lands, board-edge and insertion envelope | Cable clearance, shell process, provider capability |
| USB data ESD | TPD2EUSB30DRTR / 1 proposed | SLVSAC2G pp. 3–5 and ordering addendum | DRT land/mask/paste overlay and clamp-context review | Fine-pitch assembly capability and provider record |
| PTT logic | SN74LVC1G04DBVR and SN74LVC1G08DBVR / 1 each proposed | TI datasheets and ordering pages cited below | SOT-23-5 land overlay and pin-1 orientation | Provider record |
| LED driver | MMBT3904,215 / 1 proposed | Nexperia datasheet and ordering record cited below | SOT-23 land overlay and symbol-pin audit | Provider record |
| Isolated closure | AQY212GS / 1 proposed | Panasonic product specification cited below | SOP4 pin 1, input/output polarity, lands, mask/paste, and isolation geometry | Tube-handling/assembly policy and provider record |
| Audio transformers | LM-NP-1001-B1L / 2 proposed | Bourns drawing/data sheet pp. 1–2 | Bottom-view pin pairs, drill pattern, body/height and lead clearance | Through-hole responsibility and provider/manual-install decision |
| Radio TRRS | SJ-43514 / 1 proposed | Same Sky data sheet pp. 1–2 | Top-view pad coordinates, drill pattern, edge datum, body and cable envelope | Measured radio PTT versus 16 V/300 mA rating; provider/manual-install decision |
| TX/RX adjustments | 3296W-1-102LF / 2 proposed | Bourns 3296 data sheet | Terminal order, drill pattern, top-adjust access, body/height | Actual #13 resistance requirement and manual-install decision |

Open functions without even a provisional MPN are the sound-card-facing audio connectors, passive values/packages, USB VBUS fuse/TVS, CC protection, and any timeout/arming parts selected by #12. They are intentionally absent from a populated BOM. This ledger must not be used to imply that every Rev A component is selected.

## USB bridge

**Selected candidate: Silicon Labs CP2102N-A02-GQFN24-R**, tape/reel option of CP2102N-A02-GQFN24. [Datasheet Rev 1.5](https://www.silabs.com/documents/public/data-sheets/cp2102n-datasheet.pdf), ordering p.2, QFN24 pins pp.29–30, dimensions pp.37–40.

Verified pin correspondence against installed `Interface_USB:CP2102N-Axx-xQFN24`:

| Pad | Signal | Pad | Signal |
|---|---|---|---|
| 1 | RI/CLK | 13 | GPIO1/RXT |
| 2 | GND | 14 | GPIO0/TXT |
| 3 | D+ | 15 | SUSPENDb |
| 4 | D− | 16 | NC |
| 5 | VIO | 17 | SUSPEND |
| 6 | VDD | 18 | CTS |
| 7 | VREGIN | 19 | RTS |
| 8 | VBUS sense | 20 | RXD |
| 9 | RSTb | 21 | TXD |
| 10 | NC | 22 | DSR |
| 11 | GPIO3/WAKEUP | 23 | DTR |
| 12 | GPIO2/RS485 | 24 | DCD |
| Center / KiCad 25 | GND | — | — |

RTS is active low. Leave NC pins floating. Body 4 × 4 mm, pitch 0.5 mm, height 0.70–0.80 mm. Manufacturer center land is 2.55 × 2.55 mm. Installed default `Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm` exists but differs in center-land size: **do not mark the footprint verified from its name**. Compare all lands, mask and paste to p.39–40 before placement approval.

Use the datasheet bus-powered connection diagrams, including the VBUS-sense divider; VBUS sense is not VREGIN. Recheck decoupling, reset pull-up and SUSPENDb reset pull-down from the full diagrams during #15. Assembly needs exposed-pad reflow; provider acceptance and paste aperture review remain open.

## PTT logic and switch

| Exact candidate | Verified documentary facts and mapping | Installed library / outstanding audit |
|---|---|---|
| TI SN74LVC1G04DBVR | DBV/SOT-23-5 inverter; 1 NC, 2 A, 3 GND, 4 Y, 5 VCC. 1.65–5.5 V supply. | `74xGxx:74LVC1G04` mapping matches; assign `Package_TO_SOT_SMD:SOT-23-5` explicitly. Full land audit pending. |
| TI SN74LVC1G08DBVR | DBV/SOT-23-5 AND; 1 A, 2 B, 3 GND, 4 Y, 5 VCC. 1.65–5.5 V supply. | `74xGxx:74LVC1G08` mapping matches; same footprint candidate, full land audit pending. |
| Nexperia MMBT3904,215 | SOT23 NPN: 1 base, 2 emitter, 3 collector; 40 V VCEO, 200 mA limiting IC. Nominal body 2.9 × 1.3 × 1 mm, 1.9 mm lead pitch. | `Transistor_BJT:MMBT3904` and `Package_TO_SOT_SMD:SOT-23` exist. Resolve inherited symbol pins and compare lands independently before approval. Computer-side LED driver only. |
| Panasonic AQY212GS | SOP4, normally-open AC/DC PhotoMOS; exact GS suffix is tube packing. Recommended LED current 5–30 mA and load voltage ≤48 V; maximum on resistance 0.7 Ω, off leakage 1 µA, turn-on 5 ms, turn-off 0.5 ms. | Exact symbol absent. A nearby AQY282GS is a different part, not an approved substitute. Verify AQY212GS input polarity, output pads, package drawing and lands before making a custom symbol or reusing geometry. |

Primary references: [TI inverter Rev AF](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf), [inverter ordering](https://www.ti.com/product/SN74LVC1G04/part-details/SN74LVC1G04DBVR); [TI AND Rev AA](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf), [AND ordering](https://www.ti.com/product/SN74LVC1G08/part-details/SN74LVC1G08DBVR); [Nexperia datasheet, April 8 2026, pp.1–2 and 6](https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf), [exact ordering suffix](https://www.nexperia.com/chemical-content/MMBT3904.html); [Panasonic specifications](https://industry.panasonic.com/ap/en/products/control/relay/photomos/number/aqy212gs).

TI's Ioff support does not establish safe analog behavior during supply ramps. #12 must calculate transistor forced-beta drive, PhotoMOS LED tolerance bounds, and default-off behavior. Radio PTT voltage/current and leakage tolerance remain unmeasured. Panasonic component isolation rating does not establish assembled-board isolation. Timeout selection and any supervisor/arming logic remain #12 decisions, not silently populated BOM options.

## Audio and connector candidates

| Exact candidate | Documentary evidence | CAD/selection disposition |
|---|---|---|
| Bourns LM-NP-1001-B1L, two units | 1:1, 600:600 Ω, 2.8 H minimum at 200 Hz; 66 Ω winding resistance listed; through-hole. Datasheet p.1 distinguishes LM-NP-1001-B1 geometry and bottom-view pin drawing. | No exact bundled symbol/footprint located. Do not assign generic transformer pin numbers to physical pads. Visual drawing transcription, dimensional audit and pin-pair confirmation remain required. |
| Same Sky SJ-43514 radio TRRS | 3.5 mm, four contacts, no switch, horizontal through-hole, plastic bushing. Pin 1 sleeve, 2 tip, 3 ring1, 4 ring2. Rating **16 Vdc, 300 mA**. | Exact footprint not located. Custom verified mapping must be 1 PTT_RETURN, 2 MIC_AUDIO, 3 MIC_RETURN, 4 PTT. Selection is blocked if measured PTT exceeds rating; do not infer compatibility from PhotoMOS's higher rating. |
| Bourns 3296W-1-102LF | Proposed 1 kΩ top-adjust through-hole trimmer; resistance code 102 and W construction are documented. | `Device:R_Potentiometer` plus `Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical` exists. Actual resistance depends #13; physical terminal order, direction and complete dimensions require visual audit before assignment. |
| GCT USB4105-GF-A | USB4105 USB 2.0 Type-C SMT top-mount family drawing identified; current drawing retrieval failed. | `Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal` exists. Exact suffix, pad/drawing overlay, insertion envelope and shell attachment remain unverified. Do not freeze on library presence alone. |

Sources: [Bourns LM-NP/-LP datasheet pp.1–2](https://www.bourns.com/data/global/pdfs/LMNPLP.pdf), revision not established; [Same Sky SJ-4351X, dated 09/12/2024, pp.1–2](https://www.sameskydevices.com/product/resource/sj-4351x.pdf), [SJ-43514 product](https://www.sameskydevices.com/product/interconnect/connectors/audio-connectors/jacks/sj-43514); [Bourns 3296 datasheet](https://www.bourns.com/docs/product-datasheets/3296.pdf), revision not established; [GCT drawing](https://gct.co/files/drawings/usb4105.pdf), indexed as B4 18/12/23 but not fully inspected; [GCT USB4105 specification A3](https://gct.co/files/specs/usb4105-spec.pdf).

SJ-43514 p.2 provides a **top-view** PCB layout and PCB-edge datum. This differs from the transformer's **bottom-view** pin drawing. Keep these views explicit in custom-library review. The TRRS bushing is horizontal at the board edge; actual cable-body clearance must be added beyond the jack itself. Connect and disconnect the radio cable with radio power off.

Audio input/output jacks other than radio TRRS remain unselected: the unknown Hyper-X adapter contact arrangement prevents treating a particular TRS/TRRS contact as confirmed. Preserve separate returns and configurable RX contact routing. Capacitor MPNs and voltage/polarity choices await #13; no generic electrolytic is approved where bias polarity is unknown.

## Protection candidate

**TI TPD2EUSB30DRTR** is a documented orderable USB data ESD candidate. [Datasheet SLVSAC2G, June 2021, pp.3–5 and ordering addendum](https://www.ti.com/lit/ds/symlink/tpd2eusb30.pdf): pad 1 D+, 2 D−, 3 GND; 0–5.5 V recommended operation; typical 0.7 pF; DRT package nominal body 1.00 × 0.80 mm. `Power_Protection:TPD2EUSB30` and `Package_TO_SOT_SMD:Texas_DRT-3` exist. Verify land dimensions and clamp compatibility with the bridge before final selection; package is small and needs provider capability confirmation. This part covers the USB data pair, not a complete VBUS/CC protection solution. VBUS fuse/TVS and CC protection choices remain open in #15; respect the bridge's 5.25 V VREGIN limit.

## Sourcing, assembly and closure gate

Manufacturer ordering pages demonstrate part-number existence, not current assembler stock. TI AND-page stock was unavailable in the retrieved view; no quantity, price or lead-time commitment is recorded. Provider selection is unknown. Tube AQY212GS, through-hole transformers/jacks/trimmers, and fine-pitch USB/QFN parts require explicit assembly responsibility and process review in #22.

The following evidence requests are the remaining #11 handoff, separated so that a later sourcing snapshot cannot be mistaken for manufacturer qualification:

| Evidence owner / source | Required record | Decision it unlocks |
|---|---|---|
| Manufacturer drawing review | PDF revision/page, saved visual overlay or review note, pad/pin/dimension comparison, orientation/view, reviewer, and any discrepancy | Exact KiCad footprint/symbol approval and placement |
| Radio/cable measurement (#9/#10) | Radio-off continuity; PTT open voltage/current; connector/cable dimensions and mating orientation | SJ-43514 electrical suitability and custom pad mapping |
| Audio measurements (#9/#13) | Endpoint levels, bias, impedance/loading, channel/contact routing and clipping conditions | Audio connector, transformer/trimmer, capacitor and protection selection |
| Assembly provider (#22) | Provider identity, date, SKU/MPN match, stock/lead time, assembly class/capability, substitution and manual-install policy | Release BOM/CPL and process approval |
| Independent CAD reviewer | Exact source SHA; symbol pin-to-pad, drills, courtyard, mask/paste and model-scope check | Library/footprint acceptance without fabricated geometry |

Do not represent supplier web availability as an approved substitute or an electrical verification. A provider snapshot expires and must be refreshed at release; it cannot waive the manufacturer drawing, measured-interface, or independent CAD-review gates.

Before closing #11:

1. Finish each manufacturer's visual pin/land comparison, recording drawing revision, dimensions, orientation and reviewer. Store justified custom assets only after that comparison.
2. Resolve connector ratings against measured radio signals; identify remaining audio connectors and full passive/protection MPNs from #12/#13 calculations.
3. Obtain provider-specific sourcing evidence for every populated part, acceptable substitutions and assembly capability. Never substitute a nearby relay or jack by package resemblance.
4. Independently audit library pins (including inherited symbols), pad coordinates, drills, mask/paste and verified mechanical models. Generic STEP models are visual aids only.

Checks performed: primary-source retrieval above; installed symbol pin extraction for CP2102N and logic; exact library-name searches; documentation whitespace check. No CAD models changed, no physical tests run. #11 remains open with provisional evidence suitable for continuing circuit calculations.
