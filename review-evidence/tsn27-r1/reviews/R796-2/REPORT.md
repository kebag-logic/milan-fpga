[R796] POSITIVE - exact head c687810b74b53b69c1fbdff7bfd0ec9da94eaa78

External independent review R796-2 of kebag-logic/tsn-c-stack PR #29 (issue #27). This is a delta round against R796-1. Tree 20c8786758807efef217f6db8dc97158a5fa8a95, one commit on base 70936b77dc41981e192438388cd0aced69954f18. Review start: https://github.com/kebag-logic/tsn-c-stack/pull/29#issuecomment-6719849741.

**Summary.** The source has not changed since R796-1. The head, tree and all 98 tracked blobs are identical. The only change is one paragraph of the PR body. That edit resolves F1, my only open finding: the paragraph now names the CI toolchain and gives its figures from the hosted maps, and it names the host compiler behind the figures it gave before. I re-derived every number in the edited paragraph from the hosted `rv32_smoke.map` files of the base and head runs, and all of them match. With no open MINOR, MAJOR or BLOCKER finding, all five lenses are clean and the verdict is POSITIVE.

## Reconstruction (order followed)

1. `CONTRIBUTING.md` (there is no `AGENTS.md`) and the docs set as in R796-1. Nothing in them changed at this head.
2. Issue #27: it still has only its body and two comments (TAKEN, REVIEW READY). There is no new scope decision.
3. `git diff 70936b77..c687810b`: same head and tree as R796-1, with 8 files, +76/-7. There is no source delta (`receipts/clone-integrity.txt`; the PR `headRefOid` is still c687810b).
4. The PR body history (GitHub `userContentEdits`) shows exactly one edit after R796-1, at 2026-11-08T09:31:20Z. That is before this round's start comment (09:32:14Z). The edit replaces one line, the paragraph starting "This repository's own RV32 smoke images", and leaves every other line of the body unchanged (`receipts/pr-body-edit-diff.txt`).
5. Hosted evidence: I downloaded the `rv32-evidence` artifacts again, read-only, for base run 38295188787 (push at 70936b77) and head runs 42465293588 (pull_request) and 42465283076 (push). All three runs completed with conclusion success and point at the stated shas. The milan-fpga evidence commit `d40afd2b…/review-evidence/tsn27-r1` is pinned by sha and still resolves. Its blobs were verified blob by blob in R796-1 and cannot change under that sha.
6. Prior public review findings on PR #29: see the section "Prior public findings" below. I read them only after writing the verdict and ledger.

## F1 (R796-1, MINOR, Docs): RESOLVED

The R796-1 verification step was to compare the edited body with the `rv32_smoke.map` output sections of the base and head hosted runs and with the host-toolchain size receipts. That comparison was done claim by claim:

| Claim in the edited body | Check | Result |
|---|---|---|
| Toolchain is the workflow's Ubuntu 24.04 `gcc-riscv64-unknown-elf` | `.github/workflows/quality.yml:42,51`: `runs-on: ubuntu-24.04` and apt `gcc-riscv64-unknown-elf`. The hosted job logs for the base and head runs both install `gcc-riscv64-unknown-elf (13.2.0-11ubuntu1+12)` and `binutils-riscv64-unknown-elf (2.42-1ubuntu1+6)` on image ubuntu-24.04 | Matches. Base and head used the same compiler package, so the comparison is like for like (`receipts/hosted-toolchain.txt`) |
| Figures come "from the hosted `rv32_smoke.map` at the base and at this head" | Map output sections parsed by `scripts/map_sections.py` | Matches (`receipts/hosted-map-sections.txt`) |
| Debug `.text`+`.rodata`: 47072 to 46992 B (-80) | base .text 45024 + .rodata 2048 = 47072; head 44944 + 2048 = 46992 (pull_request and push runs identical) | Exact |
| Release `-O3`: 36649 to 37577 B (+928, all in `.text`) | base .text 34688 + .rodata 1961 = 36649; head 35616 + 1961 = 37577; .rodata unchanged | Exact |
| Host riscv64-elf-gcc 16.2.0 gives 47508 to 47428 B and 36857 to 37653 B (+796) | R796-1 `receipts/baremetal-local-sizes*.txt` (`size` text column) and `receipts/tools.txt` (riscv64-elf-gcc 16.2.0). The host compiler identity was confirmed again this round | Exact; 37653 - 36857 = 796 |
| The host and CI figures measure the same thing | In the hosted map the only allocated read-only output sections are `.text` and `.rodata` (`.rela.dyn` is 0). So the `size` text column equals `.text`+`.rodata`. Also, the `size` bss of 65552 equals `.bss` 0x8 + `.stack` 0x10008 | Consistent |
| The smoke images never call `__lshrdi3` | No map line mentions `__lshrdi3` in Debug or Release, at base or head | Matches |

The required outcome was to name the toolchain behind 47508/47428/36857/37653 and to add the CI figures, both from the hosted maps. Both are met, with a PR-body edit only and no new head. The trade-off verdict in R796-1 stands: the +928 B cost in the `-O3` test image against the roughly -420 B gain in the parent's `-Os` split image is accepted.

## Findings at this head

No open MINOR, MAJOR or BLOCKER finding. No RESIDUE.

### S3 - SUGGESTION - Docs
- **Where:** PR #29 body, paragraph "This repository's own RV32 smoke images…", in the parenthesis "(Ubuntu 24.04 `gcc-riscv64-unknown-elf`, …)".
- **Evidence:** The workflow pins the runner image (ubuntu-24.04) but installs the distro package without a version (`.github/workflows/quality.yml:51`). Both measured runs got `13.2.0-11ubuntu1+12` (`receipts/hosted-toolchain.txt`). A later runner image could ship a different package, and the figures would then drift with "pinned" still in the text.
- **Optional outcome:** Write "Ubuntu 24.04 `gcc-riscv64-unknown-elf` 13.2.0-11ubuntu1+12". You may also move this paragraph out of the section headed "Effect on the parent's split image", because it describes this repository's own images. This does not block, and the figures are correct as written.

### S1, S2 (R796-1) - SUGGESTION - not taken this round, still optional
- **S1 (Tests, Robustness):** a `scripts/mutation_selftest.py` control for the unknown-arm ERROR path (`scripts/mutation.py:219-220`) and for the header-without-source build rule (`:221-224`).
- **S2 (Tests):** W1's message "and nothing past them" (`tests/test_acmp.cpp:2577`) would be more accurate as "and nothing outside them".

Neither blocks. Both are carried for the author.

**Comment-rule and privacy scan.** The reviewed delta changes no source, comment or document. R796-1's scan of every added line stays valid: no lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs. The edited body paragraph has no host locations, account details or private identifiers. "the host's riscv64-elf-gcc 16.2.0" names a public compiler release only. PR text may name lanes, so the body's `[A751]` prefix is allowed.

## Lens notes (artifact-specific)

- **Conformance:** No delta. The R796-1 verdict carries: ACMP-02 serialisation is bit-exact (`include/wire.h:38-47`, `docs/PORTING.md:388-391`). It depends on nothing the body edit touches.
- **RTL (RV32 target code generation; there is no HDL in this repository):** The edit's claims about this target were checked against the exact-head and base hosted maps and job logs. The figures, the toolchain identity and the absence of `__lshrdi3` all match. The parent split-image figures (107278 to 106854 B, 122106 to 121686 B) are unchanged in the body and still rest on the author's receipts, as in R796-1.
- **Robustness:** No delta, so the R796-1 verdict carries: `include/wire.h` shifts are all 32-bit by constants, and `scripts/mutation.py` turns an unknown arm into a per-plant ERROR.
- **Tests:** No delta, so the R796-1 verdict carries: W1 kills 13/13 planted defects, and the hosted mutation results at this head are 390/390 CAUGHT. The body's "How to validate" section and its expected `{"CAUGHT": 390, "ESCAPED": 0, "ERROR": 0}` are unchanged.
- **Docs:** F1 is resolved, as shown above. The repository docs are unchanged and their R796-1 verdict carries. The only change to the PR body is the F1 paragraph.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | no delta; `include/wire.h:38-47`, `docs/PORTING.md:388-391`, ACMP-02 (R796-1 evidence) | R796-1, carried in R796-2 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| RTL (RV32 target code generation) | CLEAN | hosted `rv32_smoke.map` Debug/Release at base 38295188787 and head 42465293588/42465283076 (`receipts/hosted-map-sections.txt`); hosted bare-metal job toolchain (`receipts/hosted-toolchain.txt`) | R796-2 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Robustness | CLEAN | no delta; `include/wire.h`, `scripts/mutation.py:36-37,141,219-225` (R796-1 evidence) | R796-1, carried in R796-2 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Tests | CLEAN | no delta; `tests/test_acmp.cpp:2561-2580`, `tests/mutations.json:5831-5862`, `tests/coverage.ratchet:4` (R796-1 evidence) | R796-1, carried in R796-2 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Docs | CLEAN (F1 resolved) | PR #29 body and its edit history (`receipts/pr-body-edit-diff.txt`); hosted maps; R796-1 host-toolchain size receipts | R796-2 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |

Clone state (`receipts/clone-integrity.txt`):
- HEAD and tree are exact.
- Worktree, index and ignored files are all clean.
- All 98 tracked blobs match their ids, with mode 100644.
- There are no gitlinks (the repository has no submodules).
- No probe wrote into the clone this round. Downloads and parsing used only the packet scratch directory.

## Real limits

- This round ran no build, test or mutation campaign, because no source changed. The Conformance, Robustness and Tests verdicts carry from R796-1 by the delta rule.
- The host-toolchain figures rest on my R796-1 local build receipts and were not rebuilt. The CI figures were re-derived this round from the hosted artifacts, which I inspected but did not produce.
- The parent split image was not rebuilt (out of scope). Its figures rest on the author's receipts, as in R796-1.
- The author's frozen evidence (`HANDOFF.md` at milan-fpga d40afd2b) still gives the host-toolchain figures only. It is pinned by sha and cannot be edited, and the PR body is the record that carries both sets. No action is required.
- No manager source bank was run at this head, and none is claimed. Physical calibration was NOT RUN. Skipped field contexts are not hardware proof. The pinned Verilator was not used, because there is no HDL in scope.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn. Source base 70936b77; live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c. Link those receipts on the PR. Hosted/act acceptance is the manager's.
- Merge order with PR #28 (issue #26), as in R796-1. They conflict on the `docs/VERIFICATION.md:24` plant count (combined 408 core plants), on the `tests/mutations.json` insertion point before the entity plants, on `tests/coverage.ratchet`, and on the `docs/TESTS.md`/`docs/TRACEABILITY.md` anchors. Recheck that W1 is still the only killer of both wire plants on the combined candidate.
- Parent follow-up: move `third_party/tsn-c-stack` to the merged commit and drop the `__lshrdi3` hot-list entries (`plat/ctrl_split.ld`, `plat/ctrl_split_hot.txt`) in the same commit.
- Optional for the author: S1, S2 and S3.

## Prior public findings (read after the verdict and ledger above were written)

PR #29 has no reviews and no inline comments. Its public review reports are my own R796-1 (NEGATIVE, F1 MINOR, plus S1 and S2) and R795-1 (POSITIVE, no BLOCKER, MAJOR, MINOR or RESIDUE, three SUGGESTIONs). Here is how each stands at this head:

| Finding | Severity | State at c687810b | Reason |
|---|---|---|---|
| R796-1 F1 | MINOR | RESOLVED | PR-body edit verified above |
| R796-1 S1 | SUGGESTION | RETAINED (optional) | No source change; same as R795-1-S1 |
| R796-1 S2 | SUGGESTION | RETAINED (optional) | No source change |
| R795-1-S1 | SUGGESTION | RETAINED (optional) | Same as R796-1 S1; `scripts/mutation_selftest.py` is unchanged |
| R795-1-S2 | SUGGESTION | RETAINED (optional), concurred | `scripts/mutation.py:222-224` applies the fallback whenever `src/<module>.c` is missing, not only for `.h` targets. The `:221` comment and `docs/VERIFICATION.md:195` describe headers only. It fails safe (ESCAPED fails the gate), and no such plant exists today |
| R795-1-S3 | SUGGESTION | RETAINED (optional) | The body still says "defined, 7 call sites" for the 1x1 image without a call-site receipt. This figure is context, not acceptance, and R796-1 recorded the same limit |

None of these changes the verdict.

R796-2 FINISHED
