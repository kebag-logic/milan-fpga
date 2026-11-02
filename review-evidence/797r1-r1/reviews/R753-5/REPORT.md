[R753] NEGATIVE - exact head ef7dc9850827e0eadae5ae098d5db3dc91d29b3d

Round R753-5 is the internal cleared-context review of kebag-logic/milan-fpga PR #825 (#797 lane R1). It covers head `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` at tree `b0ae22190efb307eb997f3f8ff896c2657a88747`, and the round-5 delta `79fdea05..ef7dc985`, which has two commits:

- `f24695e4` changes the `srp_fresh_r` wording pair in `scripts/register_descriptions.json` and the four generated rows on `docs/reference/REGISTER_MAP.md`.
- `ef7dc985` changes `scripts/register_read_sweep.py`.

`git diff --stat 79fdea05..HEAD` lists only those three files. The delta touches no `hdl/`, `sw/`, `syn/`, `configs/` or gitlink path. The lane merged live dev `1f29f189` in an earlier round, and its one merge base is `1f29f189`. Live dev `503bc97c` is not merged.

**Why NEGATIVE:** one MINOR is open, F1 (Tests).

- **What holds:**
  - R753-4 F1 is resolved at its cause. The page now states every case that clears the word, and the generated page is fresh.
  - The sweep now drives the two separating states R753-4 F1 asked for.
  - The old wording, planted back, makes the sweep exit 1 with exactly the author's count.
  - Nothing else on the page changed.
- **What is open:** the sweep still cannot fail on one of the clause's four clearing cases, a provisioning `STRMW_CTRL` write that follows a poll answer. Deleting that clear from the RTL leaves the sweep at rc 0 with 0 disagreements. Adding one drive state catches it, and the exact head still passes with that state added.

My verdict, F1 and every probe were complete before I read any prior-round report (`receipts/order_of_work.txt`: the last probe rc was written at 12:27:31, and the R753-4 body was fetched at 12:34:17). Reading the prior reports changed neither the verdict nor F1.

## Findings

### F1 - MINOR - Tests - `scripts/register_read_sweep.py:17-18`, `:337`, `:345-350`, `:368` - the sweep cannot fail when the `STRMW_CTRL`-write clear of `srp_fresh_r` is missing

- **Where:**
  - **The clause:** it is printed at `docs/reference/REGISTER_MAP.md:3462`, `:3483`, `:3639` and `:3640`, and worded at `scripts/register_descriptions.json:4086-4087`. Its words include "after the last `STRM_SEL`/`STRMW_CTRL` write".
  - **The RTL:** the clause covers the provisioning clear at `hdl/common/csr/milan_csr.sv:3120-3128` (`srp_fresh_r <= 1'b0` at `:3128`, gated by `srp_prov_w` at `:3091-3093`).
  - **The sweep:** its eight SRP drive states are at `:345-350`, its loop at `:337`, and the record read at `:368`. Its docstring at `:17-18` says the drive covers "a provisioning write, in either order around the write".
- **Evidence:** `probe_r753_5.sh`, `probe_r753_5_mode8.sh`, `receipts/probe_summary.txt`. Every run used the scoped Verilator 5.050 (`receipts/verilator_version.txt`).

  | Probe | rc | Disagreements |
  |---|---:|---|
  | p0: exact head | 0 | 0 on both builds |
  | p2: steal clear `:3132` removed | 1 | 144 |
  | p3: write-answer clear `:3115` removed | 1 | 144 |
  | p5: `STRM_SEL` clear `:3119` removed | 1 | 96 |
  | **p4: `STRMW_CTRL` clear `:3128` removed** | **0** | **0 on both builds** |

  - **Why p4 passes:** none of the eight drive states answers a poll between the `STRM_SEL` write and the `STRMW_CTRL` write. States 2 and 3 issue the CTRL write straight after the selection. States 4 and 5 grant only from the write handshake on (`wr_ctrl_answered`, `:282-295`). So `srp_fresh_r` is already 0 when every provisioning write lands. `at_ans > at_selwr` (`:368`) never differs from the same test against the last `STRM_SEL` write alone. The "`STRMW_CTRL` write" half of the clause is computed, but no state ever separates it.
  - **One added state fixes it** (`probe_r753_5_mode8.sh`): a poll answered, then a provisioning `STRMW_CTRL` write whose write is not answered, then the reads.
    - The exact head stays at rc 0, with 0 disagreements over 54,007 reads on each build (`receipts/m8_p0_head.log`).
    - The p4 mutant exits 1 with 144 disagreements (`receipts/m8_p4_noprov.log`): shipping `STRMW_SRP` 24; 2x2 `STRMW_SID_LO` 24, `STRMW_SID_HI` 24 and `STRMW_SRP` 72.
    - At the head the state is reachable at block level: a provisioning write is posted and the engine has not yet granted it.
- **Authority:**
  - AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect."
  - The sweep's own contract at `:5-10`: "This sweep reads each clause as the page prints it."
  - Commit `f24695e4` names "a selection or STRMW_CTRL write" as one of the cases that clear the word, and the page prints it.
  - This is the same class R753-4 F1 named: no driven state separates the printed clause from a weaker one.
- **Impact:** the generator words `srp_fresh_r` from `condition_words`, a fixed string keyed by the flop name. A change that drops the provisioning clear at `:3128` would therefore leave `--check` fresh and the sweep green. The page would still say the word reads 0 after a provisioning write, while the block served the pre-write snapshot.
  - This is block level only. The shipping datapath ties the grant and the steal to 0 (`hdl/milan/milan_datapath.sv:8720`, `:3010`). The page is true at this head.
- **Not the same claim as R753-4's "harmless" note:** that note judged the page wording, which is broader than the RTL's provisioning-only clear. I agree with it. At non-provisioning selections the harness counts every `0x810` write as a clear while the RTL does not, and the m8 run at the head still gives 0 disagreements, because those selections never read `srp_fresh_r`. F1 is about whether the sweep can detect the clear, not about the wording.
- **Why MINOR:** it is a test-adequacy gap in a claim the PR offers as evidence. It is not wording only, and nothing at the head is false.
- **Required outcome:**
  - The committed sweep drives a state where a poll is answered after the selection and before a provisioning `STRMW_CTRL` write, with no answer after the write, and reads every swept word in it.
  - The docstring at `:17-18` states the drives that are actually made.
  - One feasible change is in `probe_r753_5_mode8.sh`: bound 9, plus `if (srpmode == 8) { srp_ans = answer_srp(); wr(0x810, @aaf_ctrl@u); srpw = t->o_srp_ctx_we; }`.
- **Verification:**
  - The committed sweep gives rc 0 at the head, with 0 disagreements on both builds.
  - With the `:3128` clear removed (`probe_r753_5.sh` p4), the committed sweep exits 1.
  - p1, p2, p3 and p5 still exit 1.

### S1 - SUGGESTION - Docs, Robustness - `scripts/register_descriptions.json:4086-4087` (page rows `:3462`, `:3483`, `:3639-3640`) - "since" has no stated anchor

- **The ambiguity:** "with no other master using the table since" does not say since what.
  - **The natural parse is since that poll answer.** It matches the RTL, and the harness reads it that way: `srpsteal = at_steal > at_ans` at `:368`, with the comment at `:363-367` saying "since that answer".
  - **A reader who anchors it to "the last ... write" predicts the wrong value** after drive state 7: a steal and then a poll answer. There the RTL serves the word, and that reading predicts 0.
- **A same-cycle edge:** a grant and a steal in one cycle read 0, because the steal is last and beats the grant (`milan_csr.sv:3130-3132`). An exclusive "since" would say the word is served.
  - No build drives `i_srp_ctx_stolen` (`milan_datapath.sv:3010` ties it to 0).
  - The port comment at `:624-630` frames a steal as a beat the window did not win, so this state is outside the contract today.
- **Optional fix:** "... with no other master using the table at or since that answer". In the negation, "... or another master has used the table at or since its latest answer". Update the matching `CLAUSE` keys at `:91-96` and regenerate.

### Residue

None new. The added lines of the delta (`receipts/delta_79fdea05_ef7dc985.diff`) contain no non-ASCII character. They also carry no lane label, review round, reviewer ID or comment ID. The new source comments state behaviour and cite `#797`.

## Focus results

- **(1) The pair states every clearing case, and the page is fresh: holds.** The cases in `milan_csr.sv:3108-3133` map to the words as follows:

  | RTL | Effect | Words |
  |---|---|---|
  | Poll grant `:3116-3117` | Sets the word | "latest answer ... was a poll" |
  | Write-answer grant `:3113-3115` | Clears | "was a poll" fails |
  | `STRM_SEL` write `:3119` | Clears | "after the last `STRM_SEL`... write" |
  | Provisioning `STRMW_CTRL` write `:3120-3128` | Clears | ".../`STRMW_CTRL` write" (broader, and harmless, as above) |
  | Steal `:3132` | Clears, last in priority | "no other master using the table since" |
  | Reset `:3109` | Clears | "any other case" |

  - Same-cycle answer and write: the write wins in the RTL, the page's "after" is exclusive, and the harness compares strictly with `>`. All three agree.
  - The negation is the De Morgan form.
  - The page and the descriptions carry identical strings.
  - `gen_register_reference.py --check`: fresh, 203 registers (`receipts/gen_check.log`).
  - `--selftest`: 61/61 (`receipts/gen_selftest.log`).
- **(2) The new drive states and the harness comment: holds.** F1 is the separate gap above.
  - State 4 is a poll answered after the write and then the write answered. State 6 is a poll answered and then a stolen beat. States 5 and 7 are the variants.
  - The edge record at `:238-253` classifies a grant by the `o_srp_ctx_we` it sampled the cycle before. That matches `srp_cmd_was_wr_r` (`:3111`).
  - The harness comments at `:238-242`, `:345-350` and `:363-367` state the page's words.
  - `answer_srp` (`:274-277`) now tests the request registered on the previous edge, which is consistent with that record.
- **(3) The old wording planted back fails: holds.** In p1, all four rows reverted give rc 1 with 288 disagreements: 48 on shipping and 240 on 2x2. That equals the author's `plants/sweep_old_wording.summary.txt`.
- **(4) The probe states agree with the new rows: holds.** I did not rerun the probe script; this rests on the hash-checked receipt and on sweep drive states 4 and 6.
  - The author's rerun (`author-r5/receipts/probe/probe_marked_states.log`, rc 0) reports 25 states and 0 that disagree with the new rows.
  - The four marked states (A len=2 off=1, A len=3 off=0, A len=3 off=1, and B) read 0 with `new_clause=0`.
  - The receipt matches the published manifest by sha256.
  - The same two orderings are sweep drive states 4 and 6, and they agree at the head (p0).
- **(5) Nothing else on the page changed: holds.** The page diff is 4 lines removed and 4 added, in those four rows only. The descriptions diff is 2 lines removed and 2 added. `--check` is fresh.

## Prior findings at this head

| Prior item | Status at `ef7dc985` | Evidence |
|---|---|---|
| R753-4 F1 (the SRP-served clause omits the write-answer and steal clears) | Resolved at its cause | Focus (1)-(5) above. The F1 gap above is a different clear, and R753-4 did not raise it |
| R753-4 S1 (`register_sv.py` loop step), S2 (row with 0 hits), S3 (`STRM_SEL[9]` read-back reading), S4 (selftest arms) | Not taken, optional | `register_sv.py` and `register_selftest.py` are untouched by the delta |
| R754-4 S1 and S2 | Optional | No effect on coverage |
| R753-3 RES2 (`REGISTER_MAP.md`, "a CPU write in the same cycle clears it") | Retained, RESIDUE | The text is unchanged (`REGISTER_MAP.md:4503`) |
| R753-3 RES3 (`CSR_REGISTER_NOTES.md:974`) | Retained, RESIDUE | The file is untouched by the delta |
| R754-3 R1 (`CSR_REGISTER_NOTES.md:78`, "every RW word still stores") | Retained, RESIDUE | The file is untouched by the delta |

## Lens results

```text
[R753] PASS Conformance - REGISTER_MAP.md:3462,3483,3639,3640; register_descriptions.json:4086-4087 - each set/clear of srp_fresh_r (milan_csr.sv:3108-3133) and the read mux (:2543-2576) checked against the printed clause and its negation; sweep p0 rc 0 on both builds, p1 old wording rc 1 (288)
[R753] PASS RTL - hdl/common/csr/milan_csr.sv:3106-3133, :2543-2576, :606-633 (untouched by the delta) - the clause depends on the clear priority order (grant, then STRM_SEL, then provisioning, then steal last); mutants p2, p3 and p5 each change reads the sweep catches; port contract against the shipping ties (milan_datapath.sv:3010, :8720)
[R753] PASS Robustness - milan_csr.sv:3112-3132 vs page clause; register_read_sweep.py:282-295,391 - same-cycle grant and write (write wins, matches "after"), pending-write state 5, reset to 0, cleanup of a pending write between iterations; the same-cycle grant and steal is outside the port contract (S1, optional)
[R753] UNCLEAN Tests - register_read_sweep.py:17-18,337,345-350,368; receipts/p4_noprov.log, m8_*.log - F1: no drive state separates the STRMW_CTRL-write clear
[R753] PASS Docs - REGISTER_MAP.md rows above; register_descriptions.json:4086-4087; gen_check.log (fresh), gen_selftest.log (61/61); PR body Round 5 rows f24695e4 and ef7dc985 and the REVIEW READY, against the receipts - claims accurate, and none says every clear case is separated; no new residue
```

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `REGISTER_MAP.md:3462,3483,3639-3640`, `register_descriptions.json:4086-4087` vs `milan_csr.sv:3108-3133`, `:2543-2576`; p0, p1 | R753-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| RTL | CLEAN | `milan_csr.sv:3106-3133`, `:2543-2576`, `:606-633` (no `hdl/` change in the delta); p2, p3, p5 | R753-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| Robustness | CLEAN | same-cycle and pending-write orderings in `milan_csr.sv:3112-3132`; sweep `:282-295`, `:391` | R753-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| Tests | UNCLEAN (F1) | `register_read_sweep.py:17-18,86-102,238-295,337-392`; probes p0-p5, m8 | R753-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| Docs | CLEAN | page rows, descriptions pair, `gen_check.log`, `gen_selftest.log`, PR body Round 5, REVIEW READY | R753-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |

## Real limits

- **Block level only:** the sweep and my probes elaborate `milan_csr` alone. On the shipping datapath the SRP grant and the steal input are tied to 0, so neither F1 nor S1 has a shipping-SoC read. No real SRP engine is wired to this port in any build.
- **Author evidence:** I downloaded all 167 `author-r5/` files of the evidence tree at `5f1367c3`. Each matches its `published_sha256` in `review-evidence/797r1-r1/MANIFEST.json` (sha256 `534c52caeb035bb5...`; `receipts/evidence_manifest_check.txt`). All 69 published rc files read 0.
  - The commit `5f1367c3` itself reports `verified=false (unsigned)` through the commits API. Its integrity rests on the manifest hashes, not on a commit signature.
  - I did not rerun the 58-step docs-workflow table, the TOC and anchor checks, or the reviewer probe script; for those I rely on the hash-checked receipts.
- **Not run:** Verilator suites, Yosys, the behave suite, and any parent, PP, gPTP or builder bank. No manager source bank runs at this head, and none is claimed.
- **Hosted:** in the snapshot at this head (`receipts/hosted_checks_snapshot.txt`), `docs-check-no-git` and `wire-accountability` succeeded; `docs-gates-*`, `elaborate-gates-*` and the fail-fast jobs were in progress; `bdd-conformance` and `changes` were queued. A queued or skipped context is not execution.
- **Hardware:** physical calibration NOT RUN. No hardware or field evidence.
- **Tools and packages:**
  - All sweeps ran on the scoped Verilator 5.050, through a shim under `scratch/`. A first pass picked up an unpinned 5.052 by mistake; it gave the same results, and its logs are discarded and not published.
  - The pinned `wavedrom` 2.0.3.post3 was installed into a disposable environment under `scratch/`.
- **Clone state:** the clone is at the exact head. The index equals tree `b0ae2219`, the work tree equals the index, and nothing is untracked or ignored. The six gitlinks equal HEAD (`receipts/clone_state.txt`).
  - The generator runs had left `__pycache__` files in ignored paths. I removed them before taking that record.
  - Every probe ran on extracted copies under `scratch/`.

## Pending manager duties

- Hosted and act acceptance at the exact head. Exact-head `verilator-suites` and `yosys-portability` evidence, if this head is to be the merge candidate.
- The current-dev merge candidate against live dev `503bc97c`, with builder and native banks, and its receipts linked on the PR.
- Carry the residue checklist: R753-3 RES2 and RES3, and R754-3 R1.
- After the F1 fix, a re-review at the new head covering Tests. Conformance and Docs too, if the page or the descriptions change, for example by taking S1.

R753-5 FINISHED
