Run from a detached checkout of `154722e14781c7373f3229420b6e007f9bcf9835` with the four required submodules initialized at their gitlinks. The host needs the repository's ordinary C/C++ test and coverage dependencies. `PACKET` is this directory; all disposable products go into its `scratch/` directory.

```sh
python3 -B "$PACKET/scripts/integrity.py" --source . --output "$PACKET/receipts/integrity-before.json"
python3 -B "$PACKET/scripts/focused.py" --source . --packet "$PACKET" --jobs 4
python3 -B "$PACKET/scripts/focused.py" --source . --packet "$PACKET" --jobs 4 --worker prior-probes --interfaces 1
python3 -B "$PACKET/scripts/focused.py" --source . --packet "$PACKET" --jobs 4 --worker prior-probes --interfaces 2
python3 -B "$PACKET/scripts/public_evidence.py" --source . --packet "$PACKET"
python3 scripts/docs_check.py
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
python3 sw/mailbox/gen_mailbox.py --check
git diff --check efea74858dffc482820d4f19c26c38796a57ff75 HEAD
python3 -B "$PACKET/scripts/integrity.py" --source . --output "$PACKET/receipts/integrity-final.json"
```

Fetch the immutable public evidence commit first if it is absent:

```sh
git fetch origin ef69cd574960ff0ed632630d82d41383e38b1acc
```

Expected: all commands return zero. The focused driver runs the unmodified 52-case composition suite at each interface count, seven sanitizer suites totaling 140 cases at each count, three named standing mutations at each count, and the unchanged 22-file coverage ratchet. Its foreground process waits for every child. Four concurrent processes each request four compilation workers, at most sixteen workers. The two original-probe commands each run three cases; they were executed concurrently with separate logs and exit-status receipts for this review.

Each mutation binary must return a behavioral failure containing the named diagnostic; the campaign succeeds only when that failure is caught. Build failures never count. The source checkout is never edited; mutations and appended public probe headers exist only in scratch copies. The original probe header is byte-identical to the published R532-12 input, SHA-256 `7fa2d66d681f1ceaf8a0dbcbf2e98bb602bd7b4a22b081bc29fd53042ea45c32`.

The evidence audit reads only published author command receipts and source metadata. It verifies all retained hashes and exact mutation-table membership. It does not execute the full campaign or any manager bank. The public full-campaign raw log is absent; its structured receipt is the evidence for that full run.

Receipt logs preserve command output, with only local source and packet roots replaced by `$SOURCE` and `$PACKET` for publication. Unredacted local logs and all builds remain under unpublished `scratch/`. No reported result or diagnostic is changed by that path substitution.
