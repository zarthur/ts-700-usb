# Candidate release package

Issue: [#23](https://github.com/zarthur/ts-700-usb/issues/23). A candidate package is a reproducible CAD-review artifact, not a fabrication, procurement, assembly, radio-operation, or validation release.

## Command contract

From a clean checkout at the intended commit, run:

```sh
scripts/export-release.sh \
  --source-sha "$(git rev-parse HEAD)" \
  --output-dir /absolute/path/outside-the-checkout/ts700sp-rev-a-candidate
```

The command accepts only a full lowercase 40-character SHA that exactly matches `HEAD`. It rejects tracked source changes, a pre-existing output path, an output path inside the checkout, missing/incomplete CAD, non-KiCad-10 CLI, or ERC/DRC violations. On failure it removes only the newly-created explicit output directory; it never edits source CAD or `fabrication/`.

When the complete provisional model exists, the package contains source copies, KiCad 10 ERC/DRC JSON, schematic PDF/SVG/netlist, board STEP/SVG, candidate BOM/placement, Gerbers, drills, a visible provisional notice, and a checksum manifest. `scripts/validate-candidate-release.py` checks the package before writing the manifest and can re-check it later:

```sh
scripts/validate-candidate-release.py \
  --package /absolute/path/outside-the-checkout/ts700sp-rev-a-candidate \
  --source-sha "$(git rev-parse HEAD)"
```

The current repository intentionally lacks a populated PCB and circuit model, so export must fail before creating a package. That is the expected safe result until #15–#21 have completed their provisional CAD and review gates.

## Deferred gates

The package labels itself `PROVISIONAL — NOT FOR FABRICATION, PROCUREMENT, ASSEMBLY, OR RADIO OPERATION`. It has no provider SKU, substitute, placement approval, mechanical-fit proof, order authorization, or hardware-validation claim. The assumptions and required physical-finalization evidence are in [cad-completion.md](cad-completion.md). Provider selection and an independently reviewed board remain prerequisites for the eventual #22–#23 release work.
