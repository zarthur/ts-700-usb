# Rev A staged prototype acceptance procedure

Issue: [#24](https://github.com/zarthur/ts-700-usb/issues/24). Status: **procedure scaffold; no prototype has been tested**. This procedure controls the order and evidence for tests, but it does not supply the still-unresolved component, radio, cable, sound-card, or numeric acceptance data.

## Preconditions and run record

Before energizing, complete the per-run record in [the measurement worksheet](docs/measurements.md): tested source commit and board serial, populated/DNP configuration, cable IDs, instrument calibration/check date, hookup, supply limit, load ratings, and numeric pass/fail limits with their verified source. A qualified physical operator must review the setup. If an applicable limit, safe load, or instrument is unavailable, mark the run **not executed** rather than estimating a result.

The timeout is a populated, non-retriggerable approximately 20-second limiter. Its nominal duration and tolerance are design predictions until the populated assembly passes the timer tests; it is not application-health or sound-card-loss detection.

## Stage 0 — de-energized inspection and cable evidence

1. Record component orientation, soldering, creepage/isolation gaps, cable labels, board revision, populated/DNP options, and visual anomalies.
2. With the radio off and every cable detached from powered equipment, perform the documented TRRS/contact continuity test. Record connector view, every intended and unintended pair, shell/shield connections, and meter range.
3. With all intended cables, shields, mounting hardware, and enclosure parts installed but de-energized, record computer-domain-to-radio-domain isolation. Keep `MIC_RETURN`, `PTT_RETURN`, and `RX_RETURN` distinct; an `OL` meter reading means only beyond the recorded meter range.

**Advance only when:** actual cable mapping agrees with the approved contract, no unintended conductive bypass is found, and #10/#12 reviewers accept any discrepancy. Never connect or disconnect the TRRS cable with radio power on.

## Stage 1 — USB/PTT bench checks with an isolated simulated load

1. With no radio connected, power from USB under a recorded current limit. Record current, CP2102N enumeration, device/driver/host settings, and default-open state.
2. Use only a reviewed isolated fixture that is within the measured PTT voltage/current envelope. Measure off leakage, on voltage/current, release latency, and PhotoMOS drive at supply corners.
3. Capture `/RTS`, USB-ready/qualification, closure, and supply behavior for attach, reset, slow ramp, brownout, enumeration, idle/key/release, application close, stuck request, suspend/resume, and unplug/reconnect.
4. For the populated limiter, capture a full active window, early release, a second request during that window, request after expiry, a held request, and reconnect/power-transition behavior. Confirm the documented non-retriggerable rearm behavior.

**Advance only when:** all predefined electrical limits pass, startup/reset/suspend/reconnect remain open unless deliberately asserted, and the fixture demonstrates no unsafe or unexplained closure. A failure blocks radio connection and creates a correction/retest record.

## Stage 2 — isolated audio and gain checks

1. Use the identified sound card and actual host configuration. Record selected playback/input contacts, gain/enhancement/AGC state, source waveform, source impedance, and load.
2. Sweep each TX and RX path across approximately 300–3000 Hz at zero, minimum, nominal, and maximum adjustment. Begin TX at zero/minimum level.
3. Record source and transformer-winding amplitudes, gain or attenuation, clipping criterion, DC offsets, waveform evidence, and endpoint load. Verify winding DC blocking and confirm no direct stereo-channel short.
4. Compare each result with the numeric limits derived from verified endpoint/component data. Record any extra roll-off relative to the documented useful radio band before proceeding.

**Advance only when:** the recorded limits pass at all applicable adjustment extremes, no clipping/DC-winding/bypass condition appears, and #13 finalizes the measured values. Otherwise correct the editable design and repeat affected tests.

## Stage 3 — staged radio and RF operation

Only after Stages 0–2 pass, connect the radio using the verified cable with an appropriate RF load and the reviewed safety setup. Run RX first, then TX with adjustment at minimum, followed by staged SSB/FT8 operation and RF-immunity observation. Record frequency, mode, power, levels, settings, resets, false PTT, audio interference, and the full assembly/source revision.

**Pass criterion:** the pre-recorded numerical criteria for #27 pass with no unresolved safety anomaly. Any failure stops progression, creates a linked correction issue, updates the editable source, and requires repeat of affected CAD and physical checks.

## Evidence and scope boundary

Archive raw meter readings, oscilloscope captures, logs, photographs, CSV data, calculations, operator/reviewer identities, and source revision with each run. Passing ERC/DRC, CI, or this document’s checklist is not analog, isolation, radio, or RF validation. This procedure authorizes neither manufacturing nor radio operation; physical work requires the applicable human/operator authorization.
