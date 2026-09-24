[A266] REVIEW READY — issue #112 / PR #114, round 1b

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112#issuecomment-5816726610

Repository: `$LANES/pp112-stale-grant`, branch `112-stale-grant`.
Baseline: `73a5478784bd861f8c8d33c0d1619594390b9529`.
Final head: `90e1ce13bb1c49c0c985b64e583128b7b8c6a9c4`.
Commit message: `test: satisfy SRP test idiom gates without changing coverage`.
The commit has one subject line, no body, and no trailers. The checkout is clean.

Only `tb/srp_top/sim_main.cpp` and `tb/srp_admission/mutants.py` changed.
The C++ declarations each introduce one name, and the recorded-cycle checks
are extracted into `check_redeclaration_samples`, which does not advance the
simulation. The Python entry point now has an `int` return annotation and a
docstring. Stimuli, assertion expressions, ordering, expected values, printed
output, and RTL are preserved. See [change.patch](change.patch) and
[source-equivalence.log](source-equivalence.log).

Both runs completed every normal check with zero failures:

| Suite / shape | Before checks / PASS / FAIL | After checks / PASS / FAIL |
|---|---:|---:|
| SRP top | 735 / 735 / 0 | 735 / 735 / 0 |
| SRP decoder | 190 / 190 / 0 | 190 / 190 / 0 |
| SRP encoder | 556 / 556 / 0 | 556 / 556 / 0 |
| SRP stream FSMs | 1068 / 1068 / 0 | 1068 / 1068 / 0 |
| Admission N=1 | 683 / 683 / 0 | 683 / 683 / 0 |
| Admission N=2 | 5252 / 5252 / 0 | 5252 / 5252 / 0 |
| Admission N=3 | 20053 / 20053 / 0 | 20053 / 20053 / 0 |
| Admission N=5 | 123286 / 123286 / 0 | 123286 / 123286 / 0 |
| Admission N=8 | 723046 / 723046 / 0 | 723046 / 723046 / 0 |
| Full bank, 33 suites | 739421 / 739421 / 0 | 739421 / 739421 / 0 |
| Mutation campaign | 4 / 4 / 0 | 4 / 4 / 0 |

Commands ran in the foreground, with a 7200-second timeout for each repository
validation command. Standard output and error went directly to log files;
the suite bank and lint commands were never piped. Both runs returned rc 0 for:

```sh
bash scripts/run_suites.sh
make -C tb/srp_admission shapes
bash scripts/lint_hdl.sh
python3 tb/srp_admission/mutants.py --output <output-directory>/<before-or-after>-mutants
```

Lint passed all 40 modules before and after. After each build, the SRP top
binary and all five admission binaries were also run directly, each with rc 0,
to capture their complete output independently of build messages.
The bank summaries, lint output, six direct simulation outputs, mutation
campaign output, and all four mutant/control runtime outputs are byte-for-byte
identical before and after. [output-comparison.log](output-comparison.log)
records each comparison and SHA-256; [output-comparison.json](output-comparison.json)
contains both hashes. Commands, return codes, durations, and log paths are in
[before-results.json](before-results.json) and [after-results.json](after-results.json).
The latter records the final head for every command.

The mutant results are unchanged:

| Case | Before checks / PASS / FAIL | After checks / PASS / FAIL | Before / after make rc |
|---|---:|---:|---:|
| Control N=2 | 5252 / 5252 / 0 | 5252 / 5252 / 0 | 0 / 0 |
| Stale evaluation N=2 | 5252 / 5068 / 184 | 5252 / 5068 / 184 | 2 / 2 |
| Control N=8 | 723046 / 723046 / 0 | 723046 / 723046 / 0 | 0 / 0 |
| Stale evaluation N=8 | 723046 / 719014 / 4032 | 723046 / 719014 / 4032 | 2 / 2 |

Both mutants reached the simulation and failed the required
`refused current TSpec never pulses a grant` assertion: 82 occurrences at N=2
and 1984 at N=8, unchanged. The campaign returned rc 0 with 4 PASS / 0 FAIL.
Raw logs are under [before-mutants](before-mutants/) and [after-mutants](after-mutants/).

Parent gate evidence comes exclusively from
`$LANES/pp112-parent-consumer`, parent head
`54112923417837dffc8722890e2beb733468f441`, using Rules 11 and 12 in
`docs/development/CODE_QUALITY.md`:

| Gate | Baseline rc and findings | Final-head rc and targeted findings |
|---|---|---|
| `python3 scripts/check_cpp_idiom.py` | rc 1; 3 multi-declarator declarations, 1 long function | **rc 0**; both populations 0 |
| `python3 scripts/check_py_idiom.py` | rc 1; 1 unannotated and 1 undocumented public function | **rc 0**; both populations 0 |

The C++ gate examined 152 first-party translation units; the Python gate
examined 234 first-party modules. Both final runs used the final head
`90e1ce13bb1c49c0c985b64e583128b7b8c6a9c4` as both the checked-out child and
the staged parent gitlink, prepared with:

```sh
git -C protocol-processor fetch $LANES/pp112-stale-grant HEAD
git -C protocol-processor checkout --detach FETCH_HEAD
git add protocol-processor
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
git reset -q protocol-processor
git -C protocol-processor checkout --detach 73a5478784bd861f8c8d33c0d1619594390b9529
```

Gate commands had 600-second timeouts. The parent index and detached child
checkout were restored to their initial state; both are clean and parent HEAD
is unchanged. Evidence: [gitlink preparation/restoration](after-parent-gitlink.log),
[C++ gate](after-parent-cpp-idiom.log), [Python gate](after-parent-py-idiom.log),
and [gate return codes and heads](after-parent-results.json).
Baseline failure logs are [C++](before-parent-cpp-idiom.log) and
[Python](before-parent-py-idiom.log).

`git diff --check 73a5478784bd861f8c8d33c0d1619594390b9529 HEAD` returned rc 0.
No push, PR edit, merge, parent commit, delegation, or hardware operation was
performed. No open blocker remains for this test-code-only assignment.
