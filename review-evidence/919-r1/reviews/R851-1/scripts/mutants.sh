#!/usr/bin/env bash
# mutants.sh: the round's disposable mutants of ctrl_plat_phy.c, each built into a copy and run against
# test_plat_phy.cpp (phy_probe.sh); one line per mutant with the suite's exit status (0: the mutant survives).
# Needs the unit gate's generated headers (phy_probe.sh's G), i.e. test_ctrl_firmware.py run once with
# --build-dir scratch/fw-unit.
set -u
P=${PACKET:?export PACKET, this packet directory}
S=${CLONE:?export CLONE}/sw/firmware/ctrl/plat/ctrl_plat_phy.c
M=$P/scratch/probe/mutants; mkdir -p "$M"
mk() { python3 -I "$P/scripts/mkmut.py" "$S" "$M/$1.c" "$2" "$3" || echo "$1: anchor refused"; }
# m1: gigabit_only ignores register 4 (both the restart decision and the read-back)
mk m1 'return (anar & CTRL_PLAT_PHY_ANAR_BELOW_GIGABIT) == 0u &&\n' 'return (anar & 0u) == 0u &&\n'
# m2: the read-back ignores register 4
mk m2 'if (phy->local >= 0 && v >= 0 && gigabit_only((uint32_t)phy->local, u)) {' 'if (phy->local >= 0 && v >= 0 && gigabit_only(0u, u)) {'
# m3: the after-loss restart decision ignores register 4 (a PHY that lost 4 alone is not restarted)
mk m3 '((phy->adv & CTRL_PLAT_PHY_ADV_BOOT) == 0u && gigabit_only((uint32_t)phy->local, (uint32_t)phy->gig))' '((phy->adv & CTRL_PLAT_PHY_ADV_BOOT) == 0u && gigabit_only(0u, (uint32_t)phy->gig))'
# m3b: the after-loss restart decision ignores register 9
mk m3b '((phy->adv & CTRL_PLAT_PHY_ADV_BOOT) == 0u && gigabit_only((uint32_t)phy->local, (uint32_t)phy->gig))' '((phy->adv & CTRL_PLAT_PHY_ADV_BOOT) == 0u && gigabit_only((uint32_t)phy->local, CTRL_PLAT_PHY_GCTRL_1000_FULL))'
# m4: the advertisement owed again only on the latched-loss path, not on every published loss
mk m4 '	if ((phy->published & ~word & CTRL_PLAT_PHY_LINK_UP) != 0u) {\n		phy->adv = CTRL_PLAT_PHY_ADV_OWED;\n	}\n' ''
[ -f "$M/m4.c" ] && sed -i 's|\t\t\t\tpublish(phy, 0u);|\t\t\t\tpublish(phy, 0u);\n\t\t\t\tphy->adv = CTRL_PLAT_PHY_ADV_OWED;|' "$M/m4.c"
# m5: a frame needs more than its stated cost of room
mk m5 'if (room >= (int32_t)CTRL_PLAT_PHY_STEP_US) {' 'if (room > (int32_t)CTRL_PLAT_PHY_STEP_US) {'
# m6: an unacknowledged ability read is taken as no ability (equivalent: -1 reads as all ones)
mk m6 '		if (v >= 0 && (u & CTRL_PLAT_PHY_ESTAT_1000T_FULL) == 0u) {' '		if ((u & CTRL_PLAT_PHY_ESTAT_1000T_FULL) == 0u) {'
# m7: a poll due one microsecond late
mk m7 'return !phy->polled || now - phy->started >= CTRL_PLAT_PHY_POLL_US;' 'return !phy->polled || now - phy->started > CTRL_PLAT_PHY_POLL_US;'
# m8: the advertisement only at boot
mk m8 '	if (stage == CTRL_PLAT_PHY_STATUS && v >= 0 && phy->adv != 0u) {' '	if (stage == CTRL_PLAT_PHY_STATUS && v >= 0 && phy->adv != 0u && (phy->adv & CTRL_PLAT_PHY_ADV_BOOT) != 0u) {'
for m in m1 m2 m3 m3b m4 m5 m6 m7 m8; do
  "$P/scripts/phy_probe.sh" "$M/$m" "$M/$m.c" > "$M/$m.summary" 2>&1
  echo "$m rc=$? $(grep -m1 -o 'FAILED  \] [A-Za-z0-9_.]*' "$M/$m/run.log" 2>/dev/null)"
done
