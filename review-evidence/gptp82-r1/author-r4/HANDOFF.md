# [A649] #82 handoff: grandmaster thisClock and path {thisClock} from reset

## Round 4 (head acfef36b)

Status: REVIEW READY at head acfef36b39283c3102ba5f6948fe1f8c8c494853 (tree
e2e1cb62ba1a232761aa80c74a2230e7c9ac078f). No STOP condition was met.

- Assignment: the newest [A10] comment on PR #83, "Round 4 assignment" (2026-10-18T22:33:33Z).
  It applies R650-3-R1 from the R650-3 report on PR #83.
- Branch 82-boot-gm-thisclock. Round-4 commits on 334e9fe6, local, not pushed:
  - dea718c9 Split the engine suite's phase list and mutation arm under the parent's function-length ratchets
  - acfef36b State the reset flags for a priority1-255 image
- Receipts: `receipts/r4/`. `RECEIPTS.md` is regenerated from the files present
  (`receipts/r4/scripts/make_index.py`) and checked by `receipts/r4/scripts/verify_receipts.py`.
  The copies replace host path prefixes with placeholders (`<scratch>`, `<parent>`, `<manager>`,
  `<lane>`, `<tools>`, `<home>`, `<tmp>`). The raw logs stay in scratch.

### What changed, by item

1. Ratchets. I reproduced the manager's failure on my own committed parent snapshot c85ab500
   (dev e9cbb676 with gitlink 334e9fe6): `long function 1 > ratchet 0` (C++) and
   `long function 10 > ratchet 9`, `undocumented public function 1 > ratchet 0` (Python),
   each rc 1 (`receipts/r4/pgates/base-334e9fe6/`). Dev as is passes both
   (`pgates/dev-e4869fd0/`). The parent's own scan functions name the three sites
   (`idiom/base-334e9fe6-sites.txt`):
   - `sim_main.cpp:244`, `run_suite`, 102 lines;
   - `mutants.py:549`, `main`, 104 lines;
   - `mutants.py:624`, the nested `failing`, which had no docstring.

   All three came from round 3: the fourth-pass branch in `run_suite`, and the pass-split
   matching in `main`. At head the same scan finds nothing in either file
   (`idiom/head-acfef36b-sites.txt`). Both gates read at or under their ratchets, and none
   was raised: C++ long function `0 <= 0`; Python long function `9 <= 9` and undocumented
   public function `0 <= 0`. Both have rc 0.
2. The full consumer list, on committed local snapshot dd2e1fd9 (one commit on dev e9cbb676,
   gitlink acfef36b): all 11 template commands rc 0 (table below).
3. R650-3-R1: `docs/INTEGRATION.md:480` carries the exact text, "Flags carry gmPresent alone,
   or nothing with priority1 255."

R650-3-S1 to S5 are suggestions outside this assignment and are not taken.

### Changes (file:line at head)

- `tb/verilator/engine/sim_main.cpp`:
  - `:244-251` `run_suite` (8 lines) runs `run_the_self_publication_phases` when
    `self_present == 0`, else `run_every_phase`, then prints the tally once.
  - `:253` `private:` now precedes both helpers.
  - `:255-266` `run_the_self_publication_phases`: the former branch body, unchanged, including
    the boot-stamp line.
  - `:268-353` `run_every_phase` (85 lines): the former phase list, unchanged and in the same
    order.
- `tb/verilator/engine/mutants.py`:
  - `:549-558` `_named_failure`: the former nested `failing`, now with a docstring; same
    expression.
  - `:561-590` `named_verdict`: the #75 and #82 narrowing, moved verbatim with its comments.
  - `:593-636` `run_mutant`: the loop body. Each `fails += 1; ... continue` becomes
    `print; return False`, and the catch becomes `return True`. The messages are unchanged.
  - `:639-676` `main`: the positive control, the `run_mutant` loop over the module's
    `MUTATIONS` (so the shard runner's reassignment still applies) and the tally.
- `docs/INTEGRATION.md:480`: R650-3-R1.

### New checks, controls, failing words

This round adds no check: it is a behaviour-preserving split. Every check and every mutant
verdict is shown identical, and the split's own code is graded with planted controls:

| what | evidence | result |
|---|---|---|
| engine suite, three images and the fourth pass | `gates/{base,head}/engine.log`, `compare.txt` | identical apart from one build-timing line; 1642 x3 + 46, 0 FAIL at both |
| engine mutation arm, 18 shards | `gates/{base,head}/engine-mutants-s*.log` | all 18 logs byte-identical; 58/58 at both; the same 71 named failure lines (got/exp words) |
| every branch of the moved verdict code (`controls/meta-branches-*.log`) | 8 meta rows, main() rc 1 by design; base and head byte-identical | `its pattern appears 0 time(s)`; `the generator refused its image`; `did not build`; `mutant SURVIVED`; `missed its named check` (slew); `missed its named check(s): #82 Pdelay loss: that mastership commit has gmPresent`; slew and p1 catches printing `got 0000000000000000 exp 0000000000000001` and `got 0000000000000001 exp 0000000000000000` |
| planted: dispatch inverted (`controls/split-swap.diff`) | `split-swap-engine.log`, rc 2 | shipping passes `46 checks: 46 PASS`; fourth pass `1642 checks: 1588 PASS, 54 FAIL`, first `FAIL p1 255 ann p1 got 00000000000000ff exp 00000000000000f8` |
| planted: one phase call dropped (`controls/split-drop.diff`) | `split-drop-engine.log`, rc 0 | not a suite failure: `1629 checks: 1629 PASS` against 1642. Only the tally comparison catches it; the suite has no check-count assertion, and did not have one at base either |

### Repository gates (Verilator 5.050 pinned first on PATH, TMPDIR in scratch, never piped)

Head ran in the lane from `make clean`. `clean` deletes three tracked ROM copies. The suites
regenerated two of them byte for byte, and `syn/ooc/work/gptp_ucode.hex` was restored with
`git checkout`, so the tree is clean. Base ran in a fresh `git archive` of 334e9fe6. Every rc
file reads 0.

| gate | base 334e9fe6 | head acfef36b |
|---|---|---|
| `make clean` | rc 0 | rc 0 |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0, 20 exact | rc 0, 20 exact |
| `make -C tb/verilator/ucpu` | rc 0, 768 | rc 0, 768 |
| `make -C tb/verilator/parser` | rc 0, 337 + 9/9 | rc 0, 337 + 9/9 |
| `make -C tb/verilator/engine run` | rc 0, 1642 x3 + 46 | rc 0, 1642 x3 + 46 |
| engine `mutants.py` (18 foreground parallel shards of its own `main()`) | 18 rc 0: 58/58 | 18 rc 0: 58/58 |
| `make -C tb/verilator/gaskets` | rc 0, 81 + 5/5 | rc 0, 81 + 5/5 |
| `make -C tb/tsngen` | rc 0, 288 + 4/4 | rc 0, 288 + 4/4 |
| `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |

### Parent consumer gates (the template's 11 commands)

The scratch parent is a fresh clone of milan-fpga at dev e9cbb676, with submodules and the push
URL `DISABLED-no-push`. It has two local snapshot commits, never pushed:
- dd2e1fd9 (head): one commit on e9cbb676 that sets the gitlink to acfef36b;
- c85ab500 (branch `r4-base-334e9fe6`): the same with 334e9fe6.

Before every git command in the submodule I checked its `rev-parse --show-toplevel`. The command
words are the template's (`receipts/r4/pgates/manager-334e9fe6/parent-consumer.json`), with three
host differences:
- PATH starts with the pinned Verilator 5.050 wrapper directory. It is the same wrapper script
  as the manager's, with the same VERILATOR_ROOT.
- TMPDIR is in scratch.
- The cwd is my parent.

The manager column is the manager's run at 334e9fe6 (manager snapshot 851f8ef8).

| # | command | manager 334e9fe6 | mine, base snapshot 334e9fe6 | mine, head snapshot acfef36b |
|---|---|---|---|---|
| 1 | `check_cpp_idiom.py` | rc 1 | rc 1 (same words) | rc 0, long function 0 <= 0 |
| 2 | `check_py_idiom.py` | rc 1 | rc 1 (same words) | rc 0, 9 <= 9, undocumented 0 <= 0 |
| 3 | `xvlog_gate.py --check` | rc 0 | not re-run | rc 0, 0 findings |
| 4 | `check_rtl_source_lists.py` | rc 0 | not re-run | rc 0 |
| 5 | `sw/builder/test_builder.py` | rc 0, 1 arm NOT RUN | not re-run | rc 0, the same 1 arm NOT RUN (gate 11 calibration needs a board build tree), 1763 s |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | rc 0 | not re-run | rc 0, controls 9, failures 0 |
| 7 | `check_port_contracts.py` | rc 0 | not re-run | rc 0, gptp-processor 19 <= 19 |
| 8 | `measure_naming.py --check` | rc 0 | not re-run | rc 0 |
| 9 | `measure_test_evidence.py --check` | rc 0 | not re-run | rc 0 |
| 10 | `docs_check.py` | rc 0 | not re-run | rc 0, 0 findings |
| 11 | `lint_rtl.py --check` | rc 0 | not re-run | rc 0, 90 <= 90 |

Commands 3, 4 and 6 to 11 print the same as the manager's run once paths, timings, PIDs and temp
names are removed; command 3 also names the other gitlink (`compare.txt`). In
command 5 the gate and verdict lines differ only in one temporary directory name.

### Process notes

- Command 5 needs about 30 minutes, more than one foreground command can last. It was the only
  command run detached (`setsid nohup`, its rc and log recorded by the same runner,
  `pgates/head-acfef36b/consumer-head-b-*`). The other gates ran in the foreground while it ran,
  and I waited for its rc before posting. Every other command ran in the foreground.
- The head snapshot was first committed on top of the 334e9fe6 snapshot. Before any gate ran,
  I rebuilt it as one commit on e9cbb676, the manager's shape, and kept the 334e9fe6 snapshot as
  a branch. No consumer gate ran at the discarded commit.
- The R650-3 report was read in the PR #83 comment thread; R1 was applied with its exact text.

### Posting

- REVIEW READY: issue #82 issuecomment-6256511083, "[A649] REVIEW READY acfef36b39283c3102ba5f6948fe1f8c8c494853" (2026-10-18T23:29:24Z).
- No TAKEN repost, no push (the remote branch still reads 334e9fe6), no PR edit, no parent push;
  the scratch parent commits stay local.

## Round 3 (head 334e9fe6)

Status: REVIEW READY at head 334e9fe64dfff5568be58a0dc9aeb302959b3b58 (tree
fdb142e8ffb1a8f68158feaf00d486f6f5e3c3e2). No STOP condition was met.

- Assignment: PR #83 issuecomment-6254393722. Reviews: R650-2 (6254388777), R651-2 (6254290649).
- Branch 82-boot-gm-thisclock. Round-3 commits on 8f3c376d, local, not pushed:
  - 784da3f6 Publish gmPresent for a grandmaster-capable thisClock in every self publication
  - 85d267a0 Grade gmPresent, the sync-ok drop and the return to mastership with planted mutants
  - 334e9fe6 Document gmPresent and mastership after a capability drop
- Receipts: `receipts/r3/`. `RECEIPTS.md` is generated from the files present
  (`receipts/r3/scripts/make_index.py`). Round-3 copies replace host path prefixes with
  placeholders (`<scratch>`, `<lane>`, `<parent>`, `<tools>`); the raw logs stay in scratch.

### What changed, by item

1. R650-2-F1 (tests). Phase 36 now keeps Syncs from the elected peer D arriving every 125 ms
   while its Pdelay stops, so sync-ok is set when asCapable falls (the fall commit carries flags
   `0x9`, presence and sync-ok, GM D). The drop commit's whole flags word is graded: exactly
   gmPresent (`0x1`; `0x0` in the priority1-255 pass), so sync-ok, mastership and asCapable are
   clear. After three incapable seconds Pdelay answers again and no Announce is sent: the port
   must commit mastership within one receipt interval (3 s plus 2 ms for the tick and handler),
   naming thisClock with {thisClock} and gmPresent. Measured: 2,000,682 cycles (1.0003 s at
   2 MHz) after the asCapable rise. E then still wins over the dropped D, as before.
   The reviewer's two mutants are in `mutants.py` with their exact pattern and replacement text:
   `drop_keeps_flags` as "the asCapable drop keeps the flags word" (:429) and `held_no_rearm` as
   "an incapable port's receipt watch is not re-armed" (:435). Each fails its named checks in
   the arm, and the reviewer's own probe script, run unmodified on an archive of the head, shows
   the same named failures (`receipts/r3/controls/reviewer-probe-*.log`).
2. R650-2-F2 (gmPresent conformance). 802.1AS-2020 sets gmPresent from gmPriority's priority1
   (the update rule is item g) of 10.3.13.2.4, updtStatesTree; 10.3.12 conditions the sync receipt
   timeout on it). gmPriority is never worse than thisClock's own vector, so a plane whose
   priority1 is below 255 always has gmPresent TRUE. Before this round the µcode used flags bit 0
   both as the published gmPresent and as its internal "a peer is elected" test (the slave gates
   on Sync and Follow_Up, BECGATE's drop test), so it could not simply set the bit at reset or in
   the drop. Now:
   - the generator marks "thisClock is grandmaster-capable" (priority1 < 255) as bit 32 of ROM
     data word 1022, beside thisClock's high half (48-bit words; bits 47:32 were zero);
   - the engine publishes `pub_flags_o[0] = pub_flags_r[0] | rom_gm_capable_w`; µcode reads of
     word 2 still return the raw bits, so the internal meaning is unchanged;
   - BECOME no longer sets raw bit 0 (no peer is elected there); for priority1 255 this also makes
     mastership publish gmPresent FALSE, consistent with reset and the drop.
   Published flags: reset `0x1` (was `0x0`), drop `0x1` (was `0x0`), mastership `0x7` and slave
   `0x5`/`0xD` (unchanged). The image changes in exactly two words (`receipts/r3/rom/image-diff.txt`):
   BECOME's OR immediate 3 -> 2 and word 1022 `000002A1B2FF` -> `000102A1B2FF`. ROM use stays 1,013
   of 1,024 words (seeded 1,014). Default-argument image sha256 ceb04562... (was 00826e9b...).
   The PR body's "Known limits" sentence and `docs/INTEGRATION.md` are corrected.
   STOP check: not met. The parent consumes only bits 3 and 2 (`milan_datapath.sv:2040-2041`);
   every parent gate passes; the dev `milan_dp` test fails exactly the same three checks as in
   round 2 and no others (`receipts/r3/pgates/head/milan_dp-gptp-dev-tests.log`).
3. R650-2-R1: the exact comment text is at `hdl/top/KL_gptp_engine.sv:708-712`.

The R651-2 items: F1 (the published verifier) was the manager's and is fixed on the evidence
branch; my round-3 index and verifier avoid the same fault (the verifier reads only the table under
"## In this directory"; negative controls in `receipts/r3/controls/verifier-controls.log`). S1: the
ROM-layout helper is revision-aware; base sections now complete (`receipts/r3/rom/layout-base.txt`).
Not taken, as suggestions outside this assignment: R651-2-S2 (the `--mac` example in
INTEGRATION.md, an inherited non-publication line), R650-2-S1 (parser identity from reset) and
R650-2-S2 (hook versus boot-arm comment or assertion).

### Changes (file:line at head)

- `hdl/top/KL_gptp_engine.sv`: `:172-175` `rom_gm_capable_w` (bit 32 of word 1022) and its rule;
  `:708-712` R1 text; `:1028-1031` published bit 0 ORs the capability.
- `hdl/ucode/gen_gptp_ucode.py`: `:22-27` module notes; `:424-427` `ROM_GMCAP_BIT_C`; `:501-502`
  flags comment; `:1708-1711` BECGATE drop comment; `:1730-1731` BECOME sets mastership only;
  `:2199-2202` the capability mark in the high data word.
- Four tracked images regenerated (`syn/ooc/work`, `tb/tsngen`, `tb/verilator/engine`,
  `tb/verilator/ucpu`), two words each.
- `tb/verilator/engine/sim_main.cpp`: header `:21-25`, `:144-165`; `:236-257` the constructor and
  the fourth pass (boot, mastership and phase 36 only; `:251` stamps the boot request as phase 2
  does); `:349-360` `self_present`, the `p1 255 ` check prefix; `:451-457`, `:593` gmPresent in
  the cold-release monitor; phase 1d `:1242`, `:1256`; `:1764` "master flags" follows
  `self_present`; phase 35 `:4881`, `:4909`; phase 36 `:4913-5016`; `:5694` the plusarg.
- `tb/verilator/engine/mutants.py`: `:72-76` the fourth-pass arguments; `:262`, `:278` two
  mastership controls re-pointed at BECOME's changed line (same defects); `:311` swapped-words
  pattern follows the new data-word line; `:388-401` two departure controls also name the new
  mastership check; `:429-474` six new controls; `:492-505` both images; `:523-546` both passes,
  one merged tally; `:618-638` pass-separated name matching.
- `tb/verilator/engine/Makefile:30-31`, `:43-46`, `:60` and `.gitignore:4`: the fourth pass.
- Docs: `docs/INTEGRATION.md:480`, `:494-508` ("Grandmaster presence"), `:534-544`;
  `docs/HDL_DEVELOPER.md:149-155`, `:161`; `docs/TEST_DEVELOPER.md:114-116`;
  `docs/SOURCE_EVIDENCE.md` ten anchors moved (20 exact, 0 findings).

### New checks, controls, failing words

Engine suite: 1,642 checks per image (round 2: 1,634), three images, plus the fourth pass of 46
checks from a priority1-255 image. Arm: 58/58 caught (round 2: 52/52), each control failing every
check it names. A name with the `p1 255 ` prefix matches only fourth-pass failures and any other
name only shipping-pass failures; a meta-run that renames the fourth-pass-only control's check to
its shipping spelling reports `missed its named check(s)`, rc 1 (`controls/meta-pass-split.log`).

| check (`#82 ` prefix dropped) | control (`mutants.py` line) | failing words (head arm) |
|---|---|---|
| cold release: every cycle to the first beat has gmPresent | the published flags leave gmPresent to the microcode (:443 RTL); the image does not mark thisClock grandmaster-capable (:454 ROM) | `got 000000000024a15d exp 0000000000000000` |
| cold release: that commit's flags are gmPresent alone | :443; :454 | `got 0000000000000000 exp 0000000000000001` |
| warm reset: its flags are gmPresent alone | :443; :454 | `got 0000000000000000 exp 0000000000000001` |
| peer leaves: the mastership commit has gmPresent | :443; :454 | `got 0000000000000000 exp 0000000000000001` |
| Pdelay loss: the drop commit's flags are gmPresent alone | :443; :454; the asCapable drop keeps the flags word (:429 ROM, reviewer's `drop_keeps_flags`) | `got 0000000000000000 exp 0000000000000001` / `got 0000000000000009 exp 0000000000000001` |
| Pdelay loss: once capable, with no Announce, master in 3 s | an incapable port's receipt watch is not re-armed (:435 ROM, reviewer's `held_no_rearm`) | `got 0000000000000000 exp 0000000000000001` |
| Pdelay loss: that mastership names thisClock, {thisClock} | :435; the self publication keeps the departed grandmaster (:388); ... departed path (:395) | `got 0000000000000000 exp 0000000000000001` |
| Pdelay loss: that mastership commit has gmPresent | :443; :454 | `got 0000000000000000 exp 0000000000000001` |
| p1 255: cold release: every cycle to the first beat has gmPresent | the capability mark ignores priority1 (:463 ROM) | `got 000000000024a15d exp 0000000000000000` |
| p1 255: cold release: that commit's flags are gmPresent alone | :463 | `got 0000000000000001 exp 0000000000000000` |
| p1 255: Pdelay loss: the drop commit's flags are gmPresent alone | :463; :429 | `got 0000000000000001 exp 0000000000000000` / `got 0000000000000009 exp 0000000000000000` |
| p1 255: Pdelay loss: once capable, with no Announce, master in 3 s | :435 | `got 0000000000000000 exp 0000000000000001` |
| p1 255: Pdelay loss: that mastership commit has gmPresent | :463; mastership sets the microcode's presence bit (:470 ROM) | `got 0000000000000001 exp 0000000000000000` |

The fourth pass also runs the existing boot, mastership and phase-36 checks under the `p1 255 `
prefix; "master flags" there expects `0x6` and fails `got 07` under :470 and at round 2.

Non-vacuity (`receipts/r3/controls/head-harness-on-*.log`), the head harness against older RTL and ROM:
- round-2 head 8f3c376d: shipping `1642 checks: 1638 PASS, 4 FAIL`, exactly the four gmPresent
  checks of reset, warm reset and the drop; fourth pass `46 checks: 44 PASS, 2 FAIL` ("master
  flags" and the mastership gmPresent). Its no-Announce mastership already worked and is now graded.
- base b9ade3a6: shipping 1622 PASS, 20 FAIL; fourth pass 33 PASS, 13 FAIL.

### Repository gates (Verilator 5.050 pinned first on PATH, TMPDIR in scratch, never piped)

Head ran in the lane from `make clean` (the tracked `syn/ooc/work/gptp_ucode.hex` that `clean`
deletes was restored with `git checkout`; the tree is clean). Base ran in a fresh `git archive`
of b9ade3a6. Every rc file reads 0.

| gate | base b9ade3a6 | head 334e9fe6 |
|---|---|---|
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0, 20 exact | rc 0, 20 exact |
| `make -C tb/verilator/ucpu` | rc 0, 768 | rc 0, 768 |
| `make -C tb/verilator/parser` | rc 0, 337 + 9/9 | rc 0, 337 + 9/9 |
| `make -C tb/verilator/engine run` | rc 0, 1613 x3 | rc 0, 1642 x3 + 46 |
| engine `mutants.py` (foreground parallel shards of its own `main()`) | 9 shards rc 0: 33/33 | 18 shards rc 0: 58/58 |
| `make -C tb/verilator/gaskets` | rc 0, 81 + 5/5 | rc 0, 81 + 5/5 |
| `make -C tb/tsngen` | rc 0, 288 + 4/4 | rc 0, 288 + 4/4 |
| `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |

### Parent consumer gates (milan-fpga dev e9cbb676, scratch copy, push URL disabled)

Head column: a fresh local branch on dev e9cbb676 with two local commits, never pushed:
1687cf53 pins the gitlink at 334e9fe6, re-points the same eight gPTP docs from e4869fd0 and adds
the one ROM-ledger row `--record-rom-digests` writes (`334e9fe6... gptp_ucode.hex ceb04562...`);
c7c60bae carries the round-2 milan_dp test update unchanged. `GITLINK` reads ` 334e9fe6...` with no
index or worktree prefix, and no gate printed `REFUSED`. Before every git command in a submodule
its `rev-parse --show-toplevel` was checked. Tools: Verilator 5.050, Yosys 0.66 (86f2ddeb), sv2v
v0.0.12, the tsn-gen oracle built at deca300c. Base column: dev as is, from round 2 (same inputs;
not re-run this round).

| consumer gate | base (round 2) | head (1687cf53 + c7c60bae) |
|---|---|---|
| `syn/yosys/run.sh --mode elaborate --no-structural` (3 tops) | rc 0; 74511 / 61944 / 3368 | rc 0; 74575 / 61944 / 3432 |
| `scripts/lint_rtl.py --check --self-test` | rc 0 | rc 0 |
| `check_port_contracts.py` + `--selftest` | rc 0 / rc 0 | rc 0 / rc 0 |
| `check_wire_accountability.py --self-test` | rc 0 | rc 0 |
| `check_gptp_docs.py` + `--selftest` | rc 0 / rc 0 | rc 0 (8 pages) / rc 0 (30) |
| `syn/yosys/ooc.sh tcam` (ROM ledger) | rc 0 | rc 0 |
| `sw/builder/test_clock_contract.py` | rc 0 | rc 0 |
| `gptp_shadow run` / `lifecycle` | rc 0, 309 / PASS | rc 0, 309 / PASS |
| `gptp_shadow mutants` | rc 0, controls 9, failures 0 | rc 0, controls 9, failures 0 |
| `gptp_tables` (limits, run, mutants) | rc 0: 36; controls 26, failures 0 | rc 0: 36; controls 26, failures 0 |
| `gptp_txts run` / `mutants` | rc 0, 85 / 6, 0 | rc 0, 85 / 6, 0 |
| `gptp_plane run` / `phc-step` | rc 0, 29 / 62 + 8 | rc 0, 29 / 62 + 8 |
| `tsn_fuzz ptp` | rc 0, 677/0/0, freshness 1/1 | rc 0, 677/0/0, freshness 1/1 |
| `milan_dp gptp` | rc 0, 182/182 | rc 0, 182/182 (dev tests: rc 2, 179/182, the same three as round 2) |
| `milan_dp gptp-lat` | rc 0, 182/182 | rc 0, 182/182 |
| `milan_dp gmstep` | rc 0, 190, 0 failures | rc 0, 190, 0 failures |

tsn_fuzz rewrote the timestamp line of `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`; a copy is
kept and the file was reverted. The parent tree is clean at c7c60bae.

Not run, recorded: the nightly physical gPTP job, the full `milan_dp` sweep, `capture_coherence`,
the media-clock suites and `sw/builder/test_builder.py` (as in round 2); Vivado `make ooc`; the
synthesis proxy (this round adds one OR of a configuration-constant ROM bit; parent elaboration
grows by two cells in `milan_datapath` and `KL_gptp_shadow`).

### Known limits after round 3

- 10.3.13.2.4 a) also ages a vector on sync receipt timeout when gmPresent; the 375 ms timeout
  still only clears sync-ok (unchanged).
- With priority1 255 (not the default), an elected peer whose own priority1 is 255 still
  publishes gmPresent 1: BTCA's adoption sets bit 0 for any elected peer, as at base.
- The parent identity is 0 after reset and thisClock after mastership or a drop (unchanged).
- An Announce naming grandmasterIdentity 0 publishes GM 0 with gated path (unchanged).

### Process notes

- Superseded local head efa5e612: its arm reported two existing controls whose pattern named
  BECOME's flags line, which this round changed (`pattern appears 0 time(s)`,
  `receipts/r3/gates/superseded-efa5e612/`). Both were re-pointed at the new line with the same
  defects, folded into the test commit, and every gate was re-run at 334e9fe6.
- Development arm runs and the meta-run ran on the working tree before the commits
  (`receipts/r3/controls/dev-*.log`); the authoritative arm is the head column above.
- One reviewer-probe log was first written into the lane's working directory (an ignored `*.log`);
  it was moved to scratch before any gate ran, and the lane is clean.
- In the scratch parent I ran `git push --dry-run` once to confirm its push state; it stopped at
  "no upstream branch". Nothing was sent; the push URL is `DISABLED-no-push`.

### Posting

- REVIEW READY: issue #82 issuecomment-6255577416, "[A649] REVIEW READY 334e9fe64dfff5568be58a0dc9aeb302959b3b58" (2026-10-18T21:50:28Z).
- No TAKEN repost, no push, no PR edit, no parent push; the two scratch parent commits stay local.

## Round 2 (head 8f3c376d)

Status: REVIEW READY at head 8f3c376d1e07d2f1417889ae2ac590c71b8cb910, with one consumer-side
residue described under "Parent consumer gates": three plane-on parent checks assert the
pre-#82 boot zeros and need the same update the pin bump makes to the docs and ROM ledger.

- Assignment: PR #83 issuecomment-6251117177, reviews R651-1 (6250976384) and R650-1 (6251114151).
- Branch 82-boot-gm-thisclock. Round-2 commits on 85373de0 (the PR #83 head), local, not pushed:
  - f29094ce Load thisClock at reset from ROM data and drop retained or incapable peers
  - ff62370c Grade the release interval, post-reset selection and both departures with planted mutants
  - 8f3c376d Document the reset-time publication and the two departure rules
- Base: b9ade3a63d1b2292d75eb9b1809647e6439542a0 (same tree as the parent pin e4869fd0).
- Head tree 359e2e2518117b70fd1efd4287ecf2888a61d102.
- Receipts: `receipts/` in this directory; `RECEIPTS.md` indexes every file exactly.

### What changed, by item

1. Cold start (R651-1-F1, R650-1-F1). thisClock is now ROM data: the generator writes its high
   and low 32 bits at the two fixed words 1022 and 1023. The engine reads them from the same
   `UCODE_HEX_P` image at configuration (a never-written copy, read at two constant indexes),
   so reset itself loads the self tuple into the publication bank: GM thisClock, count 1, zero
   tail. Parent identity and flags keep their reset values. The engine commits that state once,
   on the first clock edge after release (no handler can run that early, so the round-1 idle
   and cancel guards are gone). The init leg installs S_CID from publish word 15, which serves
   the same value, so the ROM holds thisClock once. No port, parameter or width changed
   (declarations without comments: sha256 ccf818c7... at pin e4869fd0, base, round 1 and head).
   STOP check: not met. What the parent does see: the ROM digest changes (a new ledger row) and
   the boot publication is thisClock instead of zero.
2. Capability loss (R651-1-F2). 802.1AS-2020 10.3.12 DISABLED: a port that is not asCapable
   stops contributing its vector at once. Every flags write that clears bit 2 now expires the
   Announce receipt watch (timer slot 2) in RTL, whichever handler cleared it. BECGATE then:
   a master keeps no watch; a capable port becomes master as before; an incapable port with an
   elected peer (present, not master) drops it, writes flags 0 and runs SELF (thisClock as GM
   and parent, best record to our vector, path {thisClock}, one COMMIT) with no PHC write, so
   the #75 slew contract ("asCapable loss holds level and rate") is untouched. BECOME now ends
   in SELF too, and BTCA's own-vector win branches to BECGATE (same semantics, six words less).
   Announce silence with Pdelay answering still ages the peer out at the 3 s receipt timeout.
3. Warm reset (R651-1-F3, R650-1-F2). The best record (scratch 2, 3, 20) gets reset-backed
   validity, the established claim/pairing idiom: until its first write since reset each cell
   reads all ones, the worst vector, which any received Announce displaces before BTCA weighs
   our own vector against it. The scratch read address stays the write address (single-port
   LUTRAM kept). Reset also clears the raw selected path. The init leg no longer seeds the
   record. The phase-35 comment R651 flagged is rewritten.
4. R650-1-F3: exactly one engine commit per reset is graded at cold and warm reset, and the
   warm-reset self tuple after a three-entry peer is graded for count 1 and a zero tail.
5. Parent mutation gates: committed locally (never pushed) in a scratch parent; both mutant arms
   ran to completion. See the parent table.
6. Receipts: everything cited is under `receipts/`; `RECEIPTS.md` lists each file with size and
   sha256, and the three large synthesis logs kept in scratch by sha256 and size.
7. R650-1-R1 applied in PR-BODY.md.

ROM: shipping image 1,013 of 1,024 words used (98.9%, incl. the two data words), seeded images
1,014; 11 and 10 free (`receipts/rom/layout-head.txt`; base 1,016/1,017 in `layout-base.txt`).
Default-argument image sha256 00826e9b... (was a435fba6...). All four tracked images regenerated.

### Changes (file:line at head)

- `hdl/top/KL_gptp_engine.sv`
  - `:29-31` region map adds publish word 15 (same three lines); `:121` port comment (same line).
  - `:160-171` `ROM_CID_HI_C/LO_C`, `cid_img_r`, `$readmemh`, `rom_clock_id_w`.
  - `:255-262` best-record validity; `:759-762` an unwritten cell reads `'1`; `:777` word 15.
  - `:704-707` raw-path comment; `:793-797` boot commit comment.
  - `:811-821` reset loads GM thisClock, count 1, zero tail; `:839-841` validity reset.
  - `:849-850` one-shot boot commit; `:856` new assertion (S_CID equals the ROM words).
  - `:909-915` validity set on the three writes; `:928-937` asCapable-fall receipt-watch expiry.
  - `:1021-1030` outputs restored to the base form (raw bank, zero-GM gating), plus the commit OR.
- `hdl/ucode/gen_gptp_ucode.py`: `:7-20` #82 notes; `:409-416` `ROM_CID_*`, `PUB_CID_C`;
  `:473` `clock_identity`; `:1364-1368` init reads word 15 (best seed writes removed);
  `:1663-1667` BTCA `we_win` -> BECGATE; `:1670` BECGATE; `:1706` BECOME; `:1729` SELF;
  `:2108` leg list; `:2150-2162` gaps end before the data words; `:2184-2189` data words.
- Four tracked images: `syn/ooc/work`, `tb/tsngen`, `tb/verilator/engine`, `tb/verilator/ucpu`.
- `tb/verilator/engine/sim_main.cpp`: header `:21-25`, `:144-155`; cold-release monitor
  `:413-420`, `:549-556`, `:1146-1150`, `:1175-1176`; pre-init check now "GM stays thisClock"
  `:1167`; phase 1d `:1196`; helpers `:4783`, `:4788`; phase 35 `:4806`; phase 36 `:4875`;
  run-wide invariant `:4929`; bounded commit record `:413`, `:558-560`.
- `tb/verilator/engine/mutants.py`: `:292-420` the 19 #82 controls; `:239-241` a stale packing
  comment corrected (BTCA now has room).
- Docs: `docs/INTEGRATION.md` (reset list; "Before any peer", "Selection after reset",
  "Departure of the elected peer"; image note), `docs/HDL_DEVELOPER.md` (regions, validity,
  flag hook, ROM shape, publication invariant), `docs/TEST_DEVELOPER.md`, `docs/MANAGER.md`
  (ROM budget), `docs/SOURCE_EVIDENCE.md` (13 anchors moved; 20 exact).

### New checks, controls, failing words

Each check below is graded on all three images. A #82 control must fail every check it names
(`mutants.py` rule from round 1). Failing words are from the head arm
(`receipts/gates/head/engine-mutants-s*.log`).

| check | control (`mutants.py` line) | failing words |
|---|---|---|
| cold release: every cycle to the first beat names thisClock | reset leaves the grandmaster zero (:295 RTL); the thisClock words are read swapped (:307 ROM) | `got 000000000024a15d exp 0000000000000000` (bad cycles) |
| cold release: every cycle to the first beat has {thisClock} | GM zero (:295); reset leaves the path empty (:314 RTL) | `got 000000000024a15d exp 0000000000000000` |
| cold release: one commit before the first beat | no engine commit after reset (:328); fires twice (:333); never retires (:340), all RTL | `got 0000000000000000` / `...0002` / `...0f4240 exp 0000000000000001` |
| cold release: that commit is the first edge after release | waits for the timer bootstrap (:345 RTL) | `got 0000000000000100 exp 0000000000000000` |
| cold release: that commit carries thisClock and {thisClock} | GM zero (:295); swapped (:307); path empty (:314) | `got 0000000000000000 exp 0000000000000001` |
| warm reset: one commit in the first 2 ms | no commit (:328); fires twice (:333) | `got 0000000000000000` / `...0002 exp 0000000000000001` |
| warm reset: that commit is the first edge after release | waits (:345) | `got 0000000000000100 exp 0000000000000000` |
| warm reset: it names thisClock, not the elected peer | GM zero (:295); reset keeps the elected grandmaster (:303 RTL) | `got 0082a0fffe000001 exp 02a1b2fffec3d4e5` |
| warm reset: its path is {thisClock} with a zero tail | path empty (:314); reset keeps the elected tail (:322 RTL) | `got 0000000000000000 exp 0000000000000001` |
| warm reset: a worse-than-local peer leaves thisClock | a warm reset keeps the retained best record (:354 RTL); an unwritten best record reads as the best vector (:362 RTL) | `got 0000000000000000 exp 0000000000000001` |
| warm reset: the live worse peer wins, not the absent A | retained record (:354); best-vector read (:362); a winning peer's grandmaster is not published (:371 ROM) | `got 0082a0fffe000001 exp 0082b0fffe000001` |
| warm reset: the live peer carries its own path | retained record (:354); a winning peer's path is not staged (:376 ROM) | `got 0000000000000000 exp 0000000000000001` |
| peer wins: its commit names the peer GM (kept) | GM not published (:371) | `got 02a1b2fffec3d4e5 exp 0082a0fffe000001` |
| peer wins: its commit carries the peer path (kept) | path not staged (:376) | `got 0000000000000000 exp 0000000000000001` |
| peer leaves: the mastership commit names thisClock (kept) | the self publication keeps the departed grandmaster (:382 ROM) | `got 0082b0fffe000001 exp 02a1b2fffec3d4e5` |
| peer leaves: the mastership commit path is {thisClock} (kept) | the self publication keeps the departed path (:388 ROM) | `got 0000000000000000 exp 0000000000000001` |
| Pdelay loss: thisClock is committed within 2 ms of the fall | an asCapable fall leaves the receipt watch running (:401 RTL); an incapable receipt timeout keeps the elected peer (:410 ROM); self keeps GM (:382) | `got 0000000000000000 exp 0000000000000001` |
| Pdelay loss: that commit carries {thisClock} | self keeps path (:388); incapable timeout (:410) | `got 0000000000000000 exp 0000000000000001` |
| Pdelay loss: Announces from the incapable port elect nothing | an incapable port's Announces still compete (:417 ROM); incapable timeout (:410) | `got 0000000000000000 exp 0000000000000001` |
| Pdelay loss: once capable, a live peer worse than D wins | the self publication keeps the departed record (:394 ROM) | `got 0000000000000000 exp 0000000000000001` |
| every commit naming thisClock carries {thisClock} (whole run) | keeps the elected tail (:322); self keeps path (:388) | `got 0000000000000002` / `...000c exp 0000000000000000` |
| pre-init deep Announce: GM stays thisClock (was "GM stays empty") | GM zero (:295) | `got 0000000000000000 exp 02a1b2fffec3d4e5` |
| pre-init deep Announce: no commit (baseline now after the boot commit) | waits (:345) | `got 0000000000000001 exp 0000000000000000` |

All checks carry the `#82 ` prefix except the two pre-init ones. Engine suite: 1,634 checks per
image (round 1: 1,623; base: 1,613). Measured: the cold commit lands on the first edge after
release (0 cycles); the Pdelay-loss drop commits 1,970 cycles (0.985 ms at 2 MHz) after the
commit that publishes the fall; 448 commits of the whole run are graded for the self path.

A removed round-2 candidate check ("no commit has a tail entry beyond its count") had no control
that could fail it: its only stale-tail control trips the RTL assertion and aborts the run
first, and the existing "parent refresh clears old tail" checks already catch that defect. A
removed candidate assertion (boot commit while busy) aborted runs before named checks. Neither
is in the head.

Non-vacuity controls (`receipts/controls/`), the head harness against older RTL and ROM:
- base b9ade3a6: `1634 checks: 1617 PASS, 17 FAIL`, exactly the 15 cold, warm, selection and
  Pdelay-loss checks plus the two pre-init ones.
- round 1 85373de0: `1634 checks: 1623 PASS, 11 FAIL`: cold interval (first edge at
  `000000000024a15c` = 2,400,604 cycles), the three post-reset selection checks, the four
  Pdelay-loss checks, and the pre-init GM. Its warm-reset commit, uniqueness and tail pass.

R651-1 reproducers (`receipts/r651/`): `scripts/r651_probes.py` reproduces R651-1's probe body
and consumer-edge monitor verbatim (its pinned-revision assertion and mutant campaign left out).
- round 1: cold `5 checks: 2 PASS, 3 FAIL` (release_delta 2400604), gone `24 PASS, 2 FAIL`, warm
  `25 PASS, 1 FAIL`: line for line the published control logs.
- head: cold `5 checks: 5 PASS` (release_delta 0, GM thisClock count 1 at release+2), gone
  `28 checks: 28 PASS` (thisClock count 1 after 7 s), warm `28 checks: 28 PASS` (B elected).
  Consumer-edge tuples coherent and one-cycle pulses in all three.

### Repository gates (Verilator 5.050 pinned first on PATH, TMPDIR in scratch, never piped)

Both columns started from `make clean`; the tracked `syn/ooc/work/gptp_ucode.hex` that `clean`
deletes was restored with `git checkout`, and both trees were clean afterwards.

| gate | base b9ade3a6 | head 8f3c376d |
|---|---|---|
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0, 20 exact | rc 0, 20 exact |
| `make -C tb/verilator/ucpu` | rc 0, 768 | rc 0, 768 |
| `make -C tb/verilator/parser` | rc 0, 337 + 9/9 | rc 0, 337 + 9/9 |
| `make -C tb/verilator/engine run` | rc 0, 1613 x3 | rc 0, 1634 x3 |
| engine `mutants.py` (foreground shards of its own `main()`) | 6 shards rc 0: 33/33 | 8 shards rc 0: 52/52 |
| `make -C tb/verilator/gaskets` | rc 0, 81 + 5/5 | rc 0, 81 + 5/5 |
| `make -C tb/tsngen` (default oracle checkout, as round 1) | rc 0, 288 + 4/4 | rc 0, 288 + 4/4 |
| `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |

### Parent consumer gates (milan-fpga dev e9cbb676, scratch copies, push URL disabled)

Base column: dev as is (gitlink e4869fd0). Head column: local commit e54c7c21 on dev (gitlink
8f3c376d, the eight parent gPTP docs re-pointed from e4869fd0 to 8f3c376d, and the ROM-ledger
row `--record-rom-digests` adds: `8f3c376d... gptp_ucode.hex 00826e9b...`). Nothing was pushed.
Before every git command in a submodule its `rev-parse --show-toplevel` was checked. Tools: the
pinned Verilator 5.050, Yosys 0.66 (86f2ddeb), sv2v v0.0.12, tsn-gen oracle built at deca300c.

| consumer gate | base | head (e54c7c21) |
|---|---|---|
| `syn/yosys/run.sh --mode elaborate --no-structural` (3 tops) | rc 0; 74511 / 61944 / 3368 cells | rc 0; 74573 / 61944 / 3430 |
| `scripts/lint_rtl.py --check --self-test` | rc 0, 90 <= 90 | rc 0, 90 <= 90 |
| `check_port_contracts.py` + `--selftest` | rc 0 / rc 0 | rc 0 / rc 0 |
| `check_wire_accountability.py --self-test` | rc 0 | rc 0 |
| `check_gptp_docs.py` + `--selftest` | rc 0 (8 pages) / rc 0 (30) | rc 0 (8 pages) / rc 0 (30) |
| `syn/yosys/ooc.sh tcam` (ROM ledger) | rc 0 | rc 0 |
| `sw/builder/test_clock_contract.py` | rc 0 | rc 0 |
| `gptp_shadow run` / `lifecycle` | rc 0, 309 / PASS | rc 0, 309 / PASS |
| `gptp_shadow mutants` | rc 0, controls 9, failures 0 | rc 0, controls 9, failures 0 |
| `gptp_tables` (limits, run, mutants) | rc 0: 36; controls 26, failures 0 | rc 0: 36; controls 26, failures 0 |
| `gptp_txts run` / `mutants` | rc 0, 85 / 6, 0 | rc 0, 85 / 6, 0 |
| `gptp_plane run` / `phc-step` | rc 0, 29 / 62 + campaign 8 | rc 0, 29 / 62 + campaign 8 |
| `tsn_fuzz ptp` | rc 0, 677/0/0, freshness 1/1 | rc 0, 677/0/0, freshness 1/1 |
| `milan_dp build-gptp exec-gptp` | rc 0, 182/182 | dev tests: rc 2, 179/182; updated tests: rc 0, 182/182 |
| `milan_dp gptp-lat` | rc 0, 182/182 | dev tests: rc 2, 179/182; updated tests: rc 0, 182/182 |
| `milan_dp gmstep` | rc 0, 190, 0 failures | rc 0, 190, 0 failures |

The residue. `tb/verilator/milan_dp/sim_gptp.cpp:825,826,835` (shared by `gptp` and
`gptp-lat`) assert the boot state #82 removes: "Before any peer answers, the engine's committed
bank is zero". At head they read `fabric GM low/high overrides SW got 00000000fec3d4e5 /
0000000002a1b2ff exp 0` and `compatibility CLKV fields read zero got ...0002`, where bit 3 is
the discontinuity holdover that the boot GM edge (0 to thisClock) arms in KL_ptp_clock_validity.
A second local commit 3d0cae2b expects thisClock and masks bit 3 out of the compatibility field
(`receipts/parent/milan_dp-test-update.diff`); with it both legs are 182/182 at head. Against the
base engine the updated test fails the two GM checks (`got 0 exp ...`, 180/182,
`receipts/pgates/base/milan_dp-gptp-updated-tests.log`), so it now grades #82. Not a STOP: no
interface or parameter changed; the value the parent sees at boot is the requested one.

Not run, recorded:
- `milan_dp_gptp` (the physical gPTP job, about 46 min of simulation, nightly, outside the PR
  aggregate). By reading, `sim_ax1x1gptp.cpp:1197` "reset clears complete public GM" expects 0
  after a mid-run reset and will need the same update (that image's thisClock is
  020000fffe000001).
- The full `milan_dp run` (4800 s; its other cases elaborate with the plane off),
  `capture_coherence`, `milan_dp_mclk`, `milan_dp_render`, and `sw/builder/test_builder.py`.
- `make ooc` (needs Vivado). A synthesis proxy (Yosys `synth_xilinx -flatten` of the engine,
  `receipts/synth/`): RAMB18 3 -> 3, RAM64X1S 64 -> 64, RAM32M 80 -> 80, RAM64M 28 -> 28,
  DSP 4 -> 4, FFs 3,428 -> 3,433; the ROM-word copy folds to constants and scratch stays
  single-port. LUTs 6,688 -> 6,934 in this run; a logic-identical variant (one unused wire) maps
  to 6,751, so LUT counts carry mapping noise of that size.

Process notes:
- An intermediate local candidate e246b905 redirected the scratch read address to serve S_MYPV.
  The synthesis proxy showed it broke single-port LUTRAM mapping, so it was replaced by the
  constant worst-vector read before any posting. Its gate runs are superseded and not cited.
- The engine mutation arm runs past one 10-minute foreground command, so it ran as foreground
  shards of the suite's own `main()` (`receipts/scripts/shard_mutants.py`), each with the clean
  control.
- tsn_fuzz rewrites `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` (timestamp line only); a
  copy is kept and the file was reverted in both parents.

### Known limits, unchanged here

- 10.3.13.2.4 a) also ages a vector on sync receipt timeout when gmPresent; the 375 ms timeout
  still only clears sync-ok. Not part of this assignment.
- gm_present (flags bit 0) is 0 at boot and after a dropped peer, though GM is thisClock.
- The parent identity is 0 after reset and thisClock after BECOME or a drop.
- An Announce naming grandmasterIdentity 0 publishes GM 0 with gated path, as at base.

### Posting

- REVIEW READY: issue #82 issuecomment-6254165902, "[A649] REVIEW READY 8f3c376d1e07d2f1417889ae2ac590c71b8cb910" (2026-10-18T19:28:54Z).
- No TAKEN repost, no push, no PR edit, no parent push; the two scratch parent commits stay local.

## Round 1 record (head 85373de0)

Status: REVIEW READY at head 85373de0. The cold-start residual is described under Acceptance.

- Repository: Mister-M-alt/FPGA-gPTP, branch 82-boot-gm-thisclock (local only, not pushed)
- Base: b9ade3a63d1b2292d75eb9b1809647e6439542a0 (main; same tree as the parent's pin e4869fd0)
- Head: 85373de08a5c35487f260087ac8ceaf7a3789cdc
  - dafc34c0 Publish thisClock and {thisClock} from reset until a peer is elected
  - 45f78e38 Grade the boot, winning-peer and departed-peer publication with planted mutants
  - 85373de0 Document the boot grandmaster publication

### Design

- The parent shadow (`hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`, `publication_commit`, at
  e9cbb676) resets its bank to zero. It copies the engine only on `pub_commit_o`. So the
  engine must (1) name thisClock and {thisClock} on its outputs while no grandmaster has been
  elected since reset and (2) commit that state.
- thisClock exists only as a ROM constant. The RTL takes it from the existing S_CID mirror
  (`local_clock_id_r`), written by the cold init leg and kept over a warm reset.
- The ROM is full (1016/1024; the seeded images use 1017, leaving free words 127, 251-255
  and 319). A ROM-side boot leg would not fit without changing unrelated microcode, so the fix
  is RTL-only and the ROM image is unchanged: sha256 a435fba6... at base and head (default args).
- No new port, no parameter, no width change. The engine's parameter and port declarations,
  comments stripped, are byte-identical at pin, base and head (sha256 ccf818c7...).

### Changes (file:line at head)

- `hdl/top/KL_gptp_engine.sv:118-121`: port comment rewritten in the same four lines (keeps
  every ledger anchor above it), adding the boot rule.
- `:624`, `:661`: the µCPU's COMMIT now drives `ucpu_commit_w`.
- `:681-684`: comment: the reset-cleared GM now publishes thisClock and {thisClock}, not zero.
- `:771-776`: `boot_pub_pend_r`, `boot_pub_commit_r` and their rationale.
- `:798-799`: reset sets the pending flag. `:820-828`: one registered engine commit after
  each reset, once `local_clock_valid_r` is set and `dbg_busy_o` is low (no handler between
  its staging and its COMMIT). A µCPU COMMIT first cancels it.
- `:981-993`: while the raw GM is zero (no election since reset): `pub_gm_id_o` = thisClock
  (or zero before a cold start installs it), `pub_path_count_o` = 1 (0 before install), tail zero.
  `pub_commit_o = ucpu_commit_w || boot_pub_commit_r`. The raw bank and µcode reads are unchanged.
- `docs/SOURCE_EVIDENCE.md:31`: two anchors moved (L929->L947, L934->L952).
- `docs/INTEGRATION.md:462-498`: new "Before any peer" subsection. `docs/HDL_DEVELOPER.md:176-186`
  extends the publication invariant. `docs/TEST_DEVELOPER.md:109-110` adds two engine-suite lines.
- `tb/verilator/engine/sim_main.cpp`: PubSnap gains `cyc` and `flags`, plus helpers
  `committed_path_is` (:1000) and `first_commit_since` (:1009) and `cold_boot_mark` (:1114).
  There are two new phases, 1d (:1155) and 35 (:4738), and the header map has new entries
  (:21, :143).
- `tb/verilator/engine/mutants.py:291-333`: six #82 controls. `:459-471`: a #82 control must fail
  every check it names.

Timing as seen by the parent: after a warm reset the commit arrives one cycle after release.
After a cold start the commit follows the first one-second timer beat, about 1.2 s after reset,
because that beat's init leg installs thisClock. Before that, outputs and the shadow stay zero,
as at base. This gap is the only residual against "from reset". Closing it needs either the
identity before the first beat, which would be a parameter or port and therefore a STOP, or
ROM space that does not exist.

### New checks, mutants, failing words

There are ten new checks; each runs in all three images (shipping, request seed, Sync seed). A
#82 mutant must fail every check it names, and the arm enforces this (`mutants.py:459-471`).
Non-vacuity of that rule: a meta-run that adds a name the mutant cannot fail reports
`[FAIL] mutant 'becoming grandmaster keeps the departed GM' missed its named check(s): #82 peer wins: its commit names the peer GM`, rc 1.
Failing words are verbatim from the head mutant run.

| new check | mutant (`mutants.py` line) | failing words |
|---|---|---|
| cold boot: a commit lands with the first beat | no engine commit after reset (:312, RTL) | `FAIL #82 cold boot: a commit lands with the first beat got 0000000000000000 exp 0000000000000001` |
| cold boot: first commit names thisClock | boot publication restored to zero (:293, RTL) | `FAIL #82 cold boot: first commit names thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` |
| cold boot: first commit path is {thisClock} | boot publication restored to zero (:293, RTL) | `FAIL #82 cold boot: first commit path is {thisClock} got 0000000000000000 exp 0000000000000001` |
| warm reset: a commit follows the release at once | no engine commit after reset (:312, RTL) | `FAIL #82 warm reset: a commit follows the release at once got 0000000000000000 exp 0000000000000001` |
| warm reset: first commit names thisClock | boot publication restored to zero (:293, RTL) | `FAIL #82 warm reset: first commit names thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` |
| warm reset: first commit path is {thisClock} | boot publication restored to zero (:293, RTL) | `FAIL #82 warm reset: first commit path is {thisClock} got 0000000000000000 exp 0000000000000001` |
| peer wins: its commit names the peer GM | thisClock hides an elected peer (:317, RTL) | `FAIL #82 peer wins: its commit names the peer GM got 02a1b2fffec3d4e5 exp 0082a0fffe000001` |
| peer wins: its commit carries the peer path | an elected peer keeps the self path (:321, RTL) | `FAIL #82 peer wins: its commit carries the peer path got 0000000000000000 exp 0000000000000001` |
| peer leaves: the mastership commit names thisClock | becoming grandmaster keeps the departed GM (:325, ROM) | `FAIL #82 peer leaves: the mastership commit names thisClock got 0082a0fffe000001 exp 02a1b2fffec3d4e5` |
| peer leaves: the mastership commit path is {thisClock} | becoming grandmaster keeps the departed path (:330, ROM) | `FAIL #82 peer leaves: the mastership commit path is {thisClock} got 0000000000000000 exp 0000000000000001` |

Check names in the harness all start with `#82 ` (prefix dropped in the first column).

The three scenarios:
- Boot, no peer: phase 1d (cold reset, `sim_main.cpp:1155`), plus the first half of phase 35,
  a warm reset (`:4738`).
- Peer wins: phase 35. The peer starts from the boot state (raw GM zero after the warm reset),
  with p1 0 and a three-entry PathTrace {GM82, HOP82, SRC82}.
- Peer leaves: phase 35. The Announces stop, asCapable is held, and after the 3 s receipt
  timeout the mastership commit is graded.
- The existing `announce()` helper always sends a one-entry PathTrace. So the win/leave path
  checks use their own three-entry path: a one-entry peer path is indistinguishable from
  {thisClock} by count.

Control at base RTL (new harness, base engine): `1623 checks: 1617 PASS, 6 FAIL`. Exactly the
six boot checks fail. The win and leave checks pass at base, because that behaviour already
existed and is only now graded at the commit.

Measured (scratch copy of the harness that prints the cycle): the cold-start first commit
lands 2,400,604 cycles after reset release at 2 MHz, which is 1.2003 s.

### Repository gates (pinned Verilator 5.050 first on PATH, TMPDIR in scratch, never piped)

| gate | base b9ade3a6 | head 85373de0 |
|---|---|---|
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` (incl. diagrams-check, both selftests) | rc 0, 20 exact anchors | rc 0, 20 exact anchors |
| `make -C tb/verilator/ucpu` | rc 0, 768 | rc 0, 768 |
| `make -C tb/verilator/parser` | rc 0, 337 + mutants 9/9 | rc 0, 337 + mutants 9/9 |
| `make -C tb/verilator/engine run` | rc 0, 1613 x3 | rc 0, **1623 x3** |
| engine `mutants.py`, foreground shards | 6 shards rc 0: 33/33 caught | 8 shards rc 0: **39/39** caught |
| `make -C tb/verilator/gaskets` | rc 0, 81 + 5/5 | rc 0, 81 + 5/5 |
| `make -C tb/tsngen` | rc 0, 288 + 4/4 | rc 0, 288 + 4/4 |
| `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |

Head runs started from `make clean`. The Makefile's `clean` deletes the tracked
`syn/ooc/work/gptp_ucode.hex` (pre-existing); I restored it with `git checkout` and the tree is clean.
`make ooc` needs Vivado and is not a gate here (no CI workflow in this repository).

Process note: `make -C tb/verilator/engine mutants` as one command runs past the 10-minute
foreground limit. A first unsharded base attempt went to the background, and I removed its work
directory while it was still running. That run is void, with no tally. The arm was then run as
foreground shards. A scratch wrapper loads the suite's own `mutants.py`, sets `MUTATIONS[k::n]`
and calls its own `main()`, so each shard includes the clean control.

### Scratch-parent consumer gates (milan-fpga dev e9cbb676)

Setup. The parent was cloned at dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` with all
submodules. The base column is dev's own gitlink `e4869fd0`, whose tree is identical to this
lane's base `b9ade3a6`. For the head column, a second scratch copy has `gptp-processor` fetched
from the lane, checked out at `85373de0`, and staged with `git add` in the index only. Before
every git command in a submodule, I verified that `rev-parse --show-toplevel` named it. No
parent commit was made and nothing was pushed. Tools: Verilator 5.050 (pinned), Yosys 0.66
(sha 86f2ddeb, the CI pin), sv2v v0.0.12 (CI pin). The tsn-gen field oracle was built from
source at the CI pin `deca300c` in scratch. TMPDIR was in scratch.

STOP check: the engine's parameter and port declarations (comments stripped) are
byte-identical at pin, base and head. The shadow's instance is unchanged. The ROM digest is
unchanged (`a435fba6...`, identical to the ledger row for pin `e4869fd0`). No STOP condition
was met.

| consumer gate | base (gitlink e4869fd0) | head (gitlink 85373de0, index only) |
|---|---|---|
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` (CI yosys-elaboration) | rc 0; cells 74511 / 61944 / 3368 | rc 0; cells 74523 / 61944 / 3380 (+12 in the plane) |
| `python3 scripts/lint_rtl.py --check --self-test` (CI verilator-lint, ratcheted) | rc 0, 90 <= ratchet 90 | rc 0, 90 <= ratchet 90 |
| `scripts/check_port_contracts.py` + `--selftest` | rc 0 / rc 0 | rc 0 / rc 0 |
| `scripts/check_wire_accountability.py --self-test` | rc 0 | rc 0 |
| `scripts/check_gptp_docs.py` + `--selftest` | rc 0 (8 pages) / rc 0 (30 controls) | rc 1 / rc 1 as committed: 35 findings, all "donor reference must use gitlink 85373de0, found e4869fd0" (the parent's pin-bump rule). With the eight parent docs re-pointed to the head SHA in scratch: rc 0 (8 pages) / rc 0 (30 controls). Reverted. |
| `syn/yosys/ooc.sh tcam` (ROM-digest ledger keyed by pin) | rc 0 | rc 2 before the pin is recorded (`no recorded content digest for gptp_ucode.hex at gptp-processor pin 85373de0...`, the normal pin-bump refusal). `--record-rom-digests` (scratch) adds exactly one row, `85373de0... gptp_ucode.hex a435fba6...`, the same digest as the `e4869fd0` row. Then tcam rc 0. Reverted. |
| `make -C tb/verilator/gptp_shadow run` | rc 0, 309/309 | rc 0, 309/309 |
| `make -C tb/verilator/gptp_shadow lifecycle` | rc 0, PASS | rc 0, PASS |
| `make -C tb/verilator/gptp_shadow mutants` | rc 0, controls 9, failures 0 | rc 2, `REFUSED: required dependency gitlinks differ from HEAD` |
| `make -C tb/verilator/gptp_tables` (limits + run + mutants) | rc 0: 36 checks; controls 26, failures 0 | limits + run PASS (36 checks); mutants rc 2, the same REFUSED |
| `make -C tb/verilator/gptp_txts run` | rc 0, 85 checks | rc 0, 85 checks |
| `make -C tb/verilator/gptp_txts mutants` | rc 0, controls 6, failures 0 | rc 0, controls 6, failures 0 |
| `make -C tb/verilator/gptp_plane` (run + phc-step) | rc 0 (585 s): 29; phc_step 62; campaign 8 | run rc 0: 29; phc-step rc 0: 62; campaign 8 |
| `make -C tb/verilator/tsn_fuzz ptp` (TSN_GEN_ROOT = pinned oracle) | rc 0, 677 pass, 0 fail, 0 known gaps; freshness 1/1 | rc 0, 677 pass, 0 fail, 0 known gaps; freshness 1/1 |
| `make -C tb/verilator/milan_dp build-gptp exec-gptp` (plane-on datapath leg, GET_AVB_INFO / GET_AS_PATH) | rc 0, 182/182 | rc 0, 182/182 |
| `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 182/182 | rc 0, 182/182 |
| `make -C tb/verilator/milan_dp gmstep` (the milan_dp_gm_steps leg) | rc 0, 190 checks, 0 failures | rc 0, 190 checks, 0 failures |

Not run, recorded rather than hidden:
- The gptp_shadow and gptp_tables mutant arms at head. `private_inputs.py:186-188` refuses
  unless the dependency gitlink is committed in the parent's HEAD, and I am not allowed to
  commit in the parent. They pass at base. Both suites' own checks pass at head.
- `milan_dp_gm_steps`' `gmstep_mutants.py`. The gmstep leg itself ran (above).
- Suites whose driver deadline is beyond a 10-minute foreground command: the full `milan_dp`
  `run` (4800 s), `milan_dp_gptp` / the physical-gptp job (5400 s), `capture_coherence`
  (2400 s), `milan_dp_mclk` (3600 s) and `milan_dp_render`. Most `milan_dp` cases elaborate
  with `GPTP_PLANE_EN_P=0`, where the engine is absent. The plane-on legs `gptp`, `gptp-lat`
  and `gmstep` ran above.
- `publication_census` follows the protocol processor's class-D values, not the gPTP bank.
- The tsn_fuzz and gptp suites rewrite `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` with a new
  timestamp (same `677 pass`). I reverted it in both scratch copies.

Consequence the parent will see (by reading `KL_gptp_shadow.sv` publication_commit; every
suite above passes with it): the boot commit is a GM edge from 0 to thisClock. So
`pub_disc_o` pulses once and `pub_path_gen_o` advances once after each reset.

### Acceptance

- Assignment 1, from reset: met after a warm reset (commit one cycle after release). On a
  cold start it is met from the first timer beat (1.2003 s measured). Before that, the engine
  does not yet hold thisClock, and outputs and shadow stay zero as before. This is the one
  residual, and it is why the PR body says "Refs #82", not "Closes #82". Closing it needs the
  identity at reset (a parameter or port, which is a STOP) or ROM words that do not exist.
- Assignment 1, a better GM takes over, and the instance returns to thisClock when it leaves:
  met and graded (phase 35). The return still requires asCapable at the receipt timeout, as
  before.
- Assignment 2, interface: width and commit timing are unchanged (a single-cycle pulse over
  stable outputs). Cases and mutants exist for boot (cold and warm), win and leave.
- Assignment 3: repository gates rc 0 at base and head. Consumer gates: the table above. Gaps
  are listed under "Not run".
- Assignment 4: no interface or parameter change, so no STOP.

### Known limits, unchanged here

- If asCapable falls before an elected peer's Announces stop, the receipt timeout cannot become
  master (BECGATE). The departed peer then stays published. 802.1AS-2020 10.3.13.2.4 a) would
  age it out regardless.
- From reading the BTCA code (not tested): after a warm reset the scratch best record
  survives. An Announce worse than that retained record takes `they_win` and re-publishes the
  retained GM.
- At boot, gm_present (flags bit 0) stays 0 and the parent identity stays 0, as before.
  Whether gmPresent should follow 10.3.13.2.4 g) at boot is outside this lane.

### Posting

- TAKEN: issuecomment-6249586531.
- REVIEW READY: issuecomment-6250813690 (head 85373de08a5c35487f260087ac8ceaf7a3789cdc).

Not done, by rule: no push, no PR created or edited, no parent commit, no hardware.
Scratch (not in this directory): `<data>/tmp/gptp82-a649/` (parent copies, tsn-gen,
gate logs `gates/` and `pgates/`, control and measurement copies).
