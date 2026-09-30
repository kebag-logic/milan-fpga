# R400-3 provisional verdict and ledger (written before reading any prior review finding or other reviewer report)

Written: 2026-09-30T07:43:17Z
Exact head: 921fff59d6e1243284e477f7a368173018420d35 (tree dc1d52a75724f6ab29f4831d7498dece23202ca8)

Provisional verdict: POSITIVE (no open MINOR, MAJOR or BLOCKER from the independent pass).

| Lens | Provisional | Basis |
|---|---|---|
| Conformance | CLEAN | U29 expectations match Table B.7 Release!/PortOperational!, B.3.2, B.3.5.2 and the ruling 5890772857; RTL delta byte-identical to round 2 |
| RTL | CLEAN | no hdl/ change in round 3 (lane hdl diff vs main == round-2 lane diff vs base); eng_w combinational so U29 falls are seen in the named state |
| Robustness | CLEAN | merge truth table of pp_top modes correct; every focused mode rc 0; U29 kills round-1 RTL 20/20 and 3 reviewer probes |
| Tests | CLEAN | maap 196, rx_validator 497, pp_top 7893 (MP 34, D3 133, NW 85, GSI 6182), srp_top 2200; campaign 32/32; d3 slice 2/2 + goldens |
| Docs | CLEAN | README ledger rows equal a fresh campaign run (29/29); PR-body line refs verified; S1 wording present in U23, U28, README, PR body |
