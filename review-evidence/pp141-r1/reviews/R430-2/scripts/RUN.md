# How the R430-2 receipts were produced

`$PACKET` is this packet's root; `$H` is a `git archive` export of a90ca735 copied once per
stream (`$PACKET/scratch/c-<stream>`), so no campaign shares a tree. `scratch/bin/verilator`
is `verilator-capped` (the pinned Verilator 5.050, `PINNED_VERILATOR`, with `-j 0` capped to
the number in `scratch/vjobs`: 2, then 1, then 4 for the last probe). Each stream was started
with `bg.sh NAME DIR CMD...` (log `receipts/NAME.log`, exit code `receipts/NAME.rc`) and
waited on with `wait.sh`. At most 16 compile/simulation jobs ran at once.

| Receipt | Command (cwd) |
|---|---|
| `merge-redo.txt` | clone, `checkout 76b09ff`, `merge --no-ff 2ebd4fe8`; tree and patch-id comparisons |
| `hdl-vs-main.txt` | `git diff 2ebd4fe8 a90ca735 -- hdl`; Python tokenize of both `gen_ucode.py` |
| `rom-regeneration.txt`, `rom-map*.txt`, `rom-map.txt` | `rommap.py TREE OUT_HEX OUT_MAP` at six revisions; CLI `gen_ucode.py -o`, `gen_ltn_rom.py -o`, `make image.bin` |
| `apply-check-<rev>.txt` | `apply_check.sh TREE` over every `*.patch` of a pristine export |
| `plant-*.json`, `plant-compare.txt`, `patch-refresh-diff.txt` | `plant_words.py OUT TREE PATCH...` (22 `gen_ucode.py` patches) at 39fd019, 76b09ff and a90ca735 |
| `suites.log` | `/usr/bin/time -v ./scripts/run_suites.sh` (`$H`) |
| `lint.log` | `./scripts/lint_hdl.sh` (`$H`) |
| `docs-gates.txt`, `make-check.txt` | `make check`, CI docs gates, `gen_matrix.py --check`, `check_upc_map.py`, `check_m9_opcodes.py`, `git diff --check` (a clone checked out at a90ca735) |
| `dispA.log`, `dispB.log` | `python3 aecp_dispatch_mutants.py --output OUT --verilator V --only <arms 1-18 / 19-37>` (`$H/tb/pp_top`) |
| `aecpA.log`, `aecpB.log` | `python3 aecp_mutants.py --output OUT --only <arms 1-28 / 29-55>` (`$H/tb/pp_top`) |
| `d3.log` | `python3 tb/pp_top/d3_mutants.py --output OUT --verilator V --jobs 8` (`$H`); `d3-partial-abandoned.log` is an earlier `--jobs 2` run stopped at 26 arms to restart wider |
| `notify.log` | `python3 tb/pp_top/notify_mutants.py --output OUT --verilator V --jobs 3` |
| `acmp.log` | `python3 tb/pp_top/acmp_mutants.py --output OUT --verilator V --jobs 2` |
| `gsi.log`, `namewr.log` | `python3 gsi_mutants.py --output OUT --verilator V`; `python3 name_wr_mutant.py --output OUT` (`$H/tb/pp_top`) |
| `maap.log`, `adp.log` | `make -C tb/maap mutants`, `make -C tb/adp_engine mutants` with `MUTANT_OUTPUT=OUT` |
| `srp0.log` .. `srp5.log` | `python3 tb/srp_top/mutants.py --output OUT --only <one sixth of the 73 labels>` |
| `retry.log`, `srpadm.log`, `dmg.log` | `retry_mutants.py --logs OUT`, `srp_admission/mutants.py --output OUT`, `desc_mem_guard/mutate.py --output OUT` |
| `nvmfig.log` | `make -C tb/nvm_port figures` (the clone, after fetching `refs/pull/13/head` as CI does) |
| `compare-*.txt`, `srp-chunks-summary.txt` | `compare_readme.py TREE OUT...` (and the inline retry/SRP comparisons recorded in the same files) |
| `probe-sclks-bound-three.log`, `probe-clks_row_two_bits.log` | `probe_default_build.sh EXPORT ARM` |
| `probe-fmtb.log` | `probe_fmtb.sh EXPORT` |
| `hosted-runs.json`, `hosted-jobs.txt` | read-only `gh run list --commit a90ca735` / `gh run view` |
| `clone-integrity.txt` | `git status --porcelain --ignored`, index vs `ls-tree`, `hash-object` of every tracked file |
| `verdict-before-prior-reviews.md` | written before the R430-1 and R431-1 reports were opened |
