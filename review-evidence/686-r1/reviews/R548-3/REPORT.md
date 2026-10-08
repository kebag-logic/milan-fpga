[R548] POSITIVE - exact head 9c601b5983acfd60fb269b9a88c27b48cab7cf65

# R548-3 internal cleared-context review: issue #686 / PR #695, round 3

- Head `9c601b5983acfd60fb269b9a88c27b48cab7cf65`, tree `d2337a496fb13813beb2f4a13aefcaca0e0a94db`. Source base `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. Live dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240`.
- Scope: the delta `48f12dc1..9c601b59`. That is one docs commit, `docs/design/MAAP_FABRIC.md` only (+17/-8). It answers R548-2-F1. The evidence items are R549-2-F1 (archive `16f2f7ea`) and the R549-1-F4 remainder (manager candidate receipts, archive `319f3567`, PR comment 6052017268). The round-2 code at `48f12dc1` is unchanged, and R548-2 and R549-2 are the baseline.
- Reconstruction order:
  1. AGENTS.md and CONTRIBUTING.md.
  2. Issue #686: the body, the assignment 6043036997, the round-2 ruling 6047563934 and both REVIEW READY comments.
  3. The PR #695 body.
  4. The delta and the cited RTL.
  5. The manager evidence comments 6051028263 and 6052017268, then the archive at `84add8ed`, `16f2f7ea` and `319f3567`.
- Prior public findings (the R548-2 and R549-2 comments) were read only after my independent pass over the delta and the evidence. I read no private author material and no concurrent reviewer report. Of the archive I read only the evidence directories (`author-r2/resource-receipts/`, `manager-candidate/`, `MANIFEST.json`), not the prior review packets.

The verdict is POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE item is open. Every prior finding is resolved at this head. Three new SUGGESTIONs are recorded, and three earlier SUGGESTIONs are retained.

## The delta against the RTL (R548-2-F1)

Each sentence of the new text was read against the RTL at the head:

| New text (`MAAP_FABRIC.md`) | RTL at head | Holds |
|---|---|---|
| `:91-92` "The module seeds it at reset from `station_mac_i`." | `KL_maap.sv:149` `mac_seed_w = 16'hACE1 ^ station_mac_i[15:0] ^ station_mac_i[31:16]`. `:292` (reset branch of `maap_sm`, `:286-292`) `lfsr_r <= (mac_seed_w == 16'h0) ? 16'hACE1 : mac_seed_w`. The only other writer is the step at `:316`. | yes |
| `:92-96` zero fixed point; a MAC folding to `0xACE1` (`02:00:00:00:AC:E1`) takes a nonzero constant | `:147-149`, `:292`. For `02:00:00:00:AC:E1`, `mac[15:0]` = `0xACE1` and `mac[31:16]` = 0, so `mac_seed_w` = 0 and the reset loads `0xACE1`. | yes |
| `:96-98` shipping seed sampled during `axis_resetn`, MAC_ADDR_LO/HI still 0 | The engine sits on `.rst_n(axis_resetn)` and `.clk_i(axis_clk)` (`milan_datapath.sv:7066`). `station_mac_i` is the byte-reversed `cfg_mac_addr` (`:7069-7071`). `cfg_mac_addr` is `csr.o_mac_addr` (`:2491`), which is `{mac_ahi[15:0], mac_alo}` (`milan_csr.sv:2648`), with no register stage. `milan_csr` is on `.aclk(axis_clk)`, `.aresetn(axis_resetn)` (`milan_datapath.sv:2465-2466`), and its synchronous reset clears `mac_alo`/`mac_ahi` (`milan_csr.sv:1553-1556`). | yes |
| `:98-99` firmware writes the MAC after boot | `sw/firmware/milan_baremetal/milan_baremetal.c:1591` | yes |
| `:99-100` every shipping station seeds `0xACE1`; the station MAC does not enter the draws | The fold of 0 is `0xACE1`, which is nonzero. The shipping default is `MAAP_P = 1` (`milan_datapath.sv:277`), and there is one `KL_maap` instance (`:7065`). Executed proof is below. | yes |
| `:100-101` stations differ only by when their enable and sends fall; the seed timing is a follow-up with B.3.6.1 | The LFSR free-runs from reset release (`KL_maap.sv:316`). The offset draw takes `lfsr_next_w` at Begin!/Restart! (`:282-283`, `:377`), and the interval draws take `lfsr_r` at the timer loads (`:170-171`). | yes (S1 offers a precision) |
| `:135-140` B.3.6.1 record: seeded at reset from `station_mac_i`, which is 0 in shipping, so `0xACE1`; the follow-up covers both | as above | yes |
| `:175-176` Fabric integration: seeded at `axis_resetn` from `cfg_mac_addr`, which is 0 then | as above | yes |

Every bullet of R548-2-F1's required outcome is met:
- the three sites state what ships;
- the module-level statements keep `station_mac_i` (`KL_maap.sv:141-145` and `KL_maap.md:5`, `:26` are unchanged);
- the follow-up carries the seed timing with B.3.6.1;
- the delta changes no RTL (`git diff --stat 48f12dc1 9c601b59` lists one file).

The PR body's Status line describes the same change. Its Known limitations already list "the generate_address generator and seed (B.3.6.1)".

**Executed integration proof** (`scripts/seed_probe_patch.py`, `receipts/seed_probe_*`). The probe uses a disposable copy of the head with the real `milan_datapath`, built through the crflic leg's own recipe (`make crflic`).
- A read-only public on `KL_maap.lfsr_r` is compared on every `axis_clk` edge with a shadow LFSR. The shadow loads `0xACE1` whenever `axis_resetn` is low and steps otherwise.
- Clean head: `R548-PROBE PASS: edges 17453852 post-reset 17453844 mismatches 0 counterfactual-equal 0`, harness 417 checks, 0 failures, rc 0.
  - The run covers the firmware-order MAC write (`02:00:00:00:00:01`, whose seed would be `0xACE0`), MAAP enable and the claim reaching ANNOUNCE.
  - A counterfactual shadow seeded from the programmed MAC never equals the engine.
- Planted control: `milan_csr` resets MAC_ADDR_LO/HI to that MAC, which models a MAC known at reset. The probe catches it with `R548-PROBE FAIL ... mismatches 17453851 counterfactual-equal 17453844`, rc 2.
  - The leg's own 417 checks still pass on that mutant, so no existing check pins the integration seed source (S2).

## Evidence items

**R549-2-F1 / R548-2-E1, the receipt manifest** (archive `16f2f7ea26ffdc67d314b9e4074cd794c7f9bcb3`; the tree checked is `319f3567`, which contains it):
- `sha256sum -c MANIFEST.sha256` in `author-r2/resource-receipts/` reports 186 of 186 OK, rc 0 (`receipts/r549-2-f1_sha256sum-c.log`).
- Every file in the directory is listed, and every listed file is present.
- `git diff 84add8ed..319f3567 -- author-r2` changes only `MANIFEST.sha256`, at four lines. So every record input that R548-2 and R549-2 regenerated is byte-identical, and that regeneration still stands.
- Provenance (`scripts/manifest_provenance.py`, `receipts/manifest_provenance.log`, rc 0):
  - Of the 271 `MANIFEST.json` entries at `84add8ed`, none was removed, and only one changed: the manifest's own entry, `author-r2/resource-receipts/MANIFEST.sha256`.
  - The four orchestration scripts keep `original_sha256` (`4240a680...`, `fe0efea8...`, `6284434e...`, `d926c011...`), their published hashes and `path_redacted: true`.
  - All 767 entries' published hashes match the bytes at `319f3567`, and nothing on disk is unlisted.
- The scripts' placeholders (`<repo>`, `<work>`, `<home>`, `<scratch>`) are the ones the receipt README (`README.md`, "Host path prefixes ... are replaced by") declares. That answers E1's README requirement. The superseded self-hash is S3.

**R549-1-F4 remainder, manager candidate receipts** (archive `319f3567ed693bc5dffd422164a768c142485a2d`, `review-evidence/686-r1/manager-candidate/`):
- **Commit and tree association.** Candidate `1351f398` and its parent `b959830a` are not public commits, so I reproduced the tree from public commits (`scripts/candidate_tree_check.sh`, `receipts/candidate_tree_check.log`, rc 0). Merging dev `99e4eb6c` with the #654 lane head (PR #694, `853a7357`) gives `be74ac16`, conflict-free. Merging that with this head gives `140c3b838ef3a1f72e2669744871a48b83911311`, which is exactly the claimed tree. Both `*-initial-integrity.json` files record head `1351f398`, tree `140c3b83`, 1,192 files verified, and the gitlinks `2ad2f845` / `5dce647a` / `48ff7a7e` / `efeb541a`. Those gitlinks equal the head's.
- **Statuses.**
  - `manager-builder/results.json`: head `1351f398`, base `b959830a`, 48 commands, all rc 0, `complete.json` exit 0. It includes `docs_check`, `gen_toc --check`, `check_em_dash --base b959830a`, `xvlog_gate`, `lint_rtl` and the builder SDK.
  - `full-native/results.json`: 5 of 5 rc 0. They are the five-shard parent sweep (rc 0; `full-suite-logs/maap.log` shows `KL_maap: 130 checks, 0 failures` and `maap mutants: checks: 27 failures: 0`), Yosys `run.sh`, the processor suites (`1028250 checks total, 0 failing`), gptp-processor and behave (`404 scenarios passed, 0 failed, 0 skipped`).
- **Three kinds of validation, kept apart:**
  1. *Source head*: the hosted contexts at exactly `9c601b59` (`receipts/hosted_check_runs.tsv`). 22 executed contexts completed success, including `rtl-fast`, `verilator-suites` (5 shards), `yosys-portability` (4 shards) and `docs-check`. Add the author's gate receipts at code-identical `48f12dc1` and my focused runs below.
  2. *Candidate*: the manager bank at `1351f398`, above. The comment labels it "current-dev candidate validation, not source-head validation".
  3. *Physical*: NOT RUN. The hosted context `Physical gPTP (nightly and manual)` is **skipped** and is not counted. Bench interop (acceptance 4) is a post-merge duty.
- For R548's lenses this remainder is resolved. R549 holds the final disposition of its own finding.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE item.

### Suggestions (optional; none affects coverage)

- **R548-3-S1 - SUGGESTION - Docs - `docs/design/MAAP_FABRIC.md:100-101`, the reference point of "when".**
  - "Stations differ only by when their enable and sends fall" is true, but the reference point is implicit. The LFSR state is a function of `axis_clk` cycles since `axis_resetn` release.
  - Two stations with equal reset-to-enable timing draw identical offsets and intervals.
  - Optional wording: "... differ only by how many `axis_clk` cycles after `axis_resetn` release their enable and sends fall."
  - This changes no claim.
- **R548-3-S2 - SUGGESTION - Tests - no check pins the integration seed source.**
  - The planted MAC-at-reset control passes all 417 crflic checks and is caught only by this round's probe (`receipts/seed_probe_mutant.tail.log`).
  - When the B.3.6.1 seed-timing follow-up is filed, the probe's shadow-LFSR comparison is a ready template for its check.
- **R548-3-S3 - SUGGESTION - Docs (evidence archive) - `review-evidence/686-r1/MANIFEST.json`, the entry `author-r2/resource-receipts/MANIFEST.sha256`.**
  - At `16f2f7ea` both `original_sha256` and `published_sha256` became the corrected bytes (`0dd53340...`). The superseded author-delivered hash `3d8435b5...` now survives only in archive history (`84add8ed`).
  - Recording it, or a note that the manager corrected the file, would keep the provenance mapping self-describing.
  - The integrity check passes either way.
- **Retained from R548-2 (code unchanged at this head):**
  - R548-2-S1 (Tests): [6a] grades one stall window.
  - R548-2-S2 (Tests): the own-empty-range check runs in PROBE only.
  - R548-1-S2 (Tests, Robustness): the truncated-PDU gate `KL_maap.sv:353` has no check. It is listed in the PR body's follow-up.

## Prior public findings at this head

| Finding | Status at `9c601b59` | Evidence |
|---|---|---|
| R548-2-F1 (MINOR, Conformance, Docs): the shipping engine is not seeded from the station MAC | **Resolved** | The table above and the executed integration probe. `MAAP_FABRIC.md:91-101`, `:135-140` and `:175-176` state what ships. Module statements are kept. Follow-up with B.3.6.1. No RTL change. |
| R548-2-E1 (MINOR, Docs, evidence): receipt MANIFEST fails for four files | **Resolved** | 186/186 OK at `16f2f7ea`/`319f3567`. Placeholders declared in the receipt README. Redaction provenance kept in `MANIFEST.json`. Bookkeeping nuance: S3. |
| R549-2-F1 (MINOR, Tests, Docs): the same manifest defect | **Resolved** | As above. The exact archive commit is named in comment 6051028263. Record inputs are byte-identical to the ones regenerated in round 2. |
| R549-1-F4 remainder (MAJOR, retained by R549-2): broader validation receipts | **Resolved for R548's lenses** (R549 disposes of its own finding) | Candidate commit/tree reproduced, statuses 48/48 and 5/5. Source-head, candidate and physical kept apart, as above. |
| R549-1-F1 = R548-1-F3, R548-1-F1, R548-1-F2, R549-1-F2 = R548-1-F4, R549-1-F3 = R548-1-F5 | **Resolved** (unchanged since R548-2) | No code or test changed in the delta. The maap suite rerun at this head gives 130 checks and 27 mutant rows, all as before. |
| R548-1-S1, S3, S4 | Done (unchanged) | as R548-2 |
| R548-2-S1, R548-2-S2, R548-1-S2 | Retained as SUGGESTION | Code unchanged |

## Executed evidence at this head

| Receipt | Result |
|---|---|
| `receipts/identity.txt` | Pinned simulator `5.050 2026-07-01 rev v5.050`. Head, tree and archive heads. |
| `receipts/maap_suite.log` / `.rc` | `make all` in a scratch copy: `KL_maap: 130 checks, 0 failures`; `maap mutants: checks: 27 failures: 0`; rc 0 |
| `receipts/seed_probe_probe.tail.log`, `seed_probe_clean.full.log.gz`, `.rc` | Integration seed probe on the clean head: PASS, crflic 417/0, rc 0 |
| `receipts/seed_probe_mutant.tail.log`, `seed_probe_mutant.full.log.gz`, `.rc` | Planted MAC-at-reset control: probe FAIL (caught), rc 2 |
| `receipts/docs_docs_check.log`, `docs_doc_style.log`, `docs_doc_paths.log` (+ `.rc`) | `docs_check` 0 findings over 199 md files. Doc style OK. Doc paths OK (937 resolve). rc 0 each. |
| `receipts/em_dash_added_lines_grep.log` | No U+2014 in the delta's added lines. `git diff --check 48f12dc1 9c601b59` is clean. The em-dash and TOC gates themselves could not judge here (renderer not installed). They passed in the candidate bank (commands 19, 20 and 36) and in hosted `docs-check` at the head. |
| `receipts/r549-2-f1_sha256sum-c.log`, `manifest_provenance.log` (+ `.rc`) | 186/186 OK. Provenance check rc 0. |
| `receipts/candidate_tree_check.log` / `.rc` | Tree `140c3b83` MATCH, rc 0 |
| `receipts/hosted_check_runs.tsv`, `hosted_status.txt` | 22 completed success, 1 skipped (Physical gPTP), at the exact head |
| `receipts/tree_integrity.log` / `.rc` | rc 0. HEAD and tree exact. Index equals HEAD's tree. Tracked bytes and modes are clean, with no assume-unchanged or skip-worktree flags. Nothing untracked or ignored. Gitlinks protocol-processor `2ad2f845`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e` match and are clean. `external` is not initialised. |

The clone was used read-only. The only write was a bytecode cache that the docs gates left under `scripts/__pycache__` (ignored, untracked). It was removed before the final integrity check. All builds and probes ran in unpublished copies under `scratch/`.

## Ledger (reviewer-owned)

Every lens was applied in this round at the exact head.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | B.3.6.1 deviation record `MAAP_FABRIC.md:135-140` and B.3.4 randomness text `:85-101`, against the integration seed path (`KL_maap.sv:149`, `:292`, `:316`; `milan_datapath.sv:2465-2466`, `:2491`, `:7065-7071`; `milan_csr.sv:1553-1556`, `:2648`) and the executed probe. Every sentence is accurate, and the gap is recorded for the follow-up rather than claimed conformed. Candidate tree `140c3b83` reproduced, bank statuses 48/48 and 5/5. | R548-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| RTL | CLEAN | Reset and clock domains of `KL_maap` and `milan_csr` (same `axis_clk`, same synchronous `axis_resetn`). `cfg_mac_addr` is combinational from `mac_alo`/`mac_ahi`. One `KL_maap` instance, `MAAP_P = 1` default (`milan_datapath.sv:277`, `:7065`). `lfsr_r` writers `:292`, `:316`. The delta touches no RTL (`git diff --stat 48f12dc1 9c601b59`). | R548-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Robustness | CLEAN | Reset re-seeding over the whole crflic run (17.45M edges): any reset that reseeds the LFSR also clears MAC_ADDR_LO/HI, so no reset sequence seeds from the MAC. Configuration dependence: MAC programmed after reset (clean) and at reset (planted control, caught). The zero-fold boundary `02:00:00:00:AC:E1` against `:292`. | R548-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Tests | CLEAN (S2 and the retained R548-2-S1, R548-2-S2 and R548-1-S2 are SUGGESTION) | `tb/verilator/maap` `make all` at head (130 checks, 27 mutant rows). The `tb/verilator/milan_dp` crflic leg at head (417/0) with the seed probe and its planted control (caught). Candidate `full-suite-logs/maap.log`. Hosted `verilator-suites` at the exact head. | R548-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Docs | CLEAN (S1 and S3 are SUGGESTION) | `docs/design/MAAP_FABRIC.md:85-101`, `:128-152`, `:175-176`; module page `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5`, `:26`; banner `KL_maap.sv:141-145`; `docs/reference/FR_NFR.md:167`; PR body Status and Known limitations; docs gates (receipts). Evidence archive: `author-r2/resource-receipts/README.md` and `MANIFEST.sha256`, and `MANIFEST.json` at `319f3567`. | R548-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |

## Real limits

- I did not have the standard's text in this round. Clause readings rest on the frozen issue text, the published Annex B contract and prior public clause citations. The delta's conformance question (does the B.3.6.1 record describe what ships?) needs nothing beyond the RTL.
- Not run by me: the five datapath suite sweeps beyond the crflic leg, the RV32 ctrl suite, builder, Yosys, the xvlog gate and any Vivado run, by assignment. I also could not run the em-dash and TOC gates, because the renderer is not installed and shared installs are not allowed.
- The candidate commit `1351f398` and its parent `b959830a` are not public. I verified the tree association by reproduction, not by reading the commits. The receipts' head fields and integrity files are the manager's records.
- The candidate is built on the #654 candidate at PR #694 head `853a7357`. If #694 or dev moves, that candidate no longer represents the merge result.
- Physical calibration NOT RUN. Simulation, resource results and the skipped `Physical gPTP` context are not hardware proof.

## Pending manager duties

- Publish this round. Carry S1 to S3 as optional.
- Own hosted and local-replica acceptance at the exact head.
- Rebuild and revalidate the candidate if #694 or dev moves before the merge turn. Apply the area budget's re-baseline rule to the actual merge result (dev `99e4eb6c` changes the shipping export).
- After merge:
  - acceptance 4, bench MAAP interop with the reference peer;
  - file the follow-up deviations from the PR body, including the B.3.6.1 seed timing (every shipping station seeds `0xACE1`);
  - consider S2's probe as that follow-up's check.
- Merge requires two independent positive verdicts, no round in flight, the full completion bar and maintainer authorization.

## Reproduce

From the packet directory, with a clone at the head (submodules at their pins), a disposable copy `<copy>` of it (the copy needs a git index for `scripts/pp_srcs.py`; for example `git init && git add -A && git commit`), and a git directory `<objs>` that can reach dev `99e4eb6c`, `853a7357` and this head:

```sh
python3 -I scripts/seed_probe_patch.py <copy>                          # or add --mutant-mac-at-reset
make -C <copy>/tb/verilator/milan_dp crflic VERILATOR=<pinned 5.050>   # look for the R548-PROBE line
sh scripts/candidate_tree_check.sh <objs>
python3 -I scripts/manifest_provenance.py <MANIFEST.json at 84add8ed> <MANIFEST.json at 319f3567> <archive>/review-evidence/686-r1
(cd <archive>/review-evidence/686-r1/author-r2/resource-receipts && sha256sum -c MANIFEST.sha256)
sh scripts/tree_integrity.sh <clone> 9c601b5983acfd60fb269b9a88c27b48cab7cf65 d2337a496fb13813beb2f4a13aefcaca0e0a94db
```

In receipts, host paths are replaced by `<packet>`, `<clone>`, `<tools>`, `<home>` and `<data>`, and results are unchanged. `MANIFEST.sha256` lists every publishable file. `scratch/` is not published.

R548-3 FINISHED
