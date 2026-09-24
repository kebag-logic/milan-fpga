[A267] REVIEW READY

Head: `ae7f531bc97a7277116e0df78e70c84396c499d0` (local branch `112-stale-grant`, base `939c143333d11e2378a514f1c7b6abd4c3259bfd`). Round 2 adds `fbabb94` and `ae7f531` on top of round 1 `73a5478` and round 1b `90e1ce1`, which is kept.

**The design is implemented as specified.** The pending source keeps its own grant low. A round that visits a requesting source without a valid current-declaration slope is discarded, so every other grant and granted slope, the sum and over-limit stay frozen until every requesting source has been evaluated. Capacity is released only by withdrawal or an evaluated shrink. Discarded rounds do not age the optimistic window, so the window cannot close while a verdict is held.

**Items 2–7:**

2. The cross-source test runs at every phase. In the unit suite at N ≥ 2 it covers identical, shrink, grow and double re-declarations, plus freeing controls and a pending middle source. In `tb/srp_top` it covers sources 1 and 7 with identical, still-refusing and freeing shrinks over 8 phases, plus 40 placements before a T-MRP-JOIN tick. Every clock is checked for no grant, no ACTIVE, no ACTIVE∧grant and no declared Advertise, and the wire shows no Talker Advertise.
3. Both reviewers' probes return 0 FAIL at an exact export of the head.
   - R299-1 unit N=2/N=8: 28/28 and 112/112, with P1 at 0/4 and 0/16.
   - R298-1 unit N=2/N=8: 792/792 and 32832/32832.
   - R299-1 top: 80/80. R299-1 wire: 0 of 40.
   - R298-1 srp_top: 192/192. R298-1 processor top: 0 admitted cycles.
4. The pending-absent mutant fails the new tests: the named cross-source check fails 44 times at N=2 and 368 at N=8, and the srp_top refused-source check fails in 72 of 72 runs. The campaign also kills a both-protections stale-evaluation mutant and a strobe-on-discarded-round mutant, 12/12 in total.
5. The unit oracle judges every clock in the Σ context. Every publication must equal the greedy walk over all current declarations, and between publications a grant only retires with its own declaration and the aggregate holds.
6. 10 §6.3 has the new anchor `sec-10-admission-cross-source`. The integrator rows, the admission banner and the SRP and processor-top port comments state the rule.
7. The parent gates pass with `ae7f531` as a temporary gitlink: cpp idiom, py idiom, source lists (106 files) and pp_shadow (371 checks, 0 failures). The staging was then reset.

**Gates at the head:** every CI-workflow gate returned 0 (docs, lint, 33-suite bank with 1,008,398 checks and 0 failing, nvm_port figures, portability), as did the SRP shapes, srp_top (1527), pp_top (1454) and the mutant runner.

**Latency is unchanged:** 8/16/24 clocks at the default shape (80/160/240 ns at 100 MHz). The window now lasts 25/33/41 clocks.

**Area with the repository's OOC recipe:** 7566 → 7603 LUTs and 10485 → 10502 registers against base. RAM and DSP are unchanged. The register delta is attributed bank by bank, and round 1's drop is explained in `syn/ooc/README.md`.

HANDOFF.md and PR-BODY.md are in the assigned output directory. No push, PR change, parent commit, merge or hardware action was performed.
