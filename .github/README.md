# Repository automation

`PR governance` validates the required documentary record, repository-relative
Markdown links, whitespace, portable scripts, and KiCad ERC/DRC reports. It
installs KiCad on the hosted runner, but runs the CAD checks only with a
compatible KiCad 10.x CLI. An incompatible hosted CLI writes a clearly marked
skipped report instead; local KiCad 10 visual/ERC/DRC review remains required.
ERC/DRC report artifacts are consistency evidence;
they do not certify visual KiCad review, dimensions, hardware measurements, or
radio/RF validation.

`Approved squash merge` runs only when a coordinator applies
`approved-for-merge` to a non-draft PR into `main`. It revalidates the body
against the current head, requires the repository's required checks to pass,
then squash-merges and deletes the source branch. It never creates a review or
self-approval. Repository Actions settings must permit workflow pull-request
and contents write access; branch protection should require the `governance
record` check before enabling unattended merges.
