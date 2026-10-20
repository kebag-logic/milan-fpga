# Round 1c attempts that produced no verdict

| Attempt | What happened |
|---|---|
| `s0-refused-nohup`, `s1-refused-nohup` | the first launch of both sweep shards at `75db4b57`: started under `nohup`, so the runner's own preflight "hard-HUP" cancellation control timed out (SIGHUP ignored and inherited). This is the same cause as rounds 1 and 1b. No suite started. Relaunched without `nohup`; the verdicts are `../sweep-s0/` and `../sweep-s1/` |
| `builder-refused-argv` | the builder bank, first launch: `scripts/ci_builder_legs.py` refused because the leg command was spelled `python sw/builder/test_builder.py`, not the template's `python3 ...`. No gate ran |
| `builder-refused-tsn-origin` | the second launch, in a clone whose `third_party/tsn-c-stack` was initialised from a local module store: `scripts/ci_case_receipts.py` refuses any tsn-c-stack origin other than the public one. No gate ran. Relaunched in a clean clone with only the three submodules the CI job fetches (tsn-c-stack uninitialised, as the check allows); the verdict is `../builder/` |
| `tsnfuzz-skipped-no-packetgen` | tsn_fuzz with `TSN_GEN_ROOT` at an unbuilt tsn-gen checkout (same pin, no `packet_gen`): rc 0, but both tsn-gen campaigns declared SKIP. Not counted. Re-run with the built checkout at the CI pin `deca300c`; the verdict is `../tsnfuzz/` |
