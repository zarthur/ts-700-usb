# Design decisions

## Control and safety

Use active-low CP2102N `/RTS` through inversion and an AND gate qualified by `SUSPENDb`. Pull `/RTS` high and pull `SUSPENDb` low (10 kOhm) so power-up, reset, and suspend are open. Use a transistor LED driver for the PhotoMOS and a separate status LED driver. A PhotoMOS output connects only across `PTT` and `PTT_RETURN`.

Populate a non-retriggerable approximately 20-second limiter. It is a transmission bound, not application-health or sound-card-loss detection. The selected population does not freeze its circuit: verify the measured radio PTT envelope, PhotoMOS/driver margins, timing tolerance, slow ramps, brownout, sleep, reconnect, early release, stuck RTS and rearm before radio connection. Early release does not reset the active window; a new request must satisfy the documented non-retriggerable rearm behavior.

## Audio and grounding

TX and RX each cross one 1:1 audio transformer. Attenuation precedes each transformer; trimmers can attenuate to zero; coupling capacitors prevent winding DC. Maintain `MIC_RETURN`, `PTT_RETURN`, and `RX_RETURN` as distinct radio-side nets. The selected sound-card channel is the default RX feed; optional resistor mixing is DNP until supported by the actual card.

## Freeze rule

Exact values and approved substitutions require measured endpoint data and `docs/component-verification.md` evidence. A source artifact can be provisional; a schematic, PCB, BOM, or fabrication release cannot be called final while any corresponding table entry is unmeasured.
