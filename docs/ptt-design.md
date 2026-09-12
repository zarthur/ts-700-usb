# Provisional isolated PTT control and timeout study

Partial [#12](https://github.com/zarthur/ts-700-usb/issues/12); **not a validated schematic or measured radio interface**. Read the [research](research-solutions.md) and [measurement queue](measurements.md). This document supplies conditional calculations and behavior requirements. #12 and schematic freeze remain open.

## Evidence and assumptions

Primary sources inspected September 12, 2026:

- [CP2102N datasheet Rev 1.5](https://www.silabs.com/documents/public/data-sheets/cp2102n-datasheet.pdf), §4.1 and QFN24 Table 5.2: RTS active low; SUSPENDb low in suspend/pre-enumeration. Reset can float the suspend outputs high; manufacturer recommends 10 kΩ SUSPENDb pull-down. QFN24 RTS=19 and SUSPENDb=15; other packages differ.
- [Panasonic AQY212GS specifications](https://na.industrial.panasonic.com/products/relays-contactors/semiconductor-relays/lineup/photomos-relays/series/12653/model/12659): recommended LED 5–30 mA, listed maximum forward drop 1.5 V; recommended load ≤48 V, on-resistance ≤0.7 Ω, leakage ≤1 µA, turn-on/off ≤5/0.5 ms. These component specifications are not whole-circuit guarantees; full operating-temperature/test-condition validation remains required.
- [Nexperia MMBT3904 datasheet, 8 April 2026](https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf), Tables 2/7: B/E/C pads 1/2/3; saturation ≤0.2 V at 10 mA/1 mA and ≤0.3 V at 50 mA/5 mA, at 25°C. These isolated test points do not guarantee our full load/temperature envelope. Candidate order code from component work: MMBT3904,215.
- [LTC6993 Rev F](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc6993-6993-1-6993-2-6993-3-6993-4.pdf), pp.4–5 and 12–15: timing equation, full-temperature ±3% accuracy for Ndiv≥512, divider code and non-retriggering behavior. Candidate industrial TSOT-23 variant LTC6993IS6-1#TRPBF; not a purchasing decision.

Board VBUS **4.35–5.25 V**, LED VF **0–1.5 V**, driver drop **0–0.3 V**, resistor total tolerance **±1%** are the conditional design envelope. VBUS range is an engineering assumption requiring power-path/cable verification, not a claim about all USB connections. Zero minimum LED drop deliberately gives a conservative current upper bound. Confirm VF maximum versus temperature before freezing. All resistor tolerances below include temperature/aging budget; a nominal 1% part with additional drift is not automatically sufficient.

## Drive calculation and topology proposal

Computer-side chain: VBUS → 470 Ω current limiter → PhotoMOS LED → NPN collector; emitter → computer ground. Use 1 kΩ base resistor from the qualified logic output, 100 kΩ base-emitter pull-down, and a separately driven visible PTT indicator. These are provisional values, not frozen BOM entries.

Run `python3 scripts/calculate-ptt.py` from repository root. It emits units in JSON keys, fails for invalid numeric inputs or a failed conditional LED/divider envelope, and never reads or changes CAD. CLI overrides permit sensitivity checks; they do not change the timer study.

| Calculation | Result under stated assumptions |
|---|---|
| Minimum LED current: (4.35−1.5−0.3)/(470×1.01) | 5.372 mA |
| Conservative maximum: 5.25/(470×0.99) | 11.283 mA |
| Conservative resistor dissipation: 5.25²/(470×0.99) | 59.24 mW |
| NPN collector dissipation bound: 0.3×11.283 mA | 3.385 mW, excludes base loss |
| Forced-beta-10 base target | ≥1.129 mA |
| Conditional base minimum: (2.4−0.95)/1010−0.95/99000 | 1.426 mA; forced beta ≤7.92 |
| Conservative logic source current: 3.6/990 | ≤3.637 mA |

The base calculation **assumes** final logic VOH≥2.4 V at this load, supply≤3.6 V, VBE≤0.95 V. Verify the chosen logic gate, supply and NPN temperature behavior before use. It does not interpolate a guaranteed saturation specification between manufacturer test points. The 0.3 V drop budget must be proved at the actual operating current/temperature, or select a driver with applicable guarantees and rerun. Select a resistor package whose derated dissipation exceeds 59.24 mW (0.125 W nominal is a starting candidate, not temperature proof). Budget total USB current including bridge, logic, indicators and suspend behavior separately.

Radio-side PhotoMOS outputs connect **only PTT ↔ PTT_RETURN**. Once ME-003 exists, calculate worst closure drop `I_PTT × 0.7 Ω` and dissipation `I_PTT² × 0.7 Ω`, compare measured open voltage/transients to recommended rating, and test whether ≤1 µA off leakage can falsely key this radio. For illustration only, 10 mA gives 7 mV and 70 µW; this is not the radio's measured current. Use ME-008 simulated load before radio operation; include correct temperature/rating derating. Neither datasheet isolation voltage nor the relay alone certifies assembly isolation.

## Logic, reset and grounding contract

Definitions: `REQUEST = NOT /RTS`; `USB_READY = SUSPENDb`. Base proposal `DRIVE = REQUEST AND USB_READY`; add timeout qualification if populated. Pull /RTS up to the correct computer logic rail, pull SUSPENDb down 10 kΩ, and default the driver off. Exact /RTS pull-up, gate MPNs and reset circuit remain schematic work.

| Event/state | Required output / limitation and check |
|---|---|
| Unpowered / unplug | LED off and switch opens after circuit decay/release; measure delay, not just 0.5 ms relay figure |
| Reset / pre-enumeration | USB_READY low must inhibit; verify 10 kΩ pull-down and pin floating interval |
| Ready, RTS idle high | REQUEST=0, switch open |
| Ready, RTS asserted low | Switch closes only when enabled/armed and optional window active |
| Suspend | USB_READY low inhibits; record actual host entry timing |
| Resume/reconnect with RTS held asserted | Simple AND can immediately key; require idle-observed arm interlock before claiming prevention |
| Slow ramp/brownout | Undefined below logic operating limits; verify supervisor/reset/driver hold-off across ramps, not just zero-volt Ioff |
| Normal release | REQUEST low ends drive regardless of timer; measure end-to-end release |
| Application exit/crash or external sound-card loss | USB state alone does not detect it; host may keep RTS asserted |
| Stuck request | Without timer: can remain keyed. With non-retriggering timer: ends at window expiry, subject to functioning circuitry |
| Unrelated program opens port | May change RTS; test actual host/driver/settings; not an application authorization mechanism |

**Interlock requirement for subsequent schematic work:** clear ARMED whenever power invalid, USB not ready or bridge reset; set ARMED only after a valid ready+idle REQUEST=0 state. Qualify DRIVE and timer trigger with ARMED. Do not implement an asynchronous latch by guesswork: select a concrete reset/arming circuit, examine simultaneous transitions and minimum timing, then simulate/capture it. A timer alone cannot provide this interlock. The basic AND circuit remains explicitly insufficient for held-RTS reconnect behavior until this is resolved.

Ground domains: VBUS, bridge, gates, timer, NPN and LED are computer-side. Relay load terminals are floating radio PTT pair. Audio transformer secondaries preserve MIC_RETURN and RX_RETURN independently. No shared ground, shield, mounting screw or enclosure connection may bypass the three isolation components. Audit complete attached cables and enclosure under ME-012. Radio cables connect/disconnect only with radio power off.

## Optional timeout proposal for user decision

**Recommended population for an FT8-focused build:** non-retriggerable positive pulse LTC6993-1, DIVCODE 7, RSET=480 kΩ with total ±1% budget; top DIV resistor 1 MΩ and bottom 887 kΩ, each total ±1%. Derivation: `t = 2^21 × (480k/50k) × 1µs = 20.1326592 s`. Using full-temperature IC ±3% gives **19.333–20.944 s** conditional limits. Do not quote the headline ±2.3% as full-temperature accuracy. Series precision resistors may realize 480 kΩ if their combined tolerance/drift budget is verified.

DIV ratio must remain 0.46875±0.015. Including ±1% resistor bounds and ±10 nA input current at 2.25 V, script gives 0.462969–0.477153; maximum Thevenin resistance 474.76 kΩ stays below 500 kΩ. Divider settling/layout and actual supply behavior still require checking. Timing acceptance for the assembled circuit adds measured propagation/release delays and instrument uncertainty.

Policy tradeoff: this bounds continuous held RTS but cuts continuous Tune or longer transmissions near 20 seconds. Releasing REQUEST ends transmit immediately **without resetting the one-shot**; another request during the active window gets only the remaining time. A steady held request cannot retrigger after expiration; a new edge after expiry can. Test early release, rapid re-key, expiry and reset/resume explicitly. The initial qualified rising edge starts the window; no trigger until power/USB/arming conditions are valid. Do not power-cycle the timer on request release as an undocumented workaround.

Alternative: omit timer and intentionally bypass only its qualification, retaining USB/arming/default-off logic; accept no hardware maximum continuous PTT interval. Population choice is **unresolved IN-008**. The coordinator should present these two concrete choices to the user before freeze. No application-health or sound-card-loss detection is claimed for either option.

## Checks and remaining gates

Arithmetic cross-checks: hand substitution above agrees with script rounding; timer is 2,097,152×9.6 µs. Sensitivity scenario `--v-min 4.0` must fail the 5 mA lower bound. Negative resistance and NaN inputs must fail argument validation. These are mathematical checks, not bench passes.

Resolve ME-003 radio voltage/current/leakage tolerance; actual supply/cable envelope and temperature; verified LED VF/driver/logic bounds; concrete arm/reset implementation; IN-008 population; and actual macOS/driver state-transition tests ME-008–010 before closing #12 or freezing #15/#17. Existing working-prototype reports do not verify this new isolated logic circuit. Keep all failures and observed pulses in evidence; no radio connection before prerequisite bench checks pass.
