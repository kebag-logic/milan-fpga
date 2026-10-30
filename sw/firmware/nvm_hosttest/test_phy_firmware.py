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
        "\tif (phy_live)\n\t\tphy_link_tick(gettime_ns());\n\tif (!nvm_started)\n"
        "\t\treturn;\n\tnow = gettime_ns();\n",
        "\tif (!nvm_started)\n\t\treturn;\n\tnow = gettime_ns();\n\n\tphy_link_tick(now);\n",
        "PHY boot path persistence disabled: the link-status CSR holds 0"),
    # the persistence-disabled path returning without the console idle hook
    "disabled_path_no_idle_hook": (
        "\t\t/* The console still services the PHY link on this path; the\n"
        "\t\t * writer behind the hook is never admitted (nvm_started 0). */\n"
        "\t\tset_idle_hook(nvm_service);\n", "",
        "PHY boot path persistence disabled: 0 publication(s) in 1000 ms of console idle"),
    # the poll never armed, on any path
    "phy_never_armed": ("\tphy_live = 1;\n", "",
                        "PHY boot path shipping: the link-status CSR holds 0"),
    # the poll without its identity guard: the dispatch hook bit-bangs the
    # pins of a fabric that failed its CSR identity check
    "phy_unguarded": (
        "\tif (phy_live)\n\t\tphy_link_tick(gettime_ns());\n",
        "\tphy_link_tick(gettime_ns());\n",
        "PHY boot path identity mismatch: "),
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
        for mutant in ("none", "no-publish", "defer-recovery", "late-sample", "ack-ignored"):
            text = nvm.FENCE_RE.sub("(void)0;", source)
            if mutant == "no-publish":
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
                expected = "publishes > before" if mutant == "no-publish" else "status_word == expected"
                if result.returncode == 0 or expected not in result.stderr:
                    raise RuntimeError(mutant + " escaped its named assertion")
                print("PHY_MUTANT " + mutant + ": caught")
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
