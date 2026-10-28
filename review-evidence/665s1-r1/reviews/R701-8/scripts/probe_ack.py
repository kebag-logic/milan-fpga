#!/usr/bin/env python3
"""Falsification probe for the CPU budget harness's commit-acknowledgement model.

Runs split_soc.ack_deviations (the build's refusal check) on the head's
StimulusMailbox.slowest_ack, which must give no deviation, and on planted
acknowledgement defects, each of which must be refused. Also checks that
face_ports at one and two interfaces yields exactly the held-idle inputs plus
named outputs. Nothing is written to the checkout.

Usage: python3 -B probe_ack.py <checkout>
"""
import sys
from pathlib import Path
from unittest.mock import patch

checkout = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
sys.path.insert(0, str(checkout / 'sw/mailbox'))
import split_soc  # noqa: E402
from migen import If, Signal  # noqa: E402

contract = split_soc.milan_soc.ctrl_mailbox_contract()
bound = split_soc.face_ack_cycles(contract)
print(f'bound from the contract: {bound}')


def plant(kind):
    def slowest_ack(self, send, n_if, contract):
        b = split_soc.face_ack_cycles(contract)
        ack = Signal(n_if)
        for i in range(n_if):
            waited = Signal(max=b + 4)
            src = send[1 - i] if (kind == 'swapped' and n_if == 2) else send[i]
            if kind == 'never-rearmed':
                self.sync += If(src & (waited != b), waited.eq(waited + 1))
            else:
                self.sync += If(~src, waited.eq(0)).Elif(waited != b + 3, waited.eq(waited + 1))
            at = {'early': b - 1, 'late': b + 1}.get(kind, b)
            hit = src & (waited == at)
            if kind == 'immediate':
                hit = src
            if kind == 'if0-only' and i == 1:
                hit = 0
            self.comb += ack[i].eq(hit)
        return ack
    return slowest_ack


results = {}
results['head'] = split_soc.ack_deviations(contract)
for kind in ('early', 'late', 'immediate', 'if0-only', 'swapped', 'never-rearmed'):
    with patch.object(split_soc.StimulusMailbox, 'slowest_ack', plant(kind)):
        results[kind] = split_soc.ack_deviations(contract)
with patch.object(split_soc, 'face_ack_cycles', lambda c: bound - 1):
    results['bound-not-firmware'] = split_soc.ack_deviations(contract)

ok = True
for kind, dev in results.items():
    want_clean = kind == 'head'
    good = (not dev) if want_clean else bool(dev)
    ok &= good
    print(f"{'OK ' if good else 'BAD'} {kind}: {'no deviation' if not dev else 'refused: ' + '; '.join(dev)[:300]}")

from mailbox_model import with_interfaces  # noqa: E402
for n in (1, 2):
    ports = split_soc.face_ports(contract, n)
    ins = {k for k in ports if k.startswith('i_')}
    outs = {k: len(v) for k, v in ports.items() if k.startswith('o_')}
    good = ins == set(split_soc.FACE_IDLE_INPUTS) and outs.get('o_fw_send_o') == n
    ok &= good
    print(f"{'OK ' if good else 'BAD'} face_ports n_if={n}: {len(ins)} inputs held idle, {len(outs)} outputs, "
          f"fw_send_o width {outs.get('o_fw_send_o')}")
print('PROBE', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
