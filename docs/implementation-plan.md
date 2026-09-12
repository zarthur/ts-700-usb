# TS-700SP Rev A coordinated implementation playbook

Approved execution baseline: user plan, 2026-09-12. Implement epics #1–7 and issues #8–27 in https://github.com/zarthur/ts-700-usb. Status and active ownership live in [status.md](status.md); scope/evidence live in [../DESIGN.md](../DESIGN.md) and [../PLAN.md](../PLAN.md).

## Coordination and integration

Use a root coordinator plus at most three simultaneous subagents. The coordinator owns dependencies, shared project settings/root schematic, integration, pushes, PRs, issue status and automatic squash merging. Delegate bounded independent evidence/components, electrical/layout and verification tasks. An artifact's author cannot be its sole reviewer; rotate roles when necessary.

Every task contract specifies issue, base SHA, branch/worktree, allowed files, inputs, unresolved decisions, deliverables, checks and scope exclusions. For electrical tasks also specify shared nets, hierarchical pins, reference ranges and library ownership. Agents return commit SHA, summary, validation and blockers. Stop and coordinate before crossing ownership boundaries.

Use separate issue/<number>-<slug> branches and isolated worktrees for every writer. Preserve user changes. Branch dependent implementation from merged prerequisites; avoid stacked PRs. Independent evidence preparation may start from the baseline, but update to merged conventions before review. One writer per CAD file and one PCB writer throughout placement/routing. Never blindly text-merge CAD conflicts.

Use one PR per issue by default. PR bodies identify behavior/artifacts, issue links, evidence, warnings and provisional inputs. Use Refs for partial delivery and Closes only for satisfied acceptance criteria. Refresh after intervening merges and rerun affected checks. Independent review names the exact final SHA; changes require renewed review/checks. Coordinator may squash-merge passing PRs without further user approval, respecting protections. If GitHub prohibits author approval, put actual independent subagent review identity/SHA in the PR body; do not invent a GitHub approval.

After merge verify integration, update status and epic checklists, and choose next ready work. Close an epic only after child criteria and its gate pass. Missing measurements permit provisional work, never invented values or freeze/release/validation claims. Ask for missing inputs once and continue independent work. Physical tests require a human or explicitly available bench interface; no manufacturing orders follow automatically from approval.

## Epic #1: traceable baseline (#8–10)

1. Coordinator #8: document tool version/CLI/library discovery, requirements IDs/statuses and evidence, this playbook and task ledger. Verify CLI help/commands and links.
2. Evidence agent #9: create measurement worksheet with units, methods, equipment, conditions and evidence; identify card/OS/driver, radio/cable access, dimensions and provider. Unknowns identify blocked decisions. Actual results are mandatory for completion.
3. Pinout agent #10: inspect manual diagrams, distinguish rear/solder from mating views, create cable SVG and continuity matrix. Preserve TRRS mapping, return separation and power-off connection procedure. Actual jack pad mapping and cable continuity remain gates.
4. Verifier independently checks documentary provenance, orientation and historical-versus-measured claims.

Merge #8 first; worksheet/pinout preparation may run concurrently but adopt its conventions before review. Gate: each child criterion satisfied and all unknowns explicitly tied to decisions; partial documentation does not close measurement issues.

## Epic #2: verified components and circuit choices (#11–13)

Components agent #11 selects full orderable MPNs and verifies datasheet revisions/pages, pins/pads, dimensions, mating directions, ratings, assembly and sourcing. Manufacturer evidence establishes electrical facts; suppliers separately establish availability. No fabricated libraries/models.

PTT agent #12 calculates inverted RTS AND USB-active default-off control, reset pull states, floating PhotoMOS voltage/current/leakage and LED-drive tolerance margins. Keep indicator separate. Define unpowered/reset/enumeration/active/suspend/resume/ramp/brownout/stuck-request/reconnect states and complete ground map. Prefer PhotoMOS unless verified constraints disqualify it. Present verified ~20-second timeout tolerances, rearm/early-abort and Tune tradeoffs to user; user chooses population before freeze. Do not claim app-health/sound-card-loss detection.

Audio agent #13 calculates loaded TX/RX attenuation and frequency response at tolerance/adjustment extremes, actual endpoint levels, transformer limits and DC blocking. Attenuation precedes transformers, adjustment reaches zero, stereo outputs are selected or resistively mixed. Resolve RX contacts/bias from actual card. No assumed 500-ohm microphone or 8-ohm dummy termination based only on equipment ratings.

Coordinator reconciles grounds and components; independent verifier recalculates bounds and checks mappings. Merge #11 before finalizing dependent selections; #12/#13 can proceed independently. Gate: measured final values, explicit timeout decision, complete evidence/state table/ground map. Missing measurements allow provisional calculations only.

## Epic #3: electrical models (#14–17)

1. Coordinator #14 creates portable project, root and USB/PTT/audio child sheets, shared interfaces/reference allocation and project-relative library tables only as needed.
2. Separate agents #15 and #16 exclusively own USB/PTT and audio child sheets. Shared library changes return to library owner. Annotate provisional/DNP values visibly.
3. Coordinator integrates #17; independent reviewer inspects every sheet in KiCad, ERC, intended connectivity and exported PDF/BOM.

Verify no unresolved library paths, computer supply onto radio signals, stereo short, winding DC, incorrect transistor/diode orientation or accidental ground bypass. Check connector mapping independently from ERC. Merge #14 then refreshed #15/#16 sequentially then #17. First implementation milestone: zero unexplained ERC errors, justified warnings, complete connectivity/visual evidence and all measurement-dependent freeze inputs resolved.

## Epic #4: physical model (#18–19)

Single layout owner #18 places verified footprints around connector insertion, transformers, trimmers, mounting and solder access. Test ~70 × 50 mm; document required enlargement. Separate mechanical evidence agent verifies dimensions, heights/models and enclosure constraints without editing PCB. Coordinator integrates evidence; independent reviewer #19 inspects fresh STEP/top/bottom views, pin one and clearances. Generic visual models are not dimensional proof. Merge placement then review; routing must wait for placement gate.

## Epic #5: routing and board review (#20–21)

Obtain fabricator capabilities before final rules. Single PCB owner #20 establishes two-layer stackup, widths/clearances/drills and routes with proper USB returns, local decoupling, cable-entry protection and separate isolation copper. Verifier #21 checks final-filled zones, DRC, no unrouted nets, schematic consistency, connector mapping, edges/courtyards/silkscreen and fresh STEP/renders. Merge routing then review. Gate: zero unexplained DRC errors and documented warnings, complete electrical/mechanical review.

## Epic #6: manufacturing release (#22–23)

Assembly agent #22 finalizes provider-specific BOM/CPL, exact sourcing, populated/DNP policy, substitutions and through-hole responsibilities. Automation agent #23 writes checks/exports. Coordinator generates only after board review/provider gates; independent verifier reviews outputs.

Scripts take explicit source revision/output directory, fail on errors, and never silently change editable sources. Export Gerbers, Excellon, BOM/CPL, schematic PDF, assembly drawings and STEP from one frozen source. Record tool version/options/commands/source SHA/checksums. Artifact commit points to source commit, avoiding circular self-reference. Reopen Gerbers; cross-check layers/outline/holes/references/DNP/origin/rotations/sides. Test from clean checkout. Release remains an unvalidated prototype until #7 passes; no order.

## Epic #7: prototype validation (#24–27)

Test-planning agent #24 prepares procedure early but sets quantitative limits from confirmed data before execution. Human/authorized bench interface records actual build/options/instruments/conditions/limits/results. Sequence #25 then #26 then #27; failures stop progression.

- #25: inspection, USB-only power/enumeration, simulated-load voltage/current/leakage/release, reset/ramp/brownout/suspend/resume/unplug, application-close, stuck RTS/reconnect, populated timeout/early-abort/rearm.
- #26: gain/clipping/adjustment extremes, loaded ~300–3000 Hz response using actual sound card/radio conditions, DC blocking/winding limits, radio-off cable continuity, complete cable/shield/enclosure DC isolation.
- #27: staged RX/TX/FT8 and RF immunity with appropriate load, TX adjustment initially minimum, actual settings/results recorded.

Create linked correction issues for failures. Fix editable models, repeat affected CAD/physical checks, regenerate changed releases. Close only when tested build matches documented revision and required numeric criteria pass.

## Verification and handoff

Check git diff --check, relative references and absence of transient KiCad files. Use reproducible units/tolerance calculations, independent evidence review, KiCad opening/ERC/final-filled DRC/connectivity/visual checks, clean export/BOM/CPL/Gerber/checksum validation. Actual hardware results are separate; never substitute CAD success.

Add CI once verified reproducible scripts exist; until then attach local commands/version/results. CI does not waive visual or bench review. Reviews record exact SHA, commands, results, visual evidence, warning rationale and unresolved inputs. Repeat checks for affected changes, not unrelated work. Resume from status/open PRs/issues, not assumptions of earlier completion.
