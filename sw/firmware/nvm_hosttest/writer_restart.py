# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The writer's CPU-only reset, for the host builds of the shipping writer.

A writer restart without a fabric reset: every file-scope variable of the
writer returns to its initial value and `nvm_boot()` runs again, while the
fabric, the backend and the media keep their state. `test_nvm_firmware.py`
appends it to every host build, so check 13 can boot the re-attach path under
a read fault (#671), and `tb/verilator/nvm_cosim/run_cases.py` appends it to
the contract writer for W1 to W4. One list of the writer's statics serves both.
"""
from __future__ import annotations

import re

#: the writer's file-scope state and its initial value: what a CPU-only reset
#: gives back (the C start-up zeroes .bss and reloads .data)
WRITER_STATICS = {"nvm_started": "0", "nvm_ready": "0", "nvm_retired": "0", "nvm_in_commit": "0", "nvm_seq": "0",
                  "nvm_auth_slot": "NVM_SLOT_NONE", "nvm_verdict_a": "0",
                  "nvm_verdict_b": "0", "nvm_last_verdict": "0", "nvm_commits_ok": "0",
                  "nvm_commits_failed": "0", "nvm_captures_refused": "0",
                  "nvm_acks_refused": "0", "nvm_hb_last": "0", "nvm_dirty_since": "0",
                  "nvm_unread": "0", "nvm_unstaged": "0", "nvm_held": "0", "nvm_read_faults": "0"}


def host_restart(text: str) -> str:
    """HOST MODEL ONLY, appended to the host build of the writer: a CPU-only
    reset, the writer's restart without a fabric reset. Refuses unless it
    names every file-scope variable of the writer, so a new one cannot
    survive the modelled reset unnoticed. NOTHING ELSE of a CPU reset is
    modelled -- not the boot code's memory initialisation, not the memory
    holding the live window, not the bus fabric -- so W1 to W4 ASSUME
    obligation O4 of the contract page and cannot test it."""
    found = set(re.findall(r"^static (?:int|uint32_t|uint64_t|unsigned int) (nvm_\w+)(?: = [^;(]+)?;$",
                           text, re.M))
    if found != set(WRITER_STATICS):
        raise SystemExit(f"writer statics {sorted(found)} != restart model {sorted(WRITER_STATICS)}")
    body = "".join(f"\t{k} = {v};\n" for k, v in WRITER_STATICS.items())
    return ("\n/* HOST MODEL ONLY, appended by writer_restart.py: a CPU-only reset of\n"
            " * the writer. The fabric, the backend and the media keep their state;\n"
            " * every static of the writer returns to its initial value and the\n"
            " * writer boots again. */\n"
            "void nvm_host_writer_restart(void);\n"
            "void nvm_host_writer_restart(void)\n{\n" + body +
            "\tset_idle_hook(0);\n\tnvm_boot();\n}\n")
