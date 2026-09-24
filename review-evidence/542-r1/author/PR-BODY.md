[A233]

## Contents

- **[Status](#status)** -- Green, test tally, and `542-notify-pointer` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- The issue and the code it names.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and tool commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GREEN at `68117c0bec0b767d38d9bb1150542e2346b615b7` -- `542-notify-pointer` -> `dev` (base `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`).

- milan_dp legs, plain Makefile recipes: main 230/0, notify 146/0, nxn 1708/0, nxn8 3136/0, plus nxndv 1710/0 and nxn4c 1708/0 (the other two legs that compile `sim_nxn.cpp`). All five `sim_nxn.cpp` legs print byte-identical output to dev `615b5a5d`.
- The new forced-reallocation lever against the **old** checks: notify 2 of 147 FAIL, nxn 1 of 1709 FAIL, exactly the two content bars. AddressSanitizer plus the lever: 4 heap-use-after-free reports at those two bars.
- The lever against the **fixed** checks: notify 147/0, nxn 1709/0. AddressSanitizer plus the lever: 0 sanitizer lines.
- `check_cpp_idiom.py` exit 0 (every ratchet `0 <= 0`), `--selftest` 75/75; `docs_check.py` 0 findings; `git diff --check 615b5a5d7 HEAD` clean.

## Linked Issue / roles

Closes #542

Executor: `[A233]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

**The defect.** `notify_last()` returned a `const std::vector<uint8_t>*` into `uns_log`. Two content bars kept that pointer across `aecp_xact_from()`, whose `await_aecp()` can `push_back` into `uns_log`. A push that meets a full buffer reallocates the vector and leaves the pointer dangling:

- `[NOTIFY]` (N5): `nB2`, returned by `prove_each_registry_entry_has_its_own_sequence()`, read by `notify_same_from(nB2, gB, 38)` after the GET_NAME exchange.
- `[NOTIFY-CRF]`: `n1`, read by `notify_same_from(n1, g, 38)` after the solicited GET_COUNTERS exchange.

Both passed only because no leg happens to push into a full log during those two waits.

| Commit | Change |
|---|---|
| `766b6a1` | **The lever**, compiled in only with `-DNOTIFY_REALLOC_TB`. The only two functions that push into `uns_log` are `await_aecp` and `drain_tx`. On every call, each one now moves the log into a buffer allocated while the old buffer is still live, so the new one cannot land at the old address. It then pushes one empty entry stamped -1 and frees the old buffer. No reader matches an empty entry, so no verdict moves. A lever-only check in `notify_section` fails if the lever never fired. In every Makefile leg it is compiled out (`kForceRealloc = false`). The old checks are untouched in this commit, so this commit **is** the failing demonstration. |
| `6c5fa55` | **The fix.** `notify_last()` returns a copy, empty when nothing matches. `notify_seq()` and `notify_same_from()` take that copy by const reference. The three held results (`nB1`, `nB2`, `n1`) are now copies and the other three call sites use temporaries. No helper hands out a pointer into `uns_log` any more. |
| `68117c0` | The lever's liveness count now counts only moves of a log that holds a real frame. Before this, the lever's own empty entries could satisfy its liveness check. |

**Why a copy, and why it preserves the verdicts.** Every frame `notify_last()` can match passes `aecp_is_unsolicited()`, so it is longer than 37 bytes. An empty copy therefore means exactly what the old null pointer meant. For an absent frame `notify_seq()` still gives -1 and `notify_same_from()` still gives false. The copy is taken where the pointer was taken, so each bar still compares the frame it named **before** the exchange. A re-fetch after the exchange could instead pick up a newer push that arrived during the wait. The plain legs' output is byte-identical to dev.

**Audit of the file.** I checked every pointer or reference into `uns_log` against every call that can push into it. Those calls are `await_aecp` and `drain_tx`, and through them `aecp_xact`, `aecp_xact_from`, `notify_set_name`, `grade_read_desc` and the sections that call those.

- The two holds above: fixed.
- `nB1` (N2) was held only across `ck`, `notify_seq` and `notify_same_from`, none of which pushes. It was never unsafe, and it is a copy now anyway.
- The loop-local `const std::vector<uint8_t>& f = uns_log[i]` in `notify_count`, `notify_last`, `notify_when` and `notify_ctr_when`: the loop bodies call only pure predicates, and nothing in them pushes.
- The N9 CONTROLLER_AVAILABLE lambda indexes `uns_log[i]` and `uns_log_when[i]` and makes no call that pushes.
- `uns_log_when` is only ever read by value.
- Outside the log: `desc_of()` pointers point into the `std::map` `desc_want`. Map nodes stay put when other keys are inserted, and the map is cleared only while the image is built, before any `desc_of()` caller runs. Not a hazard, and unchanged.

The lever build is the executable form of this audit. It frees the log's buffer at every call that can push into it, so any hold across such a call reads freed memory. On the fixed code, every check in the notify and nxn legs gives the same verdict under the lever, and AddressSanitizer reports nothing.

## Authoritative references

- Issue #542: observed evidence and the three acceptance criteria.
- `tb/verilator/milan_dp/sim_nxn.cpp`: `uns_log`, `await_aecp`, `drain_tx`, `aecp_xact_from`, `notify_last`, the `[NOTIFY]` N4/N5 steps and `prove_the_crf_input_counters_push_under_the_one_second_limit`.
- `tb/verilator/milan_dp/Makefile`: the leg recipes, used unchanged.
- CONTRIBUTING.md section 5 and docs/development/CODE_QUALITY.md Rule 11 (the C++ idiom gate).

No RTL, Makefile or documentation file is touched. `hdl/milan/milan_datapath.sv` (held by #530) is untouched.

## How to get into the same state

```sh
git fetch origin
git checkout 542-notify-pointer          # head 68117c0bec0b767d38d9bb1150542e2346b615b7
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
verilator --version                      # 5.050
```

## How to validate

```sh
cd tb/verilator/milan_dp
V=verilator                              # Verilator 5.050
make VERILATOR=$V ltn_rom.hex ucode.hex gptp_ucode.hex
# one leg's build line exactly as `make run` issues it, joined onto one line
recipe() { make -n VERILATOR=$V VERILATOR_JOBS=8 run \
             | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' | grep -E -- "-o Vmilan_dp_$1\$"; }
# build leg $1 into Mdir obj_$1_$2, with the extra Verilator arguments in $3
variant() { local c; c=$(recipe "$1"); c=${c/--Mdir obj_$1/--Mdir obj_$1_$2}
            c=${c/ -o Vmilan_dp_$1/ $3 -o Vmilan_dp_$1}; eval "$c"; }
LEVER='-CFLAGS -DNOTIFY_REALLOC_TB=1'
ASAN='-CFLAGS "-fsanitize=address -fsanitize-recover=address -fno-omit-frame-pointer -g" -LDFLAGS "-fsanitize=address -fsanitize-recover=address"'
export ASAN_OPTIONS=halt_on_error=0:suppress_equal_pcs=0:detect_leaks=1

# 1. the gate legs, unchanged recipes (make run builds and runs the whole suite)
for l in notify nxn nxn8; do variant $l plain ""; ./obj_${l}_plain/Vmilan_dp_$l | tail -2; done
eval "$(recipe sim | sed 's| -o Vmilan_dp_sim| --Mdir obj_sim_plain -o Vmilan_dp_sim|')" && ./obj_sim_plain/Vmilan_dp_sim | tail -3

# 2. the FIXED checks under the lever, and under the lever with AddressSanitizer
variant notify lever "$LEVER" && ./obj_notify_lever/Vmilan_dp_notify | grep '#542 lever\|checks:'
variant nxn    lever "$LEVER" && ./obj_nxn_lever/Vmilan_dp_nxn       | grep '#542 lever\|checks:'
variant notify asan  "$LEVER $ASAN" && ./obj_notify_asan/Vmilan_dp_notify > obj_notify_asan/run.log 2>&1; \
  grep -c 'AddressSanitizer' obj_notify_asan/run.log; grep 'checks:' obj_notify_asan/run.log

# 3. the same lever against the OLD checks (the fix commit reverse-applied)
(cd "$(git rev-parse --show-toplevel)" && git diff 766b6a149 6c5fa5566 | git apply -R)
variant notify oldlever "$LEVER" && ./obj_notify_oldlever/Vmilan_dp_notify | grep 'FAIL\]\|checks:'
variant nxn    oldlever "$LEVER" && ./obj_nxn_oldlever/Vmilan_dp_nxn       | grep 'FAIL\]\|checks:'
variant notify oldasan  "$LEVER $ASAN" && ./obj_notify_oldasan/Vmilan_dp_notify > obj_notify_oldasan/run.log 2>&1; \
  grep -c 'heap-use-after-free on address' obj_notify_oldasan/run.log
git checkout HEAD -- sim_nxn.cpp
```

Expected result / pass criteria:

1. main `230 checks, 0 failures`; notify `checks: 146 failures: 0`; nxn `1708 / 0`; nxn8 `3136 / 0`.
2. notify `checks: 147 failures: 0` and nxn `1709 / 0`. Each prints `[ok] [NOTIFY] (#542 lever) the waits moved logs holding real frames` and has no other difference from its plain run. The ASan run prints `0` sanitizer lines and `checks: 147 failures: 0`.
3. notify fails exactly `[NOTIFY] GET_NAME right after is byte-identical from the body on` and `[NOTIFY-CRF] ...byte-identical from the body on to the solicited answer` (`checks: 147 failures: 2`). nxn fails exactly the first of those (`1709 / 1`). The ASan run reports `4` heap-use-after-free: two 8-byte reads in `notify_same_from` from `notify_section` (the N5 bar) and two from `prove_the_crf_input_counters_push_under_the_one_second_limit`. Each shows the buffer freed in `force_uns_log_realloc` under `aecp_xact_from`.

The same failure is reproducible at the lever commit itself: `git checkout 766b6a149 -- sim_nxn.cpp` in place of the reverse-apply gives the same two FAIL lines and 4 reports. The SHAs above assume the branch is pushed as it stands.

For contrast, AddressSanitizer **without** the lever on dev `615b5a5d` gives `checks: 146 failures: 0` and no sanitizer line. The defect is latent, and a sanitizer alone does not reach it. That is why the proof needs the lever.

## Known limitations / out of scope

- The lever is not wired to a Makefile target, a CI job or the suite README. The assignment limited this change to test-bench C++, so the lever runs by adding one `-CFLAGS` to an existing recipe, as above. Its own liveness check guards it only when someone builds it. **Question for review:** should a follow-up Issue add a Makefile target and a README row for it?
- The AddressSanitizer evidence is on the notify leg, the one leg that carries both holds. nxn is covered by the lever without the sanitizer.
- Two pre-existing `-Wformat-truncation` warnings in `sim_nxn.cpp` (the `configuration_index IS the...` and `sampling_rate IS the model...` `snprintf` lines) are untouched and appear identically on dev.
- The hosted CI gates and the local `act` replica have not run: the branch has not been pushed from the authoring session.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (1: copies, not pointers; 2: forced-reallocation and AddressSanitizer runs, failing on the old code and clean on the new; 3: milan_dp legs pass)
- [x] New or changed behavior has self-checking tests (the lever build and its liveness check)
- [x] Required local verification bar passes (milan_dp legs, `check_cpp_idiom`, `docs_check`, `git diff --check`)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed (none names the changed helpers; the lever is documented at its definition)
- [ ] Post-merge containment will be checked before the Issue moves to Done
