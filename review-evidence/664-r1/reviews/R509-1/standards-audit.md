# R509-1 clause audit

The four source PDF identities are in `standards-identities.json`.
The review used the repository's pinned timing transcription first, then the
named standards directly. Full PDFs and extracted text remain unpublished.

| Subject | Primary authority examined | Result |
|---|---|---|
| ADP readiness | Milan v1.2 5.6.1 | ADP starts after AECP and the relevant connection requests can be accepted. The split boot sequence preserves this. |
| ADP startup | Milan 5.6.3.5.2 | Startup with link up selects a 0-2 s delay. 10% of the positive window extent is 200 ms. |
| ADP later advertisements | Milan 5.6.3.5.3/.4/.5/.7/.9, Tables 5.50/5.51 | The cited transitions support 0-4 s delay and a fixed 5 s advertisement timer. DISCOVER/GM events in DELAY do not restart it. |
| ADP validity | Milan 5.6.2; IEEE 1722.1-2021 6.2.2.5 | Local Milan advertisements carry valid_time 10; the field uses two-second increments, yielding 20 s. |
| ADP shutdown | Milan 5.6.3.5.8/.11 | Stop the relevant timer and send DEPARTING. These clauses provide no numeric shutdown-response maximum. |
| ADP listener discovery | Milan 5.6.4.1, Table 5.54, 5.6.4.5.1-.4 | Received AVAILABLE/DEPARTING and TMR_NO_ADP drive per-bound-sink discovery, timer updates and connection events. The new budget/hook tables omit an explicit row for these paths: finding R509-1-F2. |
| ACMP | Milan 5.5.2.3, Table 5.26 | All five named transactions have 200 ms timeouts. The 10% ceiling is 20 ms. |
| AECP AEM | IEEE 1722.1-2021 9.3.2.6 | Response 240 ms, transaction timeout 250 ms; optional IN_PROGRESS cadence 120 ms. The stated 24 ms and conditional 12 ms ceilings are correct. |
| AECP MVU | Milan 5.4.3.4 | 240 ms response and 250 ms transaction timeout; 24 ms ceiling. |
| Command and asynchronous notifications | Milan 5.4.5.2/Table 5.22; IEEE 1722.1-2021 7.5.2 | Successful modifying commands require immediate notification after the response. Asynchronous triggers are separately specified. A 10 ms project budget does not replace these obligations. |
| Counter pushes and updates | Milan Table 5.22, 5.3.7.7, 5.3.8.10 | Per-descriptor push frequency is limited to one per second; observed counter updates have a one-second maximum interval. Solicited responses are governed separately. |
| Controller liveness and lock | Milan 5.4.5.3 and 5.4.2.2 | 30-60 s monitoring and 60 s auto-unlock are supported; controller probes retain AECP transaction rules. |
| Optional identification | IEEE 1722.1-2021 7.5.1.2.1 and Figure 7-142 | Three notifications separated by 150 ms; corresponding 10% ceiling 15 ms. Optional status remains explicit. |
| MAAP intervals and count | IEEE 1722-2016 B.3.3/Table B.8, B.3.4.1/.2 | Three retransmissions; strict 500-600 ms probe and 30-32 s announcement intervals. The 50 ms ceiling follows from the shorter related interval. |
| MAAP conflict transitions | IEEE 1722-2016 B.3.2/Table B.7, B.3.5.5, B.3.6.4/.6 | B.3.2/Table B.7 governs loss/restart and when DEFEND occurs. B.3.3 only introduces constants. Finding R509-1-F1 corrects the new table's attribution. |
| MRP timers | IEEE 802.1Q-2018 10.7.4/10.7.11/Table 10-7; Milan 4.2.7.1.1/Table 4.3 | Milan overrides yield JoinTime 180-240 ms, LeaveTime 4500-7500 ms, periodic 900-1500 ms, LeaveAll 9.5-15.5 s. The respective conservative 10% ceilings are 18, 450, 90 and 950 ms. |
| MRP transmission and precision | IEEE 802.1Q-2018 10.7.11 | Point-to-point transmit opportunities are bounded by JoinTime subject to the three-per-1.5-JoinTime constraint. Timer resolution is at most 1 centisecond; it is not itself a response allowance. |

For every listed positive related interval, the proposed 10 ms is within 10%.
The table correctly labels the value as project policy awaiting approval.
Random draws and mandatory spacing remain separate waits; service, backpressure
and observation error cannot silently enlarge normative wire bounds.

The issue is table completeness and the MAAP transition citation, not arithmetic
or a demonstrated target-time result.
