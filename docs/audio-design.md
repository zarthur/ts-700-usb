# Provisional audio conditioning calculations and measurement contract

Issue: [#13](https://github.com/zarthur/ts-700-usb/issues/13). Status: **provisional calculation framework; no endpoint values, component values, or hardware results are finalized**. This document turns the Rev A audio architecture into reviewable equations and test-point requirements. It does not authorize schematic freeze, component purchase, radio connection, or a production BOM.

Inputs and test methods are identified in [measurements.md](measurements.md), especially ME-004 through ME-007 and ME-011. Transformer and candidate-component facts are recorded separately in [component-verification.md](component-verification.md). The architecture and non-negotiable constraints derive from [DESIGN](../DESIGN.md) REQ-02, REQ-08, REQ-10 and REQ-11 and [research](research-solutions.md#6-audio-solution).

## Interface contract

There are two galvanically isolated, passive paths. Each path has its attenuation and level adjustment **before** its transformer. Each transformer winding is protected from DC by a coupling network whose voltage rating and polarity are selected only after the endpoint DC measurements. The radio-side nets remain separate: `MIC_RETURN` is paired only with microphone audio, `RX_RETURN` is paired only with receive audio, and `PTT_RETURN` is outside these audio paths. Neither PCB copper, cable shield, jack shell, enclosure hardware, nor a test fixture may silently join these returns to one another or to the computer domain.

| Path | Intended direction | Computer-side endpoint (unresolved) | Radio-side endpoint (unresolved) | Required topology |
|---|---|---|---|---|
| TX | sound card to radio microphone | One identified headphone/line output channel | `MIC_AUDIO` / `MIC_RETURN` | selected channel → DC block → fixed attenuation → zero-capable adjustment → transformer → radio-side DC block / optional RF network |
| RX | radio receive audio to sound-card input | One identified microphone/line input contact | radio receive-audio contact / `RX_RETURN` | radio-side DC block / optional RF network → fixed attenuation → zero-capable adjustment → transformer → computer-side DC block → identified input contact |

The TX source is one selected channel. Left and right headphone outputs must **never** be directly connected. If the identified card requires both channels, each channel uses its own mixing resistor before the TX attenuator; the resistor values and resulting source impedance are unresolved until ME-006. RX contact selection is likewise unresolved until ME-007 identifies the card's actual input routing and bias.

## Symbols and calculation method

Use RMS voltages for sine-wave gain calculations unless a measurement explicitly records peak or peak-to-peak values. Convert waveform readings before comparing them: `Vpk = sqrt(2) × Vrms` and `Vpp = 2 × sqrt(2) × Vrms`. All measured values carry frequency, source setting, load, instrument impedance/bandwidth, and uncertainty from the worksheet record.

| Symbol | Meaning | Source/status |
|---|---|---|
| `VSC_TX(f)` | sound-card selected-channel open-circuit RMS output | ME-006, unresolved |
| `ZSC_TX(f)` | sound-card selected-channel output impedance | ME-006, unresolved |
| `VTX_REQ(f)` | radio microphone RMS level that achieves the agreed clean transmit result | ME-004, unresolved |
| `ZMIC(f)` | effective microphone input impedance under the selected radio condition | ME-004, unresolved; do not substitute the documented 500 ohm microphone specification |
| `VRA(f)` | receive-audio source RMS level at the radio's intended AF setting | ME-005, unresolved |
| `ZRA(f)` | receive-audio source impedance | ME-005, unresolved |
| `VSC_RX_MAX(f)` | sound-card input clean/clipping limit, RMS at its actual selected contact | ME-007, unresolved |
| `ZSC_RX(f)` | sound-card input impedance and any bias network | ME-007, unresolved |
| `nTX(f)`, `nRX(f)` | loaded transformer voltage ratio, secondary/primary, including frequency response | datasheet candidate only; actual loaded value unresolved |
| `RFTX(f)`, `RFRX(f)` | optional radio-entry RF network transfer | not selected; unresolved |
| `A_TX(f)`, `A_RX(f)` | total linear voltage transfer from source to destination | calculated only after above inputs are recorded |

For a passive pre-transformer divider with series resistance `RS` and shunt/adjustment equivalent `RP`, first reduce the source-side load to `ZL = RP || ZPRI`, where `ZPRI` is the transformer primary impedance under the actual secondary load. The divider transfer is:

```
Adiv(f) = ZL(f) / (ZSC(f) + RS + ZL(f))
Apath(f) = Adiv(f) × n(f) × Rf(f) × Acoupling(f)
Gain_dB(f) = 20 log10(|Apath(f)|)
```

`Acoupling` includes both coupling capacitors and must include their real source/load impedances, not an assumed 600-ohm termination. The adjustment setting is evaluated at its minimum, nominal calibration point, and maximum. Minimum must provide a demonstrable zero or effectively muted destination signal; its residual is measured rather than assumed from potentiometer wording.

The conservative TX condition must show that maximum intended sound-card output and maximum adjustment do not exceed the later agreed clean `VTX_REQ` range or transformer limit. The conservative RX condition must show that maximum intended radio receive level and maximum adjustment do not exceed `VSC_RX_MAX`. A result cannot be called compliant merely because a published receiver rating suggests `4 Vrms` at 2 W into 8 ohm: that is neither a required 8-ohm design load nor a clean/unloaded source limit.

## Frequency response, DC, and transformer bounds

For every series coupling capacitor, calculate its first-order corner using the resistance it actually sees:

```
fc = 1 / (2π C × (RSRC + RLOAD))
|HHP(f)| = f / sqrt(f² + fc²)
```

Where two coupling networks and the transformer response are present, multiply their linear transfers before converting to dB. Record the loaded response at least at 300, 400, 1000, 2600, and 3000 Hz, plus any identified transformer corner. The radio's documented transmit response is 400–2600 Hz; allowable additional interface roll-off is **unresolved** and must be agreed from actual endpoint measurements before setting an acceptance threshold.

The candidate Bourns LM-NP-1001-B1L documentary limits do not replace a loaded calculation. For each winding, record `Vrms`, `Vpk`, DC voltage before and after its coupling capacitor, and estimated sinusoidal power `P = Vrms² / Reffective` only when `Reffective` is measured or defensibly derived. Compare the resulting level with the selected transformer's documented frequency-dependent limits and insertion loss. Do not infer transformer headroom from its nominal 600:600-ohm label, and do not place DC across either winding.

## Required test points and evidence

The schematic owner allocates final designators within the audio reference range after this issue is merged. These names are an interface/test contract, not a request to edit the provisional CAD sheet now.

| Test point / observation | Measurement purpose | Required conditions and evidence |
|---|---|---|
| `TP_TX_SRC` | selected sound-card channel amplitude, clipping and source behavior | ME-006; measure unloaded and with the intended network, document channel and host settings |
| `TP_TX_PAD` | attenuation before the TX transformer | measure divider output at min/nominal/max adjustment; prove no direct stereo short |
| `TP_TX_PRI` and `TP_TX_SEC` | transformer loaded ratio, response and winding DC | ME-011 sweep; use differential/isolated measurement that does not bridge domains |
| `TP_MIC_OUT` relative to `MIC_RETURN` | delivered microphone audio and radio-side DC offset | ME-004/011; begin at minimum adjustment and connect radio only under the staged procedure |
| `TP_RX_IN` relative to `RX_RETURN` | actual radio receive-audio amplitude, DC and loading | ME-005; high impedance first, no assumed 8-ohm load |
| `TP_RX_PAD` | RX attenuation before the transformer | measure divider output at all adjustment extremes and intended AF settings |
| `TP_RX_PRI` and `TP_RX_SEC` | loaded ratio, response and winding DC | ME-011 sweep; preserve isolation during probing |
| `TP_SC_IN` | sound-card input amplitude, bias and clipping margin | ME-007/011; identify the exact contact/mode/AGC/enhancement state |

For each sweep, capture source frequency and amplitude, every test-point RMS amplitude, phase/polarity where it affects wiring, distortion/clipping observation, DC offset, adjustment position, cable IDs, endpoint settings, and raw scope/audio files. Use high-impedance probes first. A grounded bench probe can defeat isolation; document probe ground routing and use appropriate differential or isolated instrumentation when comparing across transformer domains.

## Provisional decision table and release gate

| Decision | Current disposition | Evidence required to resolve |
|---|---|---|
| TX fixed pad, trimmer range, coupling capacitance and RF filter | No values selected | ME-004 and ME-006, loaded calculation across adjustment/tolerance extremes, exact passive MPN evidence |
| RX fixed pad, trimmer range, coupling capacitance and RF filter | No values selected | ME-005 and ME-007, loaded calculation across adjustment/tolerance extremes, exact passive MPN evidence |
| Transformer selection and loading | Candidate only | verified pin/dimension/library audit plus measured loaded response and voltage/power margins |
| Sound-card RX contact and any stereo mixing | Unresolved | exact card identity, contact/bias/routing results from ME-006/007 |
| Final audio acceptance limits | Unresolved | agreed clean radio and card endpoints, documented instrument method, ME-011 results |

Before #13 can close or the audio schematic can freeze, an independent reviewer recalculates the TX and RX extrema from the recorded endpoint data, verifies the actual transformer pin/pad mapping, confirms DC isolation with the complete cable assembly, and identifies the reviewed commit. Until then, this is a reusable calculation and test framework only; issue #13 remains open and any downstream CAD/BOM values must be visibly provisional.

## Checks recorded

- Documentary cross-check against `DESIGN.md`, `docs/research-solutions.md`, `docs/measurements.md`, and `docs/component-verification.md`.
- No CAD, BOM, component-selection, or physical-test claim is introduced by this document.
- Markdown/link validation and repository checks are recorded in the pull request for the exact commit under review.
