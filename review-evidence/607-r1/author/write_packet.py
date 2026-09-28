"""Render the review packet from retained, committed-head receipts."""
import json
from pathlib import Path
import shlex

out = Path(__file__).resolve().parent
head = '350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75'
base = '54ce877371ee6e8878cf67294e86c2a8481b62f6'
work = Path('$VALIDATION_STORAGE/607-a408-work')
gates = {row['name']: row for row in json.loads((out / 'gate-results.json').read_text())}
seeds = json.loads((out / 'sweep-summary.json').read_text())
runs = {row['seed']: row for row in json.loads((out / 'sweep-results.json').read_text())}
assert all(row['head'] == head and row['rc'] == 0 for row in gates.values())
assert all(row['head'] == head for row in seeds)
complete = len(seeds) == 3 and all(row['margin_ok'] and row['bound_ok'] for row in seeds)
if complete:
    assert {row['seed'] for row in seeds} == {'asl', 'eto', 'eppo'}
    assert all(not row['critical_warnings'] for row in seeds), 'review warning text before publication'
    assert all(any('quasi_static cells=112 ' in item['text'] for item in row['application'])
               for row in seeds), 'review quasi-static census before publication'
status = 'Author validation complete; ready for independent review.' if complete else (
    f'Validation in progress: {len(seeds)} of three fresh seeds reported; acceptance 4 remains open.')

def number(value):
    return f'{value:+.3f}' if value else '0.000'

def write_table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join('---' for _ in headers) + ' |',
                      *['| ' + ' | '.join(str(value) for value in row) + ' |' for row in rows]])

parts = [f'''# [A408] Issue #607 handoff

{status}

Branch: `607-xdc-clock-names`. Base: `{base}`. Head: `{head}`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Executor: [A408]. Assigned independent reviewers: [R382] and [R383].
Assignment: https://github.com/kebag-logic/milan-fpga/issues/607#issuecomment-5865111793
Scope authority: #607 acceptance 1-4; linked #605 F1 findings; #395 AX7101 margin decision;
REQ-VER-02/03/04 and the repository integration/testing documentation.

## Acceptance evidence

| Item | Change with file:line | Proof |
|---|---|---|
| 1: real clock objects and supported hook | `sw/litex/milan_soc.py:245,268,424,449,458` retains the raw PLL clock output objects. `sw/litex/clock_constraints.py:38` resolves their names through the generated namespace. `sw/litex/clock_constraints.tcl:4,13` applies conditional class constraints after synthesis and requires exactly one clock on each selected net. | The committed tests cover renamed signals, both Ethernet ports, optional clock domains and hook order. Each completed fresh seed records 112 quasi-static cells with setup 4 / hold 3; its application log and warning census are below. |
| 2: effective 8 ns Ethernet data bound | `sw/litex/platforms/alinx_ax7101.py:301` selects the local subclass. `sw/litex/clock_constraints.py:16` removes exactly the known generic MultiReg command and refuses template drift. `sw/litex/clock_constraints.tcl:31,66` restores unrelated exceptions and applies 8 ns in both directions for sys and Milan. | Each completed seed has positive slack at an explicit 8.000 ns requirement in all four directions and `Max Delay Datapath Only` interaction, with no unsafe pair. The Tcl controls independently check the scoped exceptions. Installed LiteX was not edited. |
| 3: build refusal and planted wrong name | `sw/litex/clock_constraints.py:61` rejects emitted 12-4739 / 20-1307 diagnostics and missing logs. `sw/litex/milan_soc.py:3960` calls it after every completed shipping build, before manifest publication. `sw/builder/test_builder.py:27557` includes the tests in the complete bank. | `sw/builder/test_clock_constraints.py:163,206` covers both IDs at WARNING / CRITICAL WARNING / ERROR severity, missing logs, common build wiring, and the retained live wrong-name control. Both full banks and the live control pass at this head. |
| 4: fresh AX7101 1x1 TDM8 sweep | `sw/litex/clock_constraints.py:55` retains interaction and exception reports. The generated shipping recipe uses the three canonical placement directives, `AreaOptimized_high` synthesis and `ExploreArea` optimization. Each implementation and report process is limited to 16 threads. | The tables below report every completed seed and corner. Acceptance requires all three seeds, WNS >= +0.030 ns, WHS >= 0, TNS = THS = 0, and positive Ethernet slack against 8.000 ns. Current status: {'met' if complete else 'pending remaining seeds'}. |

Documentation: `docs/integration/BUILDING.md:517`, `docs/litex/LITEX_SOC.md:56`,
and `docs/testing/RUNNING_TESTS.md:160` describe the repaired contract and evidence.

## Exception policy

The bounded hook is selected for AX7101 GMII; MII retains its existing asynchronous
groups. The implementation-log refusal is common to all shipping builds.
The 8 ns budget covers Ethernet data crossings. The existing asynchronous reset PRE-pin
exceptions and 2 ns reset inter-stage bound remain. Other MultiReg paths, including
asynchronous inputs, retain their exceptions. A changed upstream MultiReg template
causes an explicit refusal and must be adapted before that upstream version can build.
The inspected upstream definitions are `litex/build/xilinx/common.py:48,56`
(first-stage `mr_ff` tagging) and `litex/build/xilinx/vivado.py:242,249,256,263`
(generic MultiReg, reset PRE and reset inter-stage constraints), at the source
identity recorded in `installed-constraint-source.json`.

This explains the saved-checkpoint sys-to-Ethernet slack difference from the broad
exception-clearing probe in #605: retaining reset assertion exceptions measures the
bounded data paths. No per-register placement waiver, clock-frequency change, RTL
change, firmware change or installed-package edit is part of this implementation.

## Before and after constraint application

The shipping implementation log contains 14 emitted CRITICAL WARNING lines:
ten 12-4739, two 20-1307 and two 12-5201. A fifteenth substring match is echoed
source rather than an emitted warning. In its original interaction report,
eth -> sys and sys -> eth are False Path; eth -> Milan is timed unsafe at 4 ns;
Milan -> eth is partial false path / unsafe. The quasi-static relaxation was absent.

Read-only diagnostic reports under `{work}` confirm that scoping the generic mask
away from the bounded data pairs applies the intended bound. The production hook
applied in memory to the saved checkpoint selects all raw clock nets and 112
quasi-static cells without a rejected-constraint diagnostic. These probes are
diagnostic evidence; the fresh builds below are the acceptance evidence.
`diagnostic-artifacts.json` records the retained probe, elaboration and control artifacts
by size and SHA-256, including exploratory attempts that did not complete.

The supplied shipping inputs and installed constraint-source identities are recorded
in `shipping-inputs.json` and `installed-constraint-source.json`. Their unchanged
hash verification is in `read-only-verification.json`. No checkpoint was saved into
the supplied build tree.
''']

baseline_counts = json.loads((out / 'shipping-warning-census.json').read_text())['emitted_severity_counts']
warning_rows = [['shipping input', *[baseline_counts[key] for key in ('WARNING', 'CRITICAL WARNING', 'ERROR')], 10, 2, 2]]
for seed in seeds:
    warning_rows.append([seed['directive'],
                         *[seed['emitted_severity_counts'][key] for key in ('WARNING', 'CRITICAL WARNING', 'ERROR')],
                         *[seed['warning_counts'][code] for code in ('12-4739', '20-1307', '12-5201')]])
parts.append(write_table(['Implementation', 'Warnings', 'Critical warnings', 'Errors', '12-4739', '20-1307', '12-5201'], warning_rows))
parts.append('\nCounts are emitted severity lines, excluding echoed source and repeated summary totals. The shipping log predates the assigned base; these are observed censuses of the supplied image and fresh candidates. `shipping-warning-census.json` retains the baseline count by diagnostic ID.\n\nApplication records from each completed implementation log:')
for seed in seeds:
    log = Path(runs[seed['seed']]['directory']) / 'gateware/vivado.log'
    parts.append(f'\n`{log}`\n\n```text\n' + '\n'.join(
        f"{row['line']}: {row['text']}" for row in seed['application']) + '\n```')

live = gates['live-plant-head']
parts.append(f'''
## Planted wrong-name test

At head `{head}`, the live test returned rc 0 in {live['elapsed_s']} s. The planted
vendor invocation itself returned 0 while emitting both 12-4739 and 20-1307.
`check_implementation_log` raised the expected refusal containing both IDs, so the
test passed. The harness pass records the expected build-check failure.

Exact command: `{shlex.join(live['command'])}`.
Retained raw files: `{work / ('live-plant-' + head[:9])}` contains `wrong.xdc`,
`plant.tcl`, `vivado.log` and `exit-code.txt`. Receipt: `live-plant-result.json`.

The complete banks also test missing / ambiguous clocks, renamed namespaces,
both ports, optional domains, preservation of unrelated and reset exceptions,
empty / nonempty quasi-static classes and changed upstream templates. Seven
preparatory mutations were rejected: retained generic mask, 80 ns bound,
deleted quasi-static hook, wrong clock selection, deleted Ethernet hook call,
deleted log check and disabled 12-4739 detection. Those preparatory mutations
are not represented as a separate final-head mutation campaign.

## Fresh sweep timing

All outputs are under the physical data path. The exact build and report argv and
return codes, plus build durations, are in `sweep-results.json`; `run_sweep.py` and
`report_seed.tcl` reproduce the sequence. `PYTHONHASHSEED=0`,
`PYTHON_CPU_COUNT=16`, and `--vivado-max-threads 16` are used. Runs are sequential.
The existing RV32 SDK is selected with `LITEX_ENV_CC_TRIPLE=riscv32-linux`.

The 0 C and 85 C operating settings are reported separately below. They use
the vendor Slow/Fast timing models; this is static timing evidence, with no
hardware or temperature-chamber measurement in this assignment.
''')

timing_rows = []
for seed in seeds:
    for row in seed['timing']:
        timing_rows.append([seed['seed'], row['temperature_C'], row['corner'],
                            *[number(row[key]) for key in ('WNS', 'TNS', 'WHS', 'THS')]])
parts.append(write_table(['Seed', 'C', 'Corner', 'WNS ns', 'TNS ns', 'WHS ns', 'THS ns'], timing_rows))
parts.append('\nEthernet slack against an explicitly checked **8.000 ns** datapath requirement:')
crossing_rows = []
directions = [('eth_clocks0_rx', 'milansoc_crg_clkout0'),
              ('milansoc_crg_clkout0', 'eth_clocks0_rx'),
              ('eth_clocks0_rx', 'milansoc_crg_clkout1'),
              ('milansoc_crg_clkout1', 'eth_clocks0_rx')]
for seed in seeds:
    for temperature in ('0', '85'):
        for corner in ('Slow', 'Fast'):
            matches = {(row['from'], row['to']): row for row in seed['crossings']
                       if row['temperature_C'] == temperature and row['corner'] == corner}
            crossing_rows.append([seed['seed'], temperature, corner,
                                  *[number(matches[pair]['slack_ns']) for pair in directions]])
parts.append(write_table(['Seed', 'C', 'Corner', 'eth -> sys', 'sys -> eth', 'eth -> Milan', 'Milan -> eth'], crossing_rows))
parts.append('\nAll reported Ethernet clock-interaction rows from the combined report for each seed follow, including the clean intra-domain row. Each of the four corner reports also contains all four pairs with the same constraint classification and no unsafe pair. The `Ignored` interaction class accompanies `Max Delay Datapath Only`; the path reports independently carry the 8.000 ns requirement.')
for seed in seeds:
    report = seed['interactions'][0]
    parts.append(f"\n`{report['report']}`\n\n```text\n" + '\n'.join(report['all_eth_pairs']) + '\n```')

parts.append('\n## Gate table\n\nAll final verdicts below are at `' + head + '`. Commands ran directly, without pipelines. `gate-results.json` retains each command, rc, duration, log path, size and SHA-256; `gate-summary.json` checks the final verdict set. Logs are under the physical data path.')
gate_rows = [[row['name'], '`' + shlex.join(row['command']) + '`', row['rc'], row['elapsed_s'],
              '`' + Path(row['log']).name + '`'] for row in gates.values()]
parts.append(write_table(['Gate', 'Command', 'rc', 'Seconds', 'Log'], gate_rows))
parts.append('''
Both complete builder banks ran with required elaboration. The compiler-present bank
also required RV32. Both reported the unavailable historical Arty calibration report;
the compiler-absent bank additionally reported the deliberately unavailable compiler
instruments. No required elaboration arm was skipped. `run_builder_absent.py` hides
only the three cross-compiler candidates through subprocess interception, retaining
host compiler probes; it does not alter or copy an SDK. The separate audited absence
control records its attempted compiler calls under the data directory.

The initial committed documentation run caught the reserved `kl_eth` token in the
new procedure name. The final commit renames it to `milan_eth_constraints`; the full
required banks and gates were rerun. No gate exception was added. The HDL reference
export initially refused a Git commit-graph warning, then a reused output directory;
the final run used a process-local `core.commitGraph=false` setting and a fresh
destination. Those refusals and successful reruns are retained, without repository
configuration changes.

The first sweep setup attempt stopped before implementation because the SDK Meson
launcher shadowed the working system Meson. The build-only PATH now prefers system
build utilities while retaining the same RV32 compiler. `sweep-environment-attempt.json`
records those failed setup attempts. The accepted runs used fresh directories.

## Artifact and review status

`sweep-artifacts.json` records sizes and SHA-256 values for the retained checkpoints,
bitstreams, implementation logs, generated constraints and reports. Large artifacts,
installed documentation dependencies and generated reference output remain under
the data path, outside this packet. `documentation-artifacts.json` identifies the
reference export by hash and size. The packet contains no checkpoint, toolchain,
SDK copy, environment, installed package or file over 200 KB.

`sweep-validation-result.json` records the final timing-table validation rc 0;
`final-state.json` records the closing commit, cleanliness, input-hash and packet checks.

Commits have one-line subjects, empty bodies and no trailers. No push, PR mutation,
merge, hardware access or flashing was performed. Independent review remains for
the assigned reviewers; this packet contains author validation, not a review verdict.
''')
(out / 'HANDOFF.md').write_text('\n\n'.join(parts).rstrip() + '\n')

summary_rows = [[seed['directive'], number(min(row['WNS'] for row in seed['timing'])),
                 number(min(row['WHS'] for row in seed['timing'])),
                 number(min(row['slack_ns'] for row in seed['crossings']))] for seed in seeds]
body = f'''[A408]

Closes #607

The shipping XDC selected nonexistent clocks, rejected conditional Tcl, and left the
Ethernet delay budget masked by a generic synchronizer exception. AX7101 crossing clock selections
now come from the SoC objects. A post-synthesis Tcl hook applies the quasi-static
multicycles and scopes the MultiReg exceptions so all four Ethernet/sys/Milan data
directions receive the intended 8 ns bound. Existing asynchronous-reset exceptions
and the reset inter-stage bound remain.

Every completed shipping build now checks its implementation log and fails on
12-4739 or 20-1307 before publishing the flash manifest. Tests cover generated
names, optional domains, both Ethernet ports, exception scope and a live planted
wrong name that the vendor process accepts with rc 0 but the build check refuses.

Validation at `{head}`: both complete builder banks, required elaboration,
documentation/static gates and the live negative control pass. The compiler-present
bank requires RV32. The historical Arty calibration report is unavailable; the
compiler-absent run records its expected compiler-dependent omissions.

Fresh AX7101 1x1 TDM8 results, using at most 16 threads:

''' + write_table(['Place directive', 'Worst WNS ns', 'Worst WHS ns', 'Worst eth slack ns'], summary_rows) + f'''

{'All three seeds meet WNS >= +0.030 ns and WHS >= 0 at every reported corner. TNS and THS are zero. All four Ethernet pairs report Max Delay Datapath Only, with requirement 8.000 ns and no unsafe pair. Every implementation log has zero critical warnings and applies the quasi-static class to 112 cells.' if complete else 'The remaining fresh seeds are still in progress; acceptance 4 remains open.'}

No RTL, firmware or installed package changes. Exact commands, per-corner tables,
clock-interaction rows, warning counts and artifact hashes are retained in the
handoff packet. Independent review remains pending.
'''
assert '/home/' not in body
(out / 'PR-BODY.md').write_text(body)
if complete:
    ready_rows = [[seed['directive'], number(min(row['WNS'] for row in seed['timing'])),
                   '0.000', number(min(row['WHS'] for row in seed['timing'])), '0.000',
                   number(min(row['slack_ns'] for row in seed['crossings']))] for seed in seeds]
    ready = f'''[A408] REVIEW READY

Commit: `{head}`
Branch: `607-xdc-clock-names`, based on `{base}`.

Changed: AX7101 crossing clock selections now follow the SoC clock objects. A
post-synthesis Tcl hook applies the quasi-static class and scopes the generic
MultiReg exception outside the four bounded Ethernet/sys/Milan data directions.
Every completed shipping build checks its implementation log and refuses 12-4739
or 20-1307 before manifest publication. Tests and authoritative build/testing docs
cover the changed contract. No RTL, firmware or installed package was edited.

Validation at this commit:

- `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`: rc 0.
- Complete builder bank with the three cross-compiler candidates deliberately
  unavailable, retaining required elaboration: rc 0.
- Documentation/static gate set: all final commands rc 0. The packet records
  {len(gates)} final gate verdicts with exact commands, durations and log hashes,
  including both banks and the live control.
- Live wrong-name control: the planted implementation process returned 0 and
  emitted both required diagnostic IDs; the build log check refused them.
- Fresh AX7101 1x1 TDM8 sweep: all three build and report commands rc 0, at most
  16 threads per invocation, sequentially, with outputs under the physical data path.

Worst values over Slow/Fast at 0 C and 85 C:

''' + write_table(['Place directive', 'WNS ns', 'TNS ns', 'WHS ns', 'THS ns',
                   'Eth slack vs 8 ns'], ready_rows) + '''

Acceptance 1-4: met. Every fresh implementation applies the 112-cell quasi-static
class. Each Ethernet direction reports requirement 8.000 ns and positive slack;
all four crossing pairs report Max Delay Datapath Only. No reported Ethernet pair
is unsafe. All three seeds meet WNS >= +0.030 ns and WHS >= 0 at every reported
corner, with TNS = THS = 0.

Before/after emitted CRITICAL WARNING census: shipping input 14 (10 x 12-4739,
2 x 20-1307, 2 x 12-5201); every fresh seed 0. The supplied shipping artifacts
and installed constraint-source hashes remain unchanged.

Retained scope and limits: asynchronous reset PRE exceptions and the existing
2 ns reset inter-stage bound remain; the 8 ns bound covers data crossings. An
upstream generic-constraint template change causes an explicit build refusal.
Both banks report the unavailable historical Arty calibration report; absent mode
also records its intentionally unavailable compiler instruments. No required
elaboration arm was skipped.

HANDOFF.md contains the per-acceptance file:line evidence, full gate table,
per-corner timing and crossing tables, interaction rows and artifact hashes.
PR-BODY.md is prepared. Independent review remains with [R382] and [R383].
No push, PR mutation, merge or hardware action was performed.
'''
    (out / 'REVIEW-READY.md').write_text(ready)
print(status)
print('HANDOFF.md bytes', (out / 'HANDOFF.md').stat().st_size)
