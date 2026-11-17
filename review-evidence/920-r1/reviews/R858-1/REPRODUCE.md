Run from a clean detached checkout of `bd252db1d73511307c0ecb78470f0d15d0c3ea9b` with its required submodules initialized. Set `review_packet` to the absolute packet directory. Generated trees belong only in its `scratch/` directory. The commands below are independent foreground commands; the store campaign used 12 workers, focused AECP runs at most four, and the cut probe three. Keep concurrent worker allocation within the host's assigned limits.

```sh
mkdir -p "$review_packet/scratch" "$review_packet/receipts"
TMPDIR="$review_packet/scratch" python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --self-test --jobs 12
TMPDIR="$review_packet/scratch" python3 tb/verilator/ctrl_service_budget/selftest.py
python3 "$review_packet/aecp_probe.py" . "$review_packet" --jobs 3
python3 "$review_packet/cut_probe.py" . "$review_packet" --jobs 3
python3 tb/verilator/ctrl_service_budget/load_grade.py --check
python3 "$review_packet/audit_checkout.py" .
git diff --check 659d7687 HEAD
```

Expected results: store 546 tests at five shapes with all 152 plants caught (the recorded run also built all five RV32 arms); harness zero failures and 251 mutants caught; AECP nine default-fixture cases plus the 8x8 all-names case and three pending-mark controls pass; the cut probe covers 845/823 and 2,125/2,103 boundaries on the two flash ports; load 0.517/0.70; checkout audit has an empty failures list.

The recorded AECP campaign was run in separate test and control invocations. `--tests-only` and `--controls-only` reproduce those independently. The controls retain the repository's complete mutation table and select its individual shards; they do not narrow the completeness census. The initial broad 8x8 Nvm diagnostic is retained as a failed receipt because its map test assumes the default dynamic-input-map fixture. The 8x8 static input map has capacity zero; the new name-persistence case is separately executable and passes.

For the public evidence checks, obtain the selected files from archive `4a3e37f80640ec17ab6acffbe5cf8c4ac587c5dc`, directory `review-evidence/920-r1`, under a disposable directory containing `author-r1/` and `author-r2/`. `receipts/public-evidence-manifest.json` is the exact selection and expected published hashes.

```sh
python3 "$review_packet/check_evidence.py" "$review_packet/scratch/public-evidence" "$review_packet"
```

This checks hashes, four exact-head sweep receipts, distinct suite/check tallies, save-target lines, group-source counts, budget totals, and all eight ROM/SRAM limits and ROM growth. It does not execute the author's banks. The original 37 selected files remain available from the immutable public archive; disposable local copies are not included in this packet's publication manifest.

The cut probe's final script enumerates a complete pair of saves using a separately completed reference run to determine the range. During probe development, a static original-slot protection guard was removed because it incorrectly prevented legal reuse of that slot after authority moved, and a fixed 2,000-step cutoff was replaced because it did not reach the end of the 8x8 saves. Final assertions still require all three complete snapshots, all nine phases and every boundary through completion. No candidate source or repository test was edited.
