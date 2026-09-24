## Every flagged item: before and after

All C++ locations below refer to `tb/desc_mem_guard/sim_main.cpp` at the starting
head `4f525eb55b310d6b9bc2f1a000254cb2dd483665`. The original scanner sites are
saved in [before-findings.txt](before-findings.txt). The final local scan is
[after-local-findings.json](after-local-findings.json); the parent gates below
scan the complete consumed tree.

| C-style cast | Before | After (Rule 11 ES.49/ES.48) |
|---|---|---|
| 1, line 150 | `(unsigned long long)first.data` | `static_cast<unsigned long long>(first.data)` |
| 2, line 150 | `(unsigned long long)second.data` | `static_cast<unsigned long long>(second.data)` |
| 3, line 151 | `(unsigned long long)INPUT0` | `static_cast<unsigned long long>(INPUT0)` |
| 4, line 151 | `(unsigned long long)INPUT1` | `static_cast<unsigned long long>(INPUT1)` |
| 5, line 178 | `(unsigned long long)h.delayed_accept` | `static_cast<unsigned long long>(h.delayed_accept)` |
| 6, line 178 | `(unsigned long long)h.delayed_first` | `static_cast<unsigned long long>(h.delayed_first)` |
| 7, line 179 | `(unsigned long long)h.delayed_end` | `static_cast<unsigned long long>(h.delayed_end)` |
| 8, line 179 | `(unsigned long long)presented` | `static_cast<unsigned long long>(presented)` |
| 9, line 204 | `(unsigned long long)h.accepted` | `static_cast<unsigned long long>(h.accepted)` |
| 10, line 205 | `(unsigned long long)h.terminal` | `static_cast<unsigned long long>(h.terminal)` |

| File-scope mutable finding | Before | After (Rule 11 I.2) |
|---|---|---|
| Line 13 (one declaration, two counters) | `static int checks = 0, fails = 0;` | Separate `int checks = 0;` and `int fails = 0;` members of `TestResults`; `main` owns a local instance and passes it by reference to each case and harness. No mutable global or static-local replacement. |

| Multi-declarator finding | Before | After (Rule 11 ES.10) |
|---|---|---|
| 1, line 13 | `static int checks = 0, fails = 0;` | `int checks = 0;` and `int fails = 0;` in the owned result object |
| 2, line 26 | `bool valid = false, err = false;` | `bool valid = false;` and `bool err = false;` |
| 3, line 47 | `bool stuck, error;` | `bool stuck;` and `bool error;` |
| 4, line 50 | `uint64_t cycle = 0, accepted = 0, terminal = 0;` | Three separate `uint64_t` declarations, each initialized to zero |
| 5, line 51 | `uint64_t delayed_accept = 0, delayed_first = 0, delayed_end = 0;` | Three separate `uint64_t` declarations, each initialized to zero |
| 6, line 53 | `bool stuck_next = false, error_next = false;` | `bool stuck_next = false;` and `bool error_next = false;` |

The same new harness also had `unsigned beats, index;` and
`unsigned held_cycles = 0, overlap_accepts = 0;`. Both now use one declaration
per name, although the scanner did not include those unsigned declarations in
its six findings. Member order, initialization, stimulus, checks and output stay
the same. The full guard runtime output is
[byte-identical before and after](guard-runtime-comparison.txt).

| Python finding | Before | After (Rule 12) |
|---|---|---|
| `tb/desc_mem_guard/mutate.py:9`, unannotated public function | `def main():` | `def main() -> int:` |
| Same function, undocumented public function | No docstring | `Read CLI options and return 0 only when the completed byte check kills the mutant.` |

The controller still rejects build failures, crashes, a different assertion, or
an incomplete scenario; its return-code and exact wrong-byte checks are unchanged.

| Integration finding | Before | After |
|---|---|---|
| Parent build reports missing pin `desc_mem_debt_o` | `protocol_processor_top` exports a new debt output absent from the parent instantiation | Top-level output removed. The guard retains its own `debt_o` D3 port, connected to the local `desc_mem_debt_nc_w` tap. |
| Preserve product-top debt checks | Bench binds a product-top output | Bench assigns its observation output from `u_dut.u_desc_mem_guard.debt_o`. All five debt assertions and all product-top stimulus remain byte-for-byte unchanged. |
| Document the selected D3 seam | Architecture catalog, integrator guide and diagram claim a current top-level debt output | Catalog row removed; memory contract, integrator guide, bench README and diagram state that D3 will route the guard port to the top together with parent consumer changes. |
