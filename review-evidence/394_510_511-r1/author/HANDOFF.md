# [A215] handoff: #394, #510, #511 owner decisions (2026-09-23)

Lane: `$LANES/394-510-511-decisions`, branch `394-510-511-decisions`,
base live dev `759da623072358afdb0e9d570a7b4b6a788492c9`.
Head: `64bcf768d28b4b9763fbe5917a734bcefa2a66e0`. Not pushed; no PR opened, per the brief.

## Commits (one-line subjects, no trailers)

| SHA | Subject |
|---|---|
| `909d8febee108a16769e76363c3967115974ed2b` | Record the #394 decision: v1.2 is a declared non-redundant end station, Milan Section 8 revisited with the P4/P5 PCB |
| `6c5d5b5c08a7094161959347feafee8d3cf86bdb` | Record the #510 decision: the MVU system-unique-id and media-clock-reference rows are RECOMMENDED and answered NOT_IMPLEMENTED for October |
| `b38634f4792f5dada4da4c3902434cdf8dbc85de` | Record the #511 decision: delayAsymmetry is not modelled for v1.2 and the live UART tuner stays donor-bench-only |
| `71ddc7e90bd1d70ba45ec4509bc864b1ae41ebac` | Say which FR_NFR out-of-scope entries are recorded decisions with a revisit trigger |
| `dcbe3cfaadcd7c340e74ce9b62bf06e9d401c2fc` | Name the processor issues that carry FR-MVU-02's command behavior if P4 implements it |
| `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` | State in the #511 record that the donor's ingress/egress latch compensation is not adopted |

11 files, +199/-26, all Markdown. No RTL, firmware, builder, configuration or
test file changed. No generated matrix needed regeneration: `gen_module_matrix.py
--check` is green, and no edited page is generator output.

## Closure verdicts (PR-BODY.md)

| Issue | Keyword | Why |
|---|---|---|
| #511 | `Closes #511` | Acceptance 1 to 5 met (per-acceptance table posted on the issue) |
| #394 | `Relates to #394` | Acceptance 2 (bench proof under option (a)) needs hardware; not done. Acceptance 1 and 4 met, 3 n/a under (a) |
| #510 | `Relates to #510` | Acceptance 2 is met here, but the protocol processor's F01.5 still lists `P-EN-MVU-SUID` / `P-EN-MVU-MCR` = 1 / 1 at the pin `424c688` (line 169) and at its main `fbc1f71` (line 170). PP issue 77 owns it. Acceptance 3's byte-exact evidence covers `0x0002` only (pp_top M4) |

The assignment comment says "closes all three". The frozen acceptance criteria of
#394 and #510 are not fully met by a docs PR, so the owner has two options:
amend them publicly (for example, move #394 acceptance 2 into a bench issue
under #117/#75, and accept #510's donor half as tracked by PP77/PP55/PP56), or
keep both open after this merges.

## Held files: no edit required

No acceptance criterion needs `CHANGELOG.md`, `docs/integration/BAREMETAL_FIRMWARE.md`
or `docs/ENDSTATION_BUILDER.md`. Neither of the last two mentions redundancy,
the MVU recommended commands or delayAsymmetry (searched: `redundan`,
`Section 8`, `MILAN_REDUNDANCY`, `delayAsym`, `asymmetry`, `SYSTEM_UNIQUE`,
`MEDIA_CLOCK_REF`; the only hit is an unrelated "input/output asymmetry" at
`docs/ENDSTATION_BUILDER.md:848`).

Optional, for the lane that holds `CHANGELOG.md`: if the owner wants a changelog
line, this exact text satisfies `check_doc_style.py` and must not say "N MVU
commands" (`check_feature_status.py` judges that count against the served list).
Insert a Contents entry after the `## Contents` heading, above the current first
entry:

```markdown
- **[Unreleased - three product-profile decisions](#unreleased---three-product-profile-decisions)** -- Scope recorded, no behavior change.
```

and this section above `## Unreleased - gPTP egress launch time`:

```markdown
## Unreleased - three product-profile decisions

- No gateware, firmware or builder behavior changes.
- v1.2 stays a declared non-redundant end station (#394).
- Milan Section 8 is revisited with the P4/P5 PCB.
- FR-MVU-02 is now SHOULD, Milan's own level (#510).
- Those recommended commands still answer NOT_IMPLEMENTED.
- P4 implements them if the conformance lab requires it.
- delayAsymmetry is not modelled; its value is zero (#511).
- The live UART tuner stays donor-bench-only.
```

## Material assumptions (stated in the PR and on the issues)

1. #510 "downgraded to RECOMMENDED" is recorded as FR-MVU-02 priority M to S
   (RFC 2119 RECOMMENDED = SHOULD), verification stays T (the fallback is graded).
2. #511 revisit trigger: the decision cites REQ-PTP-06 elaboration constants and
   the single cabled port, so the record revisits "when a profile adds a second
   cabled port" (such as #394's Section 8) and requires a REQ-PTP-06 amendment
   before any runtime correction. The owner may want to confirm or replace it.
3. #394 README wording: P3 "redundancy net cabled + failover proof" became
   "one-port link loss + return proof (#394)"; P4 gained "redundancy (Section 8)
   revisit, #394". The ASCII columns were kept aligned.
4. #511: the donor's proposed ingress/egress latch compensation is recorded as not
   adopted. REQ-PTP-06 already forbids applying a correction twice. The owner's
   comment covers delayAsymmetry and the tuner; this third item follows from the
   existing requirement, not from a new choice.

## Discovered work (not fixed; for the manager to file or route)

1. `tests/features/aecp_response_contract.feature` scenario "a Milan MVU command
   is answered as a VENDOR_UNIQUE response with its protocol_id intact" sends
   `build_mvu_command()` with its default `MVU_GET_MILAN_INFO` (0x0000) and
   asserts status 1. The offline model (`tests/steps/aecp_engine_model.py`) has
   no MVU dispatch, while the pinned engine serves GET_MILAN_INFO (pp_top M1).
   So the model disagrees with the RTL for a served command. Re-pointing the
   scenario at `0x0002` and adding `0x0001`, `0x0003` and `0x0004` rows would
   also give the parent a (model-level) fallback check for #510's commands.
2. Protocol processor tb/pp_top grades only `0x0002` of the four; per-command
   arms for `0x0001`/`0x0003`/`0x0004` (PP55/PP56/PP77 scope).
3. Protocol processor F01.5 `P-EN-MVU-SUID` / `P-EN-MVU-MCR` = 1 / 1 (PP77).
4. gPTP processor citations: donor issue 58 cites 802.1AS-2011 11.2.15 (the
   MDPdelayReq machine, whose `computePropTime()` has no asymmetry term); the
   donor's historic prototype pages cite 10.2.4.5 (that clause is `syncInterval`).
   The 2011 text puts delayAsymmetry at 10.2.4.8, applied in 10.2.12 and
   11.2.13.2.1. Recorded in `GPTP_PLANE.md`; the donor text is the donor's to fix.
5. The builder's unknown-`gptp`-key refusal (`_known_gp`,
   `sw/builder/endstation_builder.py:3940`) has no test that plants an asymmetry
   key, so the #511 exclusion's configuration half is structural and ungraded
   (SUGGESTION).
6. #417 has no line naming the #394 Section 8 revisit, and neither #416 nor #417
   names the #510 P4 implementation trigger. #416 lists #394 as a release-scope input.
7. `scripts/nvm_contract.py`, `KL_nvm_backend.sv` and the firmware reserve
   SUID and MCR record slots. That is space reserved, not a support claim, so
   it is consistent with #510 and left unchanged.

## Evidence (receipts in `receipts/`, private; public comments carry the content)

| Receipt | What it shows |
|---|---|
| `standards-clause-receipts.txt` | Line-numbered clause hits in the extracted Milan v1.2 and IEEE 802.1AS-2011 (+Cor1/Cor2) text |
| `394-single-interface-evidence.txt` | `MILAN_FEATURES_FLAGS = 0`, pp_top M2 grades it, `N_IF_P(1)` at the top, one `--eth-port` |
| `510-pp-pin-mvu-evidence.txt` | Engine banner and the one non-echo MVU decode (`KL_aecp_engine.sv:1290-1296`), no SUID/MCR state, pp_top M4 (`sim_main.cpp:2330-2340`), no arm for `0x0001/3/4`, F01.5 line 169 |
| `510-pp_top-run.log` | `make -C protocol-processor/tb/pp_top run` at `424c688`: 1371 PASS, 0 FAIL (M1 to M9 run from `MilanInfoPhase::run`) |
| `511-gptp-pin-asymmetry-grep.txt` | At gPTP pin `c1b6174`: any `asym` outside `docs/history` and SVG: exit 1 (none) |
| `511-parent-no-asymmetry-control.txt` | Parent hdl/sw/configs/avdecc/scripts: no asymmetry control; `_known_gp` set |
| `baseline-gates.txt` | All documentation gates green at the base |
| `per-commit-gates.txt` | docs_check, feature_status self-test, em-dash, gen_toc, doc_style, gptp_docs: 0 at each of the six commits |
| `gates-at-64bcf76.txt` | Full gate set at the head, all exit 0 |
| `test_builder-at-909d8fe-tree.log`, `-at-71ddc7e.log`, `-at-64bcf76.log` | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 needs a local arty build report) |

`test_builder.py` was not run at `6c5d5b5` or `b38634f`. Those commits change
only Markdown the builder does not read. The two pages its source names
(`README.md`, `GPTP_PLANE.md`) appear only in comments and strings.

## Worktree state

The three pinned submodules (`third_party/verilog-axis`, `protocol-processor`,
`gptp-processor`) were initialised in this worktree with the CONTRIBUTING 2.2
command, at their gitlinks. The pp_top build outputs and Python caches were
removed afterwards. `git status` is clean and HEAD is the branch tip above.

## Posted

- #394: https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5801831612
- #510: https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5801832005
- #511: https://github.com/kebag-logic/milan-fpga/issues/511#issuecomment-5801832329

Comment sources are in `comments/`. The lane stops here: no push, no PR, no merge.
