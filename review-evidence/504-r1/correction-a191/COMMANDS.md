# A191 second correction round: exact commands

Placeholders: `$LANE` is the lane checkout (`$LANES/504-hosted-rv32-compiler`),
`$PKT` is this packet (`$REVIEWS/504-a191-packet`), `$ARCHIVE` is the verified
official archive, and `$VBIN` is the scoped Verilator 5.050 directory. `$S` is
`$PKT/scratch/sdk/host`. Every command runs from `$LANE`. Unless a step says
otherwise, it runs at head `97aa1ec943ac740a27b942210a248f6512ae3ff6`.

Nothing below writes into `$LANE` except the two commits and the dev merge. The
gate runs write only ignored `__pycache__` directories, and those were removed
before the final integrity check. Disposable output went to `$PKT/scratch/`,
which was deleted at the end.

## Identity (receipts/03)

```sh
stat -c 'size=%s' "$ARCHIVE"; sha256sum "$ARCHIVE"
"$VBIN/verilator" --version; sha256sum "$VBIN/verilator"
```

## Dev merge (receipts/01, 02, merge-static/)

```sh
git fetch origin 504-review-evidence dev                      # dev = 574c29fa
git merge-tree --write-tree HEAD 574c29fa111c74e5e5ed63e4670aff1f492e28e2   # exit 0, fdf07c85
git merge --no-ff --no-edit -m "Merge dev 574c29fa into 504-hosted-rv32-compiler" 574c29fa111c74e5e5ed63e4670aff1f492e28e2
python3 scripts/ci_events.py --check; python3 scripts/ci_events.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_em_dash.py --base 574c29fa111c74e5e5ed63e4670aff1f492e28e2
```

## SDK (receipts/04, 07, 08)

The SDK was installed into a new prefix with the head's installer, whose
bytes are unchanged.

```sh
python3 scripts/ci_rv32_sdk.py --destination "$S" --archive "$ARCHIVE"   # fresh
python3 scripts/ci_rv32_sdk.py --destination "$S" --archive "$ARCHIVE"   # cache hit
python3 scripts/ci_rv32_sdk.py --destination "$S" --verify-only
```

## Pristine gate 1b, mapped and absent (receipts/gate1b/, 14)

```sh
$PKT/scripts/run_pristine_gates.sh "$LANE" "$S" $PKT/receipts/gate1b "$VBIN"
```

The script runs the lane's own `sw/builder/test_firmware_compiler.py`, once
with `--sdk-destination "$S"` and once with `--absent`, each with `--audit`.
The two runs go in parallel, with `$VBIN` first on `PATH`.

## Fix-removal mutants and reviewer plants, in memory (receipts/mutants/)

```sh
python3 $PKT/scripts/gate_variants.py drive "$LANE" "$S" $PKT/receipts/mutants "$VBIN" 6
```

This command applies no edit to any file. Each mutant edits the committed
bytes of `sw/builder/test_builder.py` in memory. Each plant patches the
committed firmware text in memory with a reviewer's published diff, from
`scripts/plants/`. The lane's gate 1b driver then runs as one process per
entry, at most 6 at once. That made 8 processes at most, together with the
two pristine runs.

## Resolver probes and equivalence (receipts/05, 06, 09, 10, 12)

```sh
python3 $PKT/scripts/r227-2/resolver_controls.py .                                  # receipts/05
git show 4914eea5:sw/builder/test_builder.py > $PKT/scratch/old/test_builder.py
python3 $PKT/scripts/resolver_compare.py $PKT/scratch/old/test_builder.py \
  sw/builder/test_builder.py $PKT/scratch/cap-pristine/census-0.s                   # receipts/06
PATH=$VBIN:$PATH python3 $PKT/scripts/capture_census.py . "$S" $PKT/scratch/cap-all  # receipts/09
python3 $PKT/scripts/resolver_compare.py $PKT/scratch/old/test_builder.py \
  sw/builder/test_builder.py $PKT/scratch/cap-all/census-*.s                        # receipts/10
python3 $PKT/scripts/r228-2/probe_resolver.py . "$S/bin/riscv32-linux-gcc" \
  $PKT/receipts/12-r228-2-probe-resolver-head.json                                  # receipts/12
```

The pristine census assembly, `cap-pristine/census-0.s`, was captured with
`capture_census.py . "$S" $PKT/scratch/cap-pristine 1` on the working tree.
That was before the first commit. The firmware is unchanged, so its
assembly does not depend on the builder revision.

## Static and focused gates (receipts/static-head/)

```sh
$PKT/scripts/run_static_receipts.sh "$LANE" $PKT/receipts/static-head \
  52711029f374650dc93830d5ea28e81cb5c8f410 574c29fa111c74e5e5ed63e4670aff1f492e28e2 \
  483a133ed08867ea0d300d2b4a027b5b48a4282f
```

## Boundary and integrity (receipts/11, 13)

```sh
python3 $PKT/scripts/verify_integrity.py . 97aa1ec943ac740a27b942210a248f6512ae3ff6 \
  third_party/verilog-axis protocol-processor gptp-processor
```

The `scripts/r227-2/` and `scripts/r228-2/` directories hold unmodified copies
of the reviewers' published scripts. They come from evidence commit
`fb25b8cee0f66922d9c388ab6955e3278a842e41`; see
`scripts/REVIEWER-SCRIPTS-SOURCE.txt`. Only `resolver_controls.py` and
`probe_resolver.py` were executed. Their mutant and plant edits were
reproduced in memory by `gate_variants.py`, since this lane copies no tree.
