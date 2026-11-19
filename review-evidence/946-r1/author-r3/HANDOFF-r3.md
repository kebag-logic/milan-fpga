STATUS: DONE (round 3, tests and docs only): lane head `fe297847`, every re-run gate green on both bases, REVIEW READY (round 3) posted on #946 (issuecomment-6995837315, 01:30 CET).

# #946 round 3 handoff ([A797])

Lane `946-ctx-fmt`, head `fe297847`: dev-soft-core `cb96336d` + 13 commits. Round 3 adds `cbbd1ac0` (tests and
plants) and `fe297847` (a source comment and the platform README) on round 2's `9f4f3de0`.
- No firmware behaviour changes, and no production source changes apart from one comment in `sw/litex/ctrl_memory.py`.
- Nothing is pushed: the manager pushes.

Scratch composition `f8694fdd`, made by round 2's recipe at `fe297847`:
- it is round 2's `d98dd322` plus exactly this round's test, plant and README changes;
- the ledger comment is not among them, because its file takes the train's side.

## RESOLUTIONS

| Finding | Severity / lens | Resolution | Commit | Evidence |
|---|---|---|---|---|
| R867-2-F-1: the refusal gate's kind and type tests never exercised at an index with a context | MINOR; Tests | Fixed with the reviewer's case as S11. Input n is bound and its stream published. STREAM_OUTPUT n's SET_STREAM_FORMAT waits, is acknowledged, answers SUCCESS and writes no context. SET_NAME of input n answers SUCCESS and writes no context. Both reviewer plants are in `sink_mutants.py`, each caught by S11 on its own words: `sink-output-taken-for-its-input` (the type test dropped) and `sink-any-kind-of-an-input` (the kind test dropped). | `cbbd1ac0` | `firmware/sinks-both-shapes.txt` (11/11 at 8x8/1if and 1x1/1if); `firmware/new-plants.txt`; the firmware gate receipts (28 of 28 in the control campaign) |
| R867-2-F-2: the PR body's "Why it is race-free" states a mechanism the code lacks | MINOR; Docs | Rewritten to the code. The change port forwards the change to the face first; the face's publication makes its own mailbox accesses. The port then reads the applied state (unless the core is doing a waiting change again), and only then writes the contexts. All of this happens before the core answers and before control returns to the event loop, so no ACMP input is processed between the change (or the bound check) and the write. Round 2's handoff and REVIEW READY used the false phrase too; they are superseded by this text, since posted comments are not edited. | PR body | `PR-BODY.md`, "Why it is race-free" |
| R867-2 RESIDUE-1 and R868-2-R1: a lane name in the new `ctrl_memory.py:254` comment | RESIDUE; Docs | Fixed in a comment-only diff: "named debt owed to the hybrid XIP work, the cold-code and descriptor flash migration (#665 decision D3)". The LEDGERED values and records are unchanged. At composition this file takes the train's side. | `fe297847` | the diff |
| R867-2 RESIDUE-2: #950 not named | RESIDUE; Docs | Fixed: the input-0, CRF and STREAM_OUTPUT limitation now reads "it is #950". | PR body | `PR-BODY.md`, Known limitations |
| R867-2 RESIDUE-3 and R868-2-R2: line 61's wording | RESIDUE; Docs | Fixed as F-2. | PR body | as above |
| R867-2 S-1: refused waiting change answered ENTITY_MISBEHAVING, not STREAM_IS_RUNNING | SUGGESTION; Conformance | Not taken. Changing the status is a core change, which moves every CPU-budget image, and round 3 changes no behaviour. #950 carries "the clause's status"; the PR body says so. | — | `PR-BODY.md` |
| R867-2 S-2: a context decided on the current format's subtype | SUGGESTION; Robustness | Taken as a test-only check: S1 now asserts that every format an input with a context advertises is AAF, so a change keeps its context at every tested shape. A builder rule would be a builder change, so it is not added this round. | `cbbd1ac0` | `firmware/sinks-both-shapes.txt` |
| R867-2 S-3: stale boot figures in `ctrl_split_boot/README.md:137` | SUGGESTION; Docs | Not taken. The line predates the PR and lies outside the delta (#746-class upkeep). That README is also one of the 7 files that take the train's side at composition, where the train's own figures stand, so a lane edit would only add to the composition step. Left to #746. | — | — |
| R868-2-S1: a public follow-up for the core's unchecked redo, the face copy and the channel map | SUGGESTION; Conformance, RTL, Robustness, Docs | Answered in the PR body: #950 is the redo's issue, and the face copy's exposure (the map's channel clip) plus delayed-acknowledgement tests for input 0, the CRF input and STREAM_OUTPUTs are named as #950's to cover. Widening #950 or filing another issue is the manager's. | PR body | `PR-BODY.md`, Known limitations |

## Evidence (receipts/INDEX.md lists every file)

| Gate | Lane `fe297847` | Composition `f8694fdd` |
|---|---|---|
| Firmware gate `--require-rv32 --self-test` | PASS: 75 verdicts; control campaign 745 of 745 (the 28 sink defects among them); AECP and SRP 729; ESCAPED 0 | PASS: 74 verdicts; control 825 of 825; AECP and SRP 875; ESCAPED 0 |
| `Sinks.S1` to `S11` | 11/11 at 8x8/1if and 1x1/1if | the same |
| fw_coverage `--check` | PASS; `ctrl_plat.c`, `ctrl_plat_csr.c` 100 % lines and branches after exclusions | PASS, the same |
| Docs workflow steps | every step dev-soft-core has: rc=0 (5 call train-only scripts) | 97 of 97 |
| `plat_ledger.py --self-test` | PASS, 8 of 8 controls | PASS, 9 of 9 |
| Product images (`ctrl_app.elf` at the 4 ledger points) | byte-identical to round 2's (`548324b5`) | byte-identical to round 2's (`d98dd322`) |
| CPU-budget images (arm A, 1x1 and 8x8/1if) | equal to dev-soft-core `cb96336d`'s | equal to the train's recorded ones |
| `test_ctrl_memory.py` | 0 failures | (the file takes the train's side; round 2's receipt holds) |

Carried from round 2, whose inputs round 3 does not change: the receive stack's suite (CTXFMT 96/96, engine plants 5/5),
the split boot simulation, the twin and its plants, and the composition's sweep (65 of 65 suites). The sweep reads no
firmware test: `scripts/run_all_suites.sh` names none.

No firmware behaviour change was needed, so there was no STOP.
