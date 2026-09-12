# Research findings and proposed solutions

Reviewed September 11, 2026. These are engineering recommendations for the schematic, not a validated circuit or an assembly-ready BOM. No hardware measurements were made in this research pass.

## Decisions in brief

| Issue | Proposed resolution | Remaining work |
|---|---|---|
| RTS polarity | Invert active-low RTS; qualify with USB-active signal | Verify host commands and power transitions on a bench |
| Unintended prolonged PTT | USB-state inhibit; optional approximately 20-second hardware limit for FT8 | Choose timeout policy; validate startup and rearm behavior |
| Grounding | Isolated PhotoMOS PTT switch plus both audio transformers | Verify complete cable/shield/enclosure isolation |
| TRRS insertion | Retain TRRS; user will connect before radio power-on | Exact jack/pad verification only; no hot-plug redesign |
| Audio | Passive attenuation before transformers, adjustable level, DC blocking | Sound-card identification and actual level measurements |
| Radio pin mapping | Manual confirms mic pins 1/4 and switch pair 2/3 | Continuity check of the actual adapter |

## 1. RTS and USB-state control

The [Silicon Labs CP2102N datasheet](https://www.silabs.com/documents/public/data-sheets/cp2102n-datasheet.pdf), sections 4.1 and 4.3.7 and the QFN24 pin table, identifies active-low RTS. SUSPENDb is low during suspend and before enumeration completes. The datasheet recommends a 10 kΩ pull-down because SUSPENDb can float high during reset. These signals identify USB state, not application health.

Proposed logic, with `/RTS` meaning the physical active-low pin:

```
REQUEST = NOT /RTS
USB_READY = SUSPENDb
DRIVE = REQUEST AND USB_READY
DRIVE -> LED driver -> isolated PTT switch
```

| USB_READY | /RTS | Switch | Radio |
|---|---|---|---|
| 0 | Either | Open | Receive |
| 1 | 1 | Open | Receive |
| 1 | 0 | Closed | Transmit |
| Unpowered | Undefined | Open after release delay | Receive |

Use a pull-up on /RTS, a 10 kΩ pull-down on SUSPENDb, and a default-off LED driver. Candidate logic: TI [SN74LVC1G04](https://www.ti.com/product/SN74LVC1G04) inverter and [SN74LVC1G08](https://www.ti.com/product/SN74LVC1G08) AND gate, available in assembly-friendly SOT-23 packages with partial-power-down support. Add local decoupling. Do not assume Ioff specifications at zero volts guarantee behavior throughout a slow supply ramp: verify ramps/brownouts and add a supply supervisor if needed.

Use manual RTS control, with hardware flow control and automatic UART-transmit RTS mode disabled. Silicon Labs [AN571, section 5.9](https://www.silabs.com/documents/public/application-notes/AN571.pdf) documents modem-line control and its dependency on handshaking settings. WSJT-X supports RTS PTT on a selected serial port; use Rig=None, RTS PTT, and manual radio USB mode. Check actual settings with the [WSJT-X user guide](https://wsjt.sourceforge.io/wsjtx-main_en.html) and test on the intended OS/driver. Do not try to correct the circuit by guessing software polarity settings.

## 2. Replace shared-ground PTT with an isolated switch

Recommended candidate: Panasonic **AQY212GS PhotoMOS**, a normally-open isolated semiconductor relay. Connect its output terminals only between radio PTT and PTT return. Its input LED and driver remain entirely on the computer side. This replaces the radio-side NPN with a floating closure while preserving the required grounding action. It requires no radio-side power supply.

Panasonic lists 0.7 Ω maximum on resistance, 1 µA maximum off leakage, 5 ms maximum turn-on and 0.5 ms maximum turn-off; recommended load voltage is at most 48 V. Recommended LED drive is 5–30 mA, despite a lower operate-current threshold. Design for at least 5 mA across tolerances. [Panasonic specifications](https://industry.panasonic.com/ap/en/products/control/relay/photomos/number/aqy212gs)

For illustration, at 10 mA radio PTT current, 0.7 Ω produces only 7 mV drop. Actual PTT current and leakage tolerance still need checking. A transistor driver supplied from USB VBUS can drive the input LED without loading a bridge pin; calculate its resistor from minimum supply, maximum LED voltage and driver drop, then check maximum current at the opposite extremes. Drive the visible PTT indicator separately so its voltage drop does not affect the PhotoMOS input.

A phototransistor optocoupler is another option, but requires more care with minimum current transfer ratio and saturation. The [Vishay VO617A datasheet](https://www.vishay.com/docs/83430/vo617a.pdf) specifies CTR under a nonzero collector voltage; that figure alone does not guarantee a low enough saturated PTT voltage. PhotoMOS is the preferred candidate here for its directly specified closed-switch resistance. Exact ordering suffix and assembler availability remain to be checked.

Keep computer and radio copper separated across all three isolation components. Preserve separate MIC_RETURN, PTT_RETURN and RX_RETURN nets up to their intended connections; do not arbitrarily join them on the PCB. Use insulated jack mountings where a metal enclosure could bridge domains. USB shield termination must not accidentally bond to radio connector shells. No continuity across the assembled interface's computer/radio domains is the DC acceptance criterion, checked with all adapter cables attached. Isolation does not eliminate capacitive RF coupling, so RF filtering and station tests remain necessary.

## 3. Fail-safe scope and the timeout option

The proposed USB inhibit addresses reset/suspend and loss of USB power, subject to bench validation. It does not detect an application crash, a disconnected external sound card, or an unrelated program opening the serial port. An asserted RTS retained by the host can still transmit.

For this FT8-focused interface, recommend an **optional approximately 20-second maximum continuous PTT window**. A candidate is the non-retriggerable, rising-edge **LTC6993-1**. Its range extends to 33.6 seconds. A positive output pulse starts on a request edge; AND that pulse with REQUEST and USB_READY. Dropping REQUEST immediately ends PTT, while a stuck REQUEST ends when the window expires. A steady high input must not retrigger it. [Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc6993-6993-1-6993-2-6993-3-6993-4.pdf)

Calculated example: divider 2^21 and RSET=480 kΩ give 20.13 seconds nominal using the datasheet timing formula. Component tolerances and divider programming must be checked in the schematic. This is a proposed FT8 policy, not a requirement for all digital modes: longer transmissions and continuous Tune would be cut off. An early release does not reset this particular one-shot; a second request during its active window receives only the remaining window. Standard alternating FT8 slots leave time to rearm, but rapid manual re-keying must be tested and documented.

For strict startup behavior, permit a new transmit edge only after USB is ready and an idle RTS state has been observed; implement an arm latch if the host can leave RTS asserted across reconnect. Test timer power-up, resume, early abort and timeout before claiming a guarantee. A timeout bounds a stuck transmission; it cannot recognize why it occurred or prevent all short unintended transmissions. Immediate detection of sound-card loss would need host monitoring or additional sensing and is outside the simple hardware baseline.

## 4. TRRS decision

Per the user's instruction, use the TRRS connector and document connecting it before radio power-on; disconnect with the radio off as well. Live insertion protection is no longer a design blocker. Keep the project-specific mapping: tip=MIC_AUDIO, ring 1=MIC_RETURN, ring 2=PTT, sleeve=PTT_RETURN. Label the jack RADIO MIC/PTT, TS-700SP ONLY. This decision does not waive verification of the selected jack's pad numbers or the adapter wiring.

## 5. What the original radio documentation establishes

The downloaded Kenwood operating manual was visually checked on printed pages 3 and 6:

- Low-impedance microphone specification: 500 Ω. This does not establish the actual input resistance or sensitivity in millivolts.
- Transmit AF response: 400–2600 Hz.
- Receiver audio rating: 2 W into 8 Ω, corresponding to 4 Vrms at that rated loaded condition by V=sqrt(PR). It is not a guaranteed maximum unloaded output.
- External speaker: supplied 1/8-inch plug; inserting it disconnects the internal speaker.
- Figure 3, explicitly viewed from the rear of the microphone connector: pin 1 carries microphone signal, pin 4 its shield/return, pins 2/3 the PTT switch. Prototype history identifies 2 as PTT and 3 as PTT return.

Source: [Kenwood operating manual, archived by W5RKL](https://w5rkl.com/wp-content/uploads/2022/10/TS700sp-Operators-Manual.pdf), local copy `docs/references/ts700sp-operating-manual.pdf`. Rear/solder-side diagram orientation must not be reused as a front/mating-side view without mirroring.

The service PDF begins with TS-700S material but includes a **TS-700SP(K)** schematic. PDF page 73 shows the AF output through coupling capacitor C25 and the ground-referenced speaker-jack network; this supports using a high-impedance audio tap instead of an 8 Ω dummy load. Confirm board variant and actual DC offset on the physical radio. Source: [Kenwood service manual archive](https://w5rkl.com/wp-content/uploads/2022/10/kenwood-ts-700sp-service-manual.pdf), local copy `docs/references/ts700sp-service-manual.pdf`. Do not substitute the earlier S-model circuit for the SP sheet.

## 6. Audio solution

Use two passive transformer paths with attenuation **before** each transformer to limit winding signal level. Add adjustment and DC blocking appropriate to each endpoint. Avoid DC in a winding from sound-card microphone bias. Provide configurable tip/ring routing on RX AUDIO OUT because the sound card is not yet identified. Select one headphone output channel by default; if both are used, combine through separate resistors.

Candidate transformer: **Bourns LM-NP-1001-B1L**, 1:1, nominal 600:600 Ω, through-hole. Its datasheet gives a typical voice-band response over 200–3500 Hz, insertion loss up to 1.5 dB at 2 kHz and a +3 dBm upper listed power level. The datasheet includes bottom-view winding/pin drawings and dimensions. This is a credible candidate, not a claim of current PCBA stock or measured performance in our loading network. [Bourns datasheet](https://www.bourns.com/pdfs/LMNPLP.pdf)

Starting networks for calculation and bench evaluation, **not final BOM values**:

| Path | Illustrative fixed divider before transformer | Ideal unloaded result |
|---|---|---|
| TX, one sound-card channel | 10 kΩ series / 100 Ω shunt | 1 Vrms becomes 9.9 mVrms, about -40 dB |
| RX, speaker output | 22 kΩ series / 1 kΩ shunt | 4 Vrms becomes 174 mVrms, about -27 dB |

Transformer and destination loading change these results. Include a level trimmer that can reduce to zero; choose its position/value jointly with winding impedance and destination loading. Provide resistor options if the measured microphone needs more drive than the initial conservative pad permits. Neither a 500 Ω microphone specification nor an 8 Ω speaker rating means we should place those resistor loads across the connectors.

Use coupling capacitance calculated from effective impedance, not a generic small capacitor. For example, a 10 µF capacitor seeing 600 Ω has an ideal high-pass corner near 26.5 Hz; actual source/load and transformer behavior must be included. Use a nonpolar part or establish DC polarity before selecting an electrolytic. Add optional RF filter footprints at the radio entries and verify that their loaded response preserves the voice band.

Bench acceptance: sweep approximately 300–3000 Hz, record gain and clipping at adjustment extremes, and test at the actual sound card's maximum output and the radio's intended AF settings. The interface should not introduce appreciable extra roll-off within the radio's specified useful band. Begin TX adjustment at minimum. Do not equate the receiver's 10%-distortion power rating with a clean operating point for decoding.

## 7. What remains before schematic freeze

1. Identify the sound card and intended OS/driver. Determine its input contacts, DC bias, clipping point and output amplitude.
2. Confirm adapter continuity against the now-documented radio pin mapping.
3. Measure PTT open voltage and sink current; test the proposed isolated closure and off-state leakage using a simulated load first.
4. Measure microphone bias and the signal level that produces the desired clean SSB output. Check RX DC offset and audio level at normal/high AF settings.
5. Decide whether to populate the FT8 timeout. Verify complete logic and power-transition behavior before radio connection.
6. Select exact orderable component variants and connector MPNs; compare every symbol/footprint against the manufacturer drawing. Record assembler sourcing separately from electrical suitability.

Research resolves the architecture and documentary pinout questions. It narrows the remaining measurements to calibration, actual-unit confirmation and validation of the new control circuit.
