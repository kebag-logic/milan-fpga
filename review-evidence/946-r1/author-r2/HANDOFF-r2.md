STATUS: DONE (round 2): lane head `9f4f3de0`, every gate green on both bases, REVIEW READY (round 2) posted on #946 (issuecomment-6993699335, 23:37 CET). Kept open for further findings (R867-1 and R868-1 are answered here).

# #946 round 2 handoff ([A797])

Lane `946-ctx-fmt`, head `9f4f3de0`: dev-soft-core `cb96336d` + 11 commits. Round 2 adds `62296be7`, `85363367`,
`0f6c12ba`, `548324b5` and `9f4f3de0` (one docstring rewrapped) on round 1's `66c6edf3`. Nothing is pushed: the manager pushes.

Scratch composition onto the flip train (PR #945, `b1f1161b`), in a scratch clone only:
- `87fa7d23` is the merge, with the ROM ledger's files at the train's side;
- `d98dd322` raises the train's `platform-8x8-two-interfaces` entry from 62.5 to 63.0 (`receipts/merge/`).

## RESOLUTIONS

| Finding | Severity / lenses | Resolution | Commit | Evidence |
|---|---|---|---|---|
| R868-1-F1: a BIND_RX settling while a SET_STREAM_FORMAT waits; the deferred change done again onto the bound input, its LCTX words stale meanwhile | MAJOR; Conformance, RTL, Robustness, Tests, Docs | Fixed by another ordering: the change is not done again onto an input bound meanwhile. The platform wraps the face's `applied` port. While the core waits on a change that moves the context of an input bound now (that input's SET_STREAM_FORMAT, or any input's SET_CONFIGURATION), the change is not applied. The core keeps the values in force and answers ENTITY_MISBEHAVING at `AECP_WAIT_MS`: its documented timeout rollback, bounded, with no contract change. The change port writes each kept change's contexts in the change itself, before the core answers it, with no mailbox access between. The poll backstop is gone. The race argument is corrected in `ctrl_plat.c`, `plat/README.md` and the PR body. | `62296be7`, `0f6c12ba` (code, tests, plants), `85363367` (docs) | `test_plat_sinks.cpp` S6 to S10, each mailbox access watched for a published stream whose context differs from the current format: S6 is the reviewer's order, then unbind and rebind; S7 is acknowledged with the probe unanswered; S8 is the timeout; S9 is unbound again before the acknowledgement, then rebind; S10 is SET_CONFIGURATION. On round 1's platform, S6 reproduces the reviewer's observation (`input 7: current 0205022000806000, context 0205022002006000`), and S4, S5, S7, S10 fail too (`receipts/firmware/platsinks-oldcode-fails.txt`). 7 new planted defects, 26 of 26 caught (`receipts/firmware/sink-campaign-0f6c12ba.txt`). RTL boundary: [CF4], the first PDU after a bind whose format was written the cycle before, accepted (`receipts/rtl/`). |
| R868-1-R1: work-lane and flash-lane names in new comments | RESIDUE; Docs | Fixed: "the multi-stream receive stack of avtp_rxmon_nx_wrap", "the saved-state flash model". Also removed a review label from a new comment in `sink_mutants.py`. | `85363367`, `62296be7`, `0f6c12ba` | the diff |
| R867-1 F-1: ROM ledger entries not raised | MINOR; Docs, Tests | Fixed on the lane, by the owner's rule of 2026-11-15. `platform-8x8-two-interfaces` goes from 60.5 to 61.0, and a new `platform-8x8-one-interface` entry sits at 56.5. They come with their memory-test cases, the ledger's point and a control for it, the boot SoC's ledgered points, and `SPLIT_CONTROL_MEMORY.md` sections 3 and 5 and the READMEs. At composition the ledger files take the train's side: its 8x8/1if entry is 58.0 and the composed image fits it. The train's 8x8/2if entry goes from 62.5 to 63.0, stated in the PR body. | `548324b5`; scratch `d98dd322` | `receipts/ledger/`: lane PASS, 8 of 8 controls; composition PASS, 9 of 9. `receipts/memory/`: 0 failures on both. |
| R867-1 F-2: the poll's owed-flag clearing untested | MINOR; Tests, Robustness | Resolved by removal: the platform has no poll now, so no code runs per pass. The idempotence is checked directly. S5: a change of another kind (SET_NAME, a STREAM_OUTPUT's format, one that waited), and 100 passes with no change and the clock moved 2 s, write no context. S2 and S4: a change writes its own context alone. Planted: `sink-every-pass-rewrites` (a pass rewriting every context, the finding's class), `sink-other-kind-writes-every-context`, `sink-change-writes-every-context` (the reviewer's R1 probe). | `62296be7`, `0f6c12ba` | `receipts/firmware/sink-campaign-0f6c12ba.txt` |
| R867-1 F-3: follow-up tickets not named | MINOR; Docs, Conformance | Fixed: the PR body's Known limitations names F-G2 as #948 and the release image's F-G1 as #949, with F-G3 #943's. "Closes #946" kept: its scope is the split image. | PR body | `PR-BODY.md` |
| R867-1 R-1: a work-lane name in `sim_ctxfmt.cpp:5` | RESIDUE; Docs | Fixed (as R868-1-R1). | `85363367` | the diff |

## The design choice, and what it leaves

**Option P was considered and not taken.** P serializes by holding the binding's stream from the datapath until a
waiting change lands. It leaves a format changing on a bound input after BIND_RX's response, the order IEEE
1722.1-2021 7.4.9 refuses. It would also hold ACMP's own record of the published stream apart from the datapath's.

**The refusal (W) uses the core's applied contract as written.** A waiting change is done again only once applied,
else it is kept undone and answered ENTITY_MISBEHAVING at `AECP_WAIT_MS`. So a context's format moves only while its
input is unbound, the invariant round 1 claimed.

**W is limited to inputs with a context.** For input 0 the datapath's judge is the face's own commit (`fmt0_i`),
which the datapath has already taken when the acknowledgement releases the change. Refusing then would leave
`fmt0_i` on the refused value until the face's republish, up to 100 ms on a live binding.

**Open, for a new ticket (manager):**
- For input 0, the CRF input and STREAM_OUTPUTs, the core still does a waiting change again without repeating its
  bound or running check (`aecp.c`, the waiting command). Fixing it there is the core's change, which moves every
  CPU-budget image.
- During a refused wait, the datapath's copy of the face may hold the refused format until the face republishes the
  values in force. That copy is `F_FMT_IN` for inputs above 0, the map's channel clip, not the monitor's judge. It is
  the face's existing rollback path, at most the wait's bound.

Both are stated in the PR body's Known limitations.

## Evidence (receipts/INDEX.md lists every file)

Heads:
- The lane's receipts are at `548324b5` unless named. `9f4f3de0` rewraps one docstring of
  `sw/litex/ctrl_memory_ledger.py`, so they carry; the memory test, the docs steps and the boot simulation were run
  again at `9f4f3de0`. The RTL suite ran at `0f6c12ba`, and nothing it reads changes after it.
- The composition's receipts are at `d98dd322`. Composed again at `9f4f3de0` by the same recipe, it gives the same
  tree, `21a39a5c` (`merge/composition.txt`).

| Gate | Lane | Composition |
|---|---|---|
| Firmware gate, `test_ctrl_firmware.py --require-rv32 --self-test` | PASS: 75 verdicts, 0 failed; control campaign 743 of 743, AECP and SRP 729, ESCAPED 0 (`gates/lane-548324b5-firmware-gate.txt`) | PASS: 74 verdicts; control 823 of 823, AECP and SRP 875, ESCAPED 0 |
| `platsinks` S1 to S10 | 10/10 at 8x8/1if and 1x1/1if | the same |
| The 26 sink defects | 26 of 26 caught, each on its named test; no test of the suite unnamed | the same |
| fw_coverage `--check` | PASS; `ctrl_plat.c`, `ctrl_plat_csr.c` 100 % lines and branches after exclusions | PASS, the same |
| `plat_ledger.py --self-test` | PASS: 8x8/1if 56.5 (`platform-8x8-one-interface`), 8x8/2if 61.0; controls 8 of 8 | PASS: 8x8/1if 58.0, 8x8/2if 63.0; controls 9 of 9 |
| `test_ctrl_memory.py` | 0 failures (at `9f4f3de0`) | 0 failures |
| `make -C tb/verilator/avtp_rxmon` (pinned Verilator 5.050) | PASS: CTXFMT N=8 96/96, engine plants 5/5 (at `0f6c12ba`) | in the sweep: the same |
| Sweep (4 shards) | | 65 of 65 suites, 2,713,122 checks, 0 in-suite failures; the 4 declared skips are tsn_fuzz's external-generator campaigns |
| Twin and plants | dev-soft-core's own result: the owed row `split-talker-failed`, plant `srp-plus-k` escaping, captures byte-identical to `cb96336d` (run here at `cb96336d` too) | 0 findings; every plant refused |
| Docs workflow steps | every step dev-soft-core has: rc=0 (5 call train-only scripts) (at `9f4f3de0`) | 97 of 97 rc=0 |
| Split boot simulation | 8x8: PASS, ready 65.775 ms (at `9f4f3de0`) | 8x8: PASS, 67.328 ms, 28 context writes; 1x1: PASS, 27.936 ms, none |
| CPU-budget images | no input changed (`budget/`) | hash-equal to the train's recorded images |
| Round 1's platform under round 2's tests | S6 reproduces R868-1-F1; S4, S5, S7, S10 fail too (`firmware/platsinks-oldcode-fails.txt`) | |

**A correction to round 1's public numbers.** Round 1's REVIEW READY called its "1,546 / 1,778" totals planted
defects caught. Each total also counted the gate's 81 / 87 `[ok] arm` lines. The defects were 736 + 729 = 1,465 on
the lane and 816 + 875 = 1,691 on the composition. This round states the split (`fw_summary.py`'s first lines).

**ROM, per image:** the platform image at every point, in plat_ledger's POINT lines:
- lane: 1x1/1if 43.5, 1x1/2if 44.0, 8x8/1if 56.5, 8x8/2if 61.0;
- composition: 45.0, 46.0, 58.0, 63.0.

## Rules kept

- One commit subject a line, no body, no trailer.
- No push, no PR edit, no merge, no rebase, no force.
- No hardware, and no RTL, mailbox-contract or CPU-budget bound change.
- The only comments are this round's one REVIEW READY on #946.
- The review packets were read, and nothing in them was changed.
- Every unit is this lane's (`milan-946-a797-r2*`). No other unit was touched.
