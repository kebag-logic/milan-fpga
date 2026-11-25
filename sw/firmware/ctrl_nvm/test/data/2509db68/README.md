# A store written by 2509db68

Each slot of the saved-state store as the `2509db68` image's own store left it, at the minor before delta frames
(KLJ3 minor 0, #1009): the bytes `store_of_2509db68` ([`test_nvm_delta.cpp`](../test_nvm_delta.cpp)) boots on.

| File | Shape | What |
|---|---|---|
| `endstation_ax7101_8x8-a.hex`, `-b.hex` | 8x8, one interface | slot A at sequence 1 (input 0 bound), slot B at 2 (input 0 unbound) |
| `endstation_ax7101_1x1_tdm8-a.hex`, `-b.hex` | 1x1, one interface | the same at that shape |

**Where they come from.** The CPU budget harness ([`tb/verilator/ctrl_service_budget`](../../../../../../tb/verilator/ctrl_service_budget/README.md))
ran the split image of `dev-soft-core` `2509db68` at each point on blank flash: a BIND_RX of input 0 from the harness's
talker, its PROBE_TX answered, left 3 s (the store's first save, written whole into slot A), then its UNBIND_RX, left
3 s (the second, into slot B); the testbench wrote the journal at the end. Each file is one slot cut to its
container's length (its header's length word at 16), as hex, 64 bytes a line; the rest of the slot was erased. The
containers hold the harness's synthetic identifiers and names only.

A build of a shape whose shape has no such file reads none of them ([`nvm_fixture.py`](../nvm_fixture.py)); the two
AX7101 shapes must.
