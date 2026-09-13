# Provisional CAD-completion contract

Issue: [#47](https://github.com/zarthur/ts-700-usb/issues/47). This contract permits a complete, reviewable Rev A KiCad model before human measurements. It does not permit a fabrication, procurement, radio-operation, or validation claim.

## Gates

**Provisional CAD completion** requires a complete schematic and PCB using documented defaults, visible `PROVISIONAL`/`NOT FOR FABRICATION` markings, clean or justified ERC/DRC, generated review artifacts, and a reproducible candidate-release manifest. It may contain assumptions listed below.

**Physical finalization** follows only after the CAD package is complete. Actual cable/jack continuity and dimensions, radio PTT/mic/RX behavior, sound-card routing/levels/bias, host transitions, enclosure constraints, provider capability, and prototype/RF results may change values, footprints, dimensions, and release eligibility. Repeat affected CAD checks after each change.

## Fixed sheet contract

| Owner | File and references | Interface ownership |
|---|---|---|
| Coordinator | Root sheet and project settings | `USB_5V`, `COMPUTER_GND`, `MIC_AUDIO`, `MIC_RETURN`, `PTT`, `PTT_RETURN`, `RX_AUDIO`, `RX_RETURN`; connects sheets by named hierarchical labels only. |
| #15 | `hardware/usb-ptt.kicad_sch`, 100–199 | USB-C, bridge, protection, host-domain control, floating `PTT`/`PTT_RETURN` closure, timeout, indicator and test points. |
| #16 | `hardware/audio.kicad_sch`, 200–299 | Isolated TX/RX paths, audio connectors, transformers, attenuation, DC blocking and audio test points. |

`MIC_RETURN`, `PTT_RETURN`, and `RX_RETURN` remain distinct radio-side nets. No writer may connect a computer return, shell, mounting feature, or test instrument ground across an isolation boundary.

## Stable CAD assumptions

| ID | Default used before human evidence | Later evidence that may revise it |
|---|---|---|
| CAD-A01 | CP2102N bridge and documented USB-C/ESD candidates | exact supplier drawing, assembly capability and host test |
| CAD-A02 | Active-low RTS, USB-qualified default-off PhotoMOS PTT and populated non-retriggerable ~20-second limiter | radio PTT envelope, host transition and timer bench results |
| CAD-A03 | One selected sound-card TX channel; optional resistor mixing DNP | card contact mapping, output level and loading |
| CAD-A04 | Two 1:1 audio transformers with attenuation before transformers and DC blocking | endpoint levels/bias/loading and loaded response |
| CAD-A05 | Conservative two-layer rules and approximately 70 × 50 mm target | fabricator capability, connector/enclosure dimensions and placement review |
| CAD-A06 | Candidate release is non-procurement and provider-neutral | selected provider, sourcing snapshot, assembly policy and prototype evidence |

Every assumption must be visible in the relevant schematic/PCB text or field and cited from this table in the generated review package.
