[R639] NEGATIVE - exact head 18f2df92b13cb3f4036b073ed76940187bf10487

Independent diff pass recorded before consulting prior review findings. This is a checkpoint; image inspection and public-receipt authentication continue in the final report.

R639-2-F1, MAJOR, Conformance/Robustness/Tests/Docs: scripts/ci_tool_inventory.py:215 accepts ordinary keyword command arguments without examining them; its path recognizer also misses root-level scripts, and its Makefile pass misses download/build installation. `inventory-probes.json` reproduces three empty inventories accepted by both regeneration and comparison, with the positional-string positive detector control refused. docs/testing/CI_IMAGE.md:23 claims unsupported installers are refused. The required outcome is derivation or explicit refusal of those installation requests, with controls that test regenerated inventories.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | inventory-probes.json; scripts/ci_tool_inventory.py; issue assignment 6160953880 | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| RTL | CLEAN | Full diff from fa7347fc; ci/image/Dockerfile; ci/image/install.py; unchanged workflows, RTL, firmware, patches and gitlinks | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Robustness | UNCLEAN | inventory-probes.json; build/privacy/integrity/patch controls | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Tests | UNCLEAN | scripts/ci_tool_inventory_selftest.py; focused-checks.json; independent inventory probes | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Docs | UNCLEAN | docs/testing/CI_IMAGE.md:23; documented regeneration procedure | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
