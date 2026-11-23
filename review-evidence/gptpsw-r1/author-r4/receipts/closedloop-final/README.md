# Fresh closed-loop and flood run after the hot-list relearn

Run head: 334ca4b7116d6b3ab636488d411716c9ef3850e5. Final head 8267b895 differs only in design-page prose.
The relevant source equality is checked in ../after-relearn/source-equivalence.txt.

`make -j16 -C tb/verilator/gptp_sw`: all 48 checks pass. Slave and grandmaster modes run at two interfaces.
Flood: 490 delivered messages stamped, zero unstamped, zero lost egress records; lock by 2.9 s and worst later
absolute offset 95 ns. baseline.log is the complete command output captured from the separate simulation unit.

The initial nine-minute foreground unit completed the baseline, then reached its time limit while the stock
mutation driver was redundantly repeating that same baseline. This is not a failed assertion, and its incomplete
mutation run is not counted. The completed baseline and all 14 existing plants are split into separate legs:
`python3 run-plants.py <same-clean-clone> <scratch-output> <baseline-log>` invokes the unmodified driver's one()
for every entry of MUTANTS, with its own required failing words. The runner is included here. No plant or test
was removed or weakened. The aggregate is complete only when plants.log reports all 14 caught.
