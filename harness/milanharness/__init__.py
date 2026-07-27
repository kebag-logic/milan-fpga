# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Milan validation + torture harness - host-side package.
#!
#! Design rules that the rest of this package obeys without restating them:
#!
#!   * Nothing bench-identifying is ever compiled in. Hosts, interfaces, outlet
#!     numbers and webhook URLs come from the config file (`config.py`).
#!   * Register OFFSETS are compiled in - they are the stable ABI of
#!     `docs/reference/REGISTER_MAP.md`. Only the window BASE is configuration.
#!   * Board-side work is POSIX `sh` + `devmem`/`dd` (no Python on the boards);
#!     all analysis happens here.
#!   * A step that cannot run is BLOCKED, not FAILED. Only a real defect is
#!     FAILED, because only FAILED wakes a human.

__all__ = ["VERSION"]

VERSION = "1.0.0"
