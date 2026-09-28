[A385] TAKEN
Branch: 590-592-599-firmware at 8bc97021f28fb7f729418d3a00851c84ea0b50fd.
Authoritative references: #590, #592, #599 and the assignment above; #397 and PR #588; BAREMETAL_FIRMWARE.md; SAVED_STATE_FASTCONNECT.md section 9.4; REGISTER_MAP.md.
Interpreted scope: console heartbeat opportunities, word-wide capture copy and firmware MDIO link publication in one lane. The #599 bench rerun follows after merge. Internal reviewer [R368]; external reviewer [R369].
Validation plan: full builder bank in both compiler modes, every-shape firmware host self-test, firmware census, one final capture re-measure and receipt gate, service-budget harness, CI scope self-test, docs gates and git diff --check. Observe the assignment's capture and MDIO STOP conditions.
Blockers: none identified during assignment read.
