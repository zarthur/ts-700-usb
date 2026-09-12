# Rev A inputs and measurement worksheet

Issue: [#9](https://github.com/zarthur/ts-700-usb/issues/9). Status: **provisional worksheet; no new hardware measurements recorded**. Preparing this document does not satisfy the physical-input acceptance criteria or close #9.

Baseline: [PLAN](../PLAN.md) and [research](research-solutions.md). Historical prototype claims are **reported**, not measurements repeated for this revision. The user additionally reports a sound card supplied with Hyper-X headphones and a working existing prototype on an Apple Silicon MacBook Pro using WSJT-X and a working macOS driver; these reports establish context, not fresh electrical or host-transition verification. Manufacturer specifications and radio-manual ratings are documentary evidence, not measurements of the actual equipment. In particular, the 500 Ω microphone specification is not measured input resistance or sensitivity; 2 W into 8 Ω implies 4 Vrms only at that rated loaded condition, not a maximum open-circuit output.

## Record conventions

Keep the IDs below stable. Input/measurement status is one of **unresolved**, **proposed** (method or assumption), **reported** (unrepeated external observation), or **verified** (identified evidence reviewed against a stated criterion). Completion requires actual evidence; an empty cell, estimated value, instrument over-range, or planned test is not a pass. Store repeated runs under the same ID with run suffixes; retain failed runs and superseded values.

For every run copy this record and attach evidence under an explicitly identified source/board revision. Use relative links to committed evidence where practical; describe any external evidence location and access requirements.

| Field | Entry to complete |
|---|---|
| Measurement/input ID; run ID; status | Unresolved |
| Date/time with zone; operator; reviewer | Unresolved |
| Source commit; board serial/revision; populated/DNP options; cable IDs | Unresolved |
| Device model/variant/serial; OS, driver, application and configuration | Unresolved |
| Instruments, probe impedance, bandwidth, calibration/check date | Unresolved |
| Schematic of hookup, polarity/contact view, load and its tolerance/rating | Unresolved |
| Supply voltage/current limit; frequency; AF level; temperature if relevant | Unresolved |
| Acceptance limit with units, tolerance and source; stop condition | Define and review before energizing; unresolved |
| Raw readings with units, range and uncertainty; processed calculation | Not measured |
| Evidence links (photos, scope captures, logs, CSV) | None |
| Pass/fail/not executed; anomaly; resulting decision and affected issues | Not executed |

The coordinator records limits from verified component/radio data before each powered procedure. If limits or an appropriate setup cannot be established, leave the measurement unresolved. An agent without physical access prepares procedures and analyzes supplied evidence; it must not claim to have operated instruments or the radio.

## Required inputs

| ID | Input and evidence requested | Current status | Decisions/gates blocked |
|---|---|---|---|
| IN-001 | User reports the external USB sound card came with Hyper-X headphones. Exact model/revision, port/label photos and electrical specifications remain needed. | Reported origin; exact identity unresolved | RX contact routing, bias blocking, TX/RX values; #13, #16, #17 |
| IN-002 | User reports an Apple Silicon MacBook Pro running WSJT-X, a working macOS driver, and an existing prototype that works well. Exact macOS build, driver identity/version, WSJT-X version, USB connection/hub and serial/PTT/audio settings remain needed. | Reported operation; exact configuration unresolved | Host-state behavior and test matrix; #12, #15, #25 |
| IN-003 | Actual radio identification and variant; maintenance/modification history relevant to mic/PTT/speaker connections | Unresolved | Applying SP manual evidence to actual unit; #10, #12, #13 |
| IN-004 | Cable/adapter inventory with IDs, both-end photos and contact views; cable length and shields; working prototype availability | Unresolved | Pinout confirmation and complete isolation; #10, #17, #26 |
| IN-005 | Exact TRRS jack MPN/drawing and plug dimensions; other connector MPNs and mating cables | Unresolved | Jack-pad mapping and insertion envelopes; #11, #18, #19 |
| IN-006 | Enclosure material/internal dimensions or explicit unenclosed prototype choice; mounting method, hardware, height/access constraints | Unresolved | Board outline, insulation and mechanical freeze; #18, #19 |
| IN-007 | Fabricator/assembler and service tier; two-layer stackup/capability table, BOM/CPL format and through-hole responsibilities | Unresolved | Routing rules, sourcing and release; #20, #22, #23 |
| IN-008 | Populate or omit approximately 20 s FT8 timeout, after reviewing duration/tolerance, Tune cutoff and early-release/rearm behavior | Unresolved | Timeout circuit/population and schematic freeze; #12, #15, #17 |
| IN-009 | Available DMM, oscilloscope/probes, current-limited supply, signal generator/audio capture, suitable loads and RF test equipment; physical operator | Unresolved | Selecting executable measurement procedures and #25–#27 |

TRRS use is settled; IN-005 concerns the physical jack and cable, not reconsidering connector type. IN-006 does not expand scope to custom enclosure design. Missing inputs permit documented provisional work but do not waive the listed gates.

## Measurement queue and methods

All rows below have status **unresolved / not executed**. Methods are proposed and require the numeric preflight record above. Measure cable continuity with radio power **off**, cables detached from powered equipment, and resistance-mode instruments only on de-energized circuits. Connect/disconnect radio cables only with radio power off. Do not use a current-meter input as an unrestricted short across an unknown PTT circuit.

| ID | Quantity and units | Setup, method and conditions to record | Decision / gate |
|---|---|---|---|
| ME-001 | Actual adapter contact mapping; continuity and unintended connection resistance (Ω) | DMM and labeled cable photographs; test every intended pair and every unintended pair. Record front/mating versus rear/solder view explicitly. Proposed mapping: TRRS tip→mic pin 1, ring 1→mic return pin 4, ring 2→PTT pin 2, sleeve→PTT return pin 3. Confirm actual connector numbering before applying this proposal. Record shield/shell connections and any internal shorts separately. | #10 adapter verification; no radio connection before passing |
| ME-002 | Connector dimensions/envelopes (mm), mounting clearances (mm) | Calipers plus exact manufacturer drawing; identify dimensions, tolerances, datum and view. Include insertion/removal clearance, protrusion, maximum heights, hole spacing, insulated mounting and trimmer/solder access. | #11, #18–#19 mechanical freeze |
| ME-003 | PTT open-circuit voltage/polarity (V DC) and closure operating point (V, mA) | Following radio-off cable verification, qualified operator uses correctly rated high-impedance measurement across PTT pair. Characterize closure only with reviewed rated load/closure fixture and staged procedure; record load resistance and infer current from measured voltage where suitable. Record idle and asserted conditions; intended transmit test requires appropriate RF setup. | #12 PhotoMOS voltage/current/drop/leakage margins |
| ME-004 | Radio mic DC bias (V DC), usable clean input (mVrms), frequency (Hz) | High-impedance measurement first. Subsequent isolated, DC-blocked signal injection begins at minimum through reviewed attenuation; record MIC GAIN/mode/frequency and appropriate RF load/output monitoring. Record distortion/clipping criterion and usable range rather than guessing from 500 Ω specification. | #13 coupling polarity/capacitance and TX gain; #26–#27 |
| ME-005 | RX DC offset (V DC), signal level (Vrms/Vpk), clipping, loading (Ω) | Identify speaker contact view. Begin high-impedance scope/DMM observation; record AF settings, signal source and connected load. If loading is characterized, use reviewed known loads and their ratings; do not automatically apply an 8 Ω dummy load. Record normal/high intended AF settings and clean limits. | #13 RX pad, transformer level and coupling; #26 |
| ME-006 | Sound-card output per channel (Vrms/Vpk), clipping, source/load conditions (Ω), frequency (Hz) | Use identified card and actual host/settings. Measure selected headphone channel unloaded and with intended equivalent load, sweep output setting through maximum intended level; record playback gain/enhancements, channel, test waveform and capture bandwidth. Do not short stereo channels together. | #13 TX attenuation and transformer headroom |
| ME-007 | Sound-card input contacts, DC bias (V DC), clean input range (mVrms), frequency (Hz), loading (Ω) | Confirm model/contact wiring first. Measure bias high-impedance, then inject isolated DC-blocked low-level audio with reviewed resistor network. Record mic/line mode, AGC/enhancements, gain and clipping threshold. Infer loading only with documented source and known-load method. | #13 RX routing/coupling/gain |
| ME-008 | Isolated PTT bench closure voltage (V), current (mA), off leakage (µA), release delay (ms) | **Simulated load before radio.** Set a current-limited isolated source and rated load from ME-003 envelope and component limits. Verify off/on behavior, driver LED current at supply corners, leakage measurement resolution and transient capture. Never exceed component ratings to discover a limit. | #12 margins and #25 prerequisite for radio |
| ME-009 | USB/RTS/PTT states; unintended pulse width and release latency (ms); supply (V) | With simulated load and actual IN-002 host, capture supply, /RTS, USB-ready and closure. Test initial attach, reset, enumeration, idle/key/release, application close/crash, stuck request, suspend/resume, unplug/reconnect, slow ramp and brownout using reviewed equipment. Log hardware-flow-control settings. Host/application behavior is observed, not inferred from enumeration. | #12/#15 default-off design; #25 |
| ME-010 | Timeout duration (s), tolerance, early abort/rearm and reconnect behavior | Execute only for populated timer, with simulated load. Capture request and closure for full window, early release, second request inside window, request after expiry, held request and power/resume transitions. If omitted, record explicit IN-008 decision; do not label timeout tested. | #12 policy and #25 |
| ME-011 | TX/RX gain (dB), response (Hz), clipping (Vrms/Vpk), adjustment extremes | Bench audio paths into identified equivalent loads before radio; sweep approximately 300–3000 Hz, include zero/min/max adjustment and actual endpoint maximum levels. Record both transformer winding amplitudes and evidence of DC blocking. Quantify allowable extra roll-off over the radio's documented 400–2600 Hz band before test. | #13 values and #26 |
| ME-012 | Complete assembly DC isolation (Ω / instrument lower bound) | De-energized assembly with all intended cables/shields/mounting hardware attached, detached from powered host/radio. Enumerate computer-domain to radio-domain conductor/shell pairs, test idle and simulated asserted closure as the approved isolated fixture permits. Record DMM range; “OL” means beyond that range, not infinite insulation resistance. Do not arbitrarily join MIC_RETURN/PTT_RETURN/RX_RETURN. | #17 ground audit and #26 isolation |
| ME-013 | Staged radio/RF operating results, power (W), frequency (MHz), levels and anomalies | After #25 then #26 pass, follow #27's reviewed procedure with appropriate RF load. Record RX first, minimum TX adjustment, clean SSB/FT8 operation and intended RF-power progression; capture resets, false PTT, audio interference and corrections. | #27 final validation; not worksheet completion |

## Execution order and handoff

1. Collect IN-001–IN-009; obtain device documentation and equipment evidence. The coordinator may continue independent provisional design while inputs remain outstanding.
2. Perform ME-001/002 and de-energized checks first. Build a reviewed physical-radio measurement procedure for ME-003–005; absence of actual-unit measurements remains an explicit design blocker.
3. Characterize the external sound card (ME-006/007), calculate limits, then test the assembled interface on simulated loads (ME-008–010) before connecting it to radio signals.
4. Complete bench audio and isolation (ME-011/012); only then execute staged radio/RF validation (ME-013). The baseline actual-radio characterization and final interface/radio validation are distinct activities.
5. Feed each verified result into linked circuit/component decisions and test acceptance limits. Retain original readings, calculation assumptions, reviewer and changed design revision. A failed result generates a correction/retest entry; passing CAD checks cannot override it.

Current handoff: request actual device/cable details and available measurements from the user/operator using the input IDs. No hardware evidence is supplied by this worksheet. #9 remains open, and later measurement-dependent freezes and prototype-validation issues remain open until evidence is captured and reviewed.
