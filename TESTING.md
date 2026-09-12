# Rev A staged test procedure

1. Inspect soldering, orientation, isolation gaps, cable labels, and no-populated-DNP configuration. With no radio attached, verify USB-only current and CP2102N enumeration.
2. Use a simulated PTT load to measure open leakage, closed voltage/current, default-open startup, reset, slow-ramp, suspend/resume, unplug, application-close, stuck-RTS, timeout, early-release, and rearm behavior.
3. With radio power off, verify TRRS continuity and absence of DC continuity between computer and radio domains with all interface cables attached.
4. Sweep 300–3000 Hz at TX/RX adjustment extremes. Record source level, gain, clipping, DC offsets, waveform, and settings. Begin TX at minimum.
5. Only after steps 1–4 pass, connect the radio for staged RX, TX, FT8 and RF-immunity tests using an appropriate RF load. Record quantitative limits before testing and link the tested assembly to the KiCad commit and BOM.

Failure at any stage blocks radio connection and release closure. Passing ERC/DRC alone is not a bench or RF pass.
