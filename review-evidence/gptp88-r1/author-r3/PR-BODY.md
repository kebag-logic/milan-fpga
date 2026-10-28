[A690d]

Closes #87, Closes #88

## What changes

IEEE 802.1AS-2011 (+Cor1/Cor2), the edition Milan v1.2 profiles, disqualifies a received Announce only by 10.3.10.2.1 a), b) and c). Its item d) is the whole pathTrace rule:

- a present path trace TLV's pathSequence is copied to pathTrace, and thisClock is appended;
- with no TLV nothing is written, so pathTrace keeps its previous value.

The engine now follows both halves.

- #88, qualification. The receive parser no longer refuses an Announce for any of these:
  - a hop count other than stepsRemoved+1 (10.5.3.3.4 states that only as a NOTE);
  - a first entry other than grandmasterIdentity;
  - an empty pathSequence.

  8N framing, one PathTrace per Announce, and the all-hop loop verdict for c) stay.
- #88, publication. The path is copied as received, head included, and thisClock is appended. An empty TLV gives {thisClock}.
- #87. Without a TLV the previous pathTrace stays:
  - {thisClock} after reset or mastership (10.3.12.1.1, 10.3.12.1.4 i), Cor1);
  - otherwise the last path copied from a TLV, across a grandmaster change too.
- ABI, as ruled (option A). `pub_path_o` carries eight entries from entry 0 (`[8*64-1:0]`, entry k at bits `64*k`). `pub_path_count_o` counts the entries published (1..8).
  - Entry 0 is the received head or thisClock, never the grandmaster put in its place.
  - `pub_gm_id_o` is unchanged.
  - No other port, parameter or register-map change.
- Message word 12 gains a presence bit (63). It lies above the 32 bits the microcode's loop test compares, so the microcode is unchanged; only comments in the generator move. The generated ROM images are byte-identical to main's.
- `docs/INTEGRATION.md` and the HDL and test guides describe the new ABI and rules.

### Merge with main (#89, #90, #91)

Main (`3426089a`) is merged in as a merge commit (`98edabb`), not a rebase.

- Both sides' checks and engine mutation arms are kept, with the union of the strict named-check prefixes: `#82 #84 #85 #87 #88 #89 #90 #91` and priority1 255.
- The arm is main's 100 entries and this branch's 84, 69 of them shared. Each entry missing from the union was deleted on purpose by one side.
- The source-evidence anchors resolve at the merge head.

Main's sync receipt ageing (802.1AS-2011 10.3.11, Figure 10-13 as corrected by Cor1) ages a grandmaster that sends no Sync within syncReceiptTimeout.

- This branch's two issue shapes waited a whole Announce interval, with no Sync, after electing the peer. Merged as is, the plane aged that peer and took mastership, and the aged port refused every later Announce: 200 of 1968 engine checks failed.
- `b0473e6` runs those two shapes as phase 43, after phase 40, where usable Sync already flows. The parent sends a usable pair every 125 ms through the whole interval.
- Feeding Sync at the old place instead would spend pairs before phase 10. That makes its link-up pair no longer the run's first, and the base check "late FU never steers" fails.
- No check is added, removed or renamed.

Seven commits on `55680bff`, then the merge of main and one commit on it:

- the count refusal (`2ae9a957`), then the ABI and the rest (`6f7b79c8`);
- two test-arm refinements (`97dcac4a`, `f88221c3`) and a tsngen mutant pattern (`c1bc9e21`);
- from review, the #87 mutants held to every check they name (`7c71dcb`) and a spacing fix in the parser arm (`5ed415a`);
- the merge (`98edabb`) and the phase-43 relocation (`b0473e6`).

## Tests

- Parser suite, 378 checks (337 at base):
  - every present TLV reports presence, every absent one does not;
  - heads other than the grandmaster, a thisClock head (loop still reported) and empty TLVs are accepted;
  - a PathTrace after an empty one is still refused as a duplicate.
- Engine suite, 1977 checks per shipping pass (1805 at base) and 60 in the priority1 255 pass (59):
  - Both of the issue's shapes, from priority1 247 against 248, defer. Each is elected, is not master, publishes one coherent commit, sends no Announce for a whole interval of the parent's Sync, then hands back mastership when degraded:
    - stepsRemoved 3 with one entry;
    - a path not headed by its grandmaster, with a check that entry 0 is the received head.
  - An empty TLV publishes {thisClock}.
  - A better grandmaster G2 without a TLV keeps G1's path, G1 at entry 0.
  - After a warm reset, a TLV-less grandmaster keeps {thisClock}.
  - TLV-less parent refreshes keep the full eight-entry path.
  - a), b) and c) still refuse.
- Mutants, each caught by every check it names:
  - parser, 6 new: the head refusal restored, the head replaced by grandmasterIdentity, the empty-path refusal restored, and three that lose or fake TLV presence;
  - engine, 8 new: the three parser refusals planted in the engine build, the empty sequence published without a TLV (the 802.1AS-2020 rule), a TLV-less Announce published as {thisClock}, the received head replaced by the grandmaster or not published, an empty path taking no thisClock, and {thisClock} losing entry 0.
  - At the merge head the engine arm is 113/113: 112 mutants plus the control.
  - Every strict-prefix mutant from either side printed every check it names as FAIL: 79 mutants, 332 named checks.
  - The restored count and head refusals fail "no Announce for one interval" in phase 43, the issue's symptom.

## milan-fpga companion

Lands with the gPTP pin adoption, as a patch, not committed. Apply it on top of #92's companion: the adoption stacks #92's patch first, then this one. This one does not apply to bare dev.

- `KL_gptp_shadow`: eight-entry `pub_path_o`; the path generation covers entry 0 and not the grandmaster.
- `milan_datapath`: GET_AS_PATH (IEEE 1722.1-2021 7.4.41.2) serves entry 0 from the engine's head, and the Table 5.22 AS_PATH comparator watches entry 0. The CSR AS_PATH face keeps its width and takes entries 1..7; `milan_csr` changes only port comments.
- `docs/reference/REGISTER_MAP.md` 0x7DC, `docs/reference/REGISTER_MAP_CLASSES.md` 0x7DC–0x7E4 and the README describe the 2011 rules: entries from entry 0, no TLV keeps the previous pathTrace, an empty TLV gives {thisClock}, and the Table 5.22 comparator works on entry 0.
- tsn_fuzz:
  - the two retired-rule fixtures are adoptions now;
  - stepsRemoved 255 on a one-hop path is the (b) refusal with no parser drop;
  - the campaign README is corrected, and `TEST_RESULTS.md` is regenerated once, after both companions (675 checks).
- gptp_shadow and the milan_dp gPTP leg: TLV-less keep-previous, the empty TLV, a path headed elsewhere served from that head, and the in-flight response cut now on an empty TLV.
- Both path-change detectors are held on a change of entry 0 alone, at equal count and tail.

Stacked on #92's companion, the selected peer must keep its Sync wherever these benches wait:

- The milan_dp gPTP leg's #87/#88 waits send the peer's Sync pair first, as #92's do. The two end-of-leg probes send one usable pair, heard as master, before their Announce.
- tsn_fuzz's two BTCA adoptions do the same, as #92's 12-hop vector does.
- The leg's #207 full-queue arm holds the forced level on every cycle until its Sync's event arrives. Stacked, a periodic counter push reaches the MAC first and dispatch pops inside the window, so a single poke let the event through.
  - That arm's old form fails on the stack.
  - An engine that stops counting the refusal fails the new form.
  - With #92's companion alone, the new form passes.

Every new parent check fails under at least one companion mutant: 64 of 64 from the first companion and 13 of 13 for the entry-0-only change. This round adds 9 controls and mutants, and each fails as intended.

## Gates

Every repository gate ran at base `3426089a` and at the merge head `b0473e69`, each command with its own exit code and log.

| Repository gate | Base | Head |
|---|---|---|
| `make contract` | rc 0 | rc 0 |
| `make -C tb/verilator/ucpu` | 768/768 | 768/768 |
| `make -C tb/verilator/parser` (with mutants) | 337/337, arm 9/9 | 378/378, arm 16/16 |
| `make -C tb/verilator/engine` (4 passes, with mutants) | 1805 ×3 + 59, arm 101/101 | 1977 ×3 + 60, arm 113/113 |
| `make -C tb/verilator/gaskets` | 81/81, arm 5/5 | 81/81, arm 5/5 |
| `make -C tb/tsngen` | 288/288, arm 4/4 | 288/288, arm 4/4 |
| `make -C bench/arty test` | PASS | PASS |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0 | rc 0 |

The milan-fpga consumer gates ran on dev `97aab1d0` with #92's companion applied, in two configurations: at base with the gitlink at main, and at head with this companion stacked on top and the gitlink at the merge head. Both were committed locally.

- All 15 are rc 0 at base and at head: both idiom checks, the HDL front-end gate, RTL source lists, the builder, gptp_shadow (with its mutation arm), port contracts, naming, test evidence, docs, RTL lint, milan_dp `gptp` and `gptp-lat`, milan_dp_gptp and milan_dp_gm_steps.
- Head tallies:
  - gptp_shadow 325 (310 at base);
  - milan_dp `gptp` and `gptp-lat` 200 each (185 at base);
  - milan_dp_gptp PASS;
  - milan_dp_gm_steps 6.
- The tsn_fuzz gPTP campaign: base 677/677; head 675/675, with its results file fresh.
