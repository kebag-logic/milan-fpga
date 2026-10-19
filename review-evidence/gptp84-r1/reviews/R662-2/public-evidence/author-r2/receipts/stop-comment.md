[A655] STOP at head 53ac2e9d75ceb381c2d2b04854e760304d9ae43f (branch 84-85-tu-pathtrace, two commits on main 43acfbcc: #84 4d6288e8, #85 53ac2e9d; not pushed).

- Repository gates: all rc 0 at base and head. Engine mutation arm: 72/72 caught at head (58/58 at base); 7 new #84 arms and 9 new #85 arms, each failing every check it names.
- Parent consumer gates, full list, on committed local snapshots of dev e9cbb676: all 11 rc 0 at base (gitlink 43acfbcc). At head, 10 of 11 rc 0; `make -C tb/verilator/gptp_shadow` fails 4 of 309 checks, all asserting the received-only path that #85 corrects: `tb/verilator/gptp_shadow/sim_main.cpp:891`, `:930`, `:943`, `:1003` expect counts 3, 1, 3, 3 where head publishes 4, 2, 4, 4 (802.1AS-2020 10.3.13.2.4 f) 5)).
- No port or parameter change (check_port_contracts passes); the meaning of the path count changes, as #85 requires.
- Measured options: the #84 commit alone passes that suite 309/309; head plus a seven-line update of those four expectations passes it 310/310.

Needs a decision: land #84 alone, or land both with a parent companion for those expectations.
