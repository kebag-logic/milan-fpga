[A259] Keep SRP admission grants tied to the current declaration

Closes #112

Accepted declarations now invalidate their source throughout the slope pipeline,
retire its grant immediately, and restart the partial admission round. The grant
stays low until the new TSpec is evaluated and its full round completes.
Top-level parameters and ports are unchanged.

Tests cover cold refusal, growth from 224 to 20000 bytes, shrink, identical
re-declaration, rapid withdrawal/re-declaration, and both TSpec fields across
five source shapes. The service-port suite exercises three sources at every
sampling phase with real Listener Ready PDUs. Refused declarations produce no
grant pulse; admitted default-shape declarations grant after 8/16/24 clocks
from acceptance. ACTIVE's optimistic window and round-latched slope accounting
are documented and checked.

All 33 processor suites pass: 739421 checks, zero failures. All workflow gates,
HDL lint, portability, the historical figure gate and both prescribed parent
consumer checks pass. The consumer suite has 371 checks, zero failures. The
stale-evaluation mutants fail at both two and eight sources; clean controls pass.

Default-shape SRP area: 7566 → 7334 LUTs and 10485 → 10464 registers, with RAM
and DSP unchanged under the same out-of-context recipe. Full evidence is in
HANDOFF.md and gate-ledger.json.
