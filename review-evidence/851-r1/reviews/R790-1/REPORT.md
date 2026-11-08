[R790] NEGATIVE - exact head 2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a

External independent review, round R790-1, of issue #851 / PR #852: adoption of processor `044cb25f` (processor PR #215, issue #214, one vector per value per MRPDU) from `92100657` on dev `1eb5289d`. Exact head `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a`, tree `42c092d1a9ec53f3655aa3e3605105a14e79ee7b`. All five lenses applied. No prior public review findings exist on the PR or the issue at review time; the only PR comments are the two review-start notices.

The adoption is correct. The gitlink, the processor change, the parent gates and the route figures all check out, and the record follows the maintainer decision. One open MINOR keeps the verdict NEGATIVE: the routed critical-path statements in three authoritative pages have no published receipt, and the receipt named `worst-setup-path.txt` holds a different, non-critical path.

## Findings

### F1 - MINOR - RTL, Docs - critical-path claims have no receipt; the published "worst setup path" receipt is not the worst path

- Where:
  - `docs/design/AREA_BUDGET.md:211-212` (selected ExtraTimingOpt route: 29 logic levels, `u_pp/u_notify/ctr_pend_r_reg[0]` to `u_pp/u_nvm_shadow/hs_r_reg[1]`, 19.439 ns data delay, 14.237 ns routing).
  - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:127-130`: the same setup path, plus the worst hold path `cap_l_r_reg[18]` to `u_tcdc/mem_r_reg_0_7_42_47` at +0.036 ns.
  - `docs/reference/SUBMODULES.md:721-725` and the PR body's shipping-route paragraph (ExtraPostPlacementOpt route: AECP microcode CPU to the D3 debounce counter, 36 logic levels, "outside the encoder").
- Authority/evidence:
  - AGENTS.md section 6, Docs lens: the PR and Issue must carry enough evidence for a cold reviewer.
  - RTL lens: resource and timing effects are understood.
  - The only path receipts are `review-evidence/851-r1/author/receipts/route-2d939d2d/worst-setup-path.txt` and `route-a566d4f9/worst-setup-path.txt` (identical, SHA-256 prefix `3dd487d5c6dc5b0d`). Both hold a `clk200_p` path with slack +3.609 ns and 0 logic levels, but that route's WNS is +0.044 ns (`head-2d939d2d.json`), so this is not the worst path. `receipts/figures_crosscheck.txt` flags it: "NOT THE WORST PATH".
  - No published file contains `ctr_pend_r`, `hs_r_reg`, `19.439`, `cap_l_r_reg`, `u_tcdc/mem_r` or a 36- or 29-level path. The gate's `eto-timing-design-tables.txt` carries summaries only, and `alinx_ax7101_timing.rpt` is listed "not copied".
- Impact:
  - The statement that the WNS fall (-0.115 ns on the record, -0.154 ns on the shipping route) sits outside the encoder this pin changes cannot be checked or disputed from public state.
  - The receipt named for the worst path points a reader at the wrong path.
  - This is a measured claim (endpoints, levels, delays), not wording.
- Required outcome, either of:
  - (a) Publish the worst setup path (and, for the 234 page, the worst hold path) of the ExtraPostPlacementOpt route at `2d939d2d` and of the selected ExtraTimingOpt route at `a566d4f9`. Each receipt's slack must equal that route's WNS/WHS, and the extractor must stop taking the first path of the report. The docs and PR text must match those receipts.
  - (b) Remove the path claims these receipts cannot support.
- Verification: the new receipts' slacks are +0.044 ns (EPPO, setup), +0.258 ns (ETO, setup) and +0.036 ns (ETO, hold). The start and end points, logic levels and data delays in the three pages and the PR body equal the receipts' values.

### S1 - SUGGESTION - Tests - no parent gate notices a doubled vector

- Evidence: `receipts/probe_parent_crflic_base_encoder.log`. With the `92100657` encoder swapped into a disposable copy of this head, `make -C tb/verilator/milan_dp crflic` still passes 427 of 427. That includes "every DUT LeaveAll flagged all four MSRP attribute types". The PR already says so ("No parent harness drives a doubled vector through `milan_datapath`"), and neither issue #851 nor processor #214 asks for a parent row. The rule is graded in the processor, and my probe confirms those rows can fail: `probe_srp_top_onevec_base_encoder.log` fails OV0 to OV7 (8 of 12), and `probe_srp_encoder_base_encoder.log` fails 85 of 1604.
- Optional outcome: a follow-up issue for a parent-level check that no MRPDU on the integrated wire carries one value in two VectorAttributes. It could go in the existing milan_dp MSRP/MVRP readers, with the base encoder as its planted control.

### S2 - SUGGESTION - Docs - the adoption's own route share is now measurable

- Evidence: PR #846's round 2 routed dev `1eb5289d` on this recipe (`843-review-evidence` at `425a829e`, `review-evidence/843-r1/author-r2/receipts/route-dev/gate-check.log`, copied as `receipts/dev_1eb5289d_route_gate_check_from_843r1_author_r2.log`): ExtraTimingOpt selected at 52,973 LUT, 54,595 FF, 15,817 slices, +0.234 / +0.033 ns. This PR's selected route is 53,050 / 54,729 / 15,831 / +0.258 / +0.036, so the adoption's share is +77 LUT, +134 FF, +14 slices and +0.024 ns WNS. That agrees with the manager's figures; the receipts do not disagree.
- Optional outcome: at the post-#846 sync and re-measure, which is already a manager sequencing step, replace "no route of dev `1eb5289d` exists on this recipe, so the adoption's own share of the route is not measured" (`AREA_BUDGET.md`, the 234 page, the PR body) with that measured share.

### RS1 - RESIDUE - Docs - stale count next to the new record

- `docs/design/AREA_BUDGET.md:129` still reads "All nine measurements use the same recipe identity and policy." right after the delta appends the fourteenth record's paragraph.
- Exact fix: "All these measurements use the same recipe identity and policy."
- This changes no figure or claim and is pure wording, so it goes to the residue checklist.

## Focus checks

1. **The gitlink is processor main `044cb25f`, and the processor change matches the PR body.**
   - Checks: `git ls-tree HEAD protocol-processor` gives `160000 commit 044cb25f4ed2...`. `git ls-remote` gives processor `refs/heads/main` = `044cb25f4ed2187bd238490650e73d5d189855d1`. That commit is the merge of PR #215 with parents `92100657` and `7feeccea`, and its tree `60300bb0` equals `7feeccea`'s. `git diff 92100657 044cb25f -- hdl` touches only `hdl/srp/KL_srp_encoder.sv` (+146/-12), with no port or parameter change.
   - The pin's code matches the PR body's description:
     - The identity is application + AttributeType + FirstValue's first 8 octets, and the MVRP identity is the VID alone (`key_f`, `KL_srp_encoder.sv:205`).
     - The merge table is `merge_ev_f`/`merge_fp_f` (`:222`).
     - The search goes through the existing read port, one clock per pending entry (`:443-480`).
     - A merge takes no new entry (`:680`).
   - `KL_pp_shadow` and `milan_datapath` are unchanged by the delta.
   - Processor suites at the pin with the pinned Verilator 5.050: `tb/srp_encoder` 1604/1604 PASS, `tb/srp_top RUN_ARGS=onevec` 12/12 PASS.
2. **The parent consumer gates that read MRP encoding ran at this head and pass.**
   - Author receipts at `2d939d2d`:
     - sweep 65/65, 2,192,502 checks, with milan_dp in shard 0 (only its tail is published; digest in `RAW-RECORDS.txt`);
     - `test_ctrl_firmware` shards 0-3 rc 0, with shard 3 holding the SRP campaigns;
     - behave 508/508;
     - crflic/gsi/unb mutants rc 0.
   - The one rc 1 receipt (`fw_rv32_sdk_selftest.symlinked-path`) is disclosed in the author's handoff as a symlinked-HOME provenance refusal, re-run rc 0 at the real path.
   - My runs at this head, all rc 0:
     - milan_dp `crflic` 427/427, including the Run B LeaveAll exchange where every DUT LeaveAll flags all four MSRP types;
     - `pp_shadow` 317/317;
     - `cd tests && behave`: 14 features, 508 scenarios, 2,330 steps;
     - ROM recorder with `git diff --exit-code` rc 0, and the `044cb25f` rows equal the `92100657` rows;
     - `check_submodule_docs.py` (6 exact gitlinks);
     - `pp_resource_gate.py check-baseline` (3 endpoints);
     - `docs_inventory.py --check` (fresh);
     - `lint_rtl.py --check` (89 <= 89);
     - `pp_srcs.py --check`;
     - `git diff --check 1eb5289d 2d939d2d`.
3. **The route figures match the receipts, the floors are met, and the decision is followed.**
   - `receipts/figures_crosscheck.txt` (script `scripts/crosscheck_figures.py`):
     - The shipping route at `2d939d2d` is 53,033 LUT, 54,729 FF, 15,792 of 15,850 slices, +0.044 / +0.035 ns, 0 routing errors. Every corner meets WNS >= +0.030 and WHS >= 0 (`BUILDING.md:569`).
     - The gate's selected ExtraTimingOpt route, which the image is built from (`BUILDING.md:579`), is 53,050 / 54,729 / 15,831 (19 free) / +0.258 / +0.036, and all four corners meet the floors.
     - The committed `syn/ooc/pp_resource_baseline.json` figures equal the gate candidates on all three endpoints.
     - `check` exited 1 on `route-1x1` only (+521 of +500 LUT) and 0 on both standalone endpoints. After the re-record, `check` is 0 on each endpoint and `check-baseline` passes.
   - The maintainer decision (issue #845 comment of 2026-11-06) requires each adoption to record it in `AREA_BUDGET.md` and on the pin page, and to re-baseline through `pp_resource_gate.py`. Both pages and the gate record do so, with no tolerance, floor or ceiling moved. Processor #214 was raised from a conformance-run capture, so it qualifies as a lab fix.
   - **Judgement call 1:** the standalone endpoints were measured at this pin, not copied. Each has its own Vivado run: `ooc-1x1` 20:22-20:35Z and `ooc-8x8` 19:09-19:47Z on 2026-11-07, with their own log SHA-256s. Each has a new `inputs_sha256`, and every sub-block figure differs from the thirteenth record. The encoder's FFs grew by +75 / +71, matching the 73 + 4 + 1 new search registers.
   - **Judgement call 2:** the receipts agree with the manager's estimate (+77 LUT, +14 slices; see S2).
   - The #846 conflicts are a manager sequencing matter, not a finding.
4. **Comment rule.** The parent delta changes no source comment. The processor HDL diff's new comments cite issue #214 and clauses only: no lane labels, lane names, rounds, reviewer IDs or comment IDs. No new RESIDUE of that kind.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #851 scope and acceptance, against the author receipts at `2d939d2d` and this round's reruns. The encoder at the pin (`KL_srp_encoder.sv:205-240`, `:443-480`, `:680`) against 802.1Q-2022 10.7.7, 10.7.5.13 c), 10.8.2.10.1, Table 10-3, 10.7.6.3/.5/.12, 35.2.2.8/.8.1/.8.2/.9.1 and 11.2.3.1.7, as cited in processor docs 10 section 3. Processor `tb/srp_encoder` 1604/1604 and `srp_top onevec` 12/12 at the pin. Route fit and floors (`head-2d939d2d.json`, `gate-route-1x1.log`, `BUILDING.md:569,579`). The maintainer decision | R790-1 | `2d939d2d` |
| RTL | UNCLEAN (F1) | The `92100657..044cb25f` HDL diff: read-port sharing with the drain (`base_ok_w`, `msrp_raddr_w`/`mvrp_raddr_w`), search reset and restart (`value_search`), and the full-table hold. Ports and parameters unchanged, `KL_pp_shadow`/`milan_datapath` untouched, `lint_rtl.py --check` 89 <= 89, `pp_srcs.py --check`. Single clock domain, so no CDC change. Area attribution per sub-block in `gate-*.log` and `record-facts.json`. Critical-path claims (F1) | R790-1 | `2d939d2d` |
| Robustness | CLEAN | The full-table hold, the restart on a changed offer, the drain-start overtake and reset of the search state (`KL_srp_encoder.sv:443-480`), graded by processor PV and OV rows with planted controls (base-encoder probe: OV0-OV7 and 85 PV/O checks fail). The shipping-shape latency case (a Domain re-join slips one joinTime with a third Domain entry pending) matches processor docs 10 section 3 and is disclosed in `INTEGRATION_GUIDE.md:89-109` and `SUBMODULES.md:673-680`. Parent crflic Run B LeaveAll repetition 427/427 | R790-1 | `2d939d2d` |
| Tests | CLEAN (S1 optional) | The processor rows can fail for the defect (probe receipts). Parent consumer gates rerun at the head (crflic, pp_shadow, behave). Author sweep, firmware, builder and mutant receipts and their rc files. The parent probe shows no parent row detects a doubled vector: disclosed, not required by the issue, so a SUGGESTION | R790-1 | `2d939d2d` |
| Docs | UNCLEAN (F1) | `CHANGELOG.md:11,57-90`, `INTEGRATION_GUIDE.md:89-109`, `SUBMODULES.md:25,635-782`, `AREA_BUDGET.md:13,122-129,142-215,228-231,632-636`, `MARK_II_AREA_PLAN.md:59,938-939`, `234_PP_SHADOW_AREA_BASELINE.md:10-156`, `findings/README.md:25`, the generated diagram/manifest/audit (`docs_inventory.py --check` fresh, `check_submodule_docs.py` OK), the baseline JSON `measured` notes, and the PR body against the receipts (`figures_crosscheck.txt`). F1 is open. RS1 and S2 do not affect coverage | R790-1 | `2d939d2d` |

## Real limits

- This round ran no Vivado, Yosys bank, full parent sweep, firmware campaigns or builder. The route, gate, sweep, firmware and builder figures are the author's published receipts, which I cross-checked but did not reproduce.
- The full milan_dp sweep log is not published (tail only). I re-ran the crflic leg only.
- The act replica at this head has not run: **open**.
- Hosted exact-head contexts were still in progress or queued at the snapshot (`receipts/hosted_checks_snapshot.txt`). The completed ones (`changes`, `docs-check-no-git`, `docs-gates-1`, `elaborate-gates-0/2/3/4`, `wire-accountability`, `bdd-conformance`, `full-ci-gate`, `Verilator shard 6/19`) were successful. Physical gPTP was skipped, which is not hardware proof. I claim no hosted verdict.
- Physical calibration: NOT RUN. No bench, no flash, no hardware proof.
- No manager source bank ran at this head, and I claim none.
- My review clone was verified byte-exact after the probes (`receipts/clone_integrity.txt`): HEAD, tree, index equal to HEAD, clean worktree, and gitlinks `044cb25f` / `135afd04`. The only changes were read-only `git fetch` objects and refs. All builds and probes ran in disposable copies under `scratch/`.

## Pending manager duties

- Resolve F1, then re-review the docs and RTL lenses at the new head.
- Run the act replica at the head.
- Accept the hosted exact-head contexts when they complete.
- Sequence #846 first, then sync this lane and re-measure the baseline JSON, `AREA_BUDGET.md`, the 234 page and the pin page. S2 and RS1 can be folded in then.
- Build and validate the current-dev merge candidate (builder and native banks).
- Get the second independent positive review, then do post-merge containment.

R790-1 FINISHED
