[R730] NEGATIVE - exact head 9d509029de967c50de7527edf2b8869aa9db9074

Three MAJOR behavioural findings remain open. The ordinary cease-toggle path works, including a one-clock low pulse, but disable does not reliably cancel an already pending transmission or an outstanding response exchange. A cease also survives the first enable after a warm reset taken with the port disabled. These are executable failures of the portEnabled contract, not wording findings.

Repository: Mister-M-alt/FPGA-gPTP, issue #94 / PR #95. Base `f97c18035be6ef5345e5af27db2124c5697c1b40`; exact head `9d509029de967c50de7527edf2b8869aa9db9074`; tree `4d0c9d078cb2d575b100e23c6b34c2637c247594`. Covering round: R730-1.

Source remained unchanged. Probes used disposable copies under this packet's `scratch/`, changing only the harness. No source fixes, full banks, parent builds, hardware operations, or public writes were performed.

## Authorities and independent reconstruction

The supplied AGENTS instruction and referenced command policy were read first. No repository AGENTS.md or CONTRIBUTING.md exists in this donor tree. README, docs/README and the current integration, HDL, testing and source-evidence guides established the interfaces. The [issue body](https://github.com/Mister-M-alt/FPGA-gPTP/issues/94) and [manager assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/94#issuecomment-6489657856) freeze acceptance: effective-link input, NOT_ENABLED on the fall, silence and false asCapable while disabled, fresh request on the rise, unchanged countdown, and both named mutation controls. The assignment permits local Announce/Sync suppression and requires the parent companion and consumer evidence. No public maintainer waiver for the findings below was found.

Authorities are Milan v1.2 4.2.6.2.4/.5, IEEE 802.1AS-2011 10.2.4.11 and 11.2.15.3 Figure 11-8 with Cor1/Cor2, and disabled-port rules in 10.2.4/10.3. The public issue supplies relevant clause extracts. Parent [REQUIREMENTS.md](https://github.com/kebag-logic/milan-fpga/blob/e06ade312a80eb578579365134ab797cda90622b/REQUIREMENTS.md) supplies REQ-PTP-05/07; the parent integration guide and source define effective-link and publication ownership. This review does not claim a fresh audit of the complete standards texts.

The independent source pass covered the complete 15-file diff and four commits, then the [pinned public evidence](https://github.com/kebag-logic/milan-fpga/tree/635234810f71ec72166d2ba226e483cfd247d2b1/review-evidence/gptp94-r1). `INDEPENDENT-VERDICT.md` records the initial negative verdict and all five lenses before PR comments or prior reviews were read. An additional reset probe subsequently confirmed a limitation disclosed in the public author handoff.

## Findings

### R730-F1 — MAJOR — A stalled serializer prevents disable and can start a frame while disabled

**All attributable lenses:** Conformance, RTL, Robustness, Tests, Docs.

**Locations:** `hdl/top/KL_gptp_engine.sv:503`, `:617`, `:1138`; `hdl/wire/KL_gptp_tx_slot.sv:116`; `tb/verilator/engine/sim_main.cpp:6002`; `docs/INTEGRATION.md:204` and `:218`.

**Authority/evidence:** Issue #94's link-loss acceptance and IEEE 802.1AS-2011 10.2.4.11 / 11.2.15.3 Figure 11-8 require NOT_ENABLED and false asCapable on disable; the approved implementation promises no gPTP transmission while disabled. The new gate checks only SEND. Once SEND sets `ser_run_r`, portEnabled cannot disable the serializer or its output. Event dispatch requires `ser_idle_w`, preventing queued NOTEN from running while that frame is stalled.

`probe-run.log` captures a capable port with ready low, valid high, SOF high, and no accepted first byte. After portEnabled falls, 8,000 cycles at 2 MHz (4 ms) elapse: flags remain `0xf`, including asCapable, and SOF remains pending. Releasing ready while portEnabled stays low transmits one complete frame. Its first accepted byte occurs well after disable; this is not merely an already accepted frame's tail. The stall can last arbitrarily long.

**Impact:** False capability can persist indefinitely on a disabled port, and a frame can begin transmission while disabled. Prompt NOT_ENABLED depends on downstream progress. Existing phase 45 keeps ready high; its 16-cycle SOF allowance does not exercise this case.

**Required outcome:** Make disable effective independently of a blocked serializer. Define and implement unsent-frame cancellation and partial-frame handling at the parent boundary while preserving the agreed ready/valid contract. Clear and publish capability without requiring a disabled transmit path to drain. Align documentation with the corrected behaviour.

**Verification:** Keep the pre-SOF stall probe; extend it across accepted byte positions and a sustained stall. Plant controls for cancellation and capability clearing. Require no accepted SOF while disabled, bounded false-capability publication, and recovery without a stranded timestamp claim. Preserve ordinary backpressure and toggle tests.

### R730-F2 — MAJOR — NOT_ENABLED retains an armed response and accepts its late Follow_Up

**All attributable lenses:** Conformance, RTL, Robustness, Tests, Docs.

**Locations:** `hdl/ucode/gen_gptp_ucode.py:2180`, `:2021`, `:1982`; `hdl/top/KL_gptp_engine.sv:1079`; `docs/TEST_DEVELOPER.md:140`.

**Authority/evidence:** IEEE 802.1AS-2011 11.2.15.3 Figure 11-8 forces the requester into NOT_ENABLED while portEnabled is false; it cannot continue the previous WAITING_FOR_PDELAY_RESP_FOLLOW_UP exchange. Issue #94 requires that transition. NOTEN clears cease/streak and capability state but retains `S_RSPSEQ` and requester timestamp validity. The new RTL invalidates transmit claims only. Follow_Up checks sequence, source and cease, but no disabled state; NOTEN has just cleared cease.

The probe sends a valid response to outstanding request sequence 12, disables the port and waits 8,000 cycles for NOTEN, confirming false asCapable. A matching Follow_Up while still disabled changes published peer delay from **601 ns to 701 ns** and emits **one commit**. Both assertions fail in `probe-run.log`. This changes an external measurement and state-machine behaviour. The probe does not claim that this single late Follow_Up alone raises asCapable.

**Impact:** A pre-fall exchange continues calculating and publishing during NOT_ENABLED and advances qualification state. Clearing egress claims does not cancel requester pairing. The existing disabled-traffic phase injects a request, Announce and Sync, not an already armed response followed by its delayed Follow_Up.

**Required outcome:** Invalidate or gate outstanding requester-pair continuations at disable, including deferred timestamp completion. Pre-fall exchanges must not update delay or qualification in NOT_ENABLED. Preserve response/timestamp ownership on re-enable. Correct the publication-hold documentation alongside the behavioural fix.

**Verification:** Keep response-before-fall / Follow_Up-after-fall coverage and add deferred-timestamp ordering. After NOTEN, require unchanged delay and no exchange-completion commit while disabled. Require two fresh good exchanges after re-enable and a mutation control restoring stale pairing.

### R730-F3 — MAJOR — First enable after a disabled warm reset resumes the retained cease

**All attributable lenses:** Conformance, RTL, Robustness, Tests, Docs.

**Locations:** `hdl/top/KL_gptp_engine.sv:1095` and `:1107`; `hdl/ucode/gen_gptp_ucode.py:1559` and `:1620`; `docs/INTEGRATION.md:214`; public author `HANDOFF.md:48`.

**Authority/evidence:** Milan v1.2 4.2.6.2.5 makes a portEnabled/link toggle an exit from cease. Figure 11-8 requires INITIAL_SEND_PDELAY_REQ; issue #94 requires the first request within one interval after the rise. Reset clears `port_seen_r`, but retained scratch can keep `S_CEASE`. Suppressing every first enable after reset therefore fails for a retained cease.

The probe enters cease, asserts reset and port disable together, holds reset eight cycles, and releases reset with the port still low for 1.3 s. After the rise there are **zero requests within one interval**. The first request arrives **7,800,201 cycles**, approximately **3.9001 s**, after the rise with the accelerated three-second cease image. It waits through the retained countdown instead of ending it. `probe-run.log` records the missed deadline and eventual request. The public handoff discloses this corner; disclosure is not a maintainer scope waiver.

**Impact:** The original prolonged silence can recur after reset with the link down. The shipping countdown is five minutes. The parent not normally resetting the engine on a link toggle does not eliminate this documented warm-reset/input combination.

**Required outcome:** Distinguish fresh-boot suppression from retained cease, or otherwise ensure a disabled reset and its first enable cannot preserve cease. Preserve the cold-release publication invariant without suppressing required restart.

**Verification:** Keep this reset/disabled/rise sequence with its one-interval deadline and fresh qualification. Add a control retaining cease across first rise. Preserve cold boot, always-enabled warm reset, and countdown-only checks.

No RESIDUE or SUGGESTION finding is raised. Added source comments were inspected for prohibited bench labels, lane names, review identifiers and issue-comment identifiers; no new instance was found. Existing material outside the delta was not treated as new residue.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Frozen issue/assignment; Milan 4.2.6.2.4/.5 and Figure 11-8 extracts; parent REQ-PTP-05/07; NOTEN, restart and countdown; F1–F3 | R730-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| RTL | UNCLEAN | Registered input; event priority and slot-6 dispatch; serializer, claims and pairing validity; four ROMs; companion effective-link path; F1–F3 | R730-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| Robustness | UNCLEAN | Pre-SOF stall, one-clock cease toggle, outstanding response, disabled warm reset and recovery; built-across-fall and countdown phases; F1–F3 | R730-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| Tests | UNCLEAN | Phases 44–47 and 15 new controls; published 113/113 and 128/128 arms, 2002×3+60 runs, both parent 205/205 legs and four controls; independent 32/32 and 19/24; F1–F3 gaps | R730-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |
| Docs | UNCLEAN | Integration/HDL/test/source-evidence guides, PR and public handoff, companion guide; doc gates and 20 exact anchors pass but disable/restart claims conflict with F1–F3 | R730-1 | 9d509029de967c50de7527edf2b8869aa9db9074 |

## Positive evidence and limits

| Check | Evidence and assessment |
|---|---|
| Port contract and parent | Level synchronous to `clk_i`, registered once in `port_en_r`. Companion passes `eff_link_w` through the shadow. Parent source at `e06ade31` defines it as PHY link AND software enable AND enabled/healthy guard, in the documented engine clock domain. No added synchronizer is required under that contract. |
| Ordinary toggle/countdown | Independent focused run of the four new phases plus setup: **32/32**, rc 0. Covers cease toggle, capability loss, frame built across fall, two-exchange qualification, lost-response accounting and unchanged accelerated countdown. |
| Short toggle | A one-clock low pulse during cease produced a request **288 cycles** after the rise, within 2 ms. This is a sampled synchronous pulse, not an asynchronous sub-clock pulse claim. |
| Lost-response count | NOTEN sets `S_PDGOT`; the next request's calculation makes `S_PDLOST=0` before judging it. It does not physically zero that scratch cell on the fall. Focused checks verify four losses without the fifth-loss commit, then the fifth-loss action. |
| Dispatch and ROM | Slot 6 is synthetic NOTEN with restart queued behind it. Ordinary timers use slots 0–5; no slot-7 writer was found. Shared cease tail preserves its clear/commit actions. All four tracked images regenerate byte-identically. Public packing evidence records 3,000 configurations without used-count regression. |
| BMCA/Announce/Sync regression | Public source-head logs show **2002/2002 ×3 + 60/60**, including publication/mastership/peer-path checks. Base/head mutation logs finish **113/113** and **128/128**, with strict named failures. The changed generator paths do not rewrite those protocol algorithms. These results do not disprove the disable races. |
| Companion patch | Verified all eight ordinary-file preimages, applied the patch in a disposable subset tree, and verified all resulting blob identifiers. Its donor gitlink changes the exact base to the exact reviewed head. See `companion-check.log`. No parent bank rerun. |
| Parent execution | Public author snapshot `f64eba22dd5bd642332c6f955080a51ee8b92daa`, based on `e06ade312a80eb578579365134ab797cda90622b`, records all 15 consumer commands rc 0. Both `milan_dp` gptp and gptp-lat finish **205/205**; four controls fail their named checks. Extra-suite receipts report rc 0. The suite called the physical gPTP leg is simulation, not a hardware measurement. |
| Area | Public reports: synthesized LUTs **4990 → 4922**, FFs **3455 → 3459**, placed slices **1663 → 1659**, placed WNS **+0.524 → +0.513 ns**. These are engine out-of-context figures at 10 ns, not parent route headroom. |
| Docs/integrity | Documentation gate rc 0, **20 exact source anchors, 0 findings**. All **109 tracked blobs** and executable modes match HEAD; index matches HEAD; working tree clean. Donor has no submodule gitlinks. Companion donor gitlink separately verified. **25 downloaded evidence files** match published SHA-256 values. |

The independent adversarial run is **24 checks: 19 PASS, 5 FAIL**, rc 1. Five failed assertions map to F1–F3; build succeeded. No failing simulation is counted as a successful gate. Focused and adversarial builds ran concurrently with eight compile jobs each, within the sixteen-job limit; documentation/static checks ran concurrently. Commands were foreground commands, with no detached job left behind. No heavy implementation build ran.

Reproduction:

```sh
python3 run_probes.py --repo /path/to/exact-head-clone --jobs 16 --case focused
python3 run_probes.py --repo /path/to/exact-head-clone --jobs 16 --case probe
python3 check_static.py --repo /path/to/exact-head-clone
python3 check_companion.py
```

The probe driver verifies head and pinned compiler identity, creates trees below `scratch/`, and records build/run logs and rc files separately. It records simulation failure in the run's `.rc` file; successful orchestration exit is not the simulation verdict. `MANIFEST.sha256` lists publishable files; `scratch/` is excluded.

## Prior findings and pending manager duties

After the independent verdict and ledger were written, PR comments, formal reviews and review threads were inspected. They contained two review-start comments, **zero formal reviews and zero review threads**, and no published FINDINGS to resolve or retain at this head. No other reviewer's report was read. The issue readiness comment is author source-head evidence. Manager comments start the reviews; they do not claim a source-head bank. Exact-head workflow lookup returned no runs; no hosted execution or skipped context is credited as an executed job.

There is **no manager source-bank run at this head**. The manager owns hosted/act acceptance and final current-dev merge-candidate validation, including builder and native banks, and must link those receipts when published. Reviewed source base: `f97c1803`; supplied live dev: `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. The author's parent snapshot is not that final candidate. F1–F3 require correction and independent re-review before a positive recommendation.

Parent adoption still owes the companion at the durable donor pin, route-1x1/ooc-1x1/ooc-8x8 area checks, and the built-image link-toggle scenario. Physical calibration is **NOT RUN** here; field skips and simulation are not hardware proof. The public handoff also records retained neighbor-rate history and a non-randomized sequence across restart; these were not validated as full Cor2 initialization conformance. This negative review makes no full-state-machine conformance claim. No full source, parent, builder or portability bank was run by this reviewer.

R730-1 FINISHED
