[A225] DONE — pre-review fix of PR #109 for the parent idiom gates

Branch `92-93-boot-restore`, `69a6eac2` → `156c206c`, 5 commits. **Local only: not pushed**, so PR #109 still shows 69a6eac2. Packet: `$REVIEWS/pp92-a225-packet` (`HANDOFF.md`, `logs/gate-summary.txt`).

- **Parent gates.** Checked in a scratch clone of `kebag-logic/milan-fpga` at dev 26d855a9, with the gitlink committed locally and not pushed. Moving the gitlink from 69a6eac2 to 156c206c:
  - `check_cpp_idiom.py` goes from exit 1 to exit 0: multi-declarator 10 → 0, long function 3 → 0, build without warnings 1 → 0.
  - `check_py_idiom.py` goes from exit 1 to exit 0: long module 11 → 10.
  - With `--list`, no processor file is over its ratchet. The only processor file still listed is `hdl/aecp/ucode/gen_ucode.py`, which has not changed since the parent pin and is inside the recorded 10. No budget file changed.
- **What changed.**
  - Every declaration in these benches now declares one name.
  - `LsnAdmitSuite::run`, `sample_dev` and `boot_window_at_the_top` are split along their existing sections. BW3 is now its own section, `boot_window_read_deadline`.
  - The warning finding was the acmp_nvm `pinned` target's define-only `-CFLAGS` group, which now carries `-Wall -Wextra`. The one real compiler warning in these builds was the unused `be_get` added with #92, which is deleted.
  - The pre-fix matrix forms and git pins in `measure_figures.py` moved byte-for-byte into `tb/nvm_port/pre_fix_forms.py`. The two files are now 788 and 238 lines.
- **Behaviour.** Bench outputs are byte-identical at both heads for acmp_nvm, its pinned control (the same 96 FAIL lines), lsn_admit, nvm_port and both pp_top builds. Six RTL mutants fail the same checks with byte-identical output at both heads; they include B01, which fails both BW3 checks, and LG01, which fails BW1 and BW2 in pp_top.
- **Processor gates at 156c206c, all exit 0:**
  - `run_suites.sh`: 31 suites, 15 773 checks, 0 failing.
  - nvm_port `figures`.
  - lint, `make check` and `gen_matrix --check`.
  - The synthesis run.
  - `git diff --check 09f9bf38..HEAD`.
- **Not fixed here.** `tb/dispatch/sim_main.cpp:608` and `:611` still warn `-Wsequence-point`. That file is unchanged on main and at the parent pin, and it is not a parent gate finding, so it needs its own issue.

R278 and R279 can start once 156c206c is pushed.
