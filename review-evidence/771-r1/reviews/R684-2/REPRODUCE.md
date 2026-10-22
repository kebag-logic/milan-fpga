# R684-2 reproduction

Use a clean checkout at `1098978f4a931a667e147b68a791520eb141c917` with the five required submodules initialized at their gitlinks. Set `REPO` to that checkout and `PACKET` to this packet directory. The only generated/build trees belong under `$PACKET/scratch/`.

```sh
mkdir -p "$PACKET/scratch"
python3 "$PACKET/scripts/verify_integrity.py" "$REPO"
python3 "$PACKET/scripts/check_delta.py" "$REPO"
git -C "$REPO" fetch --no-tags origin b6d9eaa187cb2c43548e22e7adae21b35b539107
python3 "$PACKET/scripts/audit_evidence.py" "$REPO"
```

For the focused host probes, select an existing GoogleTest/GoogleMock 1.14.0 installation through `PKG_CONFIG_PATH` and `LD_LIBRARY_PATH`. No installation or RV32 SDK is needed for these focused arms. Each build uses four workers. Use fresh output labels or remove only the disposable probe output before repeating.

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 "$PACKET/scripts/probe_acmpwalk.py" "$REPO" "$PACKET/scratch/probes" clean
python3 "$PACKET/scripts/probe_acmpwalk.py" "$REPO" "$PACKET/scratch/probes" controls --controls acmp-kind-lost,acmp-kind-not-notified
cd "$REPO"
TMPDIR="$PACKET/scratch" python3 scripts/check_nvm_capture.py
python3 "$PACKET/scripts/verify_integrity.py" "$REPO"
```

The two focused builds were launched concurrently as foreground processes, with separate logs and return-code files; neither wrote source files. Expected: clean 127/0; both controls `killed: true`, each with named core and walk failures; capture and integrity PASS. A mutant returning 1 is expected only when its named assertions fail. The script asserts those outcomes.

Receipt map:

- `receipts/clean-*`, `receipts/controls-*`: independent raw test logs and results. Path-prefix normalization, where needed, only replaces checkout/packet roots.
- `receipts/clean.log`, `receipts/controls.log`: compiler/pin identities and probe output.
- `receipts/evidence-audit.txt`: publication hash checks, firmware tally recount, assigned firmware return codes and signature limitation.
- `receipts/delta.txt`: three-commit scope, comment-only RTL equivalence, unchanged production/oracle inputs, shipping firmware digest and source-comment scan.
- `receipts/nvm-capture.log`: independent capture checker and controls.
- `receipts/integrity-before.txt`, `receipts/integrity-final.txt`: tracked bytes, modes, indexes and required gitlinks.
- `receipts/public/`: selected unmodified public author receipts, including the full firmware text log and production-path probe logs. These are evidence inspected, not reviewer reruns.
- `receipts/public-sources.json`: immutable source links for those copies.
- `receipts/pr-body.json`: reviewed PR body snapshot and published head.

Verify this packet with `sha256sum -c MANIFEST.sha256` from its root. Scratch is intentionally absent from the manifest and publication.
