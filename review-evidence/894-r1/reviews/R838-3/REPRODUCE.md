Run from the exact detached source checkout. Set `PACKET` to this packet directory. Builds and generated descriptors go beneath `$PACKET/scratch/`.

```sh
python3 -B "$PACKET/probe_maps.py" .
# Expected exit 1: operation-count assertions fail; status/map behavior holds.
python3 -B "$PACKET/audit_hash_geometry.py" .
python3 -B "$PACKET/probe_join.py" .
python3 -B "$PACKET/audit_model.py" .
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B sw/firmware/ctrl/test/aecp_arms.py --work --output "$PACKET/scratch/baseline" --filter 'Core.MapEditsAreTheirDefinitionRowForRow:Core.MapEditWorkIsLinearInItsMappings:Core.MapKeysThatShareASlotAreTheirOwn:Core.RestoredOutputMapsHaveOneGlobalOwner'
python3 -B "$PACKET/verify_tree.py" .
```

Archive audits require the public evidence beneath scratch:

```sh
git fetch origin 183cd03d60e9d51dd8e251bbd38ffe5b3c01ee66
git archive 183cd03d60e9d51dd8e251bbd38ffe5b3c01ee66 review-evidence/894-r1/author-r8 review-evidence/894-r1/MANIFEST.json | tar -x -C "$PACKET/scratch"
python3 -B "$PACKET/verify_archive.py"
python3 -B "$PACKET/audit_receipts.py"
```

`probe_maps.py` generates a configuration and adds its probe only to a disposable test-file copy. It compiles unchanged firmware from the checkout using the existing counting instrumentation. `audit_hash_geometry.py` follows it because it examines that configuration. The baseline runs four existing tests unchanged. `probe_join.py` applies its mutation only in memory. No source restoration is necessary; `verify_tree.py` nevertheless checks exact bytes, executable modes, index entries and required submodule pins.
