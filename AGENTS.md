# TS-700SP implementation coordination

Read PLAN.md, docs/implementation-plan.md, DESIGN.md and docs/status.md before work.

- Root coordinator owns integration, root schematic, shared project settings, pushes, PRs and merges. Use one isolated worktree/issue branch per writer. Never share a writable checkout.
- Give every subagent an issue, base SHA, file ownership, interface contract, deliverables and checks. Stop and coordinate before editing another owner's files.
- One writer per CAD file; one PCB writer. Merge prerequisites before branching dependent work. Refresh branches after intervening merges and repeat affected checks.
- Independent review must identify the exact final commit. Authors cannot be sole reviewers. Changed commits need renewed applicable checks/review.
- User authorizes automatic squash merges after review/checks. Respect GitHub protections. If self-approval is unavailable, record actual independent agent review in the PR body; never fabricate account approval.
- Use Closes only for satisfied issues; use Refs for provisional or partial work. Keep unmet physical criteria and epic gates open.
- Missing measurements allow provisional work, never invented data or design-freeze/validation claims. Report blockers and continue independent tasks.
- Preserve separate computer/radio domains and MIC_RETURN/PTT_RETURN/RX_RETURN. Retain TRRS; connect/disconnect with radio off. Do not order hardware or operate a radio without separate applicable authorization.
- Keep generated review/release output separate from editable CAD; no empty custom libraries or fabricated mechanical proof.
- Record checks, warnings, reviewed SHA and unresolved inputs in PRs/reports. Update status after integration.
