[R738] POSITIVE - exact head 0e03192c050812c5f7d249edd8893d1ede151a78

# R738-7: external independent delta review of PR #812 (issue #665, round 9)

Tree `c40023bf15545478c40f80ecf35cfc0a3f15f362`. Delta `b7fe6a777e..0e03192c05`: one commit, one file, `sw/firmware/ctrl/plat/README.md`, 3 insertions and 1 deletion.

No BLOCKER, MAJOR or MINOR is open. All five lenses are clean. One new RESIDUE and one new SUGGESTION are recorded, and neither asks for a change to this head's code or tests.

R738-6-F1 and R737-5-F1 are resolved at their cause. The sentence now matches every boot I have, and I booted the cases my last report left open: a true no-map image at this head, and both stand-in headers at 8x8.

## 1. Focus results

### Only that one file changed

**Holds.** `git diff --raw` shows one blob, `7bfdb032b8` to `73cb72c5e1`, mode unchanged. At top level only the `sw` tree differs. No gitlink moved, `git diff --check` is rc 0, and the commit is one line with no trailers (`receipts/delta.txt`).

### The sentence against the boots

Page lines `plat/README.md:102-104`, each claim against its receipt:

| Claim | Result | Evidence |
|---|---|---|
| The compiler would otherwise find the stand-ins, "with no diagnostic" | **True** | With the refusal removed in a copy and `generated/csr.h` deleted, the link is rc 0 and gives the same loadable hash as the stand-in image, `2c4448a3e21821e8` (`receipts/prior-r738-6/partial_boot_check.txt`) |
| An image on the stand-in `mem.h` hangs before its banner | **True at 1x1 and 8x8** | Table below |
| An image with no map hangs before its banner | **True at this head** | Table below. This is a true no-map link, with no `--flash-map` on either `ctrl_plat_image.py` command and the refusal removed in a copy |
| An image on the stand-in `csr.h` alone boots to ready and passes the split boot | **True at 1x1 and 8x8** | Table below |
| "This refusal is the only thing that stops it" | **True for every gate in the tree** | See below the table |

| Image | Shape | `lui 0xf0004` / `0x20000` in `ls_*` | Result | Receipt |
|---|---|---|---|---|
| Control | 1x1 | 0 / 0 | `PASS (0 finding(s))`, ready at 84.372 ms | `prior-r738-6/control.log` |
| Stand-in `mem.h` | 1x1 | 0 / 1 | `FAIL`: no ready line, transcript `''`, time limit exceeded | `prior-r738-6/stand-in-mem.log` |
| Stand-in `csr.h` | 1x1 | 3 / 0 | `PASS (0 finding(s))`, ready at 84.401 ms | `prior-r738-6/stand-in-csr.log` |
| No map | 1x1 | 3 / 1 | `FAIL`: no ready line, transcript `''`, time limit exceeded | `boots/nomap-1x1.log` |
| Control | 8x8 | 0 / 0 | `PASS (0 finding(s))`, ready at 184.622 ms, 9,231,088 CPU cycles | `boots/control-8x8.log` |
| Stand-in `mem.h` | 8x8 | 0 / 1 | `FAIL`: no ready line, transcript `''`, time limit exceeded | `boots/stand-in-mem-8x8.log` |
| Stand-in `csr.h` | 8x8 | 3 / 0 | `PASS (0 finding(s))`, ready at 184.677 ms, 9,233,841 CPU cycles | `boots/stand-in-csr-8x8.log` |

The 8x8 control reproduces the published `author-r8/receipts/runs/boot-8x8.log` to the cycle, so the environment is not what separates these rows. `receipts/image_identity.txt` confirms each image holds the constants its name implies.

The three 1x1 rows were measured at `b7fe6a77`, whose code is identical to this head's. Their logs still match my R738-6 manifest (`receipts/prior-r738-6/verify.txt`).

**Why "the only thing" holds.** I looked for anything else that would stop this image:

- The compile and the link's audits pass: rc 0, an ELF.
- Both boot exports read only `flash_port.json` (`split_soc.py:91,102`). Neither `boot_soc.py` nor `split_soc.py` reads a `generated/` header, so the map's missing or stand-in `csr.h` is invisible to them.
- The boot grade is `PASS`.
- `ctrl_plat_image.py` has three callers: `ctrl_split_boot/run.py`, `ctrl_image_selftest.py` and `ctrl_runs.py`. The last compiles with no map and makes no ELF. `nvm_split_target/run.py` does not use this image.

**Coverage of the page's cases.** All four are named: no map; a JSON-only map, which is on both stand-ins and so on the `mem.h` clause; a map lacking `mem.h`; and a map lacking `csr.h`.

### Comment rule

**Holds.** The added lines hold no lane label, round, reviewer ID or comment ID, and no em dash (`receipts/delta.txt`). The page is not a source comment in any case.

## 2. Findings

**R738-7-R1 | RESIDUE | Docs | PR body lines 20, 122, 404-408, 490 | The PR's status still names the previous head.**
- Evidence: line 20 reads "REVIEW READY at `b7fe6a77...`", line 122 checks out that commit, and the commit table ends at `b7fe6a777e`. The head is `0e03192c05`.
- Impact: a cold reader following line 122 reproduces a head whose page still holds the false sentence. No figure or verdict moves, since the gates at `b7fe6a77` cover identical code. This is the class of R737-4-R1.
- Exact fix: at line 122 check out `0e03192c050812c5f7d249edd8893d1ede151a78`. Add a row: "| `0e03192c05` | `plat/README.md` states which stand-in header hangs the boot and which boots to ready, as measured (R737-5-F1, R738-6-F1). No code changed. |". Keep lines 20 and 490 naming `b7fe6a77` as the head the gates ran on, and add "the only later commit changes one page".
- Verification: read the PR body.

**R738-7-S1 | SUGGESTION | Docs | `sw/firmware/ctrl/plat/README.md:104-105` | "This refusal is the only thing that stops it" reads wider alone than with its next line.**
- Evidence: the refusal stops the stand-in reached by a missing header. It does not stop the same image when a copy of the stand-in sits in the map, which is how my probes built it. Line 105 states that limit straight after, so the two lines together are accurate. That is why this is not a finding.
- Optional outcome: "so this refusal of a missing header is the only thing that stops it". R737-5-S4 is the same point at `ctrl_plat_image.py:53,58`, and the two could be absorbed in one pass.
- Verification: read the page.

## 3. Prior public findings at this head

Read after my own pass, with the limit stated in section 6.

| Finding | State at `0e03192c` |
|---|---|
| R738-6-F1, R737-5-F1 (MINOR) | **Resolved at the cause.** Each boot claim is split by header and holds against the measurement at both shapes. R737-5-F1's required outcome, that line 102 holds for every case line 101 names, is met. |
| R738-6-R1 (RESIDUE) | **Retained.** `ctrl_plat_image.py:16-17` and `ctrl_image_selftest.py:30` are untouched. Exact fix as recorded in R738-6. |
| R738-6-R2, R737-5-R1 (RESIDUE) | **Retained.** One defect, PR body line 422, "the first step of `main`", unchanged. |
| R738-6-S1, R737-5-S1 (SUGGESTION) | **Retained.** `is_file()` is not pinned by a lasting check. Same point. |
| R737-5-S2, R737-5-S4 (SUGGESTION) | **Retained.** The delta does not touch those lines. |
| R737-5-S3 (SUGGESTION) | **Retained.** The split boot cannot see the `csr.h` half of the map, and my 8x8 row repeats that. The page now tells the reader so. `run.py` is not in the delta. |
| R738-5-S1, R737-4-S2, R737-3-S4 (SUGGESTION); R738-5-RES1, R738-5-RES2, R738-4-RES1, R738-4-RES3, R737-2-R1, R738-3-RES1 (RESIDUE) | **Retained.** The delta does not touch their lines. |
| R738-4-S1, R738-4-S2, R737-3-S2, R737-3-S3, R737-1-S3, R737-1-S4, R737-2-S1, R737-2-S2, R737-2-S3, R738-3-S1 (SUGGESTION) | **Retained.** The delta does not touch their files. |
| R737-3-S1, R737-1-S2 (SUGGESTION) | **Retained in part**, as R738-5 left them. |
| R737-4-F1, R738-4-F1, R738-4-F2, R738-4-F3, R737-3-F1, R738-F1, R738-F2, and the prior items recorded as resolved | **Stay resolved.** Nothing they depend on changed. |

## 4. Per-lens results

```text
[R738] PASS Conformance - sw/firmware/ctrl/plat/README.md:101-105 at 0e03192c against ruling issuecomment-6692215350 - the statement the ruling named is now true for each case the page lists, read against seven boots at two shapes
[R738] PASS RTL - receipts/delta.txt - one .md blob changed, no HDL, no firmware C, 0 gitlinks; nothing in this lens's scope moved since R738-6
[R738] PASS Robustness - ctrl_plat_image.py:62-71,175 at 0e03192c, byte-identical to b7fe6a77 - code unchanged, R738-6 verdict stands; the wrong-header and no-map failure cases booted at this head
[R738] PASS Tests - receipts/selftest_head.log at 0e03192c - 40 checks, 7 of them plat, rc 0, same lines as R738-6's run apart from its timing footer; no test file in the delta; R738-6's mutants stand
[R738] PASS Docs - sw/firmware/ctrl/plat/README.md:101-105 against receipts/boots/*.log and receipts/prior-r738-6/*; receipts/docs_gates.txt - sentence true; five of six docs checks rc 0, the sixth replaced by a direct scan
```

## 5. Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling issuecomment-6692215350; `plat/README.md:101-105`; `receipts/boots/*.log`; `receipts/prior-r738-6/*` | R738-7 | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| RTL | CLEAN | `receipts/delta.txt`; R738-6's RTL coverage at ancestor `b7fe6a77`, nothing in scope touched since | R738-7 | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| Robustness | CLEAN | `ctrl_plat_image.py:62-71,175`; `split_soc.py:91,102`; `receipts/boots/*.log`; R738-6's probes at ancestor `b7fe6a77` | R738-7 | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| Tests | CLEAN | `receipts/selftest_head.log`, rc 0; R738-6's mutants at ancestor `b7fe6a77`, no test file changed since | R738-7 | `0e03192c050812c5f7d249edd8893d1ede151a78` |
| Docs | CLEAN | `plat/README.md:101-105`; `receipts/docs_gates.txt`; `receipts/image_identity.txt`; PR body lines 20, 122, 404-408, 422, 490 | R738-7 | `0e03192c050812c5f7d249edd8893d1ede151a78` |

## 6. Limits

- **Review order was not kept exactly.** My verdict draft failed to write, on a file-tool precondition, and the read of R737-5's published report went ahead in the same step. So I read that report before my verdict was on disk, not after. All boots, the identity check and the docs gates had already finished: the last boot ended at 20:14:33Z and the read was at 20:16:08Z. The self-test ran after the read, and R737-5 had no bearing on it. Section 3, and the wording of R738-7-S1's cross-reference, are the only text drawn from that report. Its suggested wording also contains "only this refusal stops it", and I checked that claim before reading it.
- **My first boot attempt did nothing.** The work directory did not exist, so all four copies failed in under a second. I fixed the script and reran. Those logs were replaced and no result comes from them.
- **Boot evidence is narrow.** One run per image, in simulation, with one interface. Two interfaces were not booted. It runs on the gate environment's RV32 SDK, not the pinned build. Verilator is the pinned 5.050, rev v5.050 (`receipts/env_identity.txt`).
- **"Only thing that stops it" rests on reading the callers and on these boots.** It covers the gates in this tree. I did not run the full banks.
- **Behaviour after ready is not characterised.** A stand-in `csr.h` image's flash write path was not exercised. That its command master sits on `timer0`'s addresses is address arithmetic from the map. The hang's cause is my reading of `ls_read`, not a trace.
- **`scripts/check_em_dash.py` could not judge here.** It exited 2 because the pinned Markdown renderer is not installed, and I did not install it. I scanned the added lines directly and found no em dash. Five other docs checks are rc 0, run on an unmodified copy of the head. They are not the full `docs.yml` replay.
- **Published evidence.** No author packet exists for this head, and I infer none: `f0fbd984` is round 8's packet at `b7fe6a77`. My integrity check of it in R738-6 stands, because it is the same commit, and that check covers integrity against its manifest only. I found no signature on the manifest, and the host reports the commit as not verified.
- **Hosted state is not accepted here.** I read 2 passing and 7 pending at exact head, and I infer nothing from it (`receipts/hosted-checks.txt`).
- No manager source bank ran at this head and none is claimed. Physical calibration NOT RUN. Field skips are not hardware proof.
- R737-6 is in flight. I did not read it.

The clone is unchanged: head, tree, 1,518 index entries equal to the tree, modes, an empty status with ignored files included, and all six gitlinks (`receipts/restore_check.txt`). Every probe ran in a disposable copy. `external` was uninitialised from the start.

## 7. Pending manager duties

- Carry R738-7-R1, R738-6-R1 and R738-6-R2 to the residue checklist, #495, or fold them into a PR body edit.
- Decide whether R737-5-S3 becomes a new Issue: the split boot passes an image whose flash port is on the wrong addresses.
- No `REVIEW READY` comment names this head. Decide whether the manager's commit needs one.
- Validate the current-dev merge candidate and publish its receipts. Source base `f4c9ad4f`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.
- Own hosted and act acceptance at the exact head, once the pending contexts finish.
- Hold the two standing questions: the gate environment's SDK, and an owner for S2's 8x8 page.
- Merge needs two independent positive reviews, the full completion bar and explicit maintainer authorization.

R738-7 FINISHED
