Replay from a byte-exact clone of c4539ff107a6a4c7d2e4a4844182b00a2bf33c82. Python 3, Git and authenticated read access through `gh api` are sufficient for input recovery. Source fetching reads only the listed immutable public repositories. It performs no repository write.

Set `SOURCE` to the processor clone and `PACKET` to an empty output directory. Copy this packet's scripts there. Use a path without spaces for the recipe replay.

```sh
mkdir -p "$PACKET/receipts" "$PACKET/scratch"
python3 "$PACKET/scripts/fetch_public.py" "$PACKET"
python3 "$PACKET/scripts/fetch_sources.py" "$PACKET"
python3 "$PACKET/scripts/verify_inputs.py" "$SOURCE" "$PACKET"
python3 "$PACKET/scripts/audit_evidence.py" "$SOURCE" "$PACKET"
python3 "$PACKET/scripts/verify_checkout.py" "$SOURCE" "$PACKET"
```

Expected: all commands return 0; 124 components match, 21 generics and six image identities reproduce `24ba6a244a83a0b764e6de5131a9c94752135f01ecab5afad83258c7b4767be1`; six digest perturbations differ. Source retrieval verifies 73 measurement source/header files plus four recipe authorities. Public retrieval verifies 81 blobs including the manifest; the audit checks its 80 listed files.

Optional focused arbiter rerun, using the supplied scoped 5.050 executable:

```sh
python3 "$PACKET/scripts/run_focused.py" "$SOURCE" "$PACKET" "$PINNED_VERILATOR"
```

This joins two concurrent foreground tasks: input replay and the 66-check arbiter suite. Compilation is limited to eight jobs, with `make -j16`; no heavy physical build is involved. The executable version and wrapper hash are recorded before use. The first local setup attempt omitted `tb/common` from the disposable archive; `setup-retry.json` records that preparation failure. The corrected runner archives that directory too and passes. Full compiler captures stay in scratch; published arbiter output is the verbatim executable output, with full-capture size/hash retained.

No synthesis, firmware build, full bank, workflow execution or hardware operation is part of these scripts. Three remaining image identities come from the public manifest rather than a fresh image build. The reviewer verifies both processor ROMs and the empty SRAM independently. Scratch is never part of publication. The final finding disposition is in REPORT.md; the earlier independent ledger snapshot precedes the later public cancellation finding.
