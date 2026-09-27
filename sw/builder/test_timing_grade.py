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
    for label, (mutation, reason) in mutations.items():
        result = _run(setup + "\n" + mutation + "\nkl_timing_grade_check")
        assert result.returncode == 1 and reason in result.stderr, (label, result)
    wrong_part = _run("set part xc7a100tfgg484-1\n" + setup)
    assert wrong_part.returncode == 1 and "part mismatch" in wrong_part.stderr
    with tempfile.TemporaryDirectory(prefix="timing-grade-") as tmp:
        report = f"kl_timing_grade_reports {tcl_word(Path(tmp) / 'candidate')}"
        result = _run(setup + "\n" + report)
        assert result.returncode == 0, result.stderr
        for temp in (0, 85):
            for state in ("Slow min_max Fast none", "Slow none Fast min_max"):
                assert f"SUMMARY {temp} {state} " in result.stdout, result.stdout
        assert "SUMMARY 85 Slow min_max Fast min_max " in result.stdout
        for command in ("report_clock_interaction", "report_cdc", "check_timing"):
            assert f"REPORT {command} " in result.stdout
        assert result.stdout.count("REPORT report_timing ") == 4
        # An interrupted report propagates failure, but restores both timing models.
        result = _run(setup + "\nset fail_report 1\n" +
                      "if {![catch {" + report + "} msg]} {error {failure swallowed}}\n" +
                      "if {$msg ne {planted report failure}} {error $msg}\n" +
                      "kl_timing_grade_check")
        assert result.returncode == 0, result.stderr
    print("  [timing grade] declaration pinned; 10 wrong-condition refusals; "
          "four endpoint/model reports; complete analysis restored after success and failure")


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


if __name__ == "__main__":
    test_timing_grade_contract()
    if len(sys.argv) == 2:
        test_platform_hooks(sys.argv[1])
