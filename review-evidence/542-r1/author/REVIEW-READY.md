[A233] REVIEW READY
Commit: 68117c0bec0b767d38d9bb1150542e2346b615b7 (branch `542-notify-pointer` on dev `615b5a5d`, three commits; not pushed from the authoring session: the push and the PR are the coordinator's step)
Changed: `tb/verilator/milan_dp/sim_nxn.cpp` only. No RTL, Makefile or docs change; `hdl/milan/milan_datapath.sv` (#530) untouched.
- `766b6a149`: a forced-reallocation lever, `-DNOTIFY_REALLOC_TB`, compiled out of every Makefile leg. `await_aecp` and `drain_tx` are the only code that pushes into `uns_log`. On every call they now move the log into a buffer allocated while the old one is live, push one empty entry stamped -1, and free the old buffer. No reader matches the empty entry. A lever-only check fails if the lever never moved a log holding a real frame. The old checks are untouched in this commit, so it is the failing demonstration.
- `6c5fa5566`: the fix. `notify_last()` returns a copy, empty when nothing matches. Every match is longer than 37 bytes, so empty means exactly what the old null pointer meant. `notify_seq()` and `notify_same_from()` take the copy by const reference. `nB2` ([NOTIFY] N5), `n1` ([NOTIFY-CRF]) and `nB1` (N2) are copies, taken where the pointer was taken, so each bar still compares the frame it named before its exchange. No helper returns a pointer into `uns_log` any more.
- `68117c0be`: the lever's liveness count ignores the lever's own empty entries.

Audit of the file: no other pointer, reference or iterator into `uns_log` outlives a call that can push into it.
- The loop-local references in `notify_count`, `notify_last`, `notify_when` and `notify_ctr_when`, and the N9 CONTROLLER_AVAILABLE lambda, make no call that pushes.
- `uns_log_when` is only read by value.
- The `desc_of()` pointers point into the `std::map` `desc_want`. Map nodes stay put when other keys are inserted, and the map is only cleared while the image is built. Not a hazard, and unchanged.

Validation (Verilator 5.050, each leg built with the Makefile's own recipe from `make -n run`, at most 8 jobs):
- Plain legs at the head: main 230/0, notify 146/0, nxn 1708/0, nxn8 3136/0, plus nxndv 1710/0 and nxn4c 1708/0. The five `sim_nxn.cpp` legs print output byte-identical to dev `615b5a5d`.
- The lever against the OLD checks (at `766b6a149`, and at the head with `6c5fa5566` reverse-applied): notify 147 checks, 2 failures. They are exactly `[NOTIFY] GET_NAME right after is byte-identical from the body on` and `[NOTIFY-CRF] ...byte-identical from the body on to the solicited answer`. nxn 1709/1 (the first of the two).
- The same with AddressSanitizer (`-fsanitize=address -fsanitize-recover=address`, `ASAN_OPTIONS=halt_on_error=0:suppress_equal_pcs=0`): 4 heap-use-after-free, two 8-byte reads in `notify_same_from` at each bar. Each shows the buffer freed in `force_uns_log_realloc` under `aecp_xact_from`.
- The lever against the FIXED checks (head): notify 147/0, nxn 1709/0. Each run differs from its plain run only in the lever's two lines. AddressSanitizer plus the lever: 0 sanitizer lines, 147/0.
- AddressSanitizer WITHOUT the lever on dev: 146/0 and no report. The defect is latent, which is why the proof needs the lever.
- `python3 scripts/check_cpp_idiom.py` exit 0 (every ratchet 0 <= 0), `--selftest` 75/75. `python3 scripts/docs_check.py`: 0 findings. `git diff --check 615b5a5d7 HEAD`: clean.

Acceptance criteria:
1. Met: both checks keep a copy instead of a pointer (`6c5fa5566`).
2. Met: the forced-reallocation and AddressSanitizer runs show the stale access on the old code (2 check failures, 4 heap-use-after-free) and none on the new (0 and 0).
3. Met: the milan_dp legs pass (tallies above).

Open risks/questions:
- Nothing runs the lever automatically: it has no Makefile target, README row or CI job, because the change was kept to test-bench C++. It runs by adding `-CFLAGS -DNOTIFY_REALLOC_TB=1` to an existing recipe. Whether a follow-up Issue should add a target is a reviewer's call.
- Hosted CI and the act replica have not run, because nothing has been pushed.
- Two pre-existing `-Wformat-truncation` warnings sit in untouched `sim_nxn.cpp` `snprintf` lines. They are identical on dev.
- The exact reviewer commands and their expected output are in the PR description, and were run verbatim before this post.
