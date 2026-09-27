# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Pin #395's decision and exercise the actual Tcl hook, including its refusals."""

from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sw/litex"))
from platforms.ax7101_timing import TIMING_GRADE, configure_commands, tcl_word  # noqa: E402


STUBS = r"""
set part xc7a100tfgg484-2
set grade industrial
set temp 25
set corners [dict create Slow none Fast none]
proc current_design {} {return design}
proc get_parts {part} {return xc7a100tfgg484-2}
proc get_property {key object} {
    if {$key eq "NAME"} {return $object}
    return $::part
}
proc set_operating_conditions {args} {
    foreach {key value} $args {
        switch -- $key {
            -grade {set ::grade $value}
            -junction_temp {set ::temp $value}
            default {error "unexpected operating condition $key"}
        }
    }
}
proc config_timing_corners {args} {
    array set options $args
    if {[info exists options(-corner)]} {
        dict set ::corners $options(-corner) $options(-delay_type)
    } else {
        foreach name [dict keys $::corners] {
            dict set ::corners $name $options(-delay_type)
        }
    }
}
proc report_config_timing {args} {
    set result ""
    dict for {name delays} $::corners {
        set max [expr {$delays in {max min_max} ? "Yes" : "No"}]
        set min [expr {$delays in {min min_max} ? "Yes" : "No"}]
        append result "$name $max $min\n"
    }
    return $result
}
proc report_operating_conditions {args} {
    return "Device Grade = $::grade\nJunction Temp = $::temp (C)\n"
}
proc report_timing_summary {args} {
    if {[info exists ::fail_report]} {error "planted report failure"}
    puts "SUMMARY $::temp $::corners $args"
}
foreach command {report_timing report_clock_interaction report_cdc check_timing} {
    proc $command {args} {puts "REPORT [lindex [info level 0] 0] $args"}
}
"""


def _run(body: str) -> subprocess.CompletedProcess:
    """Run real Tcl with explicit error propagation, unlike an interactive stdin session."""
    script = STUBS + "\nif {[catch {\n" + body + "\n} message]} {puts stderr $message; exit 1}\n"
    return subprocess.run(["tclsh"], input=script, text=True, capture_output=True,
                          check=False, timeout=30)


def _check_report_content(output: str) -> None:
    """Pin the setup, hold and diagnostic content required by #395 item 2."""
    summaries = [line for line in output.splitlines() if line.startswith("SUMMARY ")]
    assert len(summaries) == 5, output
    for line in summaries:
        assert "-delay_type min_max" in line, line
        assert "-report_unconstrained" in line.split(), line
    combined = [line for line in summaries if line.endswith("_all_timing.rpt")]
    assert len(combined) == 1, output
    assert "-check_timing_verbose" in combined[0].split(), combined[0]
    for command, flags in (
        ("report_clock_interaction", "-delay_type min_max"),
        ("report_cdc", "-details"),
        ("check_timing", "-verbose"),
    ):
        rows = [line for line in output.splitlines() if line.startswith(f"REPORT {command} ")]
        assert len(rows) == 1 and flags in rows[0], (command, rows)
    negative = [line for line in output.splitlines() if line.startswith("REPORT report_timing ")]
    assert len(negative) == 4, output
    for line in negative:
        assert "-delay_type min_max" in line and "-slack_lesser_than 0" in line, line


def test_timing_grade_contract() -> None:
    """The owner decision, each disabled analysis arm, and report failure are detectable."""
    # Independent acceptance oracle from #395, not imported expected values.
    assert TIMING_GRADE == {
        "part": "xc7a100t-fgg484-2", "grade": "commercial",
        "junction_min_c": 0, "junction_max_c": 85, "corners": ("Slow", "Fast"),
    }, "#395 commercial release declaration changed"
    setup = "\n".join(configure_commands())
    good = _run(setup + "\nkl_timing_grade_check")
    assert good.returncode == 0, good.stderr
    mutations = {
        "part": ("set part xc7a100tfgg484-1", "part changed"),
        "grade": ("set grade industrial", "operating conditions changed"),
        "temperature": ("set temp 25", "operating conditions changed"),
    }
    for corner in ("Slow", "Fast"):
        for delays in ("none", "min", "max"):
            mutations[f"{corner} {delays}"] = (
                f"config_timing_corners -corner {corner} -delay_type {delays}",
                f"requires setup and hold at {corner}")
    wrong_part = _run("set part xc7a100tfgg484-1\n" + setup)
    assert wrong_part.returncode == 1 and "part mismatch" in wrong_part.stderr
    with tempfile.TemporaryDirectory(prefix="timing-grade-") as tmp:
        report = f"kl_timing_grade_reports {tcl_word(Path(tmp) / 'candidate')}"
        # The platform calls the report hook. Its leading refusal must run
        # before the report loop can overwrite a candidate's wrong conditions.
        for label, (mutation, reason) in mutations.items():
            for entry in ("kl_timing_grade_check", report):
                result = _run(setup + "\n" + mutation + "\n" + entry)
                assert result.returncode == 1 and reason in result.stderr, (label, entry, result)
                assert not result.stdout, (label, entry, result.stdout)
                assert not list(Path(tmp).iterdir()), (label, entry, "wrote before refusal")
        result = _run(setup + "\n" + report)
        assert result.returncode == 0, result.stderr
        for temp in (0, 85):
            for state in ("Slow min_max Fast none", "Slow none Fast min_max"):
                assert f"SUMMARY {temp} {state} " in result.stdout, result.stdout
        assert "SUMMARY 85 Slow min_max Fast min_max " in result.stdout
        _check_report_content(result.stdout)
        # An interrupted report propagates failure, but restores both timing models.
        result = _run(setup + "\nset fail_report 1\n" +
                      "if {![catch {" + report + "} msg]} {error {failure swallowed}}\n" +
                      "if {$msg ne {planted report failure}} {error $msg}\n" +
                      "kl_timing_grade_check")
        assert result.returncode == 0, result.stderr
    print("  [timing grade] declaration pinned; 19 wrong-condition refusals, including the report hook; "
          "four endpoint/model reports with setup, hold and diagnostics; "
          "complete analysis restored after success and failure")


def test_platform_hooks(python: str) -> None:
    """Inspect actual platform hooks after the same formatting LiteX applies to them."""
    probe = r'''
from platforms.alinx_ax7101 import Platform
from platforms.ax7101_timing import TIMING_GRADE, configure_commands
p = Platform()
assert p.device == TIMING_GRADE["part"], p.device
commands = [c.format(build_name="candidate")
            for c in p.toolchain.pre_placement_commands.resolve(None)]
assert commands == configure_commands(), commands
reports = [c.format(build_name="candidate") for c in p.toolchain.bitstream_commands]
assert reports[0] == "kl_timing_grade_reports candidate_signoff", reports
print("platform declaration reaches the part, pre-placement setup and post-route reports")
'''
    result = subprocess.run([python, "-B", "-c", probe], cwd=ROOT / "sw/litex",
                            text=True, capture_output=True, check=False, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    print("  [timing grade] " + result.stdout.strip())


def test_pll_grade(python: str) -> None:
    """Changing the declared part must reach the real AX7101 PLL constructor."""
    probe = r'''
from unittest.mock import patch
import milan_soc
from platforms.ax7101_timing import TIMING_GRADE
for part, expected in (("xc7a100t-fgg484-2", -2), ("xc7a100t-fgg484-1", -1)):
    with patch.dict(TIMING_GRADE, part=part):
        platform = milan_soc.alinx_ax7101.Platform()
        with patch.object(milan_soc, "S7PLL", wraps=milan_soc.S7PLL) as pll:
            milan_soc._CRG(platform, 100e6)
        assert pll.call_args.kwargs["speedgrade"] == expected, pll.call_args
print("declared part reaches the AX7101 PLL speed grade, including a changed-part control")
'''
    result = subprocess.run([python, "-B", "-c", probe], cwd=ROOT / "sw/litex",
                            text=True, capture_output=True, check=False, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    print("  [timing grade] " + result.stdout.strip())


if __name__ == "__main__":
    test_timing_grade_contract()
    if len(sys.argv) == 2:
        test_platform_hooks(sys.argv[1])
