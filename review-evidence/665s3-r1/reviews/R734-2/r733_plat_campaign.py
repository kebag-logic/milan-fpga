#!/usr/bin/env python3
"""Reviewer probe: the split platform's 37 shipped defects plus reviewer-added probes, through the control
campaign's own machinery (ctrl_mutants.campaign), on copies of the firmware tree.

usage: r733_plat_campaign.py CHECKOUT WORKDIR INDEX COUNT [--extras-only|--shipped-only]

Each defect is planted into a copy (ctrl_mutants.plant copies sw/firmware/ctrl); the checkout is never written.
A reviewer probe names no test (""), so any failed check in its arm catches it; an ESCAPED probe is a
coverage gap to judge, not by itself a defect.
"""
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
index, count = int(sys.argv[3]), int(sys.argv[4])
mode = sys.argv[5] if len(sys.argv) > 5 else "--all"
test_dir = checkout / "sw/firmware/ctrl/test"
sys.path.insert(0, str(test_dir))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))

import ctrl_mutants  # noqa: E402
import plat_mutants  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

PLAT = "plat/ctrl_plat.c"
CSRH = "plat/ctrl_plat_csr.h"
CON = "plat/ctrl_plat_console.c"
OPEN = ("\tif (!ctrl_app_open_held(&p->app, &p->config)) {\n"
        "\t\treturn reach(p, CTRL_PLAT_MAILBOX, \"Milan split: mailbox contract mismatch; entity disabled\\r\\n\");\n"
        "\t}\n")
NVM = "\tnvm_store_boot(env->flash, &p->binding.port);\n"
TICK = "\t(void)ctrl_loop_add_tick(&p->app.loop, nvm_store_service);\n"
IDENT = ("\tif (!ctrl_plat_csr_identity(env->csr, &p->version)) {\n"
         "\t\treturn reach(p, CTRL_PLAT_IDENTITY, \"Milan split: CSR identity mismatch; fabric remains disabled\\r\\n\");\n"
         "\t}\n")
POLICY = "\tctrl_plat_csr_policy(env->csr, env->policy);\n"


def x(name, path, old, new, arm):
    return Mutant("r733-" + name, path, old, new, arm, "", "")


EXTRAS = (
    x("saved-state-after-mailbox-open", PLAT, NVM + TICK + OPEN, TICK + OPEN + NVM, "platboot1"),
    x("adp-never-released", PLAT, "\tctrl_app_release_adp(&p->app);\n", "", "platboot1"),
    x("stopped-boot-console-silent", PLAT, "\t\t(void)ctrl_plat_console_poll(&ctrl_plat.console);\n", "",
      "platboot1"),
    x("banner-missing", PLAT, "\tctrl_plat_console_puts(&p->console, CTRL_PLAT_BANNER);\n", "", "platboot1"),
    x("policy-before-identity", PLAT, IDENT + POLICY, POLICY + IDENT, "platboot1"),
    x("store-service-not-bound", PLAT, TICK, "", "platboot1"),
    x("console-not-a-loop-poll", PLAT, "\t(void)ctrl_loop_add_poll(&p->app.loop, ctrl_plat_console_poll, &p->console);\n",
      "", "platboot1"),
    x("stream-id-shift-8", PLAT, "return entity.mac << 16 | p->env->streams[n].unique_id;",
      "return entity.mac << 8 | p->env->streams[n].unique_id;", "platboot1"),
    x("srp-mac-unset", PLAT, "\t\tp->srp_config.mac[i] = entity.mac;\n", "", "platboot1"),
    x("srp-link-rate-unset", PLAT, "\tp->srp_config.link_rate_bps = p->env->link_rate_bps;\n", "", "platboot1"),
    x("source-interface-all-zero", PLAT, "p->acmp.source_interface[n] = (uint8_t)(n % MBX_N_IF);",
      "p->acmp.source_interface[n] = 0u;", "platboot2"),
    x("csr-dropped-uncounted", PLAT, "\t\t++p->csr_dropped;\n", "", "platboot2"),
    x("window-read-any-interface", PLAT,
      "return interface == 0u ? ctrl_plat_io_read32(p->env->csr + offset) : 0u;",
      "return ctrl_plat_io_read32(p->env->csr + offset);", "platboot2"),
    x("tod-one-try", CSRH, "#define CTRL_PLAT_TOD_TRIES 3u", "#define CTRL_PLAT_TOD_TRIES 1u", "plat"),
    x("tod-no-snapshot-wait", CSRH, "#define CTRL_PLAT_SNAPSHOT_SPIN 128u", "#define CTRL_PLAT_SNAPSHOT_SPIN 0u",
      "plat"),
    x("line-max-one-early", CON, "} else if (c->len == CTRL_PLAT_LINE_MAX) {",
      "} else if (c->len + 1u == CTRL_PLAT_LINE_MAX) {", "plat"),
    x("rx-not-popped", CON, "\t\tctrl_plat_io_write32(c->uart.ev_pending, CTRL_PLAT_UART_EV_RX);\n", "", "plat"),
    x("response-max-too-small", "plat/ctrl_plat_console.h", "#define CTRL_PLAT_RESPONSE_MAX 320u",
      "#define CTRL_PLAT_RESPONSE_MAX 200u", "plat"),
)

def main() -> int:
    shipped = tuple(m for m in ctrl_mutants.MUTANTS if m.name in {p.name for p in plat_mutants.mutants(Mutant)})
    assert len(shipped) == 37, len(shipped)
    table = {"--extras-only": EXTRAS, "--shipped-only": shipped}.get(mode, shipped + EXTRAS)
    ctrl_mutants.MUTANTS = table
    # every test of the platform's three test files must be named by a shipped defect
    ctrl_mutants.NAMED_SOURCES = plat_mutants.SOURCES if mode != "--extras-only" else ()
    print(f"r733 campaign: mode {mode}, {len(table)} defects, member {index} of {count}", flush=True)
    work.mkdir(parents=True, exist_ok=True)
    reuse = work / "reuse"
    cut_reuse(reuse)
    failed = ctrl_mutants.campaign(work / "mutants", reuse, 4, (1, 1), [index, count])
    print(f"r733 campaign member {index}/{count}: {'SOME ESCAPED' if failed else 'ALL CAUGHT'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
