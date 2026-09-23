[R248] NEGATIVE - exact head 28e350b99ac240a750326b762c6d029f0653362c

Round R248-1: cleared-context external review of issue #520 / PR #522.
Head `28e350b99ac240a750326b762c6d029f0653362c`, tree `d17c117db03128e444b7b44742fe82f10746cb28`,
base `483a133ed08867ea0d300d2b4a027b5b48a4282f`. I applied all five lenses independently.

The verdict is NEGATIVE because of one open MINOR (F1, Docs).
The code change itself is correct:
- A change to generated ROM bytes now invalidates the cache.
- Stale, foreign, old-schema and tampered entries are refused.
- The identity covers every data file Yosys reads for these tops.
- No gate was weakened.

The problem is documentation only. Two summaries of the cache key were not
updated. They still say that the pre-#520 inputs are enough for a skip.
Conformance, RTL, Robustness and Tests are clean at this head.

## Reconstruction

The context was loaded in this order:
- `AGENTS.md` sections 3 and 5-8, `CONTRIBUTING.md` sections 2, 3, 5 and 6, and `docs/README.md`.
- `REQUIREMENTS.md:217-224` (REQ-VER-02/04).
- The body of issue #520: its frozen acceptance criteria 1-5 and settled scope.
- The issue comments: the manager assignment and the lane's TAKEN/REVIEW READY notes.
- The manager's source-validation comments, and PR #522's body and manager comments.
- Interface authorities:
  - `syn/yosys/run.sh` (`generate_roms`, `cache_lookup`, `cache_store`, `run_tops`);
  - `syn/yosys/result_cache.py`;
  - the processor ROM consumers;
  - `docs/testing/CI_WORKFLOWS.md` (the #350 cache contract);
  - `scripts/ci_events.py` (`check_yosys_result_cache`).
- The six-file diff `483a133e..28e350b9` (one commit), then the public evidence at
  `34ba85c5:review-evidence/520-r1` (manager source and native banks, author measurements).
- Hosted exact-head runs 35768810385 (rtl-fast) and 35768811088 (rtl-full), inspected read-only.

The other reviewer's report was read only after this round's verdict and
ledger were written (see "Prior public review findings").

## Findings

### F1 MINOR - lenses: Docs

- **Where:** `syn/yosys/README.md:27`, the hand-owned Contents description.
  Also `.github/workflows/rtl.yml:538-540`, the comment on the Yosys shard cache step.
- **Title:** two cache-key summaries still state the pre-#520 key as sufficient for a skip.
- **Authority and evidence:**
  - `AGENTS.md` section 6, Docs lens: changed contracts are reflected in the authoritative docs.
  - The #520 settled scope says to update the authoritative docs.
  - README line 27 says `--cache DIR` "skips a top whose staged sv2v output, program, Yosys binary and sv2v version match a verified PASS entry (#350)".
  - `rtl.yml:538-540` says the same: "a top whose staged sv2v output, Yosys program, Yosys binary and sv2v version match a verified PASS entry is skipped".
  - Both lines are unchanged from the base. At this head both are false.
  - My real gate probe `receipts/real-probe-gptp-probe-KL_gptp_shadow-gptp.json`, step `D-changed-cached`, shows this. The entries match on those inputs and differ only in `rom_sha256`. The result is not a skip: 206,661 cells live, against 206,752 cached.
  - The same page's section body (`README.md:98-125`) and `run.sh --help` (`run.sh:43-46`) were updated. They contradict line 27.
  - `scripts/gen_toc.py:11` says a human owns the Contents description. No gate checks it for drift. `gen_toc.py --check` and `docs_check.py` both pass at this head.
- **Impact:** a reader of the Contents entry or the workflow step would think that
  generated ROM bytes are not part of the key. That is exactly the stale-evidence
  misunderstanding #520 removes. It could also misdirect a later review of cache hits.
- **Required outcome:**
  - Neither location may present the pre-#520 input list as sufficient for a skip.
  - Each must either name the generated ROM bundle or stop listing the inputs and point to the key definition.
  - Executor note: the page's Contents block uses a U+2014 separator for the whole page. In a disposable copy, a description-only edit passes `gen_toc.py --check`. But the edited line adds a U+2014 separator, which the em-dash rule refuses (`CONTRIBUTING.md:506-509`). Switching one line's separator to `--` fails `gen_toc.py --check`. So the documented route is the page-wide separator switch (`CONTRIBUTING.md:550-559`).
- **Verification:**
  - A reviewer re-reads both locations at the corrected head.
  - `python3 scripts/gen_toc.py --check`, `python3 scripts/docs_check.py` and `python3 scripts/check_em_dash.py --base <merge-base>` pass.
  - If `rtl.yml` is touched: `scripts/ci_events.py` contract checks and the hosted/act rtl-full gates on the new head.

### Suggestions (optional, do not affect coverage)

**SG1 SUGGESTION - Tests - `syn/yosys/rom_cache_selftest.py:171,195,199,228` and `syn/yosys/cache_selftest.py:132-138` - failure diagnostics.**
- Four asserts carry no message. Most others carry a raw receipt dump rather than the contract they check (`docs/development/CODE_QUALITY.md` Rule 6 checklist).
- The hosted step runs without `--logs`, so the fixtures are deleted. A message-less failure then prints only `SELFTEST FAIL: ROM integration control: `.
- A non-`AssertionError` escapes `run_arms`. In mutant S4 this was a `KeyError` at `rom_cache_selftest.py:125`. The escape drops the original five arms' problem list and the summary line. The exit status is still 1, so the gate fails closed.
- The repository already uses many message-less asserts in Python tests, so this is not a MINOR.

**SG2 SUGGESTION - Tests - `syn/yosys/result_cache.py:52` - no control pins the schema advance.**
- Leaving `SCHEMA` at schema 1 (mutant R9) passes both self-tests.
- This is behaviour-equivalent. Old records have no `rom_sha256`, so they fail the field check, and old keys differ. The settled "advance the schema" decision is implemented but not tested.

**SG3 SUGGESTION - Docs - `.github/workflows/rtl-fast.yml:219-222`.**
- The step comment lists only the original four cache arms.
- The step now also runs the ROM bank, which the hosted log confirms. The comment is incomplete but not false.

## Evidence by lens

[R248] PASS Conformance - `syn/yosys/result_cache.py:52-125`, `syn/yosys/run.sh:503-514,428-452`, `receipts/real-probe-*.json`, `receipts/head-rom-bank-summary.txt`, `receipts/inventory-program-parity.txt`, `receipts/hosted-extract.txt` - checked frozen criteria 1-4 and the settled scope against code and execution.
- **Bundle framing.** The bundle binds exactly `gptp_ucode.hex`, `ltn_rom.hex` and `ucode.hex`, in fixed lexical order. Each entry is the name, then NUL, then an 8-byte big-endian length, then the bytes.
  - I implemented this framing independently from the README prose, over the real generated images.
  - It equals every recorded `rom_sha256` in all three probes. The baseline is `15ec9c1dd64e...`, the same value the lane and the internal review report.
- **Order in run.sh.** The digest is taken after the three generators succeed and after the existing `[ -s ]` loop, and before any lookup. One `ROM_SHA256` feeds both lookup and store, for every selected top, in both modes and both tiers.
- **Schema.** The schema is advanced to 2 with no migration code.
- **Criterion 1.** Cold then warm gives identical cells with a verified hit:
  - `KL_gptp_shadow`: 206,752 / 206,752 (hit);
  - `KL_pp_shadow`: 1,141,365 / 1,141,365 (hit), in both PP probes.
- **Criterion 2.** A generator-only change was made in a disposable copy. RTL, sv2v inputs, program and tools were unchanged; the records differ only in `cells` and `rom_sha256`. In each case the change misses and runs live, and the live count equals an uncached run of the same input:
  - gPTP: 206,661;
  - PP ACMP `ltn_rom.hex`: 1,141,463;
  - PP AECP `ucode.hex`: 1,141,333 (baseline 1,141,365).
- **Base comparison.** The same steps on the base cache code (`run.sh` and `result_cache.py` restored to `483a133e`) serve a stale hit:
  - gPTP: 206,752 reported for the changed ROM;
  - PP ACMP: 1,141,365 reported for the changed ROM, against a true live 1,141,463.
  So the probe is sensitive to the defect.

  Real-gate probe results. Every run exits 0. "hit" means the result came from the cache.

  | step | gPTP head | gPTP base | ACMP head | ACMP base | AECP head |
  |---|---|---|---|---|---|
  | A cold | 206,752 live | 206,752 live | 1,141,365 live | 1,141,365 live | 1,141,365 live |
  | B warm | 206,752 hit | 206,752 hit | 1,141,365 hit | 1,141,365 hit | 1,141,365 hit |
  | D changed ROM, same cache | 206,661 live | **206,752 stale hit** | 1,141,463 live | **1,141,365 stale hit** | 1,141,333 live |
  | E changed ROM, uncached | 206,661 live | - | 1,141,463 live | - | 1,141,333 live |
  | F changed ROM, warm | 206,661 hit | - | 1,141,463 hit | - | 1,141,333 hit |
  | G changed ROM, read-only seed only | 206,661 live | - | 1,141,463 live | - | 1,141,333 live |
  | H original ROM again | 206,752 hit | - | 1,141,365 hit | - | 1,141,365 hit |
  | I genuine foreign entry at current key | refused, live | - | refused, live | - | refused, live |
  | J genuine schema-1 seed | 206,752 live | - | 1,141,365 live | - | - |
  | K genuine schema-1 entry at current key | refused, live | - | refused, live | - | - |

- **Criteria 3-4.** Covered by the bank (54 real driver runs at head) and by my probes, detailed under Robustness.
- **Unchanged scope.** The inventory is 54 tops and byte-identical to the base. The `--emit` records for `KL_pp_shadow`, `milan_datapath`, `KL_gptp_shadow` and `cdc_pulse` are identical, and so are the program templates.
- **Criterion 5.** Only the source portion is judged here; its merge-time portions remain pending.

[R248] PASS RTL - diff `483a133e..28e350b9` (six tooling/doc files, no HDL or gitlink change), `receipts/integrity-before.txt`, `protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv:418`, `protocol-processor/hdl/aecp/KL_aecp_ucpu.sv:121`, `gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv:107`, `hdl/milan/KL_pp_shadow.sv:199,208`, `hdl/milan/milan_datapath.sv:76,321,329`, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:78` - checked that the bound names are exactly what the synthesised RTL reads.
- **ROM reads in the RTL.** A repository-wide search of `.sv/.v/.svh/.vh` finds exactly three `$readmemh` sites. Their default file parameters are the three bundle names, and every wrapper in the inventory passes those defaults through.
  - No other `$readmem` data file reaches any top.
  - Yosys runs with its working directory set to the gate's private `$TMP` (`run.sh:590-594`), so the relative names resolve to the digested files.
- **What does not change.** Program strings, stat extraction, result serialization, structural checks and the processor gitlinks are unchanged.
- **Out of scope.** Clock, reset, CDC, FSM and width concerns have no changed artifact in this issue.

[R248] PASS Robustness - `syn/yosys/result_cache.py:95-116,154-192`, `syn/yosys/run.sh:494-514`, `receipts/cli-edge-probe.txt`, `receipts/real-probe-*.json` (steps G and I for all three images; J and K for gPTP and ACMP), `receipts/head-rom-bank-summary.txt`, `receipts/hosted-extract.txt` - checked malformed, stale, foreign and old inputs and ordering.
- **Generation refusals.** A failed generator, an empty image or a wrong-name image exits 2 with its original message. This holds with and without a cache, before any lookup or store, for all three images.
- **Digest arguments.** A directory in place of an image, or an absent directory, is refused with exit 2. `--rom-sha256` must be 64 lowercase hex characters: empty, uppercase or absent is exit 2.
- **What the digest ignores and includes.** Changing mtime or directory path keeps the digest. A symlinked image digests its target bytes, which is consistent with what Yosys reads. A change of only the trailing newline moves the digest.
- **Genuine foreign entry.** The real changed-ROM entry was planted at the original key (step I). It was refused with "recorded rom_sha256 differs" and ran live.
- **Genuine schema-1 entries.** These were produced by the pre-fix code.
  - Used as a read-only seed, they miss (step J).
  - Planted at the current key, they are refused with "schema ... is not ...2" and run live (step K).
  - Hosted exact-head shards restored the pre-fix dev cache and recorded zero hits and zero refusals across 54 live PASS tops.
- **Read-only seeds.** Seed bytes were unchanged after every seed run.

[R248] PASS Tests - `syn/yosys/result_cache.py:386-463`, `syn/yosys/rom_cache_selftest.py:157-253`, `syn/yosys/cache_selftest.py:85-138`, `receipts/head-result-cache-selftest.txt`, `receipts/head-cache-selftest.txt`, `receipts/mutation-summary.txt`, `receipts/mutation-results.json`, `receipts/hosted-extract.txt` - checked that each new control can fail for the defect it claims to detect.
- **Runs at exact head.** Both named self-tests pass: unit in 0.05 s, real-gate bank in 53 s, with 54 ROM-bank runs plus the five original arms. The hosted rtl-fast job printed `ROM cache controls: OK` at this head.
- **Mutation campaign.** 18 mutants were run on disposable copies. 17 are killed. The unit test kills the 10 `result_cache.py` mutants. The real-driver bank kills 7 `run.sh` mutants that the unit test cannot see:
  - a constant digest;
  - a generator-source key;
  - seed-only runs without a digest;
  - store omitting the digest;
  - store recording another digest;
  - digesting before the nonempty loop;
  - dropping the nonempty loop.
  The one survivor (R9) is behaviour-equivalent (SG2).
- **Test independence.** The unit oracle for the framing is written independently of the implementation.
- **What the bank does not show.** It uses ROM-independent tops, so it proves binding, not cell effects. That split is documented (`README.md:172`). My three real ROM-dependent probes cover the cell effects.

Docs is UNCLEAN at this head, because of F1.
- The artifacts checked were `syn/yosys/README.md:27,90-172`, `docs/testing/CI_WORKFLOWS.md:221-257`, `.github/workflows/rtl.yml:538-547`, `.github/workflows/rtl-fast.yml:219-224` and `receipts/static-focused.txt`.
- The section bodies of the README and the CI policy correctly describe the names, the framing, the guard ordering, the conservative scope, both modes, both tiers and the schema migration.
- `check_em_dash.py --base 483a133e` (0 findings over 49 added lines), `docs_check.py`, `gen_toc.py --check`, `check_py_idiom.py` and `check_sh_idiom.py` pass.

## Prior public review findings

R247-1 (`[R247] POSITIVE`, PR comment 5782558633) recorded no findings or suggestions.
- There is nothing to resolve or to retain.
- R247-1 disposed of the triage items (the stale AECP cells, wrong-name refusal, and the cross-checkout miss left with #270). I agree with those dispositions from my own execution.
- F1 is new at this head and is not a disposition of any earlier finding. R247-1's Docs evidence cited `README.md:104` and `CI_WORKFLOWS.md:245`. Neither of those is the Contents description at line 27 or the workflow comment.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `result_cache.py:52-125`, `run.sh:428-514`, issue #520 criteria 1-4, real probes (3 images, head and base), inventory/program parity | R248-1 | `28e350b99ac240a750326b762c6d029f0653362c` |
| RTL | CLEAN | six-file diff, three `$readmemh` consumers and wrapper defaults, `run.sh:590-594`, gitlink integrity | R248-1 | `28e350b99ac240a750326b762c6d029f0653362c` |
| Robustness | CLEAN | `result_cache.py:95-192`, `run.sh:494-514`, CLI edge probe, probe steps G/I/J/K, 54-run bank, hosted zero-hit shards | R248-1 | `28e350b99ac240a750326b762c6d029f0653362c` |
| Tests | CLEAN | `result_cache.py:386-463`, `rom_cache_selftest.py`, `cache_selftest.py`, 18-mutant campaign, hosted rtl-fast log | R248-1 | `28e350b99ac240a750326b762c6d029f0653362c` |
| Docs | UNCLEAN (F1 open) | `syn/yosys/README.md:27,90-172`, `CI_WORKFLOWS.md:221-257`, `rtl.yml:538-547`, `rtl-fast.yml:219-224`, docs/TOC/em-dash/idiom gates | R248-1 | `28e350b99ac240a750326b762c6d029f0653362c` |

A later commit that fixes F1 un-covers Docs. It also un-covers every other lens
whose artifacts it touches, so those lenses need to be covered again at the new
head.

## Real limits

- **Probes.** The real cell-effect probes cover `KL_gptp_shadow` (gPTP image) and `KL_pp_shadow` (both PP images), in full mode on one host with Yosys 0.66 and sv2v v0.0.13.
  - `milan_datapath` also reads all three images. It was not probed here; the common loop and the conservative key give it the same identity.
  - I did not run the elaborate mode on ROM-dependent tops.
- **No banks rerun.** I ran no full parent/PP/gPTP/Yosys/builder bank, act or Docker.
  - The manager's full source banks, the act replica and the hosted results are accepted as public evidence, not re-executed.
  - Scoped Verilator was not needed for this tooling-only diff and was not used.
- **Out of scope for #520.** These are not findings against this PR. Each may merit its own issue:
  - Yosys's installed techlib data directory is not part of the key (the #350 design keys the binary and the version string).
  - A record/`stat.json` pair forged consistently inside a writable tier is trusted by design (the #270 scoping boundary).
  - `syn/yosys/README.md:93-94,159-160` still quote 48 tops against the 54-top inventory. Those lines are untouched here.
- **No hardware evidence.** Physical calibration was NOT RUN. The field skips and the skipped nightly physical job are not hardware evidence.

## Pending manager duties

- Resolve F1, then obtain an external re-review at the corrected head.
- Run exact-head hosted and act evidence for any new head.
- Validate the final current-dev candidate at the merge turn.
- Merge only with authorization.
- Run canonical containment, then Closed/Done.
- Keep the shared Yosys seed disabled until this lane clears.

## Integrity

- The review clone was never modified. All probes ran in disposable copies under `scratch/`.
- `receipts/integrity-before.txt` and `receipts/integrity-after.txt` record the checks:
  - HEAD and tree;
  - 856 index records equal to the HEAD tree at stage 0;
  - 852 tracked files re-hashed to their blob ids with their executable bits;
  - no assume-unchanged or skip-worktree flags and no untracked files;
  - `third_party/verilog-axis`, `protocol-processor` and `gptp-processor` gitlinks equal to their clean checkout heads.
- This round made no GitHub write.

R248-1 FINISHED
