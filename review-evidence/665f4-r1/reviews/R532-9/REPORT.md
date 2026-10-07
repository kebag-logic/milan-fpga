[R532] NEGATIVE - exact head edeef61c5a0cc6c18caa61db4019a8e378baf366

# R532-9: internal, cleared-context, independent delta review of issue #665 / PR #690

- Head: `edeef61c5a0cc6c18caa61db4019a8e378baf366`, tree `164108f28665ce5ad1a24f350bf28b056100cb56`.
- Delta reviewed: `a6e69168..edeef61c`, two commits (`877c0b9d` wires deferred ACMP binding delivery, `edeef61c` ratchets coverage). Source base and live dev: `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`.
- Round-8 findings (R532-8, R533-8) are the baseline. Unchanged F3/F4 code keeps its earlier verdicts.
- Verdict: **NEGATIVE**. One MAJOR and two MINOR findings are open. All five lenses are UNCLEAN at this head.

Every round-8 item the round-9 assignment named is fixed as specified:

- the composition now delivers ACMP's bindings to SRP;
- R533-8's probe passes without its direct-delivery workaround;
- the A0 fixture owns the 17th byte;
- the four round-8 `srp-*` probes are caught;
- the round-8 wording is corrected.

The verdict is NEGATIVE for three new reasons:

- **F1 (MAJOR):** with delivery now live, nothing reports SRP's Talker registration back to ACMP. So TMR_NO_TK withdraws every healthy SRP binding after 10 s.
- **F2 (MINOR):** a PROBE_TX_RESPONSE whose VLAN ID SRP always refuses keeps the event loop from ever sleeping.
- **F3 (MINOR):** the poll and pass terms of `srp_bounds.h` can still be understated without any test failing.

## 1. Reconstruction (public state only)

I read the following in the required order:

1. `AGENTS.md` (sections 3, 6, 7 and 8) and `CONTRIBUTING.md` (sections 3, 5 and 6), then `docs/README.md`.
2. Issue #665: the body; the FT directive (6008744385); the acceptance additions (6009661573, 6030870481); the frozen F4 assignment with Part B.4 (6030279477); the round-8 assignment (6045716528); the round-9 assignment (6047209532); and REVIEW READY (6048262038).
3. Interface authorities:
   - `sw/firmware/ctrl/loop/ctrl_loop.h` (the pass and the poll contract);
   - `acmp/acmp.h` (the `acmp_env` ports, the SRP side's `acmp_tk_registered` and `acmp_tk_unregistered`, TMR_NO_TK);
   - `srp/srp_mbx.h` (the binding port and its retry rule);
   - `srp/srp_bounds.h`;
   - `app/ctrl_app.h`;
   - `docs/design/MAILBOX_SPLIT.md`.
4. `git diff a6e69168..edeef61c` in full, `git diff d8b355fe..edeef61c --stat`, and both commits.
5. Executable evidence: `ROUND9-GATES.md`, `ROUND9-TESTS.md`, `ROUND9-COVERAGE.md` and `ROUND9-SIZES.json` from the author packet at `a07d7d05`; the live PR body; the exact-head hosted check runs.

I read the prior public findings (R532-8 and R533-8, and R533-8's published `binding_probe.py`) only after my own pass over the diff and my own probes were complete (section 4).

## 2. Delta review against the round-9 assignment

| Assignment item | Result | Evidence |
|---|---|---|
| 1. The composition owns ACMP-to-SRP delivery and keeps interface and sink identity | **Met** | `app/ctrl_app_srp.c:37-47`: the ACMP callback copies the latest request into a composition-owned slot per sink (`ctrl_app.h:75-93`) and forwards it to the original observer. `:49-73`: a poll registered after SRP's poll (`:95`) calls `srp_mbx_bind` with the sink index and `cfg.sink_interface[sink]`. `test_acmp_mbx.cpp:1152-1155` checks `polls[3]` is SRP and `polls[4]` the composition. |
| 1. Serialized under #678; no synchronous callback reentry | **Met** | The callback only copies (`:37-47`); delivery runs as a loop poll outside every port. `BindIsDeferredAndKeepsEverySinkAndInterface` checks `in_port`, an unbound sink inside the callback, and zero reentries in ACMP and SRP. The `binding-synchronous` plant is caught at IF=1/2. |
| 1. A refusal is retried after owed transmission and retained reception complete or expire | **Met** | A refused request stays pending and the poll returns true (`:67-72`). Tests cover recovery and expiry of retained reception (`srp_binding.hpp:94-117`) and owed transmission (`:119-134`), through real mailbox records. |
| 1. Unbind and replacement supersede a pending request | **Met** | Latest-wins slot (`:41-45`); `srp_binding.hpp:136-167`. |
| 1. Real-input integration at IF=1/2, each case with a discriminating plant | **Met** | 14 `binding-*` plants plus the inherited `binding-debug-guard` are caught at IF=1 and at IF=2 (`receipts/plants/if{1,2}-part*.log`, rc 0). |
| 1. R533-8's `binding_probe.py` passes without its direct-delivery workaround | **Met** | `scripts/binding_probe_nodirect.py`, adapted from the published probe (sha256 `3047858d…bf72`). It deletes the direct `srp_mbx_bind` call and its positive control, and requires the composed assertion to pass. `receipts/binding-probe-adaptation.diff` shows the deletion. Result: rc 0, `SRP_bound=1` at IF=1 and on both interfaces at IF=2 (`receipts/binding-probe-nodirect.log`). |
| 1. README updated; bounds and images re-measured | **Met**, apart from F1's missing owed item | `srp/README.md:62-74,271-279`; `ctrl/README.md:124-131`; `MAILBOX_SPLIT.md:722-726`. The bounds are unchanged because `srp_bounds.h` and every `ctrl_app.h` macro are untouched. Images: section 5. |
| 2. R532-8-F1: A0 caught by name with an owned 17th byte under gcc, clang and AddressSanitizer, with no overflow | **Met locally; hosted firmware-unit pending** | Section 4, and `receipts/a0/`. |
| 3. R532-8-F2: an executable SRP measurement that fails when any `srp_bounds.h` term is understated; the four `srp-*` probes caught | **Partly met** | The four round-8 probes and the seven `srp-bound-*` plants are caught at IF=1/2. Six single-term understatements and two real code regressions still escape (F3). |
| 4. R532-8-F3 | **Met** | `maap/README.md:134` names `CTRL_APP_THREE_PASS_MAX`. Every remaining `CTRL_APP_PASS_MAX` occurrence (`MAILBOX_SPLIT.md:715`, `ctrl/README.md:135`, `ctrl_app.h:72`, `test_acmp_mbx.cpp:1036,1041`, `srp_mutants.py:635-641`) denotes the four-module bound. |
| 5. R532-8-F4 | **Met** | `ctrl/README.md:145` now limits the claim to the exact-mask, SRP-only-wake and algebraic-bound checks. All six `four-way-*` plants behind it are caught at IF=1/2 (`receipts/plants/fourway-*.log`). |
| 6. R532-8-R1 and R2 exactly; S2 recommended | **Met** | R1 is `ctrl/README.md:44`, verbatim. R2 is `ctrl/README.md:344`, verbatim. S2 is `ctrl_app.h:137` ("MAAP must be composed."). |
| No mailbox, register-map, RTL, adapter or pin change | **Met** | `git diff --stat a6e69168..edeef61c -- hdl tb sw/mailbox docs/reference sw/firmware/ctrl/{mbx,loop,acmp} srp/srp_mbx.[ch] srp/srp_bounds.h third_party protocol-processor gptp-processor` is empty. |

## 3. Findings

### R532-9-F1 | MAJOR | Conformance, RTL, Tests, Docs | `sw/firmware/ctrl/app/ctrl_app_srp.c:75-102`; `acmp/acmp.h:414-419`; `acmp/acmp.c:749-751,906-907,1116-1144`; `srp/srp_mbx.c:483-496`; `srp/README.md:271-279` | The composition delivers bindings to SRP but never reports SRP's Talker registration to ACMP, so TMR_NO_TK withdraws every healthy binding after 10 s

- **Authority:**
  - Frozen Part B.4 (6030279477) requires Listener declarations, through a port, for each bound sink, wired in `ctrl_app` once F3 is in the base, "otherwise state the wiring as owed".
  - `acmp.h:414-419` defines the ACMP core's SRP-side inputs: `acmp_tk_registered(sink, failed)` (EVT_TK_REGISTERED, with Talker Failed as `failed`) and `acmp_tk_unregistered(sink)` (EVT_TK_UNREGISTERED).
  - Milan v1.2 5.5.3.5.42 moves a settled sink to SETTLED_RSV_OK when the Talker attribute registers. Under 5.5.3.5.36, a sink in SETTLED_NO_RSV with no registration by TMR_NO_TK (10 s, `acmp.h:50`, `:162`) stops SRP and re-probes (`acmp.c:749-751`).
  - AGENTS.md §7: "no undocumented requirement/interface change remains".
- **Evidence:**
  - `srp_mbx.c:483-496` already computes, per bound sink, whether a matching Talker Advertise or Talker Failed is registered. No code calls `acmp_tk_registered` or `acmp_tk_unregistered` outside the ACMP unit tests (search over `sw/`).
  - Before round 9 this path was unreachable in the composition because no binding reached SRP. Round 9 makes it reachable.
  - Reviewer probe `scripts/probe_tk_registered.hpp`, appended to `srp_binding.hpp` in a disposable copy and run through the arm's own build: real BIND_RX and PROBE_TX_RESPONSE for two sinks; then a matching MSRP Talker Advertise (New, then JoinIn every second) on each sink's interface.
  - Result at IF=1 and IF=2 (`receipts/probe-tk-registered-if{1,2}.log`):
    - SRP registers the Talker (`PROBE-TK0` holds at t=0);
    - ACMP stays SETTLED_NO_RSV (`PROBE-TK1` fails for both sinks);
    - at **t=10,000 ms** both SRP bindings are withdrawn and ACMP falls back to probing (state 1, PRB_W_AVAIL), although the Talker was still being refreshed.
- **Impact:**
  - In the explicit ADP + ACMP + MAAP + SRP composition, no listener connection outlives TMR_NO_TK. Every 10 s the Listener declaration is withdrawn and re-probed, even against a healthy talker.
  - SETTLED_RSV_OK, and with it `talker_registered` (`acmp.h:269`) in GET_RX_STATE/GET_STREAM_INFO, can never be reported.
  - A Talker Failed registration never reaches ACMP either.
  - The docs and PR body describe the composition as running all four modules and owning delivery. The "Integration still owed" list (`srp/README.md:271-279`, PR body line 313) does not mention this missing direction.
- **Required outcome:** either
  - (a) the composition delivers SRP's per-sink Talker registration changes (Advertise, Failed, withdrawn) to `acmp_tk_registered` / `acmp_tk_unregistered`, deferred and serialized under #678 with no reentry; or
  - (b) a public manager decision scopes this direction out of F4, and the SRP README's owed list, `ctrl/README.md` and the PR body state that the composed listener withdraws at TMR_NO_TK until it is wired.
- **Verification:**
  - For (a): `probe_tk_registered.hpp` passes at IF=1 and IF=2.
  - Integration cases cover registered, Failed, unregistered and interface isolation, each with a discriminating plant at both interface counts.
  - Coverage stays at 100 %; bounds and images are re-measured if they change.
  - For (b): the decision and the owed-item text are checked against this finding.

### R532-9-F2 | MINOR | Robustness, RTL | `app/ctrl_app_srp.c:67-72`; `srp/srp_mbx.c:294-297`; `loop/ctrl_loop.h:20-26`; `test/srp_binding.hpp:169-181` | A binding SRP refuses on every attempt keeps the loop from ever sleeping, while ACMP reports the sink settled

- **Authority:**
  - `ctrl_loop.h:20-26`: "a poll returns true while its module still owes output (a frame its transmit ring had no room for)". Only a pass that owes nothing sleeps.
  - `srp_mbx.h:97-98` defines refusal as retryable after owed transmission and retained reception, which are transient causes.
  - AGENTS.md §6 Robustness: malformed input and invalid state.
- **Evidence:**
  - `srp_mbx_bind` refuses every attempt for a bound identity with VID 0 or VID ≥ 4095 (`srp_mbx.c:295`). No SRP state change can clear that cause.
  - ACMP copies `stream_vlan_id` from the peer's PROBE_TX_RESPONSE unchecked (`acmp.c:905`) and settles the sink. The delivery poll then keeps the request pending and returns true on every pass (`ctrl_app_srp.c:67-72`).
  - The behavior is intended and tested (`OneRefusedSinkDoesNotBlockAnotherOrLetTheLoopSleep`, "earlier refusal keeps service awake"), and `ctrl/README.md:129` states it in general terms.
  - Reviewer probe `scripts/probe_invalid_vid.hpp` (`receipts/probe-invalid-vid-if{1,2}.log`): one such response, then 12 s with no input. Every pass was non-idle (40,198 passes in the probe's capped stepping); the first idle pass came at t=10,000 ms, when TMR_NO_TK unbound the sink. At t=5 s ACMP reports SETTLED_NO_RSV while SRP has no binding and the request is still pending.
- **Impact:**
  - One malformed field from a network peer keeps the core out of `mbx_hal_wait()` for as long as the binding stands. Under F1 that is until TMR_NO_TK fires, after which a re-probe answered the same way repeats the cycle. With F1 fixed and the Talker registered, it lasts indefinitely.
  - ACMP and SRP silently disagree about the sink.
  - The loop's sleep contract is broken for a cause no retry can clear.
- **Required outcome:** a refusal that no later SRP or mailbox state change can clear must not keep the loop awake indefinitely. Either the composition parks it until ACMP changes the request, or the input is rejected or surfaced before it settles. Alternatively, a public decision records the busy-wait as intended, with its bound and its reason, in `ctrl_loop.h`/`ctrl/README.md`. Transient refusals keep their current retry.
- **Verification:** `probe_invalid_vid.hpp`'s idle assertion passes at IF=1/2 (or is replaced by the decided, documented bound), with a plant that restores the perpetual retry. The existing recovery tests and plants stay green.

### R532-9-F3 | MINOR | Tests, Docs | `srp/srp_bounds.h:12-17`; `test/srp_app.cpp:116-143`; `srp/README.md:218-220`; PR body "Round 9" ("Per-term SRP access measurements") | The poll and pass terms of `srp_bounds.h` can still be understated, or exceeded by new code, without any test failing

- **Authority:**
  - Round-9 assignment item 3: the measurement "must fail when any term of `srp_bounds.h` is understated".
  - R532-8-F2's stated impact: "a later access added to `srp_mbx.c` … silently invalidates the published four-module T_svc envelope".
  - AGENTS.md §6 Tests: each test "can fail for the defect it claims to detect".
- **Evidence:**
  - `srp_app.cpp` measures the event (1/1), refused receive (2/2), maximum TX record (383/383) and maximum RX record (383/383) paths exactly at their bounds. Those terms are well guarded.
  - The poll and pass checks sit far below their bounds. Transmitting poll: 48 of 770 at IF=1, 91 of 1,540 at IF=2. Complete pass: 388 of 1,596 and 389 of 2,366 (`receipts/bounds/*.srp_app.if*.log`). Only whole-macro plants (`srp-bound-poll` to 0, `srp-bound-poll-transmit` dropping all transmits, `srp-bound-pass` dropping RX and poll) can fail them.
  - Reviewer plants (`scripts/bound_probes.tsv`, `scripts/probe_mutants.py`) were run through every suite that compiles the header (`srp_app.cpp` and `test_acmp_mbx.cpp`, IF=1 and IF=2). All of the following **escape**, while the author's `srp-bound-poll` control is caught by the same runner (`receipts/bounds/ctl-author-srp-bound-poll.rc`):
    - the poll's fixed per-interface reads 4u to 0u;
    - two transmit calls per interface to one;
    - dropping the per-interface factor;
    - the pass's event-record words dropped;
    - two RX records per pass to one;
    - the poll term halved inside the pass;
    - **real regressions:** one extra mailbox read per interface in `poll()`, and one extra read per transmitted frame in `send_pdu()`. Both make the true worst-case poll exceed `SRP_MBX_POLL_MAX`.
  - My own access trace (R532-8, unchanged code) still finds today's figures correct. This is a falsifiability gap, not a wrong bound.
  - `srp/README.md:220` ("Each bound term has a named planted understatement") and the PR body's "Per-term SRP access measurements" are true only at whole-macro granularity.
- **Impact:** the poll term is the largest share of `SRP_MBX_PASS_MAX`, and so of the published 3,128 / 3,977 T_svc envelope. It can be invalidated by a later change to `srp_mbx.c` with every gate green.
- **Required outcome:**
  - The poll's fixed-read term is checked on its own: a non-transmitting poll against `MBX_N_IF * 4`, reaching the four reads.
  - The per-transmit cost is checked through the real `send_pdu` path, and the transmit-call count per poll against `2 * MBX_N_IF`.
  - The pass composition's event-record and RX-count terms are checked against a pass that reaches them.
  - Each check gets a named plant at IF=1/2. Otherwise, narrow the README and PR claims to the terms actually measured and record the residual analytically, by a public decision.
- **Verification:** the eight escaping plants above (`receipts/bounds/rv-*.rc`, `receipts/r8probes/probe-code-*.log`) are caught, or the narrowed wording and decision are published.

### Suggestions (non-blocking)

- **R532-9-S1** | RTL | `app/ctrl_app.h:75-93`, `:137-138`. The new `ctrl_app` members and `struct ctrl_app_srp_request` are indented with four spaces inside a tab-indented header, and the attach comment breaks mid-sentence ("attach it here before" / "servicing the loop"). Match the header's tab indentation and reflow the comment. The C/C++ idiom gate passes (`receipts/idiom-gates.log`).
- **R532-9-S2** | Tests | `test/srp_binding.hpp:67-72,171-176`. Several cases hide the delivery poll by writing `app.loop.n_polls` directly. A small fixture helper that names the intent ("service without delivery") would make the cases less dependent on the poll table's layout.

## 4. Prior public findings at this head

| Prior finding | Status at `edeef61c` |
|---|---|
| R533-8-F1 (MAJOR, delivery absent) | **Resolved for its scope.** The published probe passes without direct delivery at IF=1 and on both interfaces at IF=2 (`receipts/binding-probe-nodirect.log`). All the required integration cases and plants pass and are caught. The reverse direction (SRP registration to ACMP) is not part of R533-8-F1; it is new finding R532-9-F1. |
| R533-8-R1 (RESIDUE, checkout tense) | **Resolved.** The PR body reads "Use this checkout recipe." |
| R532-8-F1 (MAJOR, A0 out-of-bounds) | **Resolved locally; hosted check pending.** `struct acmp_config` is 88 bytes with `source_interface` at offset 72, so the 17th byte is at offset 88, inside the fixture's own zeroed `extra[8]` (`receipts/a0/layout.txt`). Unplanted: 62/62 pass under gcc 16.2.1, clang 22.1.8, gcc+ASan and clang+ASan (instrumentation confirmed by `__asan_report` symbols). Planted `acmp-init-too-many-sources`: exactly one failure in each of the four builds, `AcmpCore.A0InitRefusesWhatTheStaticSizesCannotHold: A0 more sources than ACMP_MAX_SOURCES are refused`, with no sanitizer report (`receipts/a0/*.log`). Hosted `firmware-unit` (rtl-fast) was still running at my last snapshot (section 8). |
| R532-8-F2 (MINOR, no falsifiable SRP bound check) | **Resolved per its stated verification**: the four round-8 `srp-*` probes are caught and the unmodified control passes (`receipts/r8probes/`), and the seven `srp-bound-*` plants are caught at IF=1/2. **Residual carried as R532-9-F3.** |
| R532-8-F3, R532-8-F4 | **Resolved** (section 2, rows 4-5). |
| R532-8-R1, R532-8-R2 | **Resolved**, verbatim. |
| R532-8-S1 (optional) | Not taken: the F6 printout still says "three-way backlog" (`test_acmp_mbx.cpp:1025`). It remains optional. |
| R532-8-S2 | **Taken** (`ctrl_app.h:137`). |
| R532-8-S3 (optional) | Not taken. It remains optional. |
| R532-1..7 and R533-1..7 findings | Closed by the round-7 POSITIVE baseline. Round 9 does not touch `srp_mbx.c`/`.h`, the loop, the port layer or the ACMP core, so none is reopened. |

## 5. Executable evidence (this reviewer, at `edeef61c`)

All commands are in `scripts/`. Logs are in `receipts/`, with paths normalized to `$PACKET`, `$CLONE` and `$HOME`. Toolchain: gcc/g++ 16.2.1, clang 22.1.8, local GoogleTest. lwSRP is a fresh public clone at the pin `9197193e`; the review clone's lwSRP submodule was left uninitialized.

| Gate | Result |
|---|---|
| `test_ctrl_firmware.py --lwsrp <pin> --jobs 4` (no self-test, no RV32) | rc 0: 41 arms, every SRP suite at IF=1/2 and all five entity shapes (`receipts/base/suite.log`). |
| `fw_coverage.py --check --lwsrp <pin> --jobs 4` | rc 0: 22 files at 100 % lines and branches after exclusions. `ctrl_app_srp.c` is 63/63 lines and 32/32 branches. The exclusion table is unchanged in this delta (`receipts/coverage/check.log`). |
| Author plants `binding-*` and `srp-bound-*` (22), and `four-way-*` (6), each at IF=1 and IF=2, through `srp_mutants.campaign` | 28/28 caught at each interface count (`receipts/plants/`). |
| A0 matrix: unplanted and planted × {gcc, clang} × {plain, ASan} | Section 4 (`receipts/a0/`). |
| R533-8 probe without direct delivery | rc 0 (`receipts/binding-probe-nodirect.*`). |
| Reviewer probes | Talker registration: F1 reproduced at IF=1/2. Invalid VID: F2 reproduced at IF=1/2. Six bound understatements plus two code regressions escape, while the author-plant control is caught (F3). The four round-8 probes and both attach probes are caught; the control passes. |
| Pinned RV32 SDK (`riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256 `d42680e9…`), fresh install | rc 0 (`receipts/sdk-install.log`). |
| `ctrl_srp_image.py` at 1x1/8x8, IF=1/2; `ctrl_image.py`; `ctrl_image_selftest.py --require-rv32`; `fw_rv32_selftest.py --require-rv32` | All rc 0. RAM spans 78,784 / 91,488 / 93,488 / 120,960. All four ELF sha256 hashes, section tables and static-storage tables are identical to the author's `ROUND9-SIZES.json`. Growth over round 8 is +1,408 / +1,424 bytes: `image_app` +544 and text +864 / +880 (`receipts/image-comparison.txt`, `receipts/images.log`). These are size fixtures, not a shipping-image budget. |
| Bounds | `srp_bounds.h` and every `ctrl_app.h` macro are unchanged, so 3,128 / 3,977 stand. The delivery poll's zero mailbox accesses are asserted and planted (`binding-poll-adds-access`, caught). `srp_mbx_bind` makes no mailbox call. |
| Docs: `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `gen_mailbox.py --check`; pinned renderer: `check_em_dash.py --base a6e69168` and `--base d8b355fe`, `gen_toc.py --check`, `--verify-anchors`; `check_cpp_idiom.py`, `check_py_idiom.py` | All rc 0 (`receipts/docs-gates.log`, `docs-renderer-gates.log`, `idiom-gates.log`). The `--check` lines for the two idiom gates in `docs-gates.log` were usage errors (rc 2); they are superseded by the correct invocations in `idiom-gates.log`. |
| Mailbox suite | Not rerun. Round 9 changes no mailbox, RTL, contract or loop file (empty diff, section 2). The round-8 run stands for those files. |
| Clone integrity after all runs | HEAD and index tree are `164108f2…`. All 1,209 tracked blobs match by bytes and mode. Status is empty, with no ignored files (bytecode caches from my runs were removed). Gitlinks: external `efeb541a` (uninitialized), gptp-processor `5dce647a`, protocol-processor `ead80360`, lwSRP `9197193e` (uninitialized), verilog-axis `48ff7a7e`. Submodule worktrees are clean (`receipts/clone-integrity.txt`). |

## 6. Lens results

- Conformance - **UNCLEAN** (F1). Examined: Part B.4 and the round-9 assignment against `app/ctrl_app_srp.c:37-102`, `acmp/acmp.h:300-325,414-419`, `acmp/acmp.c:651-657,735-751,880-910,1116-1144`, `srp/srp_mbx.c:288-345,483-496`; Milan v1.2 5.5.3.5.36 and 5.5.3.5.42 as cited by the core; `receipts/probe-tk-registered-if{1,2}.log`. Forward delivery, identity, serialization, retry and supersession all conform.
- RTL (architecture) - **UNCLEAN** (F1, F2). Examined: `loop/ctrl_loop.h:13-26`, `loop/ctrl_loop.c:55-63,143-162`, the ACMP SRP-side port contract (`acmp.h:414-419`), `ctrl_app.h:75-94,137-147`, attach-time refusals (`ctrl_app_srp.c:77-86`), poll order and capacity (`test_acmp_mbx.cpp:1152-1155`), destroy and detach (`srp_mbx.c:224-273`), and the empty RTL/contract diff.
- Robustness - **UNCLEAN** (F2). Examined: refusal causes in `srp_mbx.c:291-304`, retained reception and expiry (`:388-418`, `:634-672`), and `srp_binding.hpp:94-203`; `receipts/probe-invalid-vid-if{1,2}.log`. Transient refusal, recovery, expiry, unbind, replacement, attach refusals and detach all behave and are planted.
- Tests - **UNCLEAN** (F1, F3). Examined: `srp_binding.hpp`, `srp_app.cpp:83-145`, `srp_mutants.py:644-709`, `test_acmp.cpp:205-220`, `test_ctrl_firmware.py:198-203`, the coverage ratchet, the plant campaigns, the A0 matrix and the bound probes.
- Docs - **UNCLEAN** (F1, F3). Examined: `srp/README.md:55-80,200-225,265-285`, `ctrl/README.md:40-48,118-146,335-346`, `maap/README.md:126-136`, `MAILBOX_SPLIT.md:710-745`, `ctrl_app.h:1-31,58-94,137-147`, and the live PR body.

## 7. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR) | Part B.4 and round-9 items vs `ctrl_app_srp.c`, `acmp.h/.c` SRP ports and TMR_NO_TK, `srp_mbx.c:483-496`; probe-tk-registered receipts | R532-9 (no clean covering round at this head) | `edeef61c5a0cc6c18caa61db4019a8e378baf366` |
| RTL | UNCLEAN (F1 MAJOR, F2 MINOR) | `ctrl_loop.h/.c` poll contract, `ctrl_app.h/_srp.c` wiring and refusals, ACMP SRP-side contract, empty RTL/contract diff | R532-9 (no clean covering round at this head) | `edeef61c5a0cc6c18caa61db4019a8e378baf366` |
| Robustness | UNCLEAN (F2 MINOR) | `srp_mbx_bind` refusal causes, retained reception and expiry, `srp_binding.hpp`, probe-invalid-vid receipts | R532-9 (no clean covering round at this head) | `edeef61c5a0cc6c18caa61db4019a8e378baf366` |
| Tests | UNCLEAN (F1 MAJOR, F3 MINOR) | `srp_binding.hpp`, `srp_app.cpp`, `srp_mutants.py`, `test_acmp.cpp` A0, campaigns (28+28 caught), coverage 22/22, A0 matrix, bound probes | R532-9 (no clean covering round at this head) | `edeef61c5a0cc6c18caa61db4019a8e378baf366` |
| Docs | UNCLEAN (F1 MAJOR, F3 MINOR) | SRP, ctrl and maap READMEs, `MAILBOX_SPLIT.md`, `ctrl_app.h` comments, live PR body; docs, renderer and idiom gates rc 0 | R532-9 (no clean covering round at this head) | `edeef61c5a0cc6c18caa61db4019a8e378baf366` |

## 8. Real limits

- These are host-model and native results only. Physical calibration was NOT RUN; no hardware, target CPU timing or booted image is involved. Field skips are not hardware proof.
- I did not run the full self-test campaign, the saved-state (ctrl_nvm) bank, the MAAP differential, the builder bank, the mailbox Verilator suite, or the parent/PP/gPTP/Yosys banks. I ran the plants and probes relevant to this delta, listed above. The manager's full source banks are the evidence for the rest.
- F1 is shown on the host model with a synthetic MSRP Talker Advertise. Its timing follows from the core's TMR_NO_TK of 10 s. I did not establish what a bench talker would send.
- F2 uses VID 0. I did not establish whether a conforming talker can emit VID 0 or 4095 in PROBE_TX_RESPONSE; the finding concerns the response to such input, whatever its source.
- F3's bound reasoning reuses my round-8 manual access trace of `srp_mbx.c`, which round 9 does not change.
- Hosted checks at my last snapshot (`receipts/gh-check-runs-edeef61c.tsv`, 2026-10-07T23:04Z):
  - success: the docs and elaborate workflows, docs-check, docs-check-no-git, wire-accountability, changes, bdd-conformance, verilator-lint, yosys-elaboration, full-ci-gate, all Yosys shards, Verilator shards 0/5 and 3/5;
  - still in progress: `firmware-unit` and Verilator shards 1, 2 and 4 (workflows rtl-fast and rtl-full);
  - "Physical gPTP" was skipped, which is not an executed result.

  I could not confirm R532-8-F1's hosted half (`firmware-unit` and `rtl-fast` green at this head).
- The SRP image runtime was rebuilt from locally provisioned Picolibc, compiler-rt and LiteX sources. The images were linked from a scratch clone of the head with lwSRP initialized at the pin. The resulting ELF hashes equal the author's record.

## 9. Pending manager duties

- Hosted acceptance at this head: `firmware-unit`/`rtl-fast` (which also closes R532-8-F1's hosted half) and `rtl-full`; trusted local replication.
- A public decision on F1 (wire SRP-to-ACMP registration in F4, or scope it out and record it as owed), and on F2 if the busy-wait is to be kept.
- The external review's round-9 verdict, current-dev candidate merge validation and post-merge containment.
- No new RESIDUE in this round. Publishing this report and the receipts listed in `MANIFEST.sha256`.

R532-9 FINISHED
