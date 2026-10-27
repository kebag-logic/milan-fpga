[A690b]

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
- Message word 12 gains a presence bit (63). It lies above the 32 bits the microcode's loop test compares, so the microcode is unchanged; only comments in the generator move. The generated ROM images are byte-identical.
- `docs/INTEGRATION.md` and the HDL and test guides describe the new ABI and rules.

Five commits: the count refusal (`2ae9a957`), then the ABI and the rest (`6f7b79c8`), two test-arm refinements (`97dcac4a`, `f88221c3`) and a tsngen mutant pattern (`c1bc9e21`).

## Tests

- Parser suite, 378 checks (337 at base):
  - every present TLV reports presence, every absent one does not;
  - heads other than the grandmaster, a thisClock head (loop still reported) and empty TLVs are accepted;
  - a PathTrace after an empty one is still refused as a duplicate.
- Engine suite, 1875 checks per shipping pass (1703 at base) and 54 in the priority1 255 pass (53):
  - Both of the issue's shapes, from priority1 247 against 248, defer: elected, not master, one coherent commit, no Announce for a whole interval, then hand back mastership when degraded:
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
  - Every check new at head fails under at least one planted mutant: parser 45 of 45, engine 217 of 217.
  - The head-refusal mutant fails "no Announce for one interval", the issue's symptom.

## milan-fpga companion

Lands with the gPTP pin adoption, as a patch, not committed:

- `KL_gptp_shadow`: eight-entry `pub_path_o`; the path generation covers entry 0 and not the grandmaster.
- `milan_datapath`: GET_AS_PATH (IEEE 1722.1-2021 7.4.41.2) serves entry 0 from the engine's head, and the Table 5.22 AS_PATH comparator watches entry 0. The CSR AS_PATH face keeps its width and takes entries 1..7; `milan_csr` changes only port comments.
- `docs/reference/REGISTER_MAP.md` 0x7DC and the README describe the 2011 rules; the cross-edition text is gone.
- tsn_fuzz:
  - the two retired-rule fixtures are adoptions now;
  - stepsRemoved 255 on a one-hop path is the (b) refusal with no parser drop;
  - `TEST_RESULTS.md` is regenerated (675 checks), and the campaign README is corrected.
- gptp_shadow and the milan_dp gPTP leg (and its comment): TLV-less keep-previous, the empty TLV, a path headed elsewhere served from that head, and the in-flight response cut now on an empty TLV.
- 64 of 64 new parent checks fail under at least one companion mutant. They include the old datapath that served the grandmaster at entry 0, and a shadow that drops entry 0.

## Gates

Every gate ran at base `55680bff` and at head `c1bc9e21`, each command with its own exit code and log.

| Repository gate | Base | Head |
|---|---|---|
| `make contract` | rc 0 | rc 0 |
| `make -C tb/verilator/ucpu` | 768/768 | 768/768 |
| `make -C tb/verilator/parser` (with mutants) | 337/337, arm 9/9 | 378/378, arm 16/16 |
| `make -C tb/verilator/engine` (4 passes, with mutants) | 1703 ×3 + 53, arm 73/73 | 1875 ×3 + 54, arm 85/85 |
| `make -C tb/verilator/gaskets` | 81/81, arm 5/5 | 81/81, arm 5/5 |
| `make -C tb/tsngen` | 288/288, arm 4/4 | 288/288, arm 4/4 |
| `make -C bench/arty test` | PASS | PASS |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0 | rc 0 |

milan-fpga consumer gates on dev `97aab1d0`, gitlink at base, and at head with the companion applied:

- All 15 are rc 0 at base and at head: both idiom checks, the HDL front-end gate, RTL source lists, the builder, gptp_shadow, port contracts, naming, test evidence, docs, RTL lint, milan_dp `gptp` and `gptp-lat`, milan_dp_gptp and milan_dp_gm_steps.
- Head tallies: gptp_shadow 320 (310 at base), milan_dp `gptp` and `gptp-lat` 192 each (185), milan_dp_gptp PASS with verdict lines identical to base, milan_dp_gm_steps 6.
- The tsn_fuzz gPTP campaign: base 677/677; head 675/675 with its regenerated results file fresh.
- The parent's csr suite (with its lockstep and controls) and gptp_txts suite also pass at head.
