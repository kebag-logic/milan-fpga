[R285] NEGATIVE - exact head f814d37d94e17435f3b6dcc424f8b2b606cdd3e9

# R285-4: external review of issue #530 / PR #549, round 4

- Head `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9`, tree `f431f698deafcc625d738714b960f109d82012df` (verified, `receipts/09-restore-verification.txt`).
- Source base `50e78097564244c124e1ec30dd8821f83951ab06`. The merge `44ad6991` brings in dev `f86c34fe` (#540).
- Scope: the merge's conflict resolution and clean overlaps, and round-3 commits `b7887343`, `35f2a54b`, `f814d37d`. RTL and Docs were re-covered at this head. The other three lenses were re-applied here too, because the merge touches the milan_dp Makefile/README (Tests) and moves the gPTP engine pin into the tree the RTL lens reads.
- Context was reconstructed in this order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and its assignment/decision comments, the diff and history, then public evidence. I read prior review findings only after my own pass.

## Verdict

One open MINOR (F1, Docs) makes the verdict NEGATIVE. The code, harness and repository documentation at this head are clean under all five lenses. F1 is in the PR body, and fixing it needs **no new commit**. Once the body is corrected, a re-read of the body at this same head clears Docs.

## Findings

### F1 - MINOR - lens: Docs - the PR body says the silicon-tested image is what this head builds; after the merge it is not

- **Where:** PR #549 body at this head (fetched read-only, quoted in `receipts/04-image-identity-and-hosted.txt`):
  - line 23: "Every `hdl/` change after `c593cbef` is a comment, so the tested image is still the one this head builds."
  - line 19: "The gitlinks do not change either."
  - line 17: Status "GREEN at `e65dccfe` ... fourteen commits". The body is not refreshed for the merge or round 3, except in its commit table.
  - The `[A241] REVIEW READY` comment on the issue makes the same claim: "The silicon PASS on c593cbef covers this head, since the RTL is identical."
- **Evidence (`receipts/04`):**
  - The flashed head `c593cbef` pins `gptp-processor` at `c1b61743`. This head pins it at `e5dcea6e`, via merge `44ad6991` (#540).
  - Between those pins the gPTP microcode generator changed: `hdl/ucode/gen_gptp_ucode.py`, +114/-48 lines.
  - As a result the ROM ledger records different images: `gptp_ucode.hex` `83f14a7d...` versus `4afe436d...` (`syn/yosys/rom_digests.tsv`).
  - The gPTP plane is in the product image, "product default ON" (`sw/litex/milan_soc.py:529-533`). The A237 silicon run relied on it ("gPTP stayed locked throughout").
  - The `hdl/` half of the claim holds: comment-stripped `milan_datapath.sv` is identical at `c593cbef`, `e65dccfe`, `44ad6991` and `f814d37d` (`receipts/02`). The conclusion drawn from it does not hold, because the image also contains the pinned gPTP engine and its ROM.
- **Impact:**
  - The public evidence record presents the A237 silicon PASS as exact-image hardware evidence for the merge head. It is exact-image evidence only for `c593cbef`.
  - A cold reader, or the merge decision, would not see that the product built from this head carries a gPTP microcode image that was never on the bench. The CRF talker's timestamps and `tu` depend on that gPTP time.
  - The #530 behaviour itself is unaffected in simulation:
    - `crflic` 85/0 and its mutants 4/4 pass at this head;
    - `gptp` passes 181/181;
    - `gmstep`'s output is byte-identical to the dev baseline.
  - This is a false evidence statement, not a behaviour defect. I do not record it under Conformance: the manager's ruling that A237 meets #530's silicon acceptance concerns the #530 RTL, which is unchanged, and the #540 pin will be in `dev` whatever this PR does.
- **Required outcome:**
  - The PR body states that the silicon PASS covers the #530 RTL (the comment-stripped datapath and processor pin `09f9bf38` are unchanged since `c593cbef`).
  - It also states that this head's image differs from the flashed one by the #540 `gptp-processor` pin `c1b61743` -> `e5dcea6e` (a different `gptp_ucode.hex`).
  - The Status paragraph names the current head, including the merge and round 3.
  - A public note corrects the `[A241]` "RTL is identical" sentence.
  - Whether the merged result needs exact-image silicon is the manager's decision, and belongs with post-merge containment.
- **Verification:** read the PR body (and the correcting note) at this head. No source change is needed, so no other lens is un-covered.

### S1 - SUGGESTION - lens: Docs - two residual imprecisions around `LWSRP_STATUS[6]`

- `docs/reference/REGISTER_MAP.md:1169`: the `0x694` field list still defines "`[6]` reservation ACTIVE" with no qualifier. The same cell later says "`[6]` ORed over sources". The label predates the PR (`|pp_cd_srp_active_w` at base as well).
- `REGISTER_MAP.md:1130`, `EGRESS_QUEUE_MAP.md:99` and `ieee8021q.md:67` open with "Both show on the licensed source's own bits" and then list `[6]`, which the next sentence says is not one source's own bit. Each site qualifies it correctly right away.
- Optional: qualify the field definition itself, and drop "own" from the lead-in. No reader is misdirected, so coverage is not affected.

## Round-3 claims checked at this head (all hold)

Evidence: `receipts/12-round3-bit-trace.txt`, `receipts/02-hdl-comment-only.txt`.

- **`LWSRP_STATUS[6]` = `|pp_cd_srp_active_w`** (`milan_datapath.sv:6652`), packed at bit 6 (`:2502-2508`, with widths from `:1652-1666`). So "ACTIVE ORed over sources, shows the corner only while no other source is ACTIVE" is exact. Where it appears:
  - `milan_datapath.sv:6614-6615`;
  - `REGISTER_MAP.md:1132-1134`, and the `0x694[9]`/`0x698` rows `:1169-1170`;
  - `EGRESS_QUEUE_MAP.md:100-102`;
  - `ieee8021q.md:68-70`;
  - `CHANGELOG.md:51`.
- **`LWSRP_STATUS[8]` = `lwsrp_stream_gate[0]`**, which is ACTIVE[0], source 0 only.
- **`CRFT_CTRL[6]`/`[7]`** are `crft_res_active_w`, the top ACTIVE slot, and `crft_emit_en_w` (`:5280-5281,5305-5307,5318-5319`). With policing on, both are the CRF output's ACTIVE.
- **`0x82C` holds AAF sources only.** The window's inputs are `8'(aaf_stream_en_w)` and `8'(acmp_lobs_v_w[N_STREAMS-1:0])` (`:2478,2483`, `milan_csr.sv:2916-2920`), so the CRF output (index `N_STREAMS`) never appears in it.
  - Gate bit `[3]` = `aaf_stream_en_w[idx]` carries ACTIVE at every index (`:1913-1916,2020-2027`).
  - Lobs bit `[2]` at index 0 is `listener_observed_w`, the registered Listener level (`:1861-1862,1883`). At index > 0 it is `lwsrp_stream_gate[gj]`, i.e. ACTIVE (`:1885-1886`).
  - This matches the `0x82C` row (`REGISTER_MAP.md:1524`) and `CHANGELOG.md:37-38` ("lobs above index 0").
- **Comment-only.** Comment-stripped, whitespace-normalised `milan_datapath.sv` has sha256 `327d63f9...` at all four heads. The canary `50e78097` vs `c593cbef` reports DIFFERENT.
  - `44ad6991..HEAD` changes five files, all mode 100644. The only `hdl/` file is `milan_datapath.sv`.
  - Every added or removed `hdl/` line is a `//` comment, with 0 metacomment tokens.
  - `KL_talker_diag_ctx.sv` is comment-identical to base.
  - No first-party `hdl/` file other than `milan_datapath.sv` differs from `c593cbef`.

## Merge `44ad6991` checked (resolution and clean overlaps)

Evidence: `receipts/05-merge-resolution.txt`, `receipts/01-merge-diagram-gates.txt`.

- **Parents** are `e65dccfe` and `f86c34fe`, with merge base `50e78097`. Eight files changed on both sides. Every one-sided file equals its side at the merge, and the round-3 commits do not touch the eight.
- **`SUBMODULES.md`:** the only conflict is the pin table. It is resolved to gptp `e5dcea6e` + protocol `09f9bf38`, and everything else is the automatic merge.
- **`tb/verilator/milan_dp/Makefile`:** the only conflicts are `.PHONY` and `clean`, resolved as the exact union (gmstep/gmstep-build + crflic/crflic-build/crflic-mutants; obj_crflic + obj_gmstep). All recipes from both sides are present.
- **`tb/verilator/milan_dp/README.md`:** both Contents rows are kept, and both sections (crflic, then gmstep), with one separating blank line.
- **Clean overlaps:**
  - `rom_digests.tsv` equals the automatic merge. It carries `09f9bf38` (ltn/ucode) and `e5dcea6e` (gptp_ucode) rows.
  - `submodule_boundaries.svg` equals the automatic merge.
- **Diagram artifacts:**
  - `submodule_boundaries.drawio`, `.png` and the `PNG_MANIFEST.json` entry: `submodule_boundaries.gen.py --check` OK (4 exact gitlinks, decoded PNG) and `--selftest` OK. `check_diagram_pngs` OK (6 rasters) and `--selftest` OK (28 controls). `check_submodule_docs` OK.
  - The manifest's `source_sha256` `6c3ba10c...` equals the drawio.
  - The PNG was inspected visually and shows both pins.
  - `timesync_chain.gen.py --check` OK, and `check_gptp_docs` (with and without `--with-submodule`) OK.
- **gmstep 44/48 equals the dev baseline** (`receipts/07-gmstep-compare.txt`).
  - At head, `make gmstep` exits rc 2 with 48 checks and 4 failures. These are the four the README (`tb/verilator/milan_dp/README.md` "It is not in the default sweep yet") names: two re-bases, no `mr` toggle, no MEDIA_RESET.
  - A disposable replica of dev `f86c34fe` (processor pin `424c688f`, gPTP `e5dcea6e`) produced **byte-identical** run output: 64 lines, `diff` empty.
  - So this PR's datapath and processor pin change nothing in that leg.

## Gates and runs at this head (all foreground, simulator 5.050 verified, `receipts/00`)

| Receipt | What | Result |
|---|---|---|
| `03-static-gates.txt` | docs_check; check_em_dash `--base 50e78097` (1100 lines) and `--base f86c34fe` (269 lines); check_doc_style; gen_toc `--check`/`--verify-anchors`; check_doc_paths; check_feature_status; gen_module_matrix `--check`; check_rtl_source_lists; check_sv_idiom; measure_test_evidence `--check`; lint_rtl `--check` (90 <= 90); xvlog_gate `--check` (4 == ratchet, 0 in `hdl/`); `git diff --check` against both bases | all rc 0 |
| `06-crflic-and-mutants-head.log` | `make crflic-mutants`: builds and runs `crflic`, then the three mutants and the clean control | 85 / 0; 4 of 4, each mutant caught on its named check |
| `07-*` | `make gmstep` at head and at the dev replica | 44/48 each, output identical |
| `08-gptp-head.log` | `make gptp` (merged gPTP pin with this datapath) | 181 / 181 |
| `10-behave.txt` | licence feature; full suite | 5/5; 317 scenarios / 1518 steps passed |
| `11-live-dev-merge-probe.txt` | textual merge probe against live dev `3d2f3e31`, in a scratch clone | conflict in `docs/reference/FR_NFR.md` (dev drift is docs only) |

## Prior public findings: disposition at this head

| Finding | Status at `f814d37d` | Evidence |
|---|---|---|
| R284-1 F1 = R285-1 F1, MINOR (RTL, Docs): a shaper that does not exist | **Resolved, still.** Round 3 adds no shaper claim. The SRP block says "NO SHAPER READS THE SLOPE OR THE VERDICT HERE" (`milan_datapath.sv:6549-6555`) | read at head |
| R284-1 F2 = R285-1 F2, MINOR (Docs): raw verdict named as the gate | **Resolved, still.** Q-9 routes to "the fabric's stream gate through ACTIVE" (`ieee8021q.md:100`) | read at head |
| R284-2 F1 = R285-2 F1, MINOR (RTL, Docs): corner premise and effect | **Resolved, still.** Round 3 changed only the bit list inside the REFUSED paragraph. The premise, both branches and the window-end fall are unchanged (`milan_datapath.sv:6580-6621`) | `receipts/02` |
| R284-3 F1, MINOR (RTL, Docs): `0x82C` lobs said to pulse with ACTIVE | **Resolved.** Scoped to index > 0 and the AAF window only, with `[3]` named (`milan_datapath.sv:6616-6619`, `CHANGELOG.md:38`). Traced true above | `receipts/12` |
| R284-3 S1 = R285-3 S1 (Docs): `LWSRP_STATUS[6]` as the CRF output's own bit | **Taken.** All three pages, both register rows and the CHANGELOG now say the OR. The remaining nuance is this round's S1 | read at head |
| R284-3 S2 (Docs, PR body): stale Contents / DoD silicon wording | **Resolved** (PR body lines 6 and 145). Other stale body text is this round's F1 | `receipts/04` |
| R284-1 S1 / R285-1 S3 (Tests, Docs): mutant time 139 s; absolute `CRFLIC_MDIR` | Retained as SUGGESTIONS, unchanged. This run measured 185 s for build, leg and mutants | `receipts/06` |
| R284-1 S2, R285-1 S1 (Tests): old-pin arm by hand only; t>0 AAF gates graded by source text | Retained as SUGGESTIONS, unchanged | read at head |
| R285-1 S2, R285-2 S1, R284-2 S1/S2 (Docs): legacy "bw-gate"/"slope MUX" terms, `:1588` wording, unnamed processor PRs | Retained as SUGGESTIONS, unchanged and pre-existing | read at head |

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #530 items 1-3 against `sim_crf_licence.cpp` phases [A]-[F]/[INV] run at head (85/0, `receipts/06`). Milan v1.2 5.3.7.3 licence = ACTIVE at `milan_datapath.sv:6637,5280-5307,1913-1916,2020-2027`. FRAMES_TX interval semantics (`tb/verilator/milan_dp/README.md` "FRAMES_TX is an interval count"). The A237 silicon acceptance at `c593cbef` covers the unchanged #530 RTL; its image scope is F1 (Docs) | R285-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| RTL | CLEAN | Comment-only proof across `c593cbef`/`e65dccfe`/`44ad6991`/`f814d37d` (`receipts/02`). Round-3 bit claims traced to `milan_datapath.sv:1861-1886,1913-1916,2020-2027,2478,2483,2502-2508,5280-5319,6637,6652` and `milan_csr.sv:2916-2920` (`receipts/12`). Merged gitlinks `09f9bf38`/`e5dcea6e`/`48ff7a7e`. lint 90<=90, xvlog 4==ratchet, source lists and idiom gates (`receipts/03`) | R285-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| Robustness | CLEAN | No logic change since `c593cbef`. At head, the leg's negative and ordering paths pass: Asking Failed close, Ready Failed reopen, Lv close inside a fresh probe window, five-plus LeaveAll cycles, unbind, `[INV]` on every cycle (`receipts/06`). The merged gPTP pin with this datapath: `gptp` 181/181, and `gmstep` (GM change, 1.5 s step) identical to dev (`receipts/07`, `08`) | R285-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| Tests | CLEAN | Merged milan_dp `Makefile` (`.PHONY`/`clean` union, crflic and gmstep recipes, `receipts/05`) and `README.md`. `make crflic-mutants` 85/0 + 4/4 with each mutant on its named check. `gmstep` equals the dev baseline byte for byte. `gptp` 181/181. behave 317/0. measure_test_evidence `--check` PASS | R285-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |
| Docs | **UNCLEAN** (F1 open) | `CHANGELOG.md:29-64`; `REGISTER_MAP.md:1105-1170,1524`; `EGRESS_QUEUE_MAP.md:64-105`; `ieee8021q.md:50-71,100`; `SUBMODULES.md`; the submodule diagram drawio/png/svg + manifest (gates and visual); milan_dp README; the `milan_datapath.sv:6548-6636` comments; the PR #549 body. The docs gates are all green (`receipts/01`, `03`). F1 is in the PR body; S1 is optional | R285-4 | `f814d37d94e17435f3b6dcc424f8b2b606cdd3e9` |

## Real limits of this round

- **Hardware:** none run. Physical calibration was NOT RUN, and field skips are not hardware proof. The only silicon evidence is A237 at `c593cbef`, whose gPTP pin differs from this head's (F1).
- **Hosted evidence:** there is none at this head. `actions/runs?head_sha=f814d37d` has 0 runs and there are 0 check-runs, and the PR reads `CONFLICTING` / `DIRTY` against live dev (`receipts/04`). No act or Docker was run.
- **Manager evidence not found:** I could not locate public manager bank evidence for this head. The pinned evidence tree `9d1b176c` holds only round-1 material (author, A236 correction, R284-1, R285-1), and neither the issue nor the PR has a manager evidence comment for `f814d37d`. I relied only on my own runs above.
- **Not run:**
  - the full milan_dp sweep, other legs (main/nxn/...), pp_shadow, Yosys/OOC, builder, xelab, and the gPTP donor suites;
  - the old-pin (`424c688f`) failing arm. It is a Tests-scope arm unchanged since earlier rounds, which ran it.
- **Probe scope:** the live-dev probe is textual only, and is not the candidate build.

## Pending manager duties

1. Correct the PR body per F1 (and post a correcting note for `[A241]`), then have Docs re-read at this head.
2. Merge the candidate with live dev `3d2f3e31` (resolving the `docs/reference/FR_NFR.md` conflict) and validate it. That changes the head, so lens coverage must then be judged against the new head per AGENTS.md section 7.
3. Obtain exact-head hosted `rtl-fast`, and the ready gates `verilator-suites` and `yosys-portability`, on the final head.
4. Publish the manager's source static/builder/native bank receipts for the head under review.
5. Decide whether the merged product (with #540's gPTP ROM) needs exact-image silicon, or whether post-merge containment covers it.

## Restore

After the probes, the clone was cleaned of every build product this round created. `scripts/verify_restore.py` then confirmed (`receipts/09`):

- HEAD and tree equal the expected ids;
- 876 tracked files are byte-exact, with modes matching;
- the index is stage 0 with no flags;
- there are no untracked or ignored files;
- gptp `e5dcea6e`, protocol `09f9bf38` and axis `48ff7a7e` are checked out at their gitlinks and clean.

Disposable trees (the dev replica and merge scratch files) are under `scratch/` only and are not published.

R285-4 FINISHED
