#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit a read-only routed-checkpoint report script from the platform declaration."""

import argparse
from pathlib import Path

from platforms.ax7101_timing import configure_commands, tcl_word


def main() -> None:
    """Write Tcl for a foreground batch run; never write a checkpoint or bitstream."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    checkpoint = args.checkpoint.resolve(strict=True)
    output = args.output_dir.resolve()
    if output == checkpoint.parent or checkpoint.parent in output.parents:
        parser.error("reports must be outside the input checkpoint directory")
    output.mkdir(parents=True, exist_ok=True)
    commands = ["set_param general.maxThreads 16",
                f"open_checkpoint {tcl_word(checkpoint)}",
                *configure_commands(),
                f"kl_timing_grade_reports {tcl_word(output / 'signoff')}",
                "exit"]
    script = output / "report.tcl"
    script.write_text("\n".join(commands) + "\n", encoding="utf-8")
    print(script)


if __name__ == "__main__":
    main()
