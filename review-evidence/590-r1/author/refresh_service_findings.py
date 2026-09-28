'''Collect completed target evidence and refresh the public findings tables.'''
from pathlib import Path
import hashlib
import json
import subprocess
root = Path.cwd()
out = Path(__file__).parent
plans = ('all', 'uart-paced', 'queued-input', 'queued-short', 'device-wait')
runs = {}
artifacts = []
for shape in ('1x1', '8x8'):
    for plan in plans:
        directory = Path('/tmp/a385-final3-service-' + shape + ('' if plan == 'all' else '-' + plan))
        waits = '3000000-5000' if plan == 'device-wait' else '0-0'
        path = directory / ('service-' + plan + '-1-' + waits + '.json')
        data = json.loads(path.read_text())
        assert data['service_findings'] == []
        assert 'BACKING armed=1 unbacked_cycles=0' in data['raw_log']
        assert data['heartbeat_500ms_met']
        runs[shape, plan] = data
        for p in (path, path.with_suffix('.log'), directory / 'service_spec.json'):
            artifacts.append(dict(path=str(p), size=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
        summary = {k: v for k, v in data.items() if k not in ('raw_log', 'events', 'build_hashes', 'input_hashes')}
        text = json.dumps(summary, indent=2) + '\n'
        if len(text.encode()) < 200000:
            (out / ('service-final-' + shape + '-' + plan + '.json')).write_text(text)
(out / 'service-artifacts-final.json').write_text(json.dumps(artifacts, indent=2) + '\n')
fw = hashlib.sha256((root / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_bytes()).hexdigest()
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
labels = {'boot_to_entity_enabled': 'Boot to entity enabled', 'aem_copy_crc': 'AEM copy/CRC',
          'restore_walk': 'Restore walk', 'journal_commit_bracket': 'Journal START-to-ACK',
          'erase_enclosed_to_first_program': 'Journal erase envelope', 'wipe_erase_envelope': 'Wipe erase envelope'}
def group(duty):
    return duty.split()[0] if duty.startswith(('milan_settime ', 'milan_utc ')) else duty
def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows]) + '\n'
def number(value):
    return 'N/A' if value is None else f'{value:.5f}'
parts = [f'''# Firmware service intervals at 50 MHz

The firmware repairs for [#590](https://github.com/kebag-logic/milan-fpga/issues/590),
[#592](https://github.com/kebag-logic/milan-fpga/issues/592) and the simulated portion of
[#599](https://github.com/kebag-logic/milan-fpga/issues/599) retain one cacheless hart.
Both shapes retain continuous backing in every executed plan.
This refresh follows the [combined assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859537529)
and [merged-pin correction](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453).
Physical switch-cycle acceptance remains a later lane.
The future-duty inventory and physical torture remain open under #397.

## Contents

- **[Measurement contract](#measurement-contract)** -- Compiled inputs, clock declarations, media fixtures and the scope of each finite plan.
- **[Measured duties](#measured-duties)** -- Per-duty elapsed times, tick gaps, UART allowances and deadline margins on both shapes.
- **[Tick placement and queued service](#tick-placement-and-queued-service)** -- Where service opportunities occur and how actual heartbeat and continuous backing are observed.
- **[PHY poll derivation and simulation](#phy-poll-derivation-and-simulation)** -- The transaction measurements, conservative scheduling charge, publication bound and real fabric observations.
- **[Device waits and limits](#device-waits-and-limits)** -- Modeled flash waits, excluded physical proof and remaining timing limitations.
- **[Controls and reproduction](#controls-and-reproduction)** -- Defect-sensitive controls, retained log bindings and commands for repeating the evidence.

## Measurement contract

The [service harness](../../tb/verilator/fw_service_budget/README.md) links the
unchanged product translation unit on the shipping cacheless RV32I CPU.
CPU and system clocks are 50 MHz and 100 MHz.
Both current configurations declare 50 MHz for Milan, including generated gPTP/lwSRP constants.
The BIOS banner reports the system clock, not the CPU clock.

The historical #397 product base was `ac18b50968b12efe4d15c0a06301264b35656b31`.
Its 8x8 CPU measurement override was 50 MHz, but its generated gPTP/lwSRP declaration remained 100 MHz.
The historical override did not rewrite that declaration.
The old report remains in [the merged findings page](https://github.com/kebag-logic/milan-fpga/blob/8bc97021f28fb7f729418d3a00851c84ea0b50fd/docs/findings/397_SERVICE_BUDGET.md).
Its queued heartbeat gaps were 2569.49201 ms at 1x1 and 2513.33593 ms at 8x8.
Those failures describe the old firmware only.

Measured source head: `{head}`.
Protocol-processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`.
Firmware SHA-256: `{fw}`.
CPU netlist SHA-256: `c208df0b7fafcaab190dba3f1734f2a38acd54645b33a834b0e59282e6a7813d`.
Later analysis, documentation and receipt commits do not change the compiled inputs.
Final bound-log regrading verifies the native executable, generated inputs and raw logs
before applying the current analysis; the evidence packet records that final head.

All five plans use populated A/B slots.
`all`, `uart-paced`, `queued-input` and `queued-short` use zero device WIP.
`device-wait` uses 3 s erase and 5 ms page WIP.
The first two plans cover every registered command, boundaries, refused arguments, two commits and wipe.
`queued-input` supplies twelve NVM status commands and register status: 133 bytes on both shapes.
`queued-short` supplies 350 status commands and isolates dispatch service from long-walk service.
Queues offer each next command immediately at its prompt, without idle time.
They do not inject all bytes simultaneously into a finite RX ring.

Fixtures contain 53 records / 3264 bytes at 1x1 and 156 / 12680 bytes at 8x8.
AEM sizes are 7352 and 18288 bytes.
Restore contains 8 and 32 matched backend requests/responses without errors.
This is the current binding walk, not all remaining saved-state work.

## Measured duties

CPU cycles are elapsed system cycles divided by two, rounded upward.
Milliseconds use the unrounded 100 MHz system count.
Each row selects the maximum elapsed duty across all five finite plans.
Boot starts at reset release and ends at entity enable.
AEM starts at the first accepted flash address and ends at entity enable.
Restore brackets real backend handshakes.
UART commands span first input byte through the returned prompt.
Journal START-to-ACK excludes preceding capture/prefill.
Erase ends at first page acceptance and includes verification.
Wipe has two erase envelopes, ending at the next erase and at the prompt.
''']
for shape in ('1x1', '8x8'):
    groups = {}
    for plan in plans:
        for row in runs[shape, plan]['rows']:
            if row['duty'] != 'maximum_heartbeat_gap':
                groups.setdefault(group(row['duty']), []).append((plan, row))
    parts.append('\n**' + shape + ' elapsed duty maxima.**\n')
    rows = []
    for duty, candidates in groups.items():
        plan, row = max(candidates, key=lambda pair: pair[1]['ms'])
        budget = row['budget_ms'] if duty in labels and duty != 'aem_copy_crc' else None
        if duty == 'milan_nvm commit': budget = 8000
        rows.append([labels.get(duty, '`' + duty + '`'), plan, row['cpu_cycles'], number(row['ms']),
                     number(budget), number(None if budget is None else budget - row['ms'])])
    parts.append(table(['Duty', 'Plan', 'CPU cycles', 'Elapsed ms', 'Deadline ms', 'Margin ms'], rows))
    parts.append('\n**' + shape + ' service opportunities.**\n')
    rows = []
    for duty, candidates in groups.items():
        plan, row = max(candidates, key=lambda pair: pair[1]['no_tick_ms'])
        uart = max(r['uart_tx_allowance_ms'] for _, r in candidates)
        poll = (max(runs[shape, p]['phy']['max_poll_sys_cycles'] for p in plans) + 9 * max(runs[shape, p]['phy']['max_transaction_sys_cycles'] for p in plans)) / 100000
        bound = 250 + row['no_tick_ms'] + uart
        phy_bound = (0 if duty in ('aem_copy_crc', 'restore_walk') else 125) + row['no_tick_ms'] + uart + poll
        if duty == 'boot_to_entity_enabled':
            rows.append([labels[duty], plan, number(row['no_tick_ms']), '0', 'Unarmed prefix', 'N/A'])
        else:
            assert bound <= 500 and phy_bound <= 250
            rows.append([labels.get(duty, '`' + duty + '`'), plan, number(row['no_tick_ms']), number(uart), number(bound), ('Startup cost ' if duty in ('aem_copy_crc', 'restore_walk') else '') + number(phy_bound)])
    parts.append(table(['Duty', 'Span plan', 'No-tick ms', 'TX allowance ms', 'Heartbeat bound ms', 'PHY check ms'], rows))
parts.append('''
The heartbeat bound adds the unchanged 250 ms rate-limit phase, measured no-tick span
and the containing command's full TX serialization at 115200 baud, 8N1.
The table combines the largest span and TX allowance for each duty across plans.
Paced spans already include UART blocking; adding the allowance again is conservative.
Boot's unarmed prefix precedes the first heartbeat.
AEM follows that first service call and restore invokes it internally.
The ordinary-command 500 ms figure is a heartbeat limit, not a UART response deadline.
A long status command passes through bounded internal service opportunities.
Raw receipts retain the historical whole-command comparison separately.

Restore, erase and commit deadlines remain 3000, 3500 and 8000 ms.
AEM shares boot's 20000 ms ADP comparison from Milan v1.2 sections 5.6.2/5.6.3.
Inherited BIOS CRC, startup delays and memory tests remain excluded.
No physical boot acceptance is claimed; AECP response timing remains a fabric duty.
No isolated final-WIP marker measures the 50 ms page timeout.

## Tick placement and queued service

Each registered Milan command begins with one opportunity.
CRC walks yield every 256 bytes after writer initialization.
Record-validation walks yield every sixteen records.
Wipe yields between its two erase-verification walks.
Existing restore and flash-wait opportunities remain.
The earlier 8x8 wipe chained two approximately 74 ms walks;
the added midpoint permits the derived PHY allowance below.
Measured per-duty maxima above justify these placements.
The heartbeat function's 250 ms rate limit is unchanged.

Retired CPU commit-PC observations count function entries, not speculative fetches.
Compressed blocks preserve internal maxima and both boundary tails.
The actual heartbeat is the standalone `PP_NVM_STAT <- 1` strobe.
Schedule maxima include a right-censored final tail when largest.
The native observer samples backing every system cycle after it first asserts.
Every positive run has zero unbacked cycles and all-positive console samples.
''')
rows = []
for shape in ('1x1', '8x8'):
    for plan in plans:
        d = runs[shape, plan]
        rows.append([shape, plan, number(d['heartbeat_max_gap_ms']), number(500-d['heartbeat_max_gap_ms']),
                     str(d['heartbeat']['right_censored']), '0', f"{d['phy']['down_edges']}/{d['phy']['up_edges']}"])
parts.append(table(['Shape', 'Plan', 'Heartbeat gap ms', '500 ms margin', 'Final tail', 'Unbacked cycles', 'Down/up edges'], rows))
parts.append('''
## PHY poll derivation and simulation

The one-hart allowance is 500 ms minus the heartbeat's 250 ms phase.
The stated publication period bound is 250 ms.
Half that allowance supplies the PHY trigger: `PHY_POLL_NS = 125 ms`.
The other 125 ms covers a pending duty stretch, full UART allowance and a conservative poll scheduling charge.
Thus `125 ms + no-tick stretch + TX allowance + scheduling charge <= 250 ms`.
For startup AEM/restore, the table lists isolated service-plus-poll cost without a phase term.
It is not the full publication interval across intervening startup work.
Actual publication-readback gaps grade that startup sequence separately.
The steady-state rows grade the derived bound and the 500 ms heartbeat bound.
The target grader also refuses observed publication-readback gaps over 250 ms.
This measured bound covers executed duties, not arbitrary new work.

Each MDIO transfer is a full Clause-22 read with a 32-bit preamble.
The poll envelope begins at retired heartbeat entry and includes clock acquisition,
transactions, negotiation resolution and publication bookkeeping.
The scheduling charge is `C = P + 9*T`, where P is the largest measured complete poll
and T is the largest measured transaction. Nine reads cover discovery, two BMSR reads,
BMCR, extended status and both local/peer negotiation pairs.
Using the complete observed poll as bookkeeping allowance deliberately counts observed
transaction time twice; the longer fallback path is bounded, not claimed as target-measured.
''')
rows=[]
for shape in ('1x1','8x8'):
    tx=max(runs[shape,p]['phy']['max_transaction_sys_cycles'] for p in plans)/100000
    poll=max(runs[shape,p]['phy']['max_poll_sys_cycles'] for p in plans)/100000
    charge=poll+9*tx
    assert charge < 50
    rows.append([shape,number(tx),number(poll),number(charge),number(50-charge)])
parts.append(table(['Shape','One transaction ms','Complete poll ms','Scheduling charge ms','50 ms page-poll margin'],rows))
rows=[]
for shape in ('1x1','8x8'):
 poll=(max(runs[shape,p]['phy']['max_poll_sys_cycles'] for p in plans)+9*max(runs[shape,p]['phy']['max_transaction_sys_cycles'] for p in plans))/100000
 grouped={}
 for plan in plans:
  for r in runs[shape,plan]['rows']:
   duty=r['duty']
   if duty in ('boot_to_entity_enabled','aem_copy_crc','restore_walk','maximum_heartbeat_gap'): continue
   if duty.startswith(('milan_settime ','milan_utc ')): duty=duty.split()[0]
   grouped.setdefault(duty,[]).append(r)
 cost=max(max(r['no_tick_ms'] for r in group)+max(r['uart_tx_allowance_ms'] for r in group)+poll for group in grouped.values())
 assert cost <= 125
 rows.append([shape,f'{cost:.5f}',f'{250-cost:.5f}','125.00000',f'{125-cost:.5f}'])
parts.append(table(['Shape','Worst duty + UART + charge ms','Maximum permissible trigger ms','Selected trigger ms','Remaining reserve ms'],rows))

parts.append('''
An independent Clause-22 peer drives simulated MDIO pins.
Firmware writes the existing link-status CSR.
A separate bus master reads real MAC_STATUS; the observer samples actual fabric link counters.
A drop at 1.5 s and recovery at 1.8 s produce one down and one up in each queued and device-wait plan.
Repeated publications leave counters unchanged.
At 2.4 s negotiation changes from 1000 to 100 Mb/s; MAC_STATUS follows.
Plans ending before recovery claim only the edges shown in the schedule table.
Host tests cover missing PHY, errors, negotiation and forced speed/duplex modes.
A latched short loss is published before a second BMSR read resolves current state in the same poll.
A regression checks both edges and current recovered state in that call, without a second-period delay.
Simulated pins and CSRs do not establish the deferred physical acceptance.

## Device waits and limits

Device-max plans execute one commit with 3 s erase and 5 ms page WIP.
There are 13 and 50 pages, giving 3065 and 3250 ms modeled WIP.
Elapsed minus WIP still includes transfers, polling, verification, bus and DDR waits.
It is not spare CPU capacity.
No device-max two-sector wipe was executed.
The unchanged 30-second guard admits supported finite plans, not arbitrary stalls.

The SPI stream-boundary substitution remains optimistic.
The historical PHY probe measured 67 versus 65 system cycles for 8 bits,
259 versus 257 for 32 bits, and 78 versus 65 after CS reassertion.
That boundary cost is not a uniform percentage correction.
DDR is simulated; the service harness has no external packet traffic.
One deterministic clock phase is exercised.
Physical twofold commit margin, liveness torture, field-update writing,
fault logging and temperature duties remain unproved here.
The separate capture harness measures concurrent request traffic.

## Controls and reproduction

Portable checks pass 42 grading controls and 14 flash controls.
They retain historical traces and their original duration comparisons.
New controls refuse one-cycle overruns, a single unbacked cycle and duplicate link edges.
A target dispatch-removal mutation must lose backing in `queued-short`.
A target publication-removal mutation must fail the named missing-publication check.
Matching unmodified plans provide positive controls.
The capture harness checks byte-only timing and missing-copy/traffic controls.

Follow the [foreground recipe](../../tb/verilator/fw_service_budget/README.md#run-and-reproduce).
Use `--populated --enforce-service`, each of five plans and separate external directories.
Only `device-wait` adds `--device-wait-us 3000000 --program-wait-us 5000`.
Use `--regrade` with identical arguments to check a retained bound log.
Reuse verifies generated inputs, BIOS, ELF and executable hashes.
The evidence packet records SHA-256 and size for large receipts and logs.
Only small summaries belong in that packet or this repository.
Author validation is not a review verdict.
''')
(root / 'docs/findings/397_SERVICE_BUDGET.md').write_text('\n'.join(parts))
print('Collected ten successful plans and refreshed service findings')
