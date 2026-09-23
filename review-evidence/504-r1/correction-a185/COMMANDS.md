# A185 correction round: exact commands

`$LANE` is the lane checkout (`$LANES/504-hosted-rv32-compiler`),
`$PKT` this packet (`$REVIEWS/504-a185-packet`), `$ARCHIVE` the
official archive and `$VBIN` the scoped Verilator 5.050 directory
(`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin`). Every command runs
from `$LANE` at head `5081a25a451b4ac1c00f286ec59ab041c22fdde9` unless noted.
Nothing below writes into `$LANE`; all disposable output went to `$PKT/scratch/`,
which was deleted at the end.

## Identity

```sh
stat -c 'size=%s' "$ARCHIVE"; sha256sum "$ARCHIVE"          # receipts/01
"$VBIN/verilator" --version; sha256sum "$VBIN/verilator"     # receipts/02
```

## Branch preparation

```sh
git fetch origin dev                                          # 483a133e
git merge --no-edit --no-ff 483a133ed08867ea0d300d2b4a027b5b48a4282f \
  -m "Merge dev 483a133e into 504-hosted-rv32-compiler"       # receipts/05
git merge-tree --write-tree 3d90958f 483a133e                 # equals the merge tree
```

## SDK (new prefix, head installer, unchanged bytes)

```sh
S=$PKT/scratch/r228run/sdk-fresh/host
python3 scripts/ci_rv32_sdk.py --destination "$S" --archive "$ARCHIVE"   # fresh
python3 scripts/ci_rv32_sdk.py --destination "$S" --archive "$ARCHIVE"   # cache hit
python3 scripts/ci_rv32_sdk.py --destination "$S" --verify-only           # receipts/20
```

## Gate 1b, mapped and absent, plus R228-1 plants and F1 slow mutants

```sh
$PKT/scripts/run_final_gates.sh "$LANE" "$PKT" "$S" "$VBIN"               # receipts/gate1b
```

It runs, at most 8 processes at once:

- `test_firmware_compiler.py --sdk-destination $S --audit ...` (pristine-sdk);
- `test_firmware_compiler.py --absent --audit ...` (pristine-absent);
- `scripts/capture_census.py` (a third mapped run that copies every census
  assembly for the equivalence check);
- `scripts/mutate_store_classes.py drive` for the two slow F1 mutants and
  R228-1's float, double and uint32 plants, applied in memory.

## F1

```sh
python3 $PKT/scripts/mutate_store_classes.py drive "$LANE" "$S" $PKT/scratch/mut-f1-final "$VBIN" \
  "FP and atomic classes dropped from the tables" "unclassified-memory default removed" \
  "pre-fix classification restored" "overlap forgetting removed" \
  "footprint reduced to the first byte's word" "AMO destination left holding its old value"
                                                              # receipts/17 (with the slow two and plants)
python3 $PKT/scripts/resolver_equivalence.py "$LANE" f6a55e4c85b6bdcdaeab6caa6b6e575c51cf97df \
  $PKT/scratch/capture-all/census-*.s                         # receipts/14, 15
python3 $PKT/scripts/r228-1/probe_fp_store.py "$LANE" "$S" $PKT/scratch/probe-fp-final   # receipts/13
```

## F2 and F3

```sh
python3 $PKT/scripts/r228-1/mutate_installer.py "$LANE" $PKT/scratch/mut-installer-final  # receipts/10
python3 $PKT/scripts/r228-1/probe_download_auth.py "$LANE" $PKT/scratch/probe-download-final  # receipts/11
python3 $PKT/scripts/mutate_download_auth.py "$LANE" $PKT/scratch/mut-download-final      # receipts/12
```

## Static and focused gates

```sh
$PKT/scripts/run_static_receipts.sh "$LANE" "$PKT" \
  52711029f374650dc93830d5ea28e81cb5c8f410 483a133ed08867ea0d300d2b4a027b5b48a4282f
                                                              # receipts/static-final
```

## Integrity

```sh
python3 $PKT/scripts/r228-1/verify_clone_integrity.py "$LANE" \
  5081a25a451b4ac1c00f286ec59ab041c22fdde9 third_party/verilog-axis protocol-processor gptp-processor
                                                              # receipts/18, 19
```

The `scripts/r228-1/` files are unmodified copies of R228-1's published
scripts from evidence commit `28242096da74411d17e51c21d2c9b80af0c2cdd3`
(`review-evidence/504-r1/reviews/R228-1/scripts/`).
