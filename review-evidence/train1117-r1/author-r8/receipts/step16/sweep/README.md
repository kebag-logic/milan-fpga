# `15168e14`: rulings cited by issue, date and item in the train's source and test comments and check texts (R865-4-R1, R2)

One commit on `8dc85884`. By the owner's source-comment rule of 2026-10-15, comments carry behaviour and reason with
issue and requirement IDs only, so this commit removes the train's issue-comment IDs and review IDs. Each ruling is
cited by its issue, date and item instead, for example "#665's ruling of 2026-11-20, item 4".

| File | What it is |
|---|---|
| `sweep-scan.log`, `.rc` | `tools/sweep_scan.py cb96336d 15168e14`, over every line the whole train adds in code, test, script and data files (not Markdown). No line in a source comment or check text carries an issue-comment or review ID; rc 0 |
| `sweep-scan-control.log` | the same scan at `8dc85884`, before the commit: 21 such lines, rc 1 |
| `sweep-classify.log`, `.rc` | `tools/sweep_classify.py 8dc85884 15168e14`: each of the 14 changed files is the same code once comments are removed and string literals masked (Python by its tokens, C and C++ by their text, the hot list by its non-`#` lines). Each changed string literal is printed with its old and new value; rc 0 |
| `sweep-classify-control.log` | the classifier on `92de01f7..fb083864`, which re-targets two plants: CODE DIFFERS, refused |
| `sweep-diff-w.txt` | `git diff -w 8dc85884 15168e14` |
| `img-vs-8dc85884.txt`, `img-hashes-15168e14.txt` | the twelve CPU budget images, rebuilt at `15168e14`: each byte-identical to `8dc85884`'s (built at `8c5e2b4f`, whose diff to `8dc85884` is one doc) |
| `product-images-vs-8dc85884.txt`, `led/` | the four product images the ledger links, byte-identical; `plat_ledger.py --self-test` PASS with 9 of 9 controls; `test_ctrl_memory.py` PASS |
| `../release/` | the release export at `15168e14`, byte-identical where loaded to `8c5e2b4f`'s |
| `q.txt` | the quick list at `15168e14` |

**The quick list** covers the self-tests, the checks, the idioms and the docs. Every self-test refuses every plant, and
the two changed check texts' self-tests run among them:
- run.py's queued-constants check, in `run.py --self-test`;
- the declaring arm's fixture check, in `record_classes.py --selftest`.

**Kept, with the reason:**
- **Three data records** that `sweep-scan.log` lists as DATA. None is a source comment or a check's message:
  - `scripts/register_descriptions.json`: the register reference's description text, a link in a generated page;
  - `syn/ooc/pp_resource_baseline.json`: the resource gate's record, written only by `pp_resource_gate.py record
    --write`;
  - `tb/verilator/nvm_capture_cpu/measurements.json`: a measurement record's provenance field.
- **`tb/verilator/reboot_ctrl/mutants.py:113`:** its comment ID is older than the train (`cb96336d` carries it), so it
  is outside the train's diff.
- **The word "lane"** in the train's code: it names the datapath's control lane, a register diagram's lanes, or (in
  `sw/litex/ctrl_memory.py`'s ledger record) the S14 stage. It is not a review or session label.
