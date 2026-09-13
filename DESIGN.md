# Design requirements and evidence baseline

Status vocabulary: **reported** = user/planning baseline or historical claim; **verified** = directly inspected documentary/tool evidence (not necessarily hardware); **proposed** = candidate awaiting acceptance; **unresolved** = missing evidence/decision. Each verification states its scope.

Sources: [PLAN](PLAN.md), [research](docs/research-solutions.md), [operating manual](docs/references/ts700sp-operating-manual.pdf), [service manual](docs/references/ts700sp-service-manual.pdf). Research reviewed September 11, 2026; original conversation results are historical, not repeated here.

| ID | Requirement / decision | Status and evidence | Completion constraint |
|---|---|---|---|
| REQ-01 | External USB audio; USB-C serial/PTT; manual frequency/mode | reported — PLAN scope | No integrated audio/hub/CAT/RF power in Rev A |
| REQ-02 | Two adjustable transformer-coupled audio paths with detachable cables | reported — PLAN | Loaded levels, DC and clipping need actual measurements |
| REQ-03 | Retain TRRS; connect/disconnect with radio off | reported — explicit PLAN decision | Actual cable continuity and jack pads required |
| REQ-04 | Mic audio pin 1, return 4; switch across 2/3 | reported here from research's manual inspection, printed pp. 3/6 | Independent diagram review and actual adapter verification in #10 |
| REQ-05 | Pin 2 PTT, pin 3 PTT return | reported — prototype history/research | Verify actual unit/cable; switch pair alone does not establish polarity |
| REQ-06 | Invert active-low RTS and qualify with USB-active state | proposed — research §1 manufacturer sources | Verify bridge package, reset/ramp/suspend/host behavior |
| REQ-07 | Floating PhotoMOS PTT closure; audio transformers | proposed — research §2 | Current/voltage/leakage/drive margins and entire assembly isolation |
| REQ-08 | Keep MIC_RETURN, PTT_RETURN and RX_RETURN distinct until intended endpoint connection | proposed — research ground map | No PCB/shield/enclosure bypass |
| REQ-09 | Approximately 20-second optional FT8 window | unresolved — research §3 | User population decision after timing/rearm tradeoffs; no app-health claim |
| REQ-10 | Attenuation before transformers; zero-level adjustment; winding DC blocked | proposed — research §6 | Calculate loaded/tolerance extremes from actual endpoints |
| REQ-11 | Select one headphone channel or combine through separate resistors | proposed — research §6 | Never directly short channels; identify card input routing/bias |
| REQ-12 | Root + USB/PTT + audio sheets, editable portable KiCad project | reported — PLAN | Verified libraries, named nets and stable references |
| REQ-13 | Approximately 70 × 50 mm, proposed two layers | proposed — PLAN | Actual parts/clearances and fabrication capability may require increase |
| REQ-14 | ERC/DRC errors explained; warnings resolved/justified; separate connectivity and visual review | reported — PLAN | No unreviewed gate closure |
| REQ-15 | Same-source reproducible release with checksums and assembly policy | reported — PLAN | Provider and frozen reviewed source required; no order |
| REQ-16 | Bench then radio/RF quantitative validation | reported — PLAN | Actual prototype/results required; no inference from CAD checks |
| TOOL-01 | KiCad CLI version 10.0.6 and bundled libraries available | verified — local CLI version/help and SharedSupport directory inspection, 2026-09-12 | Record tool version on all generated reviews |

## Unresolved inputs and affected gates

| Input | Required evidence | Blocks |
|---|---|---|
| Sound card and computer | Full card model, OS/driver, input routing/bias/clipping and output amplitude | #13 audio values; #12 host tests; #17 freeze; #25–27 validation |
| Radio/cable access | PTT open voltage/current, mic bias/usable drive, RX DC/levels/loading; continuity | #9–10 completion, #12–13 final values, #17 freeze |
| Connectors/mechanics | Exact orderable jacks and dimensions, cable insertion/mounting/enclosure constraints | #11 verification, #18–19 placement gate |
| Timeout | Population policy following verified timing/rearm proposal | #12 completion and #17 freeze |
| Fabrication/assembly | Provider capability, sourcing and BOM/CPL conventions | #20 manufacturing rules, #22–23 release |
| Prototype | Assembly revision/options, equipment and actual results | #25–27 and validated-revision declaration |

## Ground and interface contract

Computer domain: USB supply/return, serial bridge/control, sound-card cable returns. Radio domain: floating PTT output plus isolated TX/RX transformer windings. MIC_RETURN, PTT_RETURN and RX_RETURN must be named separately. USB shield termination and metal mounting must not bypass isolation. Document and test the complete cable assembly, not only bare PCB copper.

Before child-sheet implementation the coordinator assigns reference ranges and exact hierarchical pins. Provisional values must be visible in CAD and review exports. [Provisional CAD completion](docs/cad-completion.md) is permitted with documented defaults; no schematic freeze, fabrication, or validation claim is permitted until the affected unresolved rows above are resolved.
