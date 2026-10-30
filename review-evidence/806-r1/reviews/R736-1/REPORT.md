[R736] POSITIVE - exact head f99405af0b2caad46e84f50f8251ffbffaa80836

External independent review, round R736-1, issue #806 / PR #813. Tree: `6547cf95cce6a564f9c1822cbc3551301aece764`; source base: `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR. One wording-only RESIDUE follows. This source verdict does not discharge the outstanding merge and physical qualification gates.

## Isolation and public contract

Read AGENTS.md, CONTRIBUTING.md and docs/README.md, then the issue body, requirements/interfaces, the complete parent diff and history, donor executable changes, and the published author receipts. `INDEPENDENT-VERDICT.md` records the verdict and ledger before any PR/issue comment history was fetched. No private author material or other review report was used.

After that checkpoint, reviewed the [public assignment](https://github.com/kebag-logic/milan-fpga/issues/806#issuecomment-6509895143), the author's public readiness evidence, and the [manager's timing disposition](https://github.com/kebag-logic/milan-fpga/issues/806#issuecomment-6514731297). The assignment keeps built-image link-toggle qualification outstanding and requires `Relates to #806` until it passes. The timing disposition requires #814's logic cut, followed by merging dev and re-routing; it grants no floor or fall exception. At the recorded snapshot, the PR had two review-start comments, zero submitted reviews and zero inline comments: there were no prior published findings to resolve or retain. The other review remains separate.

## Findings

**R736-1-R1 | RESIDUE | Docs**

- **Artifacts:** `CHANGELOG.md:76`, `docs/design/AREA_BUDGET.md:144`, `docs/reference/SUBMODULES.md:429`, and the PR body's resource/known-limitation/DoD ownership wording.
- **Authority/evidence:** The manager's issue comment linked above explicitly assigns recovery to #814 and says the refusal is not an owner decision. The source and PR still describe an owner decision to accept/re-record or recover.
- **Impact:** Stale responsibility wording. The actual figures, refused verdict, executable gates and conformance claims remain unchanged. This is RESIDUE under the supplied rule and leaves Docs CLEAN.
- **Required outcome / exact fix:** Replace the new sentences saying an owner decision is needed with: “Timing recovery is assigned to #814; this change then merges dev and re-routes, with no floor or fall exception.” In the PR body, replace the accept/re-record-versus-recover choice and “area gate's open decision” wording with that disposition. Retain every measured figure, the route refusal, and the outstanding acceptance checkboxes.
- **Verification:** Text matches the linked public disposition; no gate threshold, measurement, test, code or generated record changes.

## Reviewer-owned coverage ledger

All paths below refer to the exact head. Donor paths are relative to `gptp-processor` at `135afd043309369a87ddbc8d6550aff8ec52a157`.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `REQUIREMENTS.md:154`; issue #806; IEEE 802.1AS-2011 10.2.4.11 and 11.2.15/Figure 11-8 with Cor1/Cor2; Milan v1.2 4.2.6.2.4/.5; `hdl/milan/milan_datapath.sv:3194,8903`; donor `hdl/ucode/gen_gptp_ucode.py:2186` | R736-1 | f99405af0b2caad46e84f50f8251ffbffaa80836 |
| RTL | CLEAN | `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:192,711,799,823,1007`; `sw/litex/milan_soc.py:1921`; donor `hdl/top/KL_gptp_engine.sv:623,1116` and `hdl/wire/KL_gptp_tx_slot.sv:127` | R736-1 | f99405af0b2caad46e84f50f8251ffbffaa80836 |
| Robustness | CLEAN | Parent `tb/verilator/milan_dp/sim_gptp.cpp:1731-1807`; donor `tb/verilator/engine/sim_main.cpp:6026` and `port_mutants.py`; `mutation/phy-only.log`; public C0/P1-P5/D1-D5 raw receipts | R736-1 | f99405af0b2caad46e84f50f8251ffbffaa80836 |
| Tests | CLEAN | `tb/verilator/milan_dp/sim_gptp.cpp:535,1668-1807`; `focused/gptp.log`, `focused/gptp-lat.log`, `focused/gptp-shadow.log`; public exact-head sweep/fuzz receipts and unchanged-input mutation receipts | R736-1 | f99405af0b2caad46e84f50f8251ffbffaa80836 |
| Docs | CLEAN | `docs/design/GPTP_PLANE.md:97`, `TIME_SYNC.md:87`, `GM_LOSS_RECOVERY.md:40`; `docs/reference/SUBMODULES.md:383`; integration guide, CHANGELOG, generated diagrams, ROM ledger and port census; `records/*` | R736-1 | f99405af0b2caad46e84f50f8251ffbffaa80836 |

**Conformance and adoption.** The gitlink is exactly the requested main merge. Donor `409c3075` and `135afd04` share tree `b552de2244475b15bfc430b683f8a4fe9c6a7db3`. Reconstructing the companion from the parent diff, changing only its donor gitlink back to the reviewed tip, reproduces all 17,728 bytes and SHA-256 `aeeab9c8785d016c9cf7f062970034fa229c41d7849f06f8e7eb412af1ec5934`. The applied companion commit `a20f458e` contains no gitlink hunk. Later changes strengthen the checks and update documentation/records. See `companion-verification.txt`.

The effective link is `i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)`. Its three terms reach the engine through the shadow. The PHY level is synchronized by the SoC; the CSR and guard terms are already in `axis_clk`. No new CDC or product top-level port, parameter or register is introduced. The engine's NOT_ENABLED path clears the capability ladder and cease, disarms the outstanding exchange, and schedules a fresh request on return. The two-exchange capability ladder and countdown exit remain intact. The named standards were read directly; `standards.sha256` identifies the editions. No new pttPortEnabled or network-access authorization control is claimed. Added source comments were also checked against the supplied comment rule; no new bench labels or review identities were found.

**RTL and robustness.** NOT_ENABLED receives dispatch priority without waiting for a stalled serializer. Disabled-port credit and timestamp-claim invalidation prevent an exchange from completing while low. Cancellation suppresses an unaccepted first byte, whereas a started frame completes. The shadow gearbox and ticket consume `valid && ready`, so withdrawal before acceptance leaves no partial frame or ticket. Reset establishes the first enable sample as a reference; a later rise after disabled warm-reset release ends retained cease state. Reviewed the donor's stalled-byte, late-pair and warm-reset phases and controls. Parent tests cover physical, administrative and guard withdrawal independently. No changed width, indexing, overflow or reset defect was found.

**Test independence.** The checks read capability through the public CSR and identify actual Pdelay_Req frames, using captured first-beat cycle stamps. Each loss check requires capability TRUE first. The 2 ms settle after each return prevents the next precondition from using stale TRUE. The storm uses two distinct clock identities. Return and countdown checks measure transmitted-request deltas against the declared cadence; they do not compare an internal counter to itself. The 3-second simulation cease tests the same countdown generator whose production default remains 5 minutes.

The public ten-mutant campaign was audited against its raw logs, expected FAIL names, unique planting counts and clean controls, not just its summary. Every named check fails under its listed defect, including the falling-edge omission and both countdown controls. These runs were at `cf3ef596`; all later changes are documentation-only, so their executable inputs equal this head. `public-evidence-audit.txt` records the audit and the 180 published-file hash checks.

## Execution and regeneration evidence

The independent focused commands used the verified scoped 5.050 build. All builds, execution and probes ran in disposable clones beneath packet `scratch/`; independent simulations ran concurrently, with no more than 16 compiler/execution jobs. No full bank, implementation fix, commit, push, GitHub write, hardware run or container orchestration was performed.

| Check | Result | Receipt |
|---|---|---|
| `make -j16 ... build-gptp`, then `exec-gptp` | 210 PASS, 0 FAIL | `focused/build-gptp.log`, `focused/gptp.log`, rc files |
| `make -j16 ... build-gptp-lat`, then `exec-gptp-lat` | 210 PASS, 0 FAIL; unequal corrections observed as 296/104 ns | `focused/build-gptp-lat.log`, `focused/gptp-lat.log` |
| `make -j16 ... run` in `gptp_shadow` | 325 PASS, 0 FAIL | `focused/gptp-shadow.log` |
| PHY-only wiring mutant, unchanged full parent gptp leg | KILLED; 210 checks, 208 PASS, 2 FAIL, exactly administrative and guard loss | `mutation/phy-only.log`, `mutation/verdict.txt` |
| ROM digest recorder, port census writer, both diagram generators, then their checkers | All rc 0; tracked outputs byte-identical to HEAD | `records/*` |
| Submodule-document and pinned gPTP-link checks | PASS; pin table and donor references agree | `records/submodule-docs.log`, `records/gptp-docs.log` |
| Raw tracked-file/mode/index/gitlink verification | PASS on review source and restored disposable clones | `source-integrity.txt`, `probe-integrity.txt`, `mutation-integrity.txt` |

Portable reproducers are `focused_checks.py`, `shadow_check.py`, `wiring_probe.py`, `record_checks.py` and `verify_tree.py`; their positional inputs name the source/disposable tree, packet and executable as appropriate. The wiring probe restores the original bytes in `finally`. The integrity check hashes every tracked blob directly, checks executable/symlink modes and stage-0 index entries, and rejects hidden index flags. The historical inactive `external` gitlink remains correctly pinned and uninitialized.

Author evidence at public commit `83d9cd72166c918d2356e8690e1c5fdceae3b57f` records the exact-head 64-suite sweep (2,191,710 checks, zero in-suite failures), `milan_dp_gm_steps` 202 checks, `tsn_fuzz ptp` 675 plus freshness PASS, 60/60 portability tops, and the static/idiom/docs gates. The physical-time simulation receipt at unchanged-input `cf3ef596` reports 205 checks in 5,653 seconds. These are author executions, not a manager source bank or new independent full-bank runs. Selected raw receipts are under `public-receipts/`; the original public tree holds the remaining logs. Published local logs redact only environment path prefixes; raw originals remain unpublished under `scratch/raw-receipts/`, with before/after hashes in `receipt-redactions.json`.

## Limits and pending manager duties

- The source verdict is positive; issue #806 is not complete. Route-1x1 remains REFUSED solely for the WNS fall: +0.032 ns versus the +0.440 ns record, beyond 0.25 ns tolerance. Other resource limits and the +0.03 ns build floor pass. The report locates the critical path in the SoC AXI-Lite-to-Wishbone bridge to SPI-flash PHY; this review establishes no causal defect in the changed gPTP code. #814 owns recovery; merge dev, re-route, and review that resulting head. No re-baseline or waiver was granted here.
- The manager must validate the current-dev merge candidate with builder and native banks, publish its receipts, finish hosted/act acceptance, ensure the other independent review and all required contexts finish, and apply normal merge/containment rules. No manager bank at this source head is claimed.
- The hosted snapshot contains successful `bdd-conformance`, `docs-check-no-git`, `wire-accountability` and selectors, with many jobs queued/running. The physical gPTP hosted context is **skipped**, not executed. `hosted-contexts.txt` is a snapshot, not a green aggregate or log-based execution proof. This review did not wait for hosted completion.
- Physical calibration is **NOT RUN**, built-image link-toggle qualification is still outstanding, and field skips are not hardware proof. The author's builder receipt also excludes its ineffective local MAKEFLAGS control and unavailable legacy calibration report. The physical-time simulation is simulation only. Keep issue #806 open and retain `Relates to #806` until the required built-image scenario passes.

R736-1 FINISHED
