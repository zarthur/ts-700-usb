# Implementation status

Updated: 2026-09-13 after merged PRs #37, #39–#42. No physical measurements, frozen schematic, board or manufacturing release exists. Epic completion requires every applicable child criterion and review gate; provisional/documentary PRs do not close hardware-dependent issues.

| Issue | Owner | Branch/PR | Dependencies | Evidence/status | Blocker |
|---|---|---|---|---|---|
| #8 | coordinator | merged #28 | none | **Closed** — requirements, toolchain and scope evidence integrated | none |
| #9 | measurements agent | merged #29/#40 (partial) | #8 conventions | Worksheet and concise operator evidence request integrated; issue remains open | actual input/measurement results |
| #10 | pinout agent | merged #30/#40 (partial) | #9 cable input | Documentary mapping/cable contract and evidence request integrated; issue remains open | actual jack/cable continuity |
| #11 | components agent | merged #31/#39 (partial) | #8 | Provisional primary-source/component-provider ledger integrated; issue remains open | exact pad/dimension/provider and CAD verification |
| #12 | PTT agent | merged #32/#40 (partial) | #9/#11 | Provisional PTT evidence integrated; populated non-retriggerable ~20-second policy selected | measured radio PTT margins, host transitions and final implementation |
| #13 | audio agent | merged #41 (partial) | #9/#11 | Provisional calculation/test-point framework integrated; issue remains open | endpoint measurements and loaded final calculations |
| #14 | coordinator | merged #33/#34 | #8/#11 | **Closed** — portable provisional hierarchy and local library tables integrated | none; circuit ERC remains #17 |
| #15–17 | unassigned | — | #12–14/#10 | Not started | circuit evidence and freeze inputs |
| #18–19 | unassigned | — | #17 | Not started | schematic freeze, mechanics |
| #20–21 | unassigned | — | #19 | Not started | placement gate, fabrication rules |
| #22–23 | unassigned | — | #21/#11 | Not started | provider, reviewed board |
| #24 | test-planning agent | merged #37 (partial) | #12/#13/#17 | Staged procedure scaffold integrated; issue remains open | numeric limits from confirmed data |
| #25–27 | human bench + agents | — | #23/#24 then sequential | Not performed | assembled prototype and measurements |

| #36 | automation coordinator | merged #42 | none | PR governance, compatible-host CAD-report handling, and approved-squash workflow integrated | Enable Actions workflow write permission before unattended merge; physical/visual gates remain manual evidence |

Current CAD-first work: #47 defines the coordinator contract, then #15/#16 implement a complete provisional model using documented defaults. Human measurements are deferred to physical finalization; they do not block provisional CAD/PCB/review artifacts. Do not call the result frozen, fabrication-ready, or validated before the later physical gates.
