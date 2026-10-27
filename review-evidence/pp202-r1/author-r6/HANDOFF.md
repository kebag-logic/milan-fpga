# [A676f] processor #202 round 6 — HANDOFF

**Status: REVIEW READY. Every required gate returned 0; no STOP condition met.**
TAKEN: issue #202 issuecomment-6433337087. REVIEW READY: issue #202 issuecomment-6433436777 (head `a5ad8cae`).

Round-6 assignment: issue #202 issuecomment-6433331386. Both reviews POSITIVE (R709-3, R710-4);
the parent consumer gates passed 16 of 17. The parent's C++ idiom gate (`scripts/check_cpp_idiom.py`,
Rule 11 in the parent's `docs/development/CODE_QUALITY.md`) reported "multi-declarator declaration
2 > ratchet 0" for one line here and one in the parent wiring patch. Scope: one declaration per line
in both places and no other change; regenerate the patch; the parent idiom gate rc 0 with this head
as the gitlink and the patch applied; the talker suite and `make check` rc 0.

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before the commit; merge base with main `ed211803`) |
| Branch | `202-maap-conflict-new-stream-id` (local; not pushed) |
| Base (processor main) | `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8` |
| Round-5 head (start) | `98e0137cfaf07b3b3efd21d2bd19648762e86f2b`, tree `9fdc9864d6ad8a900403a0ba81969b028c8d8140` |
| **Head** | **`a5ad8caea58886f01633e1545fb26300f1db9ebd`**, tree `e496f4f6faa5d95dbf531f743ecd0dc7a3f72f4a` |
| Round-6 commit | `a5ad8cae` Declare S5's four flags one per line, as the parent's C++ idiom gate requires (issue #202) |
| Parent patch | `parent-src-stream-id-wiring.patch` (this directory): **sha256 `ff5068d295872d1f872b89890ff76f9bb1d3fd0738ad650282dbe45d9e171275`, 70,091 bytes** (round 5: `e3991176…f1fa`, 70,077 bytes) |
| Scratch parent | the committed local clone `pp202-parent`, push URL invalid, never pushed (§5) |

`git diff 98e0137 a5ad8ca` is the one hunk in `tb/acmp_talker/sid_cases.hpp`
(`receipts/records/base-head-records.txt`). The lane tree is clean, ignored files included.

## 2. Changes (file:line at head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `tb/acmp_talker/sid_cases.hpp:359-362` (processor) | `bool fresh_ids = true, distinct = true, declared = true, left = false;` → four declarations, one per line, same names, initialisers and order | parent `CODE_QUALITY.md` Rule 11 (assignment item 1) |
| 2 | `tb/verilator/milan_dp/sim_sid_move.cpp:833-834` (parent, in the patch) | `long n = 0, other = 0;` → `long n = 0;` and `long other = 0;` | parent `CODE_QUALITY.md` Rule 11 (assignment item 1) |

No other line changes in either repository. No document cites `sid_cases.hpp` by line number
(`grep -rn "sid_cases.hpp:[0-9]"` over the tree is empty), so no record goes stale.

## 3. New checks

None: the assignment adds no check. The planted defect is the round-5 state itself: the parent idiom
gate on the scratch parent's round-5 pin (processor `98e0137`, the round-5 wiring) returns **rc 1**
with `FAIL: multi-declarator declaration 2 > ratchet 0. New C++ uses the named construct; see Rule
11 in docs/development/CODE_QUALITY.md.` (`receipts/parent/base_check_cpp_idiom.*`), the words of the
consumer receipt that found the two lines; with this round's two splits it returns rc 0 and
`multi-declarator declaration: 0 <= 0`.

## 4. Processor gates (every `.rc` is the command's own exit status, never through a pipe)

Run in a disposable clone at `a5ad8ca` (Verilator 5.052; CI pins 5.050), never in the lane tree.

| Gate | Round-5 head `98e0137` (round-5 record) | Head `a5ad8ca` |
|---|---|---|
| `make -C tb/acmp_talker run` | rc 0, 1,545 checks | **rc 0, `1545 checks: 1545 PASS, 0 FAIL`** (`receipts/processor/talker_suite.*`) |
| `make check` | rc 0 | **rc 0** (links, req-tags, ids, figures, matrix, parameters, AECP command selftests; `receipts/processor/make_check.*`) |

Object-code record (not a gate the assignment asks for; it shows why the round-5 campaign results
stand): `tb/acmp_talker/sim_main.o`, built at `98e0137` and at `a5ad8ca` with the suite's own flags
(`-O2`), disassembles to the same 11,790 lines except 8 immediates, each raised by exactly 3: the
`__LINE__` of the eight `REQ_TAG` calls below line 359 (414, 424, 499, 528, 561, 582, 650, 673 at
the head). The suite, the ACMP `STREAM_ID` arms and the talker retry campaign therefore execute the
same code (`receipts/records/talker-object-equivalence.txt`). The ACMP and talker retry campaigns,
the full sweep, lint and `tb/pp_top` were not re-run; their round-5 records at `b2b2bfd`/`98e0137`
stand (RTL and every other suite input unchanged).

## 5. Parent: the regenerated patch and the consumer gate

Regeneration, in the scratch parent:

```
git checkout -b scratch-pp202-a676f-wiring d3ab5b37f5
# split line 833 of tb/verilator/milan_dp/sim_sid_move.cpp, commit 878c273e46
git diff 309af35f59 878c273e46 -- . ':(exclude)protocol-processor' > parent-src-stream-id-wiring.patch
```

`309af35f59` is dev `e76a755a` with only the gitlink moved and `d3ab5b37f5` is round 4's wiring
commit, the same endpoints round 5's patch was cut from (that command at `d3ab5b37f5` reproduces
`e3991176…f1fa`). The new patch differs from round 5's in the one hunk header, the new file's blob
id and the split line (`receipts/records/patch-check-dev.txt`).

Scratch parent branches (never pushed; `receipts/records/PARENT-STATE.txt`):

- `scratch-pp202-a676f-wiring`: `878c273e46` (the wiring with the split; the patch source).
- `scratch-pp202-a676f` (checked out, tracked tree clean): from round 5's final pin `61298744b7`,
  `96e90e7d97` the same split, `a67e481010` pins processor `a5ad8ca`. No ROM-digest record was added
  for this pin: the processor's consumed inputs `hdl`, `scripts`, `syn`, `Makefile` are unchanged
  since `98e0137`, whose record is there.

| Consumer gate | Tree | Result |
|---|---|---|
| `git apply --check --index`, `git apply --index` of the new patch | fresh local clone checked out at dev `e76a755a` | rc 0, rc 0; the applied tree equals `878c273e46` outside the gitlink (empty diff) |
| gitlink | same | set to `a5ad8ca`; `protocol-processor`, `gptp-processor` and `third_party/verilog-axis` initialised at their pinned commits (`git submodule update --init`), committed locally |
| **`python3 scripts/check_cpp_idiom.py`** | same (dev + patch + `a5ad8ca`) | **rc 0**: 349 first-party translation units, `multi-declarator declaration: 0 <= 0`, every ratchet held (`receipts/parent/check_cpp_idiom.*`) |
| `python3 scripts/check_cpp_idiom.py` | scratch final pin `a67e481010` | rc 0, same counts (`receipts/parent/final_pin_check_cpp_idiom.*`) |
| `python3 scripts/check_cpp_idiom.py` (the defect) | scratch round-5 pin `61298744b7` (processor `98e0137`) | rc 1, `multi-declarator declaration 2 > ratchet 0` (`receipts/parent/base_check_cpp_idiom.*`) |
| `make -C tb/verilator/milan_dp sidmove` (fresh build outside the tree) | dev + patch + `a5ad8ca` | rc 0; the split file compiled with `-Wall -Wextra`; 50 checks, 0 failures, conflict to the new ID's declaration 1,735 ms (`receipts/parent/sidmove.*`) |
| `make -C tb/verilator/milan_dp sidmove8` (fresh build outside the tree) | same | rc 0; 52 checks, 0 failures, 1,816 ms (`receipts/parent/sidmove8.*`) |

The two recovery legs are the only parent builds that compile `sim_sid_move.cpp`; they were run
because the parent file changed, with the same results as round 5. The other 16 consumer gates
passed at `98e0137` with the round-5 patch; this round changes one declaration in each of two test
files and nothing they consume otherwise.

## 6. Completion

Both multi-declarator lines are split with no other change; the patch is regenerated (sha256
`ff5068d2…1275`); the parent's `check_cpp_idiom.py` returns 0 with this head as the gitlink and the
patch applied; the talker suite (1,545 of 1,545) and `make check` return 0. One commit on
`98e0137`: `a5ad8cae`. No push, PR creation or edit, merge, rebase, hardware operation, RTL change
or top-level interface change was performed. Resources: one service unit; every build here is
small (peak well under 2 GB; host MemAvailable about 55 GB), so no shard units were used.

## 7. Receipts

`INDEX.md` and every `receipts/**/INDEX.md` are generated from the files present. Local paths in
receipts are normalized (`<scratch>`, `<parent>`, `<host-path>`).

| Receipt | What it holds |
|---|---|
| `receipts/processor/` | `HEAD.txt`, the talker suite and `make check` logs and rcs at `a5ad8ca` |
| `receipts/parent/` | the idiom gate on dev + patch + `a5ad8ca`, on the scratch final pin and on the round-5 pin; both recovery legs; the submodule initialisation log |
| `receipts/records/` | base and head records, the parent state, the patch regeneration and fresh-dev apply check, the talker object-code record |
