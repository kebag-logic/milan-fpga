[R582] NEGATIVE - exact head db29bdd07529fbc697b7956827092f64b1241714

# R582-1: internal independent review, issue #665 / PR #736 (F3b, milan-fpga half)

- Head under review: `db29bdd07529fbc697b7956827092f64b1241714`, tree `8102aa501042b366c2a8abb5a1555fde4eaac2bf`.
- Judged range: `d40e4e9827be2516f8f34b9d65f0a483fff2194c..db29bdd07529fbc697b7956827092f64b1241714` (one commit; the base is PR #705's reviewed head).
- Scope sources: the issue #665 body; assignment [6151273346](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151273346) as corrected by [6151422598](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151422598); ruling [6092086337](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6092086337) items 4 and 5; the Release ceiling [tsn-c-stack#24 comment 6126295947](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126295947).
- Authorities: `protocol-processor/docs/architecture/05_acmp_engine.md:405` (F05.12) and `:383` (F05.11 ping), and `protocol-processor/hdl/acmp/KL_acmp_talker.sv:397` (freshness is `(now - ping_ts) < DAFRESH_MS_P`, 15000). I took Milan v1.2 4.3.3.1 as the processor page and the stack's `docs/PORTING.md` "ACMP DA freshness" restate it. I did not read the specification text itself.
- Evidence read: the public author packet at milan-fpga `52d6b147:review-evidence/665f3b-r1`. All 106 published files match `MANIFEST.json`'s published digests. 21 files are path-redacted by the publisher, which explains their difference from the author's own `MANIFEST.sha256`.
- Prior public review findings on PR #736: none existed at review time (the PR carries only two review-start notices). The finding this lane answers, R582-1-F3 on PR #704 (ruling 6092086337 item 4), is **resolved at this head**: `DA_GATE` now publishes the predicate, and the design page drops the egress-consequence choice. The R583-1-F2 two-interface test (ruling item 5) is **retained** (`test_maap_mbx.cpp:197`, plant `rv-maap-gate-on-interface-0`, killed).

## Verdict summary

The firmware change is correct. It matches the processor's `acmp_declaring_o` predicate, it is well tested, and it reproduces byte-for-byte. The stack range is exactly the reviewed, merged PRs. The verdict is NEGATIVE for two reasons:

- **F1 (MAJOR).** The exact-head hosted `firmware-boundary` and `firmware-verilator` contexts fail, so `rtl-fast` fails. Both crash in the unchanged pin-control harness. At the base, on the identical runner image and Git version, the same two contexts pass. The pin move has made a latent harness race visible on the hosted runner.
- **F2 (MINOR).** A sentence in `SUBMODULES.md` now says the opposite of what this PR does.

## Findings

### R582-1-F1 — MAJOR — Tests, Conformance

**Artifact:** hosted run [38451042997](https://github.com/kebag-logic/milan-fpga/actions/runs/38451042997) at `db29bdd0`:

- jobs `firmware-verilator` (115482633361) and `firmware-boundary` (115482633655) both fail;
- `rtl-fast` reports `FIRMWARE_BOUNDARY_RESULT: failure` and `FIRMWARE_VERILATOR_RESULT: failure`;
- the crash is in `sw/firmware/ctrl/test/ctrl_pin.py:749` (`Clone.fresh`, `shutil.rmtree`), reached from `ctrl_pin.py:962` (`pin_controls`).

**Authority and evidence:**

- AGENTS.md section 7 makes a successful `rtl-fast` at the current head part of completion. The assignment item 5 requires that "every gate the change touches passes".
- In both jobs the pin controls run in order up to the first object-store control (`ctrl_pin_store.py:126`, `forged_tree`, which calls `loose()` at `:100`). Then the next `Clone.fresh()` crashes:
  - `firmware-verilator`: `FileNotFoundError: ... 'maintenance.lock'`;
  - `firmware-boundary`: `FileNotFoundError: ... 'bitmap-ref-tips_VElR2S'`.
- Both file names belong to Git's own background maintenance or repack, which is deleting files inside the scratch clone while the harness removes it.
- Base run [38372974178](https://github.com/kebag-logic/milan-fpga/actions/runs/38372974178) at `d40e4e98` used the same image (`ubuntu24/20261004.327`) and Git 2.55.0. Both jobs there pass all three object-store controls and succeed.
- The harness files (`ctrl_pin.py`, `ctrl_pin_store.py`, `ctrl_boundary.py`) are byte-identical across the judged range. The only relevant input that changed is the stack pin, whose history grows from 231 to 357 reachable objects (`git rev-list --objects`).
- My local `ctrl_boundary.py --require-rv32 --selftest --only verilator` passes (rc 0, 120 pin controls, Git 2.56.0). So the failure depends on the environment, but it reproduced in both hosted jobs at this head and in neither at the base.
- Receipts: `receipts/hosted-boundary-crash-excerpt.txt`, `receipts/hosted-check-runs.tsv`, `receipts/boundary_verilator_selftest.log`.

**Impact:** the PR head has no green `rtl-fast`. Two mandatory firmware gates cannot produce a verdict on the hosted runner at this pin. Until that changes, the boundary and pin proofs this lane relies on are unproven in CI.

**Required outcome:**

- The exact-head hosted `firmware-boundary` and `firmware-verilator` contexts, and so `rtl-fast`, succeed at the PR head.
- The pin controls' scratch-clone lifecycle must not be raced by Git's own background maintenance. The fix is not prescribed. If the fix needs a change outside this lane's file scope, it needs a public scope ruling. Deferring it to another Issue does not resolve this finding (AGENTS.md section 7).

**Verification:**

- Exact-head hosted contexts green at the new head.
- A local control showing the controls survive a Git that starts detached maintenance after the loose fetch.

### R582-1-F2 — MINOR — Docs

**Artifact:** `docs/reference/SUBMODULES.md:256`: "That `main` also changes `src/adp.c`, which this firmware has not taken."

**Authority and evidence:**

- At this head the pin is the merge of stack PR 25 on `main` (`SUBMODULES.md:252`).
- The pin includes #19's `src/adp.c`. Its blob is `764396c2` at both `51870377` and `70936b77`, against `d96be5b3` at the old pin.
- The same page's own table (`:218`) and `sw/firmware/ctrl/README.md:77` say the firmware takes the ADP refusals.
- The sentence is now false. It also contradicts the page's own table about which protocol behaviour the firmware carries. That makes it a behaviour claim, not wording only.

**Impact:** a reader of the authoritative pin page concludes that the firmware lacks the malformed-ADP-discovery refusals, which it now has.

**Required outcome:** the sentence is removed, or it states that the pin includes #19's ADP change.

**Verification:** read the page. `scripts/check_submodule_docs.py` and `scripts/docs_check.py` stay green.

### R582-1-R1 — RESIDUE — Docs

**Artifact:** `sw/firmware/gtest/README.md:246`, `:247`, `:291`, `:299` still cite stack permalinks at the old pin `405dc68310a18f669049ffc10cc23eef7300dcff`. Every other pinned stack link in the PR moved to `70936b77`.

**Evidence:** the cited content is byte-identical at the new pin:

- `include/adp.h` and `tests/test_adp_reentry.cpp` blobs are unchanged;
- the `docs/PORTING.md` "Ownership and dispatch" section has SHA-256 `604b4408…` at both pins.

So this is link consistency only. It changes no claim.

**Exact fix:** in those four lines, replace `405dc68310a18f669049ffc10cc23eef7300dcff` with `70936b77dc41981e192438388cd0aced69954f18`.

### Suggestions (optional, no effect on coverage)

- **S1 (Tests):** `maap/maap_mbx.c:129` (receive) and `:159` (link) call `refresh_demand`, but no test notices their removal. My probes `p-rx-no-refresh` and `p-link-no-refresh` escaped the `maap`, `maap_if2` and `acmp` arms. They are near-equivalent: a stale snapshot only moves a gate write within the same pass, because the pass's poll corrects it. Either plant and test them, or document them as freshness-only.
- **S2 (Tests, RTL):**
  - The funded worst case, `MAAP_MBX_{EVENT,RX,POLL}_MAX` plus `ACMP_MAX_SOURCES` freshness clock reads, is never driven. `MaapHost.CallbackWorkAndEveryOutputCount` (`test_maap_mbx.cpp:513`) registers Listeners only, so it reads the clock zero times.
  - A measured run with every source holding an answered probe would pin the bound.
  - `demand` is a `uint32_t` built with `UINT32_C(1) << s` for `s < n_sources`. A `_Static_assert(ACMP_MAX_SOURCES <= 32u)` would guard the overridable `#ifndef ACMP_MAX_SOURCES` (stack `acmp.h:160`). The default is 16 and the parent overrides nothing, so nothing is wrong today.
- **S3 (Docs):** state the observation latencies as figures:
  - probe or Listener to gate opening: the next MAAP poll;
  - expiry to gate closing: at most one 10 ms TICK plus a pass.

  The contract currently says "refreshes it after service, including idle service ticks". The processor closes at the timer. The predicate is equivalent; the timing is bounded but not stated.
- **S4 (Docs, PR body):** the pin range also holds stack #23 (`1ba27354`). It is the reviewed integration of the old pin's content into `main`: its tree equals reviewed head `3c9ca52f`, and R622-4 and R623-5 are POSITIVE on it. The handoff lists it; the PR body's "adopting stack #19, #20 and #25" could name it too.

## Verification of the assigned points

### (1) Pin range: confirmed

`70936b77` is not a fast-forward of `405dc683`; the merge-base is `1a9f651`. `405dc683` is the closed PR #22's head, squash-integrated into `main` by #23. The 45 changed paths between the pins (`git diff --name-status`) all fall in the union of #19, #20 and #25's file sets.

Every parent-built core blob traces to exactly one PR:

| Core file | Changed by | Blob trace |
|---|---|---|
| `src/adp.c` | #19 only | |
| `src/acmp.c`, `include/acmp.h` | #25 only | #23's copies equal the old pin's byte for byte |
| `src/maap.c`, `include/wire.h`, `include/adp.h`, `include/maap.h` | unchanged | |

Each squash merge's tree equals its reviewed head's tree, and each has two POSITIVE exact-head reviews:

| PR | Merge | Reviewed head (tree equal) | Reviews |
|---|---|---|---|
| #19 | `51870377` | `66b3a757` | R576, R577 |
| #20 | `98dc9e30` | `0c5ef532` | R578, R579 |
| #23 | `1ba27354` | `3c9ca52f` | R622-4 and R623-5, each with a separate POSITIVE verdict on #23 |
| #25 | `70936b77` | `f13c9c16` | R630, R631 |

Nothing in the range is unmerged or unreviewed.

### (2) Parent-harness tests for each parent-visible effect: confirmed

| Effect | Test | Location |
|---|---|---|
| Truncated discovery, lengths 0..81 | `AdpAdapter.PinRejectsEveryTruncatedDiscovery` | `test_adp.cpp:564` |
| Versions 1..7 | `PinRejectsUnsupportedDiscoveryVersions` | `test_adp.cpp:572` |
| Control data length 0, 55, 57 and 2047 | `PinRejectsWrongDiscoveryControlLength` | `test_adp.cpp:581` |
| Complete 82-byte frame with control data length 56 and the valid_time bits set, through the mailbox | `PinAcceptsCompleteDiscoveryThroughMailbox` | `test_adp.cpp:590` |

The F3b predicate is covered by the `MaapHost.DaGate*` tests (`test_maap_mbx.cpp:252-298`) and the `AcmpMailbox.F3b*` tests. All four `pin-adp-*` plants were killed in my control campaign.

### (3) DA_GATE predicate: confirmed

`maap_mbx.c:52-64` together with `:36-50` asserts bit s only when all of these hold:

- MAAP `valid`;
- `s < count`;
- `source_interface[s] == interface`;
- demand, which is `answered || listener_registered` after `acmp_declaring` retires expiry.

Expiry happens at `(now - answered_at) >= 15000` (stack `acmp.c`, `acmp_declaring`), which equals the processor's freshness `(now - ping_ts) < 15000`. `acmp_mbx.c:102` sets `da_fresh_ms = 15000u`.

- **Interface ordering:** the gate is written before each allocation report (`maap_mbx.c:98-100`). The two-interface tests are retained (`test_maap_mbx.cpp:197,213`).
- **Idle expiry:** `ctrl_app.c:78-81` enables TICK, and every poll refreshes the gate (`maap_mbx.c:165-180`). Event sources are coalesced by contract (`mailbox.yaml:515`), so TICK cannot crowd out timers.
- **Contract text:** `mailbox.yaml:327`, generated into `mbx_contract.h`, `KL_mbx_pkg.sv:303` and `MAILBOX_CONTRACT.md`, states the equivalence. The design page's egress choice is removed (`MAILBOX_SPLIT.md:1057`).
- **One documented difference:** the DA term is MAAP validity, not the integrator's `env->source` `dest_mac_valid`. This matches the processor's "MAAP allocated AND no conflict" and is disclosed in `maap/README.md:127-134`.

### (4) Controls per arm: confirmed

| Arm | Control |
|---|---|
| Fresh probe | `DaGateFreshProbeDeclaresOnlyItsSource` |
| Listener | `DaGateListenerDeclaresWithoutProbe`, plus the SRP-composed `F3bListenerRegistrationControlsItsOwnGate` (`srp_feedback.hpp:4`) |
| Neither | `DaGateWithoutDemandStaysClosed` |
| Aged probe | `DaGateProbeExpiresAtFifteenSeconds`: 14999 ms open, 15000 ms closed; plus composed `F3bComposedGateExpiresAfterIdleTickWake` (`test_acmp_mbx.cpp:447`) |

Campaign results:

- control mutants: **519 of 519 caught**, 0 escaped (`receipts/shard1.log`);
- AECP: 76 of 76 caught (`receipts/shard2.log`);
- SRP: 280 `[ok]` lines, which is 278 plants plus 2 lwSRP pin controls, 0 escaped (`receipts/shard3.log`);
- normal suites: PASS (`receipts/shard0.log`).

My own probes (`receipts/probes-round1.log`, `receipts/probes-interface.log`): 8 of 10 caught, including:

- removing the expiry retirement;
- removing the poll refresh;
- ignoring the source interface (caught at two interfaces);
- a 14999 ms window;
- a stop that keeps the gate;
- dropping DEST_MAC_FAIL demand in the stack.

The two escapes are S1.

### (5) Images: confirmed for ADP-ACMP-MAAP; the rest are author receipts

- I rebuilt `ctrl_image.py --base d40e4e98` for all five shapes. All ten base and head ELF SHA-256 values match the author's `image-hashes.json` (`receipts/image-hash-compare.txt`). Load growth is +1,004 B on every shape (`receipts/image_matrix.log`). `ctrl_image_selftest.py` gives 33/33.
- The SRP and SRP-AECP rows (maximum +1,320 B, under the +2,048 B Release ceiling of comment 6126295947) need runtime archives I did not build. They are taken from the author's receipts.
- **All-fabric default.** I did not rebuild BIOS 52988 B and AEM 7512 B. They are corroborated by construction:
  - the default build carries no mailbox (`milan_soc.py:2609-2613`);
  - nothing in the judged diff is compiled into the default BIOS (no reference from `sw/litex` or `milan_baremetal` to `sw/firmware/ctrl` or the stack, other than the `--ctrl-mailbox` path);
  - the only HDL change is a generated comment (`KL_mbx_pkg.sv:303`).
- **Behaviour changes beyond the predicate and the pin:** none found. TICK enabling serves the predicate's idle expiry. The ACMP talker latency bound becomes 48 for the freshness clock read, and the stack makes no wire change. The new bound arithmetic checks out: 801/866, 1,783/1,879 and 3,523/4,429.

### (6) Gates

Local, all at this head and rc 0 unless noted:

- firmware shards 0 to 3 (`receipts/shard*.log`);
- `fw_coverage.py --check`: 30 files, 100% after exclusions, table identical to the author's (`receipts/coverage.log`);
- `gen_mailbox.py --check --crosscheck --selftest`;
- `check_submodule_docs.py`;
- `submodule_boundaries.gen.py --check`;
- `check_doc_paths.py`, `check_doc_style.py`, `check_em_dash.py --base d40e4e98`, `gen_toc.py --check`, `docs_check.py`;
- `check_hygiene.py --check`;
- `check_rtl_source_lists.py`;
- `measure_test_evidence.py --check`;
- `lint_rtl.py --check` (90 ≤ 90);
- `ctrl_image_selftest.py`;
- `ctrl_boundary.py --selftest --only verilator`.

Not run, or environmental:

- `ctrl_boundary.py --without verilator` stopped on a missing `migen` LiteX dependency on this host (rc 2, `receipts/boundary_host.log`). Every firmware builder it reached exited 0.
- `publication_census.py` refused because the pinned sv2v 0.0.12 is not on this host (rc 2, `receipts/census.log`). The only change to it is a description string. Hosted `publication-census` succeeded.

Hosted at exact head (read 2026-10-13T19:49Z; `receipts/hosted-check-runs.tsv`):

- `firmware-boundary`, `firmware-verilator` and `rtl-fast` **failed** (F1);
- `firmware-unit`, the control, AECP and SRP mutant contexts, `publication-census`, `verilator-lint`, `docs-check`, `elaborate`, `yosys-elaboration`, and Yosys shards 0 to 3 succeeded;
- Verilator shards 0 to 4 were still in progress;
- "Physical gPTP" was skipped, which is not execution evidence.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1: assignment item 5, touched gates fail hosted) | Assignment and correction; ruling 6092086337 items 4 and 5; `05_acmp_engine.md:383,405`; `KL_acmp_talker.sv:397`; stack pin range (merge trees, reviews); `maap_mbx.c:36-100,165-180`; `acmp_mbx.c:102`; `mailbox.yaml:327`; image rebuild; hosted run 38451042997 | R582-1 | db29bdd07529fbc697b7956827092f64b1241714 |
| RTL | CLEAN | `hdl/milan/mailbox/KL_mbx_pkg.sv:303` (comment only; `DA_GATE` offset 0x000 and OPEN lsb 0 width 16 unchanged, generator `--check --crosscheck` green); `lint_rtl.py --check` 90 ≤ 90; source lists; firmware widths and indexing (`maap_mbx.c:46,57-59`, `published_gate[MBX_N_IF]`, `ctrl_app_srp.c:53-57` interface bound by `acmp_mbx.c:88`); access-bound arithmetic (`maap_mbx.h:19-21`, `acmp_mbx.h:136`, `MAILBOX_SPLIT.md:702-727`) | R582-1 | db29bdd07529fbc697b7956827092f64b1241714 |
| Robustness | CLEAN | Expiry retired every dispatch while DA is invalid (`maap_mbx.c:43`); wrap-safe freshness (stack `acmp.c`, `da_fresh_ms < 2^31`); reset and teardown (`srp_mbx.c:348,623`, `maap_mbx_stop`, detached-SRP clear `ctrl_app_srp.c:55`); Ignore, Leave and rejoin (`srp_mbx.cpp:333`, `srp_feedback.hpp:4`); feature-disabled paths (no ACMP owner leaves the gate closed, `maap_mbx.c:55`; ticks only with ACMP and MAAP, `ctrl_app.c:78-81`); event coalescing (`mailbox.yaml:515`); malformed ADP lengths 0..81, versions and CDL (`test_adp.cpp:564-603`); reentry count 0 in the composed test | R582-1 | db29bdd07529fbc697b7956827092f64b1241714 |
| Tests | UNCLEAN (F1) | `test_maap_mbx.cpp:197-298,513`; `test_acmp_mbx.cpp:447`; `srp_feedback.hpp:4`; `srp_mbx.cpp:333`; `test_adp.cpp:564-603`; `ctrl_mutants.py:503-560`; `srp_mutants.py:43`; shards 0 to 3 (519/76/278 plus 2 pin, 0 escaped); reviewer probes (8 of 10 caught, S1); coverage; hosted contexts | R582-1 | db29bdd07529fbc697b7956827092f64b1241714 |
| Docs | UNCLEAN (F2) | `mailbox.yaml:327` and generated copies; `MAILBOX_SPLIT.md:648-727,823,1057-1090`; `maap/README.md:109-160`; `ctrl/README.md:62-90,381-435`; `SUBMODULES.md:24,214-262`; `gtest/README.md:246-318`; diagram regeneration check; doc gates green | R582-1 | db29bdd07529fbc697b7956827092f64b1241714 |

## Real limits

- **Not rebuilt here:** the all-fabric BIOS and AEM binaries; the SRP and SRP-AECP image rows (they need runtime archives).
- **Not run here:** the publication census (pinned sv2v absent); the full host `ctrl_boundary.py` (LiteX `migen` absent); the standalone stack `validate.py` and `baremetal.py` (stack-owned; the author's receipts and #25's reviews cover them).
- **Specification:** Milan and IEEE text was not read directly; the processor architecture page and RTL served as the predicate authority.
- **F1 cause:** the mechanism is inferred from the crash file names and the base/head comparison; I did not run Git 2.55.0 locally.
- **No source bank:** no manager source bank ran at this head, and none is claimed.
- **Hardware:** physical calibration was NOT RUN, and skipped field contexts are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the corrected head, including the remaining Verilator shards 0 to 4 at `db29bdd0`.
- The F1 disposition, including any scope ruling for a harness fix.
- Carrying R582-1-R1 to the residue checklist.
- The current-dev candidate merge build (builder and native banks), candidate-merge validation, the merge of dev after #705 lands, and post-merge containment.

R582-1 FINISHED
