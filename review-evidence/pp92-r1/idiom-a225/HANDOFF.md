# [A225] HANDOFF — PR #109 (issues #92/#93): parent idiom gates, pre-review fix

- Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`, PR #109
- Branch: `92-93-boot-restore` in `$LANES/pp92-93-boot-restore`
- Start head: `69a6eac2955204af999ac1b99956c9b0a6f2fbb0` (the PR's pushed head)
- Fixed head: `156c206cbaedf721f7caef5c94faa21876a28c32` — **local only, not pushed**; PR #109
  still points at 69a6eac2. Pushing is the manager's step.
- Parent checked against: `kebag-logic/milan-fpga` dev `26d855a9176d63625e6635a029a0c44e3d57ce9a`,
  in a scratch clone at `scratch/parent` (this directory). Its gitlink was moved to the fixed
  head in a local commit (`e1328fecf`), never pushed. No parent file was changed, and no
  ratchet was widened: `scripts/cpp_idiom.budget` and `scripts/py_idiom.budget` are the
  dev files, byte for byte.

## Commits (one-line subjects, no trailers)

| Commit | Subject |
|---|---|
| `ad9d156` | Give each acmp_nvm bench declaration one name, drop its unused be_get and warn on the pinned build (#92) |
| `cd5a892` | Split the lsn_admit bench's run into its five sections, one name per declaration (#92) |
| `4aa2679` | Move the nvm_port bench's owed-traffic monitor out of sample_dev (#93) |
| `73b070e` | Run pp_top's BW3 read-deadline case as its own section, one name per declaration (#93) |
| `156c206` | Move the nvm_port pre-fix matrix forms and their git pins into their own module (#93) |

`git diff --stat 69a6eac..156c206`: 7 files, +421 −352 (+334 −265 ignoring whitespace; the
lsn_admit sections lost one brace level). No HDL, doc or README file changed.

## What each finding was, and what changed

### C++ gate (`scripts/check_cpp_idiom.py`, Rule 11)

**Multi-declarator declarations, 10 → 0.**

- `tb/acmp_nvm/sim_main.cpp` (6): `drain_on/drain_off`, `exp_from/exp_until`, the four
  `bad_*` and four `first_*` counters of L05s, and the four N6 counters are one name per
  line. `bool txfree[5] = {true, ...}` was not a second declarator but an initialiser the
  gate's pattern reads as one; it is now `std::array<bool, 5> txfree = {true, ...}` (the
  parent's own form, e.g. `std::array<long, 2> leg_slip = {0, 0}` in
  `tb/verilator/chmap_capture`). Every use (`txfree[i]`, `for (bool& f : txfree)`) is
  unchanged; `<array>` is included.
- Also split, though the gate's type list does not see them: four more multi-name
  declarations this PR added in the same file (`txn_pops/txn_takes`, `tk_pops/tk_takes`,
  `why_walk/why_nvm`, and `Bind b0, b7` in the L06 case table, whose aggregate
  initialisation order is unchanged).
- `tb/lsn_admit/sim_main.cpp` (3): the stimulus struct `In` has one member per line (same
  order, still an aggregate, still zeroed by `In{}`); `long coincide[4] = {0, 0, 0, 0}` is
  `long coincide[4] = {}`, which is the same zero initialisation (and the file's own form
  elsewhere, `int txlen[5] = {}`).
- `tb/pp_top/sim_main.cpp` (1): `size_t rd21 = 0, er20 = 0;` is two lines.

**Functions over 100 lines, 3 → 0.**

- `LsnAdmitSuite::run()` (133 lines) now calls its five existing sections as member
  functions — `check_reset_ownership` (R), `check_each_release_term` (T),
  `check_release_is_one_way` (O), `check_refused_expiry_count` (D),
  `check_random_against_the_model` (M) — in the same order, then prints the same tally.
  Each section's body is the old block, dedented; every local stays local to its section
  and every member (`mism`, `first_mism`, the model, the cycle count) is shared exactly as
  before. The longest function in the file is now 38 lines.
- `sample_dev()` in `tb/nvm_port/sim_main.cpp` (107 lines): the bus-side "owed" counters it
  opened with (`req_while_owed`, `pulse_while_owed`, `fwd_while_owed`) are a monitor of the
  port, not part of the device model, and are now `count_owed_traffic()`, called at the
  same point (after the `drove_*` captures, before the command is accepted). `sample_dev`
  is 96 lines. The command-accept block was NOT the piece moved, deliberately:
  `measure_figures.py` patches `sim_main.cpp` by exact text including indentation, and its
  `_LAZY` model anchors on the erase lines inside that block — moving it would have broken
  the figures gate. The figures gate passes unchanged (below).
- `boot_window_at_the_top()` in `tb/pp_top/sim_main.cpp` (142 lines): BW0–BW2 stay; BW3
  (#93's read-deadline case) is `boot_window_read_deadline()`, called straight after it in
  the run list, so it is still last on the main DUT. The only thing BW3 shared with BW0–2
  was the `get_cmd` lambda, which is now the static helper `bw_get_cmd()` beside
  `bw_boot`/`bw_acmp`/`bw_ops`. BW3 declares its own `guard` where it used to reassign
  BW1's. Longest function in the file: 97 lines (pre-existing).

**Build without warnings, 1 → 0.** The finding was `tb/acmp_nvm/Makefile`: the `pinned`
target's second `-CFLAGS` group carried only `-DACMP_NVM_PINNED_WIRING`, and the gate needs
every group to carry `-Wall -Wextra`. It now reads `-CFLAGS "-DACMP_NVM_PINNED_WIRING -Wall
-Wextra"`, the form `tb/dyn_state` and `tb/pp_top` already use for their define-only
groups. The effective compile did not change (Verilator concatenates `-CFLAGS`, so the
pinned build already had the flags from `VFLAGS`), which is also why that build showed the
one real compiler warning in these benches:

- `tb/acmp_nvm/sim_main.cpp:188: 'uint64_t be_get(...)' defined but not used
  [-Wunused-function]`, in both the suite and the pinned build. `be_get` was added with
  #92 and never called; it is deleted. Compiler warnings across the four touched suites'
  builds: 2 → 0 (`logs/before/compiler-warnings.txt`, `logs/after/`).

### Python gate (`scripts/check_py_idiom.py`, Rule 12)

**Long module, 11 → 10.** `tb/nvm_port/measure_figures.py` was 1001 lines (989 at the
parent's pinned 424c688). Taking one line out would have left it at the limit with the
next edit putting it back over, so it is split by subject instead:
`tb/nvm_port/pre_fix_forms.py` (238 lines) now holds the pre-fix matrix's injected forms
and the git pins that prove each injection is the removed code — `MATRIX_FORMS`,
`MATRIX_ROWS`, `GIT_FORMS`, `git_verbatim`, `_check_condition_lines`, `pin_completeness`,
`line_multiplicity`. The moved block is byte-identical to lines 358–574 of the old file
(`diff` in the session; `git diff -M --color-moved` shows it). `measure_figures.py` (788
lines) imports those five names and keeps everything else: `MUTATIONS`, `ARMS`, the models,
every RTL read and write, the matrix measurement, the README coupling. That split was
chosen so the parent's other gates classify the files as before:
`scripts/measure_test_evidence.py` recognises the nvm_port mutation driver by the
`MUTATIONS =` table and records `measure_figures.py` by path as a DUT-source reader; both
stay true, and `pre_fix_forms.py` reads no RTL, rewrites nothing and is not a driver
(checked with the gate's own functions; the parent gate is unchanged, 0 unexplained
readers). `__pycache__/` is already ignored.

The one processor file still in `check_py_idiom --list` is `hdl/aecp/ucode/gen_ucode.py`
(long module), untouched since the parent's pin (2140 lines at 424c688 and at the fixed
head): recorded debt inside the ratchet of 10, not this PR's.

## Behaviour: the benches print what they printed

`tools/capture.sh` clean-built lsn_admit, nvm_port, pp_top (both builds), acmp_nvm and the
acmp_nvm `pinned` control at 69a6eac and at the fixed head, then re-ran every binary alone
and kept its output. **All six outputs are byte-identical** (`logs/before/out-*.txt` vs
`logs/after/out-*.txt`):

| Binary | Output at both heads |
|---|---|
| `acmp_nvm` | 332 checks: 332 PASS, 0 FAIL |
| `acmp_nvm` pinned control | 332 checks: 236 PASS, 96 FAIL — the same 96 FAIL lines |
| `lsn_admit` | 18 checks: 18 PASS, 0 FAIL |
| `nvm_port` | 136 checks: 136 PASS, 0 FAIL |
| `pp_top` default build | 1407 checks, 0 failures |
| `pp_top` VID fixture build | 20 checks, 0 failures |

A passing bench prints only its tally, so the same RTL mutants were also run at both heads
in the scratch clone's processor checkout (`tools/mutant.py`: one exact RTL edit, build,
run each binary, restore; the lane was never mutated). The RTL is identical at both heads,
so any difference would be the benches':

| Mutant (RTL edit) | Bench | Output at 69a6eac vs 156c206 | What fails (same lines at both) |
|---|---|---|---|
| LG01 `own_r <= 1'b1` → `1'b0` (admission gate deleted) | lsn_admit | **identical** | 18 checks: 7 PASS, 11 FAIL, across the R/T/O/D/M sections |
| D-no-saturation `(drop_r != 16'hFFFF)` → `1'b1` | lsn_admit | **identical** | 16 PASS, 2 FAIL: D2, D3 (the extracted D section) |
| A01 manager-0 busy without `iss1_w` | acmp_nvm | **identical** | 331 PASS, 1 FAIL: N6 "(92 did not, first at offset 1)" — the split counters |
| LG01 (as above) | acmp_nvm | **identical** | 236 PASS, 96 FAIL (the same 96 lines as the pinned control) |
| LG01 (as above) | pp_top | **identical** | 1407 checks, 5 failures: BW1 ×4, BW2 — in `boot_window_at_the_top` |
| B01 `rs_tmo_w` → `1'b0` (no read deadline) | pp_top | **identical** | 1407 checks, 2 failures: both BW3 checks — in the split-out `boot_window_read_deadline` |

Outputs: `logs/mutants/{before,after}-<suite>-<mutant>-<binary>.txt`. The scratch checkout was
left clean after every run.

nvm_port's own oracle is its figures gate: every mutation, probe, device model and matrix
cell it re-measures after the `sample_dev` split and the module split agrees with the README
(below).

## Gates

### Parent, scratch clone at dev 26d855a9 (`logs/parent-before/`, `logs/parent-after/`)

| Gate | gitlink 69a6eac2 | gitlink 156c206c |
|---|---|---|
| `check_cpp_idiom.py` | **exit 1**: multi-declarator 10 > 0, long function 3 > 0, build without warnings 1 > 0 | **exit 0**, every ratchet 0 <= 0 |
| `check_cpp_idiom.py --list` | exit 1, four processor files listed | exit 0, **no file listed** |
| `check_py_idiom.py` | **exit 1**: long module 11 > 10 | **exit 0**, long module 10 <= 10, long function 9 <= 9 |
| `check_py_idiom.py --list` | measure_figures.py and gen_ucode.py listed for the processor | only gen_ucode.py (pre-existing, inside the ratchet) |
| `--selftest`, both gates | 75/75, 54/54 | 75/75, 54/54 |
| `check_hygiene.py --check` | PASS | PASS (733 files: the new module) |
| `measure_test_evidence.py --check` | PASS | PASS, identical output |
| `check_sh_idiom`, `check_sv_idiom`, `check_todo_ownership`, `measure_naming --check`, `measure_fail_fast --check` | exit 0 | exit 0 |
| `check_submodule_docs.py` | exit 1 | exit 1, identical output |

`check_submodule_docs` fails at both gitlinks with "protocol-processor: documented pin
differs from Git" and the stale submodule-boundary diagram. That is the scratch gitlink
move itself (the parent's pin-bump change updates those documents), not a processor
finding.

### Processor, lane at the fixed head (`logs/gate-*.log`, `logs/suites/`)

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | exit 0, **31 suites, 15 773 checks, 0 failing**, UPC map PASS |
| every suite from clean (`tools/suites_chunk.sh`, `logs/suites/summary.txt`) | 31 of 31 exit 0, same tallies |
| `make -C tb/nvm_port figures` | exit 0, 35 builds, "all measured figures agree with the tree" |
| `./scripts/lint_hdl.sh` | exit 0 |
| `make check` | exit 0 (lint, wavedrom, links 830, matrix, modmatrix 90 rows / 0 untested, stale) |
| `python3 scripts/gen_matrix.py --check` | exit 0, 90 rows, 0 untested |
| `./syn/yosys/run.sh` | exit 0 |
| `git diff --check 09f9bf38..HEAD` | exit 0, empty |

Simulator: the pinned 5.050 (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin`),
g++ 16.2.1.

## Found and not fixed here, on the record

- `tb/dispatch/sim_main.cpp:608` and `:611` still raise `-Wsequence-point` ("operation on
  'sq' may be undefined": `sq++` and a read of `sq` in the same call). That suite is
  identical on main 09f9bf38 and at the parent's pin 424c688, so it is not this PR's; the
  parent's gate does not count it (its warning ratchet counts Makefiles without the flags),
  and it is the unsequenced-modification defect the parent's Rule 11 page says was found in
  that file. It wants its own issue.
- `sample_dev` is at 96 lines and the pre-existing longest functions in acmp_nvm and pp_top
  are at 97: under the limit, not far under it.

## Reproduce

```sh
export PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH
# processor, from the lane
./scripts/run_suites.sh && make -C tb/nvm_port figures && ./scripts/lint_hdl.sh \
  && make check && python3 scripts/gen_matrix.py --check && ./syn/yosys/run.sh \
  && git diff --check 09f9bf38..HEAD
# parent, from scratch/parent with the gitlink at the fixed head
python3 scripts/check_cpp_idiom.py --list && python3 scripts/check_py_idiom.py --list
# before/after bench outputs and gates
tools/capture.sh TAG; tools/parent_gates.sh TAG PARENT_COMMIT
tools/mutant.py TAG NAME SUITE FILE OLD NEW BIN   # runs in scratch/parent/protocol-processor
```

## Posted

- #92 note: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/92#issuecomment-5805562627
  (text in `NOTE-92.md`). Nothing else was posted; the PR, its body and its head were not touched.

## Next

1. The manager pushes `156c206` to PR #109; reviews R278 and R279 start on that head.
2. The parent's gitlink bump runs the two gates above on the pushed head.
