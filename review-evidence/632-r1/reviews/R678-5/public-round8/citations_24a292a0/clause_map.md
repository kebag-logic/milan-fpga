# Round 8 item 4: 802.1AS-2020 behaviour citations mapped to IEEE 802.1AS-2011

Text used: IEEE Std 802.1AS-2011 (sha256 a07215b3...), its Cor 1-2013 (e704e89c...) and Cor 2-2015
(dbe16669...), each extracted with `pdftotext -layout`. Milan v1.2 profiles the 2011 edition with both
corrigenda (its normative references; "defined by [802.1AS], [802.1AS-2011/Cor1], and [802.1AS-2011/Cor2]").

## The 2011 clauses (PDF page of the 2011 text)

| Clause (2011) | Page | What it says, in short | 2020 counterpart |
|---|---|---|---|
| 10.3.12.1.4 updtRolesTree() b) | 99 | gmPriority is the best of the systemPriorityVector and each port's gmPathPriorityVector; with no peer it is the systemPriorityVector, whose identity is thisClock | 10.3.13.2.4 updtStatesTree() b) |
| 10.3.12.1.4 i) | 99 | when gmPriority's clockIdentity is thisClock, pathTrace is the single element thisClock | 10.3.13.2.4 i) |
| 10.3.12.1.1 updtRoleDisabledTree() | 99 | initialisation also sets pathTrace to the single element thisClock | 10.3.13.2.1 |
| 10.3.10.2.1 qualifyAnnounce() d) | 96 | a qualified Announce with a path trace TLV, on a SlavePort, copies pathSequence to pathTrace and appends thisClock | 10.3.13.2.4 f) 5) (the append) and 10.3.11.2.1 d) (receivedPathTrace) |
| 9.6.2.1 gmIdentity | 60 | the current grandmaster's ClockIdentity while gmPresent is TRUE | 9.6.2.2 |
| 10.2.3.13 gmPresent | 71 | a grandmaster-capable system is present | 10.2.4.13 |
| 10.2.3.22 thisClock | 71 | this system's clockIdentity | 10.2.4.22 |

Corrigenda: Cor 1-2013 restates 10.3.12.1.4 whole (page 39). Its only changes there are "higher" to "better" in f) 7)
and 8) and the spelling of "clockIdentity" in i); b) and i) keep their meaning, so they are cited "with Cor1-2013".
Cor 1 does not change 10.3.10.2.1. Cor 2-2015 changes only 11.2.15.3 (the MDPdelayReq state diagram, page 12),
so it does not apply to any of these citations.

The edition difference that matters: 2011 has no per-port receivedPathTrace, and no rule that sets pathTrace to an
empty array. 10.3.10.2.1 d) writes pathTrace only from a received TLV. 2020's 10.3.11.2.1 d) sets receivedPathTrace
to the empty array when the TLV is absent.

## Each site (file:line at 24a292a0)

| Site | Was (417ec528) | Now | Behaviour |
|---|---|---|---|
| `docs/reference/REGISTER_MAP.md:1051` | 802.1AS-2020 10.3.13.2.4 b) | 802.1AS-2011 10.3.12.1.4 b), with Cor1-2013 | `0x624` reads thisClock before a peer |
| `docs/reference/REGISTER_MAP.md:1471-1475` (the pre-existing neighbour; reviewed) | 802.1AS-2020 10.3.11.2.1(d) makes the sequence empty | 2011 10.3.10.2.1 d) writes pathTrace only from a received TLV; the engine's empty sequence for an Announce without one is named as the rule 802.1AS-2020 10.3.11.2.1 d) states | count zero with no TLV (open question below) |
| `docs/reference/REGISTER_MAP.md:1478` (was 1476) | 802.1AS-2020 10.3.13.2.4 f) 5) | 802.1AS-2011 10.3.10.2.1 d) | received pathSequence plus thisClock |
| `docs/reference/REGISTER_MAP.md:1480` (was 1478, no edition named) | 10.3.13.2.4 i) | 802.1AS-2011 10.3.12.1.4 i), with Cor1-2013 | `{thisClock}` before a peer |
| `docs/reference/SUBMODULES.md:242` | 802.1AS-2020 Section 10.3.13.2.4 b) and i) | 802.1AS-2011 Section 10.3.12.1.4 b) and i), with Cor1-2013 | boot grandmaster and path |
| `docs/reference/SUBMODULES.md:244` | 802.1AS-2020 Section 10.3.13.2.4 f) 5) | 802.1AS-2011 Section 10.3.10.2.1 d) | pathTrace append |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:79-80` | 802.1AS-2020 10.3.13.2.4 f) 5) | 802.1AS-2011 10.3.10.2.1 d) | the PathTrace oracle |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1175-1176` | 802.1AS-2020 10.3.13.2.4 b) and i) | 802.1AS-2011 10.3.12.1.4 b) and i), with Cor1-2013 | own grandmaster before a peer |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1225-1227` | same | same | own grandmaster after reset |
| `tb/verilator/milan_dp/sim_gptp.cpp:51-52` | 802.1AS-2020 10.3.13.2.4 f) 5) | 802.1AS-2011 10.3.10.2.1 d) | the PathTrace oracle |
| `tb/verilator/milan_dp/sim_gptp.cpp:818-819` | 802.1AS-2020 10.3.13.2.4 b) and i) | 802.1AS-2011 10.3.12.1.4 b) and i), with Cor1-2013 | own grandmaster before a peer |

## Kept, with the reason

- `docs/reference/REGISTER_MAP.md:1474`, "the rule IEEE 802.1AS-2020 10.3.11.2.1 d) states". This is an explicit
  cross-edition statement. The engine publishes an empty sequence when the selected Announce carries no path trace
  TLV, and that rule exists only in 2020. The 2011 clause beside it states what 2011 does say. It is the only
  802.1AS-2020 citation left in the lines this PR adds (`added_2020_count.txt`: 1, against 9 at 417ec528).
- The scan found no other behavioural 802.1AS-2020 citation in the added lines (`added_lines_scan.txt`). The
  remaining 802.1AS-2020 citations in the tree are not on lines this PR adds. Among them are REQUIREMENTS.md:115
  (PHC/timestamp-assist context) and GPTP_PLANE.md:109 and :460 (explicitly not the edition of record). This PR
  leaves them as dev has them.

## Open question (published, not decided here)

Read literally, 2011 keeps pathTrace at its previous value when a qualified Announce on the slave port carries no
path trace TLV. After initialisation that value is `{thisClock}` (10.3.12.1.1). The engine (FPGA-gPTP, pinned at
55680bff, unchanged by this PR) publishes count zero, which is 2020's rule. Changing that is an engine change
outside this PR, so the documentation names both editions and the question goes to the manager.
