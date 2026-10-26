https://github.com/kebag-logic/milan-fpga/pull/788#issuecomment-6411351133


### R705-1-01: RESIDUE (Docs)

- **Where:** `docs/testing/TESTING.md:331`, "used a hosted `ubuntu-latest` runner, then the `ubuntu-24.04` image, and sequential `make -C` invocations."
- **Evidence:** the job ran once. Job 113696564335 (run 37892515345, head `8e4b1e53`) has the label `ubuntu-latest`, and its set-up log line `2026-10-09T06:15:18Z Image: ubuntu-24.04` names the image that label resolved to (`receipts/historical-job-images.txt`). "then" makes the image read like a second step after the runner.
- **Impact:** wording only. Both facts are correct, and no figure, window, verdict or test depends on the sentence.
- **Exact fix:** "used a hosted `ubuntu-latest` runner, which resolved to the `ubuntu-24.04` image, and sequential `make -C` invocations."
- **Verification:** reread the line against the job log, then run `check_em_dash.py --base a8594bb9`, `check_doc_style.py` and `docs_check.py`.

### R705-1-02: SUGGESTION (Robustness, Conformance). A predating defect for a new Issue, outside this delta

- **Where:**
  - `.github/ci-templates/rtl-fast.yml:134-138` / `.github/workflows/rtl-fast.yml:254-258`: `yosys-elaboration` has `timeout-minutes: 30`.
  - `.github/ci-templates/rtl-fast.yml:153`: its Yosys cache key hashes `.github/workflows/*.yml`.
  - This delta changes neither line.
- **Evidence** (`receipts/hosted-cancel-cause.txt`, `receipts/yosys-elaboration-history.tsv`):
  - Every workflow edit misses that cache.
  - At this head, job 121450772865 shows `Cache not found for input keys: yosys-v0.66-...-Linux`. The cold build ran 07:32:00 to 07:48:33, and the job was cancelled at 08:02:01, 30 minutes after it started.
  - The `ci-fail-fast` watcher then reported `{"first_failure": "yosys-elaboration", "conclusion": "cancelled"}` and cancelled all four runs (`Cancelled runs: [40286249776, 40286249788, 40286249845, 40286249749]`).
  - The same cold-build cancellation happened at `43a25fa7` (run 38794077148), an earlier head that changed `rtl-fast.yml`.
  - A warm-cache run at `d385b38e` (run 40187422747) took 11.5 minutes and passed.
- **Impact:**
  - The first hosted run of any head that touches a workflow cannot make `rtl-fast` green.
  - Here, that cascaded into a cancelled `rtl-fast` and failed `verilator-suites` and `yosys-portability`.
  - The image move itself caused no failure. All 62 jobs that ran report `Image: ubuntu-24.04`, and the pip installs that failed on 26.04 now pass.
- **Optional outcome:** a new Issue for the cold-cache budget of `yosys-elaboration`. Not required for this PR: the template timeout and key are unchanged, and the defect is not in this delta.

