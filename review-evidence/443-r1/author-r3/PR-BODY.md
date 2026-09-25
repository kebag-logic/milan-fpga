[A310]

Closes #443

## Status

Ready for independent merge delta review at local head `b3458db0db5a7c8b15582d80b492620f05f62e70`. Publication remains with the manager.

## Description

Expose render setpoint state at `RENDER_STAT` (`0x8DC`). The existing listener selector chooses fill, prefill and convergence; the upper half reports global saturating rails. Absent stages supply structural zero. The register map, production class and latency documentation define the layout and semantics. The latency page also corrects its TDM frame-pin statement to reflect the shipping TDM8 shape.

## How to reproduce

Select a listener through `STRM_SEL` and read `0x8DC` while receiving media.

## How to validate

Integration checks compare bus reads with source taps through prefill, convergence and a rail. The absent-stage control reads zero; the wrong-fill mutant fails its named check. Round 1 passed two-listener selection and the complete default regression. Its requested gates returned zero. Builder gate 11 was NOT RUN because the calibration placement report was absent. Round 2 results are recorded below.

Generic synthesis counts from base `0755923d983218ca6ca9db6891a558cbe6425b8d` to implementation head `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`: `milan_csr` 70,355 to 70,466; `milan_datapath` 1,633,435 to 1,631,783. The decrease is unattributed; these counts make no physical area or timing claim. Round 2 changes no RTL.

## Round 2

Addresses R320-1 F1-F3 and R321-1 F1-F5 under the recorded assignment:

- Replace the stale unmapped assertion with driven `RENDER_STAT` reads, write-ignore checks, explicit zero ties and full-width rail data. Preserve the neighbouring unmapped checks and grade all four listener indices.
- Grade `STRM_SEL[9]` with talker selection and nonzero listener indices. The control campaign now requires the formerly surviving selector mutant to fail its named check.
- List `render_csr_controls.py` in the testing guide with author and reviewer ownership.
- Add the Unreleased entry and record that VERSION remains `0x0002_0060`; the release step owns the minor bump.
- Add the `0x8DC` register-groups row and clarify reset selection, shared-selector snapshot effects and identification before the minor bump.

All required gates returned 0. The CSR variants pass 380, 380, 115, 38 and 380 checks. The full `aclk` leg passes 189 checks. The render suite passes 150 shipping checks, 64 two-listener checks and five existing controls. The render CSR campaign passes 63 clean checks and 32 absent-stage checks; both wrong-fill and bit-9 mutants exit 1 at their required named checks. The standalone missing-decode mutant also exits 1 at its named check. All mutants build successfully; their enclosing campaigns return 0.

The front-end gate actually ran: zero first-party findings and four existing pinned-processor findings, exactly matching the unchanged ratchet. Both documentation modes pass; normal mode covers the inventory-parity check that cannot run without repository metadata.

Round 2 review status is superseded by the merge-dev assignment below.

## DoD

Acceptance items 1, 2, 3 and 5 are met locally. Item 4 follows the manager decision: no `STREAM_INTERRUPTED` wiring. One independent merge delta review remains pending.

## Merge-dev round

Merged dev `864b36f5e9450ef64f75ca3f0d68c44330e447d7` into the lane. Both Unreleased entries are retained verbatim. Local head: `b3458db0db5a7c8b15582d80b492620f05f62e70`. All requested gates have a final exit status of 0. One independent delta review is assigned; the other positive review stands on the ancestor.

The only manual merge resolution is in `CHANGELOG.md`: both Unreleased sections and both Contents entries remain verbatim. Submodules match the merged gitlinks, including processor pin `990f96526bb89356c963a260ebbdcf2a77e6623a`. The worktree is clean.

The complete datapath regression passes, including 190 `aclk` checks. The CSR variants pass 380, 380, 115, 38 and 380 checks. The render CSR campaign passes 64 clean checks and 33 absent-stage checks; both mutants build and fail their required named checks. The render suite passes 152 shipping checks, 65 two-listener checks and five existing controls.

Both documentation modes, the em-dash check against the merged dev tip, documentation style, Contents, anchors, cited paths, parser, three idiom checks, test-evidence check and whitespace check pass. The parser baseline remains zero first-party findings and four existing pinned-processor findings. Three Markdown checks initially refused a missing locked dependency; after installing the recorded lock outside the worktree, all three returned 0. No repository edit was made for that prerequisite.
