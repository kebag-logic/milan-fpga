[A690]

Refs #88 and #87. This closes neither: the lane stopped on the part that needs a top-level port change (see "Not in this change").

## What changes

IEEE 802.1AS-2011 (+Cor1/Cor2) 10.3.10.2.1 disqualifies a received Announce only by a), b) and c). The relation N = stepsRemoved+1 in 10.5.3.3.4 is a NOTE, not a qualification rule.

The receive parser refused any Announce whose path trace TLV did not carry exactly stepsRemoved+1 identities. So an end station ignored a better grandmaster that announced, for example, priority1 247, stepsRemoved 3 and a one-entry path, and went on announcing itself every second.

- `hdl/wire/KL_gptp_rx_parser.sv`: the `lengthField/8 != stepsRemoved+1` term leaves the PathTrace header verdict, together with the stepsRemoved register that only fed it.
- Unchanged: the framing rules (even and 8N length, nonzero, wholly inside messageLength, one PathTrace per Announce), the head rule and the all-hop loop verdict for c).
- A path headed by its grandmaster is now accepted at any length. It is copied as received and published with thisClock appended.
- No port, parameter, register-map or microcode change. The generated ROM images are byte-identical.
- Comments and test documentation that stated the old rule are updated.

## Tests

- Parser suite, `check_a_path_count_need_not_match_steps_removed` (20 checks): one entry with stepsRemoved 3, two entries with stepsRemoved 2, and three entries with stepsRemoved 0 are each accepted, with their true count and every identity. A short path holding thisClock still reports the loop bit that c) refuses on.
- Engine suite, 54 new checks; the removed refusal probe had 6:
  - Phase 8o (37 checks), the issue's shape (priority1 247 against 248, stepsRemoved 3, one entry): the plane elects the peer, clears its master flag, publishes {GM, thisClock} in one coherent commit, and transmits no Announce for a whole interval.
  - Paths shorter and longer than stepsRemoved+1 are elected and published with thisClock, and each degraded grandmaster hands mastership back.
  - Phase 8c..8m now opens with a), b) and c), each on a path whose count differs from stepsRemoved+1 (17 checks). Each is still refused by the microcode, with no parser drop.
- Mutants:
  - One per suite restores the base rule.
  - Four new engine mutants each remove a), b) or c) from the microcode, or make a parent update compete instead of replacing the best record (10.3.5).
  - The existing "thisClock fills every later slot" mutant now also names the new zero-tail checks.
  - Every new check fails under at least one named mutant: engine 54 of 54, parser 20 of 20.
  - The engine count mutant reproduces the issue's symptom: "no Announce for one interval" fails because the plane keeps announcing.

## Not in this change

The engine publishes the path as the grandmaster identity at entry 0, plus seven tail slots (`pub_gm_id_o`, `pub_path_count_o`, `pub_path_o`). The milan-fpga GET_AS_PATH response (IEEE 1722.1-2021 7.4.41.2) serves entry 0 from that grandmaster identity.

The cases below have a pathTrace whose first entry is not the grandmaster. Serving them needs a new or wider top-level port, the assignment's STOP condition:

- #88, a path not headed by its grandmaster: {X, B} from G gives pathTrace {X, B, thisClock}.
- #87, a better grandmaster with no TLV after reset: pathTrace stays {thisClock} (10.3.12.1.4 i), Cor1).
- #87, a grandmaster change on a TLV-less Announce: the previous pathTrace is kept.
- Related: a zero-length path trace TLV is still refused. Under a)-c) it qualifies and gives {thisClock}.

So the head refusal, the count-zero publication without a TLV, and the integration description of both are unchanged here.

## Consumer impact

milan-fpga dev `97aab1d0` with this head as the gptp-processor gitlink:

- The parent's tsn_fuzz gPTP campaign pins the retired rule in two fixtures. At head it fails 6 of 677 checks:
  - "one path-trace hop against stepsRemoved 1": the plane now defers;
  - "stepsRemoved 255 on a one-hop path trace": refused by b) in microcode rather than as a parser drop.
- With those two fixtures updated (the first removed as now legal; the second expecting the b) refusal with no parser drop), the campaign passes 672 of 672. Its committed `TEST_RESULTS.md` then needs regenerating.

## Gates

All gates ran at base `55680bff` and at head `2ae9a957`, every command with its own exit code and log.

| Repository gate | Base | Head |
|---|---|---|
| `make contract` | rc 0 | rc 0 |
| `make -C tb/verilator/ucpu` | 768/768 | 768/768 |
| `make -C tb/verilator/parser` (with mutants) | 337/337, arm 9/9 | 355/355, arm 10/10 |
| `make -C tb/verilator/engine` (4 passes, with mutants) | 1703 ×3 + 53, arm 73/73 | 1751 ×3 + 53, arm 78/78 |
| `make -C tb/verilator/gaskets` | 81/81, arm 5/5 | 81/81, arm 5/5 |
| `make -C tb/tsngen` | 288/288, arm 4/4 | 288/288, arm 4/4 |
| `make -C bench/arty test` | PASS | PASS |
| `make lint` | rc 0 | rc 0 |
| `make docs` | rc 0 | rc 0 |

milan-fpga consumer gates on dev `97aab1d0`, with the gptp-processor gitlink at base and at head:

- All 15 rc 0 at base and at head. Every simulation tally at head equals base: gptp_shadow 310, milan_dp `gptp` and `gptp-lat` 185 each, milan_dp_gptp, milan_dp_gm_steps 6.
- That list is the full consumer list: both idiom checks, the HDL front-end gate, RTL source lists, the builder, gptp_shadow, port contracts, naming, test evidence, docs, RTL lint, milan_dp `gptp` and `gptp-lat`, milan_dp_gptp and milan_dp_gm_steps.
- The tsn_fuzz gPTP campaign, outside that list: base 677/677; head 671 pass, 6 fail, as described under "Consumer impact".
