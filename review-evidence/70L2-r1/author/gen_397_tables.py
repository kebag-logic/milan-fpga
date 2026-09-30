"""Regenerate the measured tables of docs/findings/397_SERVICE_BUDGET.md from the
twelve positive service receipts of one native run.

Usage: python3 gen_397_tables.py <evidence dir>
The directory holds service-<shape>-<plan>-receipt.json (or .json.gz, as
run_native.py retains them). Formulas, row order and labels are the page's;
the script is validated by reproducing the page at its previous measured head
from that run's retained receipts (PR #609's packet) before it is used.
"""
from pathlib import Path
import gzip
import json
import re
import sys

PLANS = ('all', 'uart-paced', 'queued-input', 'queued-short', 'queued-builtins', 'device-wait')
LABELS = (('boot_to_entity_enabled', 'Boot to entity enabled'), ('aem_copy_crc', 'AEM copy/CRC'),
          ('restore_walk', 'Restore walk'), ('milan_status', '`milan_status`'),
          ('milan_gettime', '`milan_gettime`'), ('milan_nvm', '`milan_nvm`'),
          ('milan_nvm commit', '`milan_nvm commit`'), ('milan_nvm wipe', '`milan_nvm wipe`'),
          ('wipe_erase_envelope', 'Wipe erase envelope'), ('milan_nvm invalid', '`milan_nvm invalid`'),
          ('milan_settime', '`milan_settime`'), ('milan_utc', '`milan_utc`'),
          ('journal_commit_bracket', 'Journal START-to-ACK'),
          ('erase_enclosed_to_first_program', 'Journal erase envelope'),
          ('mem_read 0x40000000 128', '`mem_read 0x40000000 128`'), ('', 'Empty line'),
          ('unknown_command', 'Unknown line'))
STARTUP = ('boot_to_entity_enabled', 'aem_copy_crc', 'restore_walk')


def load(directory, shape, plan):
    base = directory / f'service-{shape}-{plan}-receipt.json'
    if base.exists():
        return json.loads(base.read_text())
    return json.loads(gzip.decompress(Path(str(base) + '.gz').read_bytes()))


def key(duty):
    for prefix in ('milan_settime', 'milan_utc'):
        if duty.startswith(prefix + ' '):
            return prefix
    return duty


def f5(value):
    return f'{value:.5f}'


def armed(row):
    """The armed service span of a row (the whole row when it starts armed)."""
    return row.get('armed_no_tick_ms', row['no_tick_ms'])


def tables(directory, short, shape):
    receipts = {plan: load(directory, short, plan) for plan in PLANS}
    rows = {}
    for plan in PLANS:
        for row in receipts[plan]['rows']:
            if row['duty'] != 'maximum_heartbeat_gap':
                rows.setdefault(key(row['duty']), []).append((plan, row))
    phy = [receipts[plan]['phy'] for plan in PLANS]
    transaction = max(p['max_transaction_sys_cycles'] for p in phy) / 100_000
    poll = max(p['max_poll_sys_cycles'] for p in phy) / 100_000
    charge = poll + 9 * transaction
    out = [f'**{short} elapsed duty maxima.**', '',
           '| Duty | Plan | CPU cycles | Elapsed ms | Deadline ms | Margin ms |',
           '| --- | --- | --- | --- | --- | --- |']
    for duty, label in LABELS:
        plan, row = max(rows[duty], key=lambda pair: pair[1]['sys_cycles'])
        # An ordinary command's 500 ms is the historical comparison, not a
        # protocol deadline, which the page prints as N/A.
        deadline = row['budget_ms'] is not None and not (row['budget_ms'] == 500 and 'command_index' in row)
        budget = f5(row['budget_ms']) if deadline else 'N/A'
        margin = f5(row['margin_ms']) if deadline else 'N/A'
        out.append(f"| {label} | {plan} | {row['cpu_cycles']} | {f5(row['ms'])} | {budget} | {margin} |")
    out += ['', '', f'**{short} service opportunities.**', '',
            '| Duty | Span plan | No-tick ms | TX allowance ms | Heartbeat bound ms | PHY check ms |',
            '| --- | --- | --- | --- | --- | --- |']
    worst = 0.0
    for duty, label in LABELS:
        plan, row = max(rows[duty], key=lambda pair: armed(pair[1]))
        span = armed(row)
        tx = max(r['uart_tx_allowance_ms'] for _, r in rows[duty])
        if duty == 'boot_to_entity_enabled':
            out.append(f'| {label} | {plan} | {f5(row["no_tick_ms"])} | 0 | Unarmed prefix | N/A |')
            continue
        bound = 250 + span + tx
        if duty in STARTUP:
            phy_cell = 'Startup cost ' + f5(bound - 250 + charge)
        else:
            phy_cell = f5(125 + bound - 250 + charge)
            worst = max(worst, span + tx + charge)
        out.append(f'| {label} | {plan} | {f5(span)} | {f5(tx)} | {f5(bound)} | {phy_cell} |')
    heartbeat = []
    for plan in PLANS:
        receipt = receipts[plan]
        beat = receipt['heartbeat']
        gap = receipt['heartbeat_max_gap_ms']
        unbacked = re.search(r'BACKING armed=1 unbacked_cycles=(\d+)', receipt['raw_log'])[1]
        heartbeat.append(f"| {short} | {plan} | {f5(gap)} | {f5(500 - gap)} | {beat['right_censored']} | "
                         f"{unbacked} | {receipt['phy']['down_edges']}/{receipt['phy']['up_edges']} |")
    phy_rows = (f'| {short} | {f5(transaction)} | {f5(poll)} | {f5(charge)} | {f5(50 - charge)} |',
                f'| {short} | {f5(worst)} | {f5(250 - worst)} | 125.00000 | {f5(250 - worst - 125)} |')
    unarmed = [(plan, row) for plan, row in rows['aem_copy_crc'] if 'armed_start_sys_cycle' in row]
    return out, heartbeat, phy_rows, unarmed


def main():
    directory = Path(sys.argv[1])
    heartbeat, phy_a, phy_b = [], [], []
    for short in ('1x1', '8x8'):
        out, beat, phy_rows, unarmed = tables(directory, short, None)
        print('\n'.join(out) + '\n\n')
        heartbeat += beat
        phy_a.append(phy_rows[0])
        phy_b.append(phy_rows[1])
        for plan, row in unarmed:
            print(f"<!-- {short} {plan}: AEM row starts unarmed; prefix "
                  f"{(row['armed_start_sys_cycle'] - row['start_sys_cycle']) / 100_000:.5f} ms, "
                  f"whole no-tick {row['no_tick_ms']:.5f} ms, armed no-tick {row['armed_no_tick_ms']:.5f} ms -->")
    print('| Shape | Plan | Heartbeat gap ms | 500 ms margin | Final tail | Unbacked cycles | Down/up edges |')
    print('| --- | --- | --- | --- | --- | --- | --- |')
    print('\n'.join(heartbeat) + '\n')
    print('| Shape | One transaction ms | Complete poll ms | Scheduling charge ms | 50 ms page-poll margin |')
    print('| --- | --- | --- | --- | --- |')
    print('\n'.join(phy_a) + '\n')
    print('| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |')
    print('| --- | --- | --- | --- | --- |')
    print('\n'.join(phy_b))


if __name__ == '__main__':
    main()
