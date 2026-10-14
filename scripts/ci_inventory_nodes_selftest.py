#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check typed data operands and the structural inventory boundary."""

from ci_command_table import Audit, Runtime


def data_controls() -> None:
    """Data lists admit source changes but never executable options."""
    pattern = ['--lint-only', {'data_paths': '.sv'}, 'top.sv']
    assert Audit.matches(['--lint-only', 'first.sv', 'top.sv'], pattern)
    assert Audit.matches(['--lint-only', 'first.sv', 'second.sv', 'top.sv'], pattern)
    for operand in ('--exe=payload.sv', 'payload.cpp', Runtime('source.sv')):
        assert not Audit.matches(['--lint-only', operand, 'top.sv'], pattern)
    assert not Audit.matches(['--lint-only', 'top.sv'], pattern)
    assert Audit.matches(['generated/header.svh'], [{'data_path': '.svh'}])
    assert not Audit.matches(['-eprogram.svh'], [{'data_path': '.svh'}])
    print('PASS: typed data operands and variable source populations')


def main() -> int:
    """Run the structural controls without executing candidate commands."""
    data_controls()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
