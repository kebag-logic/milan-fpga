[A698i] REVIEW READY

Commit: `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce`, two commits on `37e0393094`, no rebase and no force. Nothing is pushed: PR #812's live head is still `37e03930`, for the manager to push.

Changed:
- `ctrl_plat_image.py` refuses a `--flash-map` that lacks `generated/csr.h` or `generated/mem.h`, by name, as the first step of `main`, so before the compiler is called.
- `ctrl_image_selftest.py`: the map fixture is complete, and new checks cover each missing header and a JSON-only map, at the shape's clock. 40 checks, 7 of them `plat`.
- The four statements are narrowed to what the check proves: a linked platform image takes no header of the stand-ins. `plat/README.md` and the docstring also state the limit: the refusal reads that both headers are there, not what they say.
- No RTL, firmware C, gitlink, `ctrl_srp_image.py` or size fixture change.

**For the manager: one file is outside the ruling's list.** The ruling says to keep the change to its named files. `sw/firmware/ctrl/README.md:711,719-722` quoted the self-test's 37 checks and its "last four", so the ruled checks would have made that page false. I corrected it in `b7fe6a777e`, a commit of its own that can be dropped alone. TAKEN said so before the edit, and no reply came.

Two listed items were fixed by the same edit, as the ruling allows:
- R738-5-S2: the check for "before the compiler is called" sits in the helper the no-map cases share.
- R737-4-R1: `How to validate` now expects 40 checks, so its checkout had to name this head.

Nothing else was folded in. R738-5-RES1, RES2 and the retained residue are untouched, for #495.

Validation, each on a clean clone of this head, all rc 0:

| Gate | Result |
|---|---|
| `ctrl_image_selftest.py --require-rv32` | `ctrl_image self-test: 40 checks PASS` |
| `firmware_boundary --without verilator` | `ctrl_boundary: PASS`; four `ctrl_plat_image.py` runs stopped at their link |
| `firmware_boundary --only verilator` | `ctrl_boundary: PASS`; four `ctrl_plat_image.py` runs stopped at their link |
| `docs.yml`, every job, fresh clone, empty `HOME`, new virtual environment | 71 steps ran, each rc 0; 24 not run, each with its reason |
| `git diff --check`, the privacy check | rc 0; `0 private line(s) in a68536fa..HEAD` |

The docs replay's two builder legs print `ALL GATES PASS EXCEPT 16 NOT RUN` and `EXCEPT 1 NOT RUN`, the counts round 7's printed. This round has no separate builder run behind them.

Added beyond the ruling's list, because none of those gates links a real generated map:

| Run | Result |
|---|---|
| R737-4's `partial_map_probe.sh`, unedited, on a fresh boot's map | three partial maps rc 2 with no ELF, each naming what it lacks; the complete map rc 0, with `lui 0xf0004` 0 and `lui 0x20000` 0 |
| Other map shapes: directory or dangling link at a header, flattened layout, absent path, a file | rc 2, no ELF, at the refusal |
| Empty headers | rc 2, no ELF, at the compiler |
| A complete map by a relative path | rc 0, 0 and 0 |
| S3's split boot, both shapes | `PASS (0 finding(s))`, 84.372 ms and 184.622 ms, the same cycles as round 7 |
| Linked ELFs at both shapes | byte-identical to round 7's, so no figure moves |
| `check_py_idiom.py` | rc 0, no new finding |

Mutants: `mutants: 15 planted, 0 escaped; clone clean after: True`. Each new check has one that fails it while the earlier new checks stay green. The driver's first run exited 1 with no defect escaped: one row's expected words had the wrong quote character. I corrected the words, added a mutant, re-ran the whole driver and kept that first log.

Acceptance criteria, met:
- The refusal, at the link, before the compiler is called: `ctrl_plat_image.py:62-71,175`.
- The complete fixture, and the JSON-only and per-header checks, each with a planted mutant: `ctrl_image_selftest.py:440-475`.
- The four statements: `ctrl_plat_image.py:14-17`, `ctrl_image_selftest.py:30-38`, `plat/README.md:101-103`, and the PR body's Round 6 paragraph.
- The size fixture is out.

Not run, as the ruling says no long gates: the 97 short gates, the other long gates, S2, S4, the D5 plant, S3's self-test and its placement controls. This is local evidence; the hosted contexts on the pushed head remain mandatory.

Open risks/questions:
- Whether the `sw/firmware/ctrl/README.md` commit stays, above.
- The two standing questions: the gate environment's SDK is not the pinned build, and S2's 8x8 page needs an owner.
