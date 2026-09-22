# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check compiler locale isolation without requiring installed message catalogs."""

from contextlib import redirect_stdout
import io
import os
import subprocess
import unittest
from unittest.mock import patch

import fixture_guards


class CompilerLocaleTest(unittest.TestCase):
    def test_compiler_environment_and_arguments(self):
        wire = "SRP VID fixture must differ from product default 2 in the 16-bit wire value"
        class_d = "SRP VID fixture must differ from product default 2 in the 12-bit class-D value"
        cases = [(None, ()), ("5A3C", ()), ("0002", (wire, class_d)), ("1002", (class_d,))]
        argv = ["fixture_guards.py", "--verilator", "test-verilator",
                "--cxx", "cache-cxx 'compiler path' --driver-flag",
                "--", "--cc", "-j", "8", "wrap.sv"]
        for inherited_lc_all in (None, "fr_FR.UTF-8"):
            caller_env = {"LANG": "fr_FR.UTF-8", "LANGUAGE": "de:fr",
                          "LC_MESSAGES": "de_DE.UTF-8", "PATH": "/test/bin",
                          "CPATH": "/test/include", "CXXFLAGS": "-test-flag"}
            if inherited_lc_all is not None:
                caller_env["LC_ALL"] = inherited_lc_all
            results = [subprocess.CompletedProcess([], 0)]  # Model generation.
            results += [subprocess.CompletedProcess(
                [], int(bool(messages)),
                "".join(f"bench:1: error: static assertion failed: {m}\n" for m in messages)
            ) for _, messages in cases]
            with (self.subTest(LC_ALL=inherited_lc_all),
                  patch.dict(os.environ, caller_env, clear=True),
                  patch("sys.argv", argv),
                  patch.object(fixture_guards.subprocess, "check_output",
                               return_value="/test/verilator\n") as get_root,
                  patch.object(fixture_guards.subprocess, "run", side_effect=results) as run,
                  redirect_stdout(io.StringIO())):
                self.assertEqual(fixture_guards.main(), 0)
                self.assertEqual(dict(os.environ), caller_env)
                get_root.assert_called_once_with(
                    ["test-verilator", "--getenv", "VERILATOR_ROOT"], text=True)
                self.assertEqual(run.call_count, 5)
                model_call, *compiler_calls = run.call_args_list
                tmp = model_call.args[0][-1]
                self.assertEqual(model_call.args[0],
                                 ["test-verilator", "--cc", "-j", "8", "wrap.sv", "--Mdir", tmp])
                self.assertEqual(model_call.kwargs, {"check": True})
                command = ["cache-cxx", "compiler path", "--driver-flag",
                           "-std=c++17", "-Wall", "-Wextra", "-fsyntax-only",
                           "-I" + tmp, "-I/test/verilator/include",
                           "-I/test/verilator/include/vltstd"]
                for call, (value, _) in zip(compiler_calls, cases):
                    define = [] if value is None else ["-DPP_TOP_SRP_DOM_DEF_VID=0x" + value]
                    self.assertEqual(call.args[0], [*command, *define, "sim_main.cpp"])
                    self.assertEqual(call.kwargs, {
                        "stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "text": True,
                        "env": {**caller_env, "LC_ALL": "C"},
                    })


if __name__ == "__main__":
    unittest.main()
