#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Drive the firmware's bit-bang transactions and kill a missing publisher.

The boot-path arms boot the whole firmware in the host harness's PHY build
and grade what reaches the link-status CSR on each path (#70): the shipping
boot and the persistence-disabled one must publish the peer's link at least
every 250 ms while the console idles, and a boot that failed the CSR identity
check must not touch the MDIO pins at all.
"""
from pathlib import Path
import re
import subprocess
import tempfile

import test_nvm_firmware as nvm

#: the planted startup states, as test_disabled_writer.py plants them
SHAPE_OFF = ("return count == NVM_N_REC && bytes == NVM_AREA_RAW &&",
             "return 0 && count == NVM_N_REC && bytes == NVM_AREA_RAW &&")
IDENTITY_OFF = ("if (id != MILAN_ID_MAGIC) {", "if (1) {")
#: (label, plant, the firmware's line that proves the path was reached,
#: whether the link must be published)
BOOT_PATHS = (
    ("shipping", None, "walk done=1", True),
    ("persistence disabled", SHAPE_OFF, "persistence disabled", True),
    ("identity mismatch", IDENTITY_OFF, "CSR identity mismatch", False),
)
#: the console idle after the boot, and the publication period it must keep
IDLE_MS = 1000
PUBLICATION_MS = 250
#: the peer's 1000BASE-T full duplex, as phy_resolved_status() encodes it
GIGABIT_FULL = 13
PHY_RE = re.compile(r"HOST phy at=(\w+) transfers=(\d+) publishes=(\d+) status=(\d+)")

#: the defects the boot-path arms must catch, each planted into a copy, and
#: the words of the finding that must name it
BOOT_MUTANTS = {
    # the heartbeat as at dev 1e80128f: the poll behind the writer's gate
    "phy_behind_the_writer": (
        "\tif (!nvm_started) {\n\t\tif (phy_live)\n\t\t\tphy_link_tick(gettime_ns());\n"
        "\t\treturn;\n\t}\n",
        "\tif (!nvm_started)\n\t\treturn;\n",
        "PHY boot path persistence disabled: the link-status CSR holds 0"),
    # the persistence-disabled path returning without the console idle hook
    "disabled_path_no_idle_hook": (
        "\t\t/* The console still services the PHY link on this path; the\n"
        "\t\t * writer behind the hook is never admitted (nvm_started 0). */\n"
        "\t\tset_idle_hook(nvm_service);\n", "",
        "PHY boot path persistence disabled: 0 publication(s) in 1000 ms of console idle"),
    # the poll never armed: only an admitted writer's path polls the PHY
    "phy_never_armed": ("\tphy_live = 1;\n", "",
                        "PHY boot path persistence disabled: the link-status CSR holds 0"),
    # the poll taken off the admitted writer's path, the shipping one
    "phy_off_the_writer_path": ("\tnow = gettime_ns();\n\n\tphy_link_tick(now);\n",
                                "\tnow = gettime_ns();\n\n",
                                "PHY boot path shipping: the link-status CSR holds 0"),
    # the poll without its identity guard: the dispatch hook bit-bangs the
    # pins of a fabric that failed its CSR identity check
    "phy_unguarded": (
        "\t\tif (phy_live)\n\t\t\tphy_link_tick(gettime_ns());\n",
        "\t\tphy_link_tick(gettime_ns());\n",
        "PHY boot path identity mismatch: "),
}

#: the PHY init's advertisement and restart writes, as milan_baremetal.c spells them
ADVERTISEMENT_WRITES = ("\tphy_mdio_write(9, ((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |\n"
                        "\t\t       PHY_GBCR_1000_FULL);\n"
                        "\tphy_mdio_write(4, (unsigned int)advertisement &\n"
                        "\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));\n")
RESTART_WRITE = ("\tphy_mdio_write(0, ((unsigned int)control | PHY_BMCR_AN_ENABLE |\n"
                 "\t\t\t   PHY_BMCR_AN_RESTART) &\n"
                 "\t\t       ~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE));\n")
#: the PHY init's check that its three reads were acknowledged
READ_GUARD = "\tif (advertisement < 0 || gigabit < 0 || control < 0)\n\t\treturn 0;\n"
#: the register 4 and register 9 values the PHY init writes, as it spells them
REGISTER_4_VALUE = ("(unsigned int)advertisement &\n"
                    "\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED)")
REGISTER_9_KEEP = "((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |"
#: the register 0 value the PHY init writes, as it spells it
REGISTER_0_VALUE = ("((unsigned int)control | PHY_BMCR_AN_ENABLE |\n"
                    "\t\t\t   PHY_BMCR_AN_RESTART) &\n"
                    "\t\t       ~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE)")
#: #840: each kept field the peer grades: its register, its bits and the
#: assertion that grades it. The init's other pass-through bits in registers
#: 4 and 0 are unmodified by construction and not graded.
KEPT_FIELDS = ((4, range(0, 5), "selector_kept"),
               (4, range(10, 12), "pause_bits_kept"),
               (9, range(10, 13), "master_slave_kept"),
               (0, range(11, 12), "power_down_kept"),
               (0, range(14, 15), "loopback_kept"))


def kept_bit_mutants() -> dict[str, tuple[str, str, str]]:
    """Each bit of a graded field forced on and dropped, one mutant each: a keep is an identity."""
    mutants = {}
    for register, bits, assertion in KEPT_FIELDS:
        for bit in bits:
            mask = f"0x{1 << bit:04x}u"
            if register == 9:
                forced = (REGISTER_9_KEEP, f"{REGISTER_9_KEEP} {mask} |")
                dropped = (REGISTER_9_KEEP, REGISTER_9_KEEP.replace("MASTER_SLAVE)", f"MASTER_SLAVE & ~{mask})"))
            else:
                value = REGISTER_4_VALUE if register == 4 else REGISTER_0_VALUE
                forced = (value, f"{mask} | ({value})")
                dropped = (value, value.replace("~(", f"~({mask} | "))
            mutants[f"force-bit-{register}.{bit}"] = (*forced, assertion)
            mutants[f"drop-bit-{register}.{bit}"] = (*dropped, assertion)
    return mutants


#: #840: the PHY init defects the pin-level peer must catch, each planted into
#: a copy of the firmware, and the assertion that must name it
ADVERTISEMENT_MUTANTS = {
    # register 4 keeps 100BASE-TX and 100BASE-TX full duplex (bits 7 and 8)
    "advertise-100base-tx": ("#define PHY_ANAR_BELOW_GIGABIT 0x03e0u",
                             "#define PHY_ANAR_BELOW_GIGABIT 0x0260u",
                             "no_100base_tx_advertised"),
    # register 4 keeps 10BASE-T and 10BASE-T full duplex (bits 5 and 6)
    "advertise-10base-t": ("#define PHY_ANAR_BELOW_GIGABIT 0x03e0u",
                           "#define PHY_ANAR_BELOW_GIGABIT 0x0380u",
                           "no_10base_t_advertised"),
    # register 4 keeps 100BASE-T4 (bit 9)
    "advertise-100base-t4": ("#define PHY_ANAR_BELOW_GIGABIT 0x03e0u",
                             "#define PHY_ANAR_BELOW_GIGABIT 0x01e0u",
                             "no_100base_t4_advertised"),
    # register 9 keeps 1000BASE-T half duplex (bit 8)
    "advertise-1000base-t-half": ("#define PHY_GBCR_1000_FULL 0x0200u",
                                  "#define PHY_GBCR_1000_FULL 0x0300u",
                                  "no_gigabit_half_duplex_advertised"),
    # register 9 loses 1000BASE-T full duplex (bit 9)
    "no-1000base-t-full": ("PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);",
                           "PHY_GBCR_MASTER_SLAVE));",
                           "gigabit_full_duplex_advertised"),
    # the advertisement written without the auto-negotiation restart
    "no-restart": (RESTART_WRITE, "\t(void)control;\n", "auto_negotiation_restarted"),
    # the restart moved ahead of the advertisement it must apply
    "restart-first": (ADVERTISEMENT_WRITES + RESTART_WRITE, RESTART_WRITE + ADVERTISEMENT_WRITES,
                      "restart_after_advertisement"),
    # a register written from a read that was not acknowledged
    "write-unread": (READ_GUARD, "", "no_write_before_its_read"),
    # register 4 written from a read that was not acknowledged
    "nak-reg4-not-checked": (READ_GUARD, READ_GUARD.replace("advertisement < 0 || ", ""),
                             "no_write_before_its_register_4_read"),
    # register 0 written from a read that was not acknowledged
    "nak-reg0-not-checked": (READ_GUARD, READ_GUARD.replace(" || control < 0", ""),
                             "no_write_before_its_register_0_read"),
    # the advertisement written though the ability read was not acknowledged
    "write-unread-ability": ("\tif (extended < 0)\n\t\treturn 0;\n", "",
                             "no_write_before_its_ability_read"),
    # the advertisement and its restart repeated on every poll
    "advertise-every-poll": ("\tif (!phy_advertised && bmsr >= 0)\n"
                             "\t\tphy_advertised = phy_advertise_gigabit_only((unsigned int)bmsr);\n",
                             "\tif (bmsr >= 0)\n"
                             "\t\tphy_advertised = phy_advertise_gigabit_only((unsigned int)bmsr);\n",
                             "advertised_once"),
    # a PHY without the extended-status register (IEEE 802.3-2022
    # 22.2.4.2.16), the 10/100 PHY of an MII build, written all the same
    "advertise-without-extended-status": ("\tif (!(bmsr & PHY_BMSR_EXTENDED))\n\t\treturn 1;\n",
                                          "\t(void)bmsr;\n", "no_write_without_extended_status"),
    # a PHY whose register 15 lacks 1000BASE-T full duplex (22.2.4.4.3),
    # written all the same
    "advertise-without-1000base-t-full": ("\tif (!(extended & PHY_ESTATUS_1000_FULL))\n\t\treturn 1;\n",
                                          "", "no_write_without_1000base_t_full_ability"),
    # the ability gate on 1000BASE-T half duplex (bit 15.12), not full (15.13)
    "gate-on-1000base-t-half": ("#define PHY_ESTATUS_1000_FULL 0x2000u",
                                "#define PHY_ESTATUS_1000_FULL 0x1000u",
                                "no_write_without_1000base_t_full_ability"),
    # a 10/100 PHY's register 15 read again by the PHY init on every poll
    "ability-reread-every-poll": ("\tif (!(extended & PHY_ESTATUS_1000_FULL))\n\t\treturn 1;\n",
                                  "\tif (!(extended & PHY_ESTATUS_1000_FULL))\n\t\treturn 0;\n",
                                  "ability_read_once"),
    # register 4 never written
    "no-register-4-write": ("\tphy_mdio_write(4, (unsigned int)advertisement &\n"
                            "\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));\n",
                            "\t(void)advertisement;\n", "no_10base_t_advertised"),
    # register 4 loses its pause bits 10 and 11 (Table 28B-2), which it keeps
    "clear-pause-bits": ("#define PHY_ANAR_BELOW_GIGABIT 0x03e0u",
                         "#define PHY_ANAR_BELOW_GIGABIT 0x0fe0u", "pause_bits_kept"),
    # register 4 keeps reserved bit 14 (Table 28-2) as read
    "keep-reserved-bit-14": ("#define PHY_ANAR_RESERVED 0x4000u",
                             "#define PHY_ANAR_RESERVED 0x0000u", "reserved_bit_14_cleared"),
    # register 9 drops its MASTER-SLAVE bits 12 to 10 (Table 40-3), which it keeps
    "drop-master-slave": ("((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |",
                          "(0u * (unsigned int)gigabit) |", "master_slave_kept"),
    # register 9 keeps its test-mode bits 15 to 13 as read
    "keep-test-mode": ("#define PHY_GBCR_MASTER_SLAVE 0x1c00u",
                       "#define PHY_GBCR_MASTER_SLAVE 0xfc00u", "test_mode_cleared"),
    # the restart keeps reset (bit 0.15) as read
    "restart-keeps-reset": ("~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE));", "~(PHY_BMCR_ISOLATE));",
                            "reset_cleared"),
    # the restart keeps isolate (bit 0.10) as read
    "restart-keeps-isolate": ("~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE));", "~(PHY_BMCR_RESET));",
                              "isolate_cleared"),
    # the restart leaves auto-negotiation disabled (bit 0.12) as read
    "no-auto-negotiation-enable": ("((unsigned int)control | PHY_BMCR_AN_ENABLE |\n",
                                   "((unsigned int)control |\n", "auto_negotiation_enabled"),
    # register 4 always written with both pause bits set
    "force-pause-on": (REGISTER_4_VALUE, f"0x0c00u | ({REGISTER_4_VALUE})", "pause_bits_kept"),
    # register 9 always written with manual MASTER-SLAVE, overriding automatic resolution
    "force-manual-master": (REGISTER_9_KEEP, f"{REGISTER_9_KEEP} 0x1c00u |", "master_slave_kept"),
    # register 9 always written with bit 12, manual configuration, set
    "force-manual-config-only": (REGISTER_9_KEEP, f"{REGISTER_9_KEEP} 0x1000u |", "master_slave_kept"),
    **kept_bit_mutants(),
}


def phy_csr(work: Path) -> None:
    """The stub CSR header with the MDIO path compiled in, ahead of the stubs'."""
    (work / "generated").mkdir(parents=True, exist_ok=True)
    (work / "generated/csr.h").write_text(
        f'#include "{nvm.STUBS / "generated/csr.h"}"\n'
        '#define CSR_MILAN_MAC_PHY_MDIO_W_ADDR 1\n')


def boot_path_findings(cfg: Path, work: Path, source: str) -> list[str]:
    """Boot each path, idle the console, and grade the link-status CSR."""
    findings = []
    for label, plant, reached, published in BOOT_PATHS:
        text = source
        if plant:
            if source.count(plant[0]) != 1:
                raise RuntimeError("PHY boot-path anchor changed: " + label)
            text = source.replace(*plant)
        bench_dir = work / label.replace(" ", "-")
        phy_csr(bench_dir)
        bench = nvm.make_bench(cfg, bench_dir, text, ("-DNVM_HOST_PHY",))
        raw, _, _ = nvm.run(bench, "--boot", "--uart", "milan_status",
                            "--idle-ms", str(IDLE_MS))
        if reached not in raw:
            raise RuntimeError("PHY boot-path precondition was not reached: " + label)
        phy = {at: tuple(int(v) for v in rest) for at, *rest in PHY_RE.findall(raw)}
        transfers, publishes, status = phy["end"]
        idle = publishes - phy["boot"][1]
        if published and status != GIGABIT_FULL:
            findings.append(f"PHY boot path {label}: the link-status CSR holds {status}, "
                            f"not the peer's 1000BASE-T full duplex ({GIGABIT_FULL})")
        if published and idle < IDLE_MS // PUBLICATION_MS:
            findings.append(f"PHY boot path {label}: {idle} publication(s) in {IDLE_MS} ms "
                            f"of console idle, fewer than one per {PUBLICATION_MS} ms")
        if not published and (transfers or publishes):
            findings.append(f"PHY boot path {label}: {transfers} MDIO transfer(s) and "
                            f"{publishes} publication(s) on a fabric that failed its identity check")
        print(f"PHY_BOOT {label}: transfers={transfers} publishes={publishes} "
              f"idle_publishes={idle} status={status}")
    return findings


def boot_path_self_test(cfg: Path, work: Path, source: str) -> list[str]:
    """Each planted boot-path defect must be caught by its named finding."""
    findings = []
    for name, (old, new, words) in BOOT_MUTANTS.items():
        if source.count(old) != 1:
            findings.append(f"PHY boot-path mutant {name}: the plant no longer matches the firmware")
            continue
        got = boot_path_findings(cfg, work / name, source.replace(old, new))
        named = [item for item in got if item.startswith(words)]
        if named:
            print(f"PHY_BOOT_MUTANT {name}: caught by {named[0]}")
        else:
            findings.append(f"PHY boot-path mutant {name} escaped {words!r}; findings: {got}")
    return findings


def main() -> None:
    """Compile the product translation with a pin-level peer and unchanged policy."""
    source = nvm.FIRMWARE.read_text()
    with tempfile.TemporaryDirectory(prefix="milan-phy-") as temporary:
        work = Path(temporary)
        nvm.make_bench(nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
        phy_csr(work)
        driver = Path(__file__).with_name("phy_host.c")
        command = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format",
                   "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
                   f"-I{work}", f"-I{nvm.STUBS}", str(driver), "-o", str(work / "phy")]
        for mutant in ("none", "no-publish", "defer-recovery", "late-sample", "ack-ignored",
                       *ADVERTISEMENT_MUTANTS):
            text = nvm.FENCE_RE.sub("(void)0;", source)
            if mutant in ADVERTISEMENT_MUTANTS:
                anchor, plant, _ = ADVERTISEMENT_MUTANTS[mutant]
                if text.count(anchor) != 1:
                    raise RuntimeError(mutant + " mutation anchor is not unique")
                text = text.replace(anchor, plant)
            elif mutant == "no-publish":
                anchor = "\tmilan_mac_link_status_write(status);"
                if text.count(anchor) != 1:
                    raise RuntimeError("publisher mutation anchor is not unique")
                text = text.replace(anchor, "\t(void)status;")
                text = text.replace("milan_mac_link_status_write(0);", "(void)0;")
            elif mutant == "ack-ignored":
                anchor = "return ack ? -1 : (int)value;"
                if text.count(anchor) != 1:
                    raise RuntimeError("acknowledgement mutation anchor is not unique")
                text = text.replace(anchor, "(void)ack; return (int)value;")
            elif mutant == "late-sample":
                anchor = ("\tvalue = milan_mac_phy_mdio_r_read() & 1u;\n"
                          "\tmilan_mac_phy_mdio_w_write(pins | PHY_MDC);\n\tcdelay(32);")
                if text.count(anchor) != 1:
                    raise RuntimeError("phase mutation anchor is not unique")
                text = text.replace(anchor,
                                    "\tmilan_mac_phy_mdio_w_write(pins | PHY_MDC);\n"
                                    "\tcdelay(32);\n\tvalue = milan_mac_phy_mdio_r_read() & 1u;")
            elif mutant == "defer-recovery":
                anchor = ("\tif (bmsr >= 0 && !(bmsr & PHY_BMSR_LINK) && (phy_published & 1u)) {\n"
                          "\t\tmilan_mac_link_status_write(0);\n"
                          "\t\tphy_published = 0;\n\t}\n")
                if text.count(anchor) != 1:
                    raise RuntimeError("recovery mutation anchor is not unique")
                text = text.replace(anchor, "")
            (work / "milan_baremetal.c").write_text(text)
            subprocess.run(command, check=True, timeout=120)
            result = subprocess.run([str(work / "phy")], capture_output=True, text=True, timeout=120)
            if mutant == "none":
                if result.returncode or "PHY_OK" not in result.stdout:
                    raise RuntimeError(result.stdout + result.stderr)
                print(result.stdout, end="")
            else:
                # A late sample first corrupts the poll's register 1 read, so
                # the PHY init sees no extended status and writes nothing:
                # the first advertisement property graded names it (#840).
                expected = ("publishes > before" if mutant == "no-publish" else
                            "no_10base_t_advertised" if mutant == "late-sample" else
                            ADVERTISEMENT_MUTANTS[mutant][2] if mutant in ADVERTISEMENT_MUTANTS else
                            "status_word == expected")
                if result.returncode == 0 or f"Assertion `{expected}' failed" not in result.stderr:
                    raise RuntimeError(mutant + " escaped its named assertion " + expected)
                print("PHY_MUTANT " + mutant + ": caught by " + expected)
        cfg = nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
        findings = boot_path_findings(cfg, work / "boot", source)
        if findings:
            raise RuntimeError("; ".join(findings))
        findings = boot_path_self_test(cfg, work / "boot-mutants", source)
        if findings:
            raise RuntimeError("; ".join(findings))
        print("PHY_BOOT_OK: every boot path past the identity check publishes the link")


if __name__ == "__main__":
    main()
