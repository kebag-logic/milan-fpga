[R741] NEGATIVE - exact head 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee

Internal cleared-context review of kebag-logic/milan-fpga PR #815 (#797 lane D0, the documentation
inventory and verification audit) into `dev`, round R741-2. This is a delta review over the round-1 head
`bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a`. Head `3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee`, tree
`6d5ae1c3548e6dddd0224cae480db97db8035f6a`, source base and live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
The delta is nine commits, `1df73301` to `3e6d92c1`, on top of `bd16b371`, with no rebase.

## Verdict basis

There is one open MINOR, F1 (Conformance, Docs). `REQUIREMENTS.md:27` makes the default-placement
statement that D0 records as a contradiction on three other release-facing pages (D0-001, D0-033 and
D0-056). The page is still marked `current`. That is the class R741-1 F2 named, and this round's fix
did not reach this instance. Every other part of the delta is correct:

- The status rule is enforced by both the generator and the gate. A finding planted on a current page
  fails `--check`. A generator that has lost the rule also fails `--check`.
- The self-test now drives the workflow's own `--check` through `git ls-files`. R741-1's three
  mutants are killed.
- All six named prior findings are resolved at their cause.
- 21 of the 39 new findings were checked against their sources, and every one holds.
- 10 sampled sentences on current pages hold.
- 15/15 docs gates pass.

The verdict does not depend on the suggestions or on the limits listed below.

## Authorities reconstructed

- `AGENTS.md`, `CONTRIBUTING.md` (gates, section 6), `docs/README.md`.
- Issue #797 rules and acceptance, the scope addition (issuecomment-6489587365) and the plan
  (issuecomment-6518880512) section D0, all reconstructed in round 1 and unchanged since.
- The round-2 assignment, issuecomment-6520804859. It lists the six findings to fix. It sets the
  status rule: a page with an open finding cannot be current, the generator enforces it, and the gate
  fails on disagreement. It asks for deeper sampling with per-page counts. It keeps the rules: record
  only, no fixes on held pages, commits on top of `bd16b371`.
- The author's REVIEW READY, issuecomment-6522752898.
- The two owner scope additions, issuecomment-6522974767 (13:33) and issuecomment-6523093123 (13:40).
  Both were posted after the REVIEW READY head. They are not part of this round's frozen assignment
  (see the pending manager duties).
- PR metadata from `gh pr view 815 --json ...`, saved as `receipts/pr815_view.json`. The head and base
  match the values above.
- My own round-1 report, issuecomment-6520804068, and the round-1 external report,
  issuecomment-6520356763. The brief allows reading both.

## Findings

### F1 - MINOR - Conformance, Docs - `REQUIREMENTS.md:27` - the D0-001/D0-033/D0-056 statement is still `current` on the requirements page

Authority/evidence:

- The round-2 status rule says a page with an open finding cannot be current. R741-1 F2 says one
  statement cannot be both a verified contradiction and current on two release-facing pages.
- The lane resolved R741-1 F2 by recording the same placement statement as a contradiction in three
  places:
  - D0-001, `README.md:60`, "ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware.";
  - D0-033, `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:23`, "Its default is bare-metal control;
    all-fabric remains supported.";
  - D0-056, `docs/reference/FR_NFR.md:77`, "Its default is bare-metal control over packet mailboxes.".
- All three cite `sw/litex/milan_soc.py:2621` and `:3838`: `--ctrl-mailbox` is `store_true`, off by
  default.
- `REQUIREMENTS.md:25-31` has the same structure:
  - "MUST each have build-selectable placement."
  - "The Mark II default places them on the bare-metal core."
  - "The all-fabric build remains a supported option."
  - "It remains the shipping default until F2 to F5 pass".
- This matches `FR_NFR.md:76-79` sentence for sentence. Yet `docs/DOCUMENTATION_AUDIT.md:126` marks
  `REQUIREMENTS.md` `current`, "no recorded contradiction", Verified `D0`.
- `REQUIREMENTS.md` is release-facing: `RELEASE_FACING` at `scripts/docs_inventory.py:100` matches it.
  It is the only remaining release-facing repetition, per `receipts/requirements_default.txt`. The
  other repetitions, such as `docs/design/MAAP_FABRIC.md:5`, are on area-lane pages outside D0's
  release-facing set.
- Note for the decision: `REQUIREMENTS.md` is the normative contract, and its "Mark II default" may
  define the design placement rather than describe the build. If so, D0-001, D0-033 and D0-056 are
  clarity items, not contradictions. AGENTS section 2 says a conflict between requirements and
  documentation is published for a decision rather than resolved privately. Either reading is
  defensible. Recording the statement as contradicted on three pages and current on the fourth is not.

Impact:

- A page marked current, on the release-facing set, carries a statement D0 itself records as
  contradicted elsewhere. The status rule therefore holds per page but not per statement.
- The reference lane receives three findings that could be undone by citing the requirements page.

Required outcome: treat the four statements the same way, in one of two ways.

- Record `REQUIREMENTS.md:27`. The page renders stale, and the requirements-versus-implementation
  conflict is published for a decision.
- Or publish a decision that the "Mark II default" wording names the design placement, and re-scope
  D0-001, D0-033 and D0-056 to match.

Verification:

- `python3 scripts/docs_inventory.py --check` passes on the regenerated page.
- The four statements carry the same judgement on the page or in a linked public decision.

### S1 - SUGGESTION - Tests - `scripts/docs_inventory.py:593-622`, `:654-686` - the escaped-pipe handling of the status-rule parser is not exercised

- Mutant `parser-cells-ignore-escapes`, which makes `cells()` split on every `|`, SURVIVED
  `--selftest` (`receipts/mutants2.txt`).
- The committed page has 17 table rows with an escaped pipe (`receipts/parse_coverage.txt`). Several
  Findings rows quote table cells, for example D0-019 and D0-028.
- Under that mutant, those rows no longer have 9 or 6 cells and are skipped silently. The status-rule
  check would then miss a page whose only Findings rows quote a table.
- At this head the parser reads all 210 Inventory rows and all 62 Findings rows. The primary rule in
  the generator, and the diff check, are fully tested. So this is a gap in the defence-in-depth control
  only.
- A fixture finding whose quote contains `|`, plus the existing "hand-edited status hides a finding"
  arm on that page, would kill it.

### S2 - SUGGESTION - Docs - `docs/DOCUMENTATION_AUDIT.md:23` - say how many statements per page were source-checked

- The page says "Statements on D0 pages were checked at dev `1e80128f`." It marks `BUILDING.md` and
  `SUBMODULES.md` current with Verified `D0`.
- The lane's own published sampling counts (`author-r2/sampling/README.md`) say otherwise: 85 and 55
  statements on those two pages were read without a per-sentence source line. So were 322 on
  `BAREMETAL_FIRMWARE.md` and 361 on `REGISTER_MAP.md`.
- The PR body and REVIEW READY disclose this. The generated page does not.
- A "checked / numeric-or-normative" column, or one sentence naming the four pages, would stop a cold
  reader taking `current` for fully verified. Whether "read" meets the assignment's "every numeric or
  normative sentence gets checked" is the manager's call; see the pending manager duties.

### S3 - SUGGESTION - Robustness - carried from R741-1 S1 - a `re-verify` row passes the gate once regenerated

Probe q08 (`receipts/probe_gate2.txt`):

- A finding whose quote is on no page, regenerated with `--write`, passes `--check`. Its row reads
  "re-verify: quote not found".
- The page still renders stale, so the status rule holds. Refusing a committed re-verify row would
  stop a mistyped quote sitting on the page as a passing row.
- Unchanged from round 1. Designed behaviour.

No new RESIDUE: the added source and workflow lines name no lane, round, reviewer, comment ID or bench
label (`receipts/delta_source.diff`, scanned). The only `D0-001` strings are fixture data.

## Prior findings named in the brief, judged at this head

| Prior finding | Cause | At `3e6d92c1` | Result |
|---|---|---|---|
| R742-1 F1 MAJOR, `QSPI_FLASHBOOT.md` current against implemented saved state | page :59-64 says journal unused, blank-flash responder, nothing survives a power cycle | D0-024 (:60) and D0-025 (:62) recorded. Sources hold: `milan_baremetal.c:329-331` (slots in `MILAN_FLASH_JOURNAL_OFFSET`), `milan_soc.py:172` (128 KiB journal, so two 64 KiB slots), `milan_baremetal.c:1393` `nvm_commit`, `:1641` `nvm_boot`, called at `:1890`; `KL_pp_shadow.sv:1123` `KL_nvm_backend`; `SAVED_STATE_MATERIALIZATION.md:163`. The correction keeps the physical-qualification gap separate. D0-035/036/037 add the AEM copy routine, the read mode and the config claims. Page `stale`. | RESOLVED |
| R742-1 F2, `VERIFICATION_DEVELOPER.md` aggregate runner | :32 "lack one aggregate runner"; :49 "no general harness framework" | D0-026 (`run_litex_sims.sh:98` `INVENTORY`, `:150` aggregate) and D0-027 (`sw/firmware/gtest/README.md:3-13`; both graders exist). Page `stale`. | RESOLVED |
| R742-1 F3, `EGRESS_QUEUE_MAP.md` q2/q3 swap | :37-38 against `ethernet_packet_pkg.sv:220-221` | D0-028 recorded. The reset `CLS_TCQ` `0x004898C0` (`milan_csr.sv:2008`) decodes TC2->q3 and TC3->q4 (computed). The correction swaps both rows. Page `stale`. | RESOLVED |
| R742-1 R1 and R741-1 R1 residue, lane label in source comment | `docs_inventory.py:83-84` at `bd16b371` | Now "The release-facing pages #797 verifies statement by statement: ..." (`:98-99`). No label. | RESOLVED |
| R741-1 F1, matrix rows 262-264, 267 | uninstantiated classifier, queue and shaper chain | D0-029 to D0-032 recorded. Sources hold: `milan_datapath.sv:654-664`, `:8552-8558`; C-TAG writers `KL_aaf_packetizer.sv:514` and `KL_crf_tx.sv:514`, reader `avtp_stream_parser.sv:159`; no `traffic_classifier`/`traffic_queues`/`traffic_controller_802_1q` instance outside their own sources (`git grep`). The transmit half of 6.9.3 is kept. Page `stale`. | RESOLVED |
| R741-1 F2, `AXIS_CORES_ON_BAREMETAL_SOC.md:23` | D0-001 statement marked current | D0-033 recorded and the page is `stale`. FR_NFR's instance is recorded too (D0-056). The `REQUIREMENTS.md:27` instance remains: F1 above. | RESOLVED for the named page; same class RETAINED as F1 |
| R741-1 F3, the self-test does not run the gate or the Git listing | `selftest()` called `is_fresh()` on a Git-free fixture | `control()` (`:698-735`) runs `main(["--write"/"--check"], root)` through `gate()` (`:687`) on a `git init` fixture staged with `git add -A` (`:647-686`). My three round-1 mutants are KILLED: `check-always-fresh`, `check-stale-returns-0`, `git-listing-includes-untracked` (`receipts/mutants2.txt`). The untracked-page control and the walk without Git that skips a submodule page both exist. | RESOLVED |
| R741-1 R2 residue, step comment too wide | `.github/ci-templates/docs.yml:422-424` at `bd16b371` | Now names exactly what the gate catches, and says that `--selftest` runs the same `--check` on Git fixtures (`:422-432`). It matches the generator docstring `:39-43`. | RESOLVED |

## Evidence by check

### (1) The status rule and the gate (manager's planted test)

All probes in `probe_gate2.sh` ran in fresh `git clone --no-local` copies with no submodules. Results
are in `receipts/probe_gate2.txt`. Every probe gave its expected rc:

| Probe | Mutation | `--check` rc |
|---|---|---|
| q00 | none | 0 |
| q01 | **finding planted on a current page** (`docs/guides/SYSTEM_INTEGRATOR.md`, a real quote), page not regenerated | **1**, STALE (current 176 -> 175) |
| q02 | same, then `--write` | 0. The page renders it `stale` with D0-999 |
| q03 | hand edit: EGRESS row `stale` -> `current` | **1**, "carries an open finding but is marked current (the status rule)" plus a diff |
| q04 | **generator with the status rule removed**, finding planted, `--write` by that generator | **1**. The status-rule check alone names every affected page |
| q05 | rule-less generator, unchanged data, `--write` | **1** |
| q06 | hand edit: two Findings rows deleted | 1 (diff) |
| q07 / q08 | planted finding whose quote is absent, without / with `--write` | 1 / 0, page `stale` with a re-verify row (S3) |
| q09 | D0-024's statement fixed on its page | 1, row becomes re-verify |
| q10 | `--selftest` under `GIT_DIR`/`GIT_WORK_TREE` pointing at a disposable repository | rc 0; the disposable index keeps 0 entries |

- Parser coverage (`receipts/parse_coverage.txt`): `current_with_findings()` (`:598-622`) reads all
  210 Inventory rows and all 62 Findings rows of the committed page. The 24 skipped rows are table
  headers.
- The set of pages with data-file findings equals the set listed in the Findings table: 13 pages, all
  `stale`.
- Status totals: 176 current, 13 stale, 21 obsolete. They match the PR body.
- By lane: reference 52, overview and guides 10, computed with the generator's own `LANES`.
- `status_rule()` (`:406-415`) runs after every source of `current`: judgement, generated page,
  archive index. The control "a recorded current judgement cannot hide a finding" covers that order.
- A superseded or obsolete page keeps its status. The docstring states this, and it meets the rule:
  neither status is current.
- The gate is neither vacuous nor broken.

### (2) Self-test strength

My 15 mutants of the head generator are in `mutate_selftest2.py` and `receipts/mutants2.txt`. 12 were
KILLED by `--selftest`, including every status-rule mutant: check ignores the rule, rule removed,
parser returns empty, wrong section, wrong cell. Three survived:

- `git-listing-keeps-gitlinks` is equivalent: a gitlink is not a `.md` path.
- `git-env-passthrough` is equivalent outside a hook environment. The author's published receipt
  `author-r2/receipts/mutants/mutants-final-head.txt` kills it under a hook environment, and probe q10
  confirms the head leaves an outer repository untouched.
- `parser-cells-ignore-escapes`, see S1.

The author's published run reports 18/18 counted mutants killed, which is consistent with this.

### (3) New findings spot-checked against their sources (21 of 39)

Receipts: `receipts/spot_A.txt`, `spot_B.txt`, `spot_C.txt`. Each one holds, and its correction is right:

- D0-024, D0-025, D0-026, D0-027, D0-028, D0-029 to D0-032: see the table above.
- D0-033: `milan_soc.py:2621`, `:3838`.
- D0-034: `milan_soc.py:1404` (`_AXIS_CDC_DEPTH = 16`), `:1523-1530` (buffered `stream.ClockDomainCrossing`
  per direction), `:1746` (`tx_sf` `PacketFIFO`); `endstation_ax7101_1x1_tdm8.yaml:43-44`.
- D0-035: no caller of `copy_image_from_flash_to_ram` under `sw/`. `load_aem_image()` has its own loop,
  the length bound and a CRC32 compare.
- D0-036: `milan_soc.py:3054-3069`, `READ_1_1_1_FAST`, `mode="1x"`, 12.5 MHz, quad read dropped
  2026-07-08; `:3076` `SPIFLASH_SKIP_FREQ_INIT`.
- D0-038: `milan_soc.py:3037-3041`, `l2_cache_size = 0`; `--l2-bytes` refused.
- D0-039: `milan_soc.py:3704-3707` (only `baremetal`) and `:4039-4041` (requires `--xlen 32`).
- D0-041: `check_baremetal_only.py:1625`; `sim_main.cpp:464`; `configure_fabric()` `:1796`, called at
  `:1881`.
- D0-048: no C source outside `sw/trace/` includes `milan_trace.h`. `Makefile:6` builds
  `milan_baremetal.o` alone. The `test_builder.py:14170` hit is a builder mutant fixture.
- D0-057: `REGISTER_MAP.md:351-356` and the matrix row 5.3.7.6.
- D0-060: `build.sh:378-384`; `adp_shape_defaults.svh:24`, `:27`. N_STREAMS of the shipping 1x1 shape
  is 1.
- D0-061: `milan_baremetal.c:1809` writes `MILAN_TCAM_CTRL`; `boot_policy.py:59`; the page has no
  `TCAM_CTRL` row.
- D0-062: `BAREMETAL_FIRMWARE.md:2264` (commit `1e80a106`); `SUBMODULES.md:371-381` (sixteen slices
  free, +0.303 ns); pins `f65c8ff7`/`f97c1803` at `:24-25`.

The last three D0-041 commits change only the source cell's wording, to satisfy the bare-metal scope
gate and the doc-path gate. The cited lines `milan_baremetal.c:1799-1802` are the identity and enable
writes inside `configure_fabric()`. The D0-050 to D0-055 descriptor measurements were not re-run
(`audit_pp_descriptors.py` needs the builder); they were checked only for internal consistency with
the page's own lines.

### (4) Sentences on pages marked current, sampled (10)

All ten hold:

1. `docs/integration/INTEGRATION_GUIDE.md:166`, 20 ms per restore wait: `protocol-processor`
   `hdl/top/protocol_processor_top.sv:169`, `CLK_HZ_P/50`.
2. `:167`, the whole restore bounded at 1,000 ms: same file `:173-178`, `CLK_HZ_P` cycles.
3. `:119`, `axis_clk` at 50 MHz: every `configs/*.yaml` `milan_clk_hz: 50000000`.
4. `:73`, the complete 64 KiB CSR window: `milan_datapath.sv:477`, `:487`, 16-bit AXI address.
5. `docs/reference/MAILBOX_CONTRACT.md:27`, `ID` at `0x000`: `KL_mbx_pkg.sv:80`.
6. `:28`, `CAPS` at `0x004`: `:94`.
7. `:30`, `IRQ_ENABLE` at `0x00C`, and the line is status AND enable: `:126`; `KL_mbx.sv:40`.
8. `:31`, `NOW_MS` at `0x010`: `:140`.
9. `docs/reference/MILAN_FEATURE_STATUS.md:60`, current version `0x0002_0060`: `milan_csr.sv:201`.
10. `REQUIREMENTS.md:3`/`:5`, VERSION `0x0002_0060` and the CSR plane at `0x9000_0000`:
    `milan_soc.py:99`.

A targeted search of the 17 current D0 pages for the statements behind each recorded finding found
one repetition, F1:

- persistence absent;
- blank-flash responder;
- `S50milan`;
- `l2_cache_size=8192`;
- `--xlen 64`;
- quad read;
- live CBS or classifier;
- q3 gPTP;
- aggregate runner;
- complete-packet FIFO;
- the AX7101 shape of 8;
- bare-metal default.

### (5) Gates at the head

Run concurrently from the review clone with the pinned Markdown renderer in a scratch venv
(`run_gates2.sh`, `receipts/gates/`, `receipts/gates_summary.txt`). 15/15 rc 0:

- `docs_inventory.py --check` and `--selftest` (29 controls);
- `docs_check.py`;
- `check_doc_style.py`;
- `check_em_dash.py --base 1e80128f...`;
- `check_doc_paths.py`;
- `gen_toc.py --verify-anchors` and `--check`;
- `check_baremetal_only.py --check` (0 findings, 1423 files) and `--selftest` (867 arms);
- `ci_gate_workflows.py --check`;
- `ci_events.py --check` (2207 items) and `--selftest` (5270 arms);
- `check_archive.py`;
- `check_feature_status.py`.

The five YAML-dependent gates first ran under the venv, which has no PyYAML, and under `-I`, which
drops the script directory from the path. Those were environment failures. They were rerun with the
system interpreter, rc 0. The `ci/image/command-table.json:13701` pin `72f60bd7...e72a` equals the
sha256 of the committed script (`receipts/inventory_sha.txt`).

### (6) The author's published evidence

- `review-evidence/797d0-r1` at `8e15dcfa`, fetched sparsely without its `reviews/` directory: 200 of
  200 `author-r2/` files match `MANIFEST.json` `published_sha256`, and no file is unlisted.
- The commit itself is not GPG-signed: GitHub verification reports "unsigned". The integrity claim
  rests on the hash manifest.
- The head receipts are `head-3e6d92c1/a/summary.tsv` (60 rows) and `b/summary.tsv` (36 rows), all
  rc 0, at `3e6d92c1` with a clean tree. They match the PR's "96 of 96".
- This is source-head evidence from the author. It is not a manager bank, and none is inferred.

### (7) RTL scope

- The delta touches no `hdl/`, `sw/`, `configs/` or gitlink path. It changes five files:
  `docs.yml`, `command-table.json`, `DOCUMENTATION_AUDIT.md`, `docs_inventory.json` and
  `docs_inventory.py`.
- Every RTL line the new RTL-attributed findings cite was opened at this head:
  - `milan_datapath.sv:477,487,654-664,6678-6679,8552-8558`;
  - `milan_csr.sv:201,2000-2008`;
  - `ethernet_packet_pkg.sv:218-222`;
  - `KL_pp_shadow.sv:1121-1124,1225-1232`;
  - the framer and parser lines in (3);
  - the processor's restore deadlines.
- The two RTL-attributed prior findings (R742-1 F1, F3) are resolved.

### (8) Restore

- After the probes, the review clone is at `3e6d92c1`, tree `6d5ae1c3`.
- The worktree and index equal HEAD, and there are no untracked or ignored leftovers (the
  `__pycache__` created by one probe was removed).
- The gitlinks are unchanged: `protocol-processor` `f65c8ff7`, `gptp-processor` `f97c1803`,
  `third_party/verilog-axis` `48ff7a7e`, `third_party/tsn-c-stack` `70936b77`.
- Receipt: `receipts/restore_verify.txt`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | round-2 assignment against `scripts/docs_inventory.json` D0-024..062 (21 source-checked), `docs/DOCUMENTATION_AUDIT.md:23,126,454-516`, `REQUIREMENTS.md:25-31`, 10 sentences on current pages, all six named prior findings | R741-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| RTL | CLEAN | `git diff --stat bd16b371..3e6d92c1` (no RTL path); cited RTL lines in section (7); `CLS_TCQ` reset decode; R742-1 F1/F3 resolved | R741-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| Robustness | CLEAN (S3 optional) | `scripts/docs_inventory.py:214-232` (Git environment, listing), `:406-415` (`status_rule`), `:593-645` (`cells`, `current_with_findings`, `check`); probes q00-q10; parser coverage 210/62 | R741-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| Tests | CLEAN (S1 optional) | `scripts/docs_inventory.py:647-845` (`track`, `fixture`, `gate`, `control`, `selftest`, 29 controls) under 15 mutants (12 killed, 2 equivalent, 1 S1); round-1 mutants re-run; `--selftest` rc 0 | R741-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |
| Docs | UNCLEAN (F1) | `.github/ci-templates/docs.yml:422-432`, generator docstring `:27-43`, `:98-99`, generated page summary/rules/inventory/findings, PR body figures (62 findings, 176/13/21, 10/52, 96/96), `REQUIREMENTS.md:27` | R741-2 | 3e6d92c17bd1d2118e9bc3d8a0e1fae90a69e8ee |

[R741] PASS RTL - `hdl/milan/milan_datapath.sv:654-664,8552-8558`, `hdl/common/ethernet_packet_pkg.sv:218-222`, `hdl/common/csr/milan_csr.sv:2008`, `hdl/milan/KL_pp_shadow.sv:1123` - every RTL claim of the new findings checked against the RTL at this head; the delta has no RTL change.

[R741] PASS Robustness - `scripts/docs_inventory.py:406-415,593-645`; `receipts/probe_gate2.txt`, `receipts/parse_coverage.txt` - a planted finding on a current page, a rule-less generator, hand edits, an absent quote, a fixed statement and a hook environment were each handled as the status-rule contract requires.

[R741] PASS Tests - `scripts/docs_inventory.py:647-845`; `receipts/mutants2.txt` - the self-test drives `main(["--check"])` on Git fixtures and kills every status-rule, gate and listing mutant except one defence-in-depth parser mutant (S1, optional).

## Real limits

- This is a delta review. Round-1 code not touched by the delta keeps its R741-1 verdict, except where
  the delta changed its dependencies (`check()`, `status()`, `selftest()`, `listing()` and `main()`
  were all re-reviewed).
- 21 of the 39 new findings were source-checked. D0-037, D0-040, D0-042 to D0-047, D0-049 to D0-056,
  D0-058 and D0-059 were read for consistency only.
- The D0-050 to D0-055 descriptor measurements were not re-run.
- Clause-only content was not re-derived from licensed standards.
- 10 sentences on current pages were sampled. This is not a census of the remaining statements, and
  the lane's 823 "read" statements were not re-graded.
- No source bank, builder, Verilator, Yosys or hosted/act run was performed or is claimed.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The evidence commit is unsigned. Integrity rests on the hash manifest.

## Pending manager duties

- Decide F1's direction: does `REQUIREMENTS.md`'s "Mark II default" define a design placement, or
  contradict the build?
- Decide whether the 823 "read" statements, 140 of them on the current pages `BUILDING.md` and
  `SUBMODULES.md`, meet the round-2 sampling requirement (S2).
- Decide whether the 13:33 and 13:40 owner additions apply to D0 before merge. They add the
  "style-gated" and "mechanisms without a diagram" columns, and "a page is current only when that
  count is zero". They arrived after this head and would change the status rule.
- The current-dev merge candidate (builder and native banks), hosted exact-head contexts and act
  acceptance remain with the manager at the merge turn.

## Prior public findings on this PR

I read these only after the verdict, findings and ledger above were on disk. At retrieval PR #815
had:

- four review-start notes, including R742-2 at this head, which has no published report yet;
- zero submitted reviews and zero inline comments;
- two published rounds: R742-1 (issuecomment-6520356763) and my own R741-1 (issuecomment-6520804068),
  both NEGATIVE at `bd16b371`.

No other reviewer's round-2 report existed, and none was opened. Every finding of both published
rounds is judged in the table "Prior findings named in the brief" above: all are RESOLVED, and
R741-1 F2's class is RETAINED as F1 at `REQUIREMENTS.md:27`. R742-1 also carried non-finding notes:

- **Freshness limit.** A same-length edit, for example 50 MHz -> 99 MHz, passes the gate. The
  workflow comment (`docs.yml:422-432`) and the docstring (`:39-43`) now state that limit
  accurately. The round-1 R2 rewording is resolved.
- **The scope addition's ETH_GUARD and MAC_STATUS assertions** contradict the code. The author keeps
  this as open risk 2. It is a manager or maintainer decision outside D0's record-only scope, and it
  does not affect this verdict.

Neither note changes the verdict above.

R741-2 FINISHED
