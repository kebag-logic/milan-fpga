"""Reviewed sources and reasons for the population's interpreter programs (input to pins.py; scratch)."""

NOTHING = 'it installs and fetches nothing'
#: Exact or contained texts whose source a line search cannot find, or finds in an unrelated file.
TEXTS = [
    ('=import yaml', 'ci/image/audit_population.py',
     "The image form of the PyYAML install step: it imports the package the image's Python layer supplies; " + NOTHING + '.'),
    ('=import cmarkgfm', 'ci/image/audit_population.py',
     "The image form of the Markdown renderer install step: it imports the locked renderer; " + NOTHING + '.'),
    ('=import wavedrom', 'ci/image/audit_population.py',
     "The image form of the diagram dependency install step: it imports wavedrom; " + NOTHING + '.'),
    ('print(os.path.dirname(os.path.dirname(', 'sw/litex/patches/apply.sh',
     'Prints the install location of a LiteX package the patch series reads; ' + NOTHING + '.'),
    ('pthread_sigmask(signal.SIG_BLOCK, set())', 'scripts/act_ci.py',
     "The act runner self-test's signal-mask probe: it prints the blocked signals; " + NOTHING + '.'),
    ('signal.SIG_DFL); time.sleep(300)', 'scripts/act_ci.py',
     "The act runner self-test's interruptible sleeper: it sleeps until signalled; " + NOTHING + '.'),
    ('# build.sh - named-config bitstream launcher', 'scripts/check_sweep_shape.py',
     'A variant of sw/litex/build.sh that the sweep/build shape self-test runs through bash -c to prove a refusal; '
     + NOTHING + '.', 'sw/litex/build.sh'),
    ('# Turnkey deploy for the Alinx AX7101', 'scripts/check_deploy_shape.py',
     'A variant of sw/litex/deploy.sh that the deploy shape self-test runs through bash -c to prove a refusal; '
     + NOTHING + '.', 'sw/litex/deploy.sh'),
    ("print('\\n'.join(['0'*", 'syn/yosys/ooc_arms.py',
     'Prints a constant all-zero ROM image for an OOC self-test arm; ' + NOTHING + '.'),
    ("spec_from_file_location('baseline', sys.argv[1])", 'syn/ooc/pp_placement_selftest.py',
     "The placement self-test's import probe: it loads one baseline module from its file; " + NOTHING + '.'),
    ('value = json.load(handle)["design"]["num_cells"]', 'syn/yosys/run.sh',
     'Reads the synthesis statistics and validates a non-negative cell count; ' + NOTHING + '.'),
    ('printf "%s\\n" "${tops[@]}"', 'scripts/check_rtl_source_lists_selftest.py',
     "The source-list self-test's array-reading probe: bash prints one parsed top list; " + NOTHING + '.'),
]
#: The reason a program is reviewed, by the tracked file that holds its text.
SOURCES = {
    'scripts/act_ci.py': "A process-control fixture of the act runner self-test (forks, signals, sleeps, markers); "
                         + NOTHING + '.',
    'sw/builder/test_builder.py': 'An end-station builder self-test probe that imports the product sources it checks; '
                                  + NOTHING + '.',
    'sw/builder/test_clock_contract.py': 'The clock-contract self-test probe: it imports a recipe with a planted value '
                                         'and prints the clock it reads; ' + NOTHING + '.',
    'sw/builder/test_soc_options.py': 'The SoC-option self-test probe: it executes a mutated copy of the SoC source '
                                      'with the build stubbed and reports the options it reaches; ' + NOTHING + '.',
    'sw/builder/test_timing_grade.py': 'The timing-grade self-test probe: it checks the declared part reaches the '
                                       'platform and PLL; ' + NOTHING + '.',
    'sw/litex/build.sh': "The launcher's artefact reader: it validates a generated build artefact and prints its design "
                         'arguments; ' + NOTHING + '.',
    'sw/litex/deploy.sh': "The deploy script's layout check: it validates the flash layout it is given; " + NOTHING + '.',
    'sw/litex/sweep_extra.sh': "The sweep helper's configuration check: it loads the builder and verifies a "
                               'configuration; ' + NOTHING + '.',
    'sw/firmware/ctrl/test/ctrl_pin.py': "The pin proof: it compiles the census's texts of ctrl_build.py and "
                                         'ctrl_pin.py under their own paths and runs the stack pin check; '
                                         + NOTHING + '.',
    'syn/yosys/ooc.sh': 'Reads one live localparam value from a package source, comments stripped; ' + NOTHING + '.',
    'tb/verilator/milan_dp/Makefile': 'Reads the simulation clock from the followed recipe module; ' + NOTHING + '.',
    '.github/workflows/elaborate.yml': 'A workflow step text, as committed at a historical revision, that the scope '
                                       'history self-test replays; it classifies a change and ' + NOTHING + '.',
    '.github/workflows/rtl.yml': 'A workflow step text, as committed at a historical revision, that the scope '
                                 'history self-test replays; it classifies a change and ' + NOTHING + '.',
    '.github/workflows/rtl-fast.yml': 'A workflow step text, as committed at a historical revision, that the scope '
                                      'history self-test replays; it classifies a change and ' + NOTHING + '.',
}
#: Job-written scripts, by path: (pattern, generator, reason with the pattern's named groups).
SCRIPTS = [
    (r'/tmp/pp-baseline-mutants[^/]*/(?P<label>[^/]+)/syn/ooc/pp_baseline\.py$', 'syn/ooc/pp_baseline_mutants.py',
     "Mutant '{label}' of syn/ooc/pp_baseline.py, which the baseline mutation self-test runs offline; "
     + NOTHING + '.'),
    (r'/tmp/pp-resource-gate-mutants[^/]*/(?P<label>[^/]+)/pp_resource_gate\.py$',
     'syn/ooc/pp_resource_gate_mutants.py',
     "Mutant '{label}' of syn/ooc/pp_resource_gate.py, which the resource-gate mutation self-test runs offline; "
     + NOTHING + '.'),
    (r'/syn/yosys/\.ooc-mut-[a-z0-9_]{8}\.sh$', 'syn/yosys/ooc_harness.py',
     'A copy of syn/yosys/ooc.sh with one or two exact substitutions, which the OOC harness runs to prove a guard '
     'fails; ' + NOTHING + '.'),
    (r'/tmp/ci-scope-history[^/]*/scripts/ci_scope\.py$', 'scripts/ci_scope_history.py',
     'scripts/ci_scope.py as committed at a historical revision, which the scope history self-test replays; it '
     'classifies paths and ' + NOTHING + '.'),
    (r'/tmp/cache-selftest[^/]*/rom/bin/python3$', 'syn/yosys/rom_cache_selftest.py',
     "The ROM cache self-test's python3 wrapper: it records each generator call and runs the image's interpreter; "
     + NOTHING + '.'),
    (r'/tmp/elaboration-guards[^/]*/unenforced\.py$', 'syn/yosys/guard_selftest.py',
     "The guard self-test's helper with its enforcement removed: it reads one file, reproducing the false green; "
     + NOTHING + '.'),
    (r'/tmp/elaboration-guards[^/]*/(?P<flow>ooc|run)\.sh$', 'syn/yosys/guard_selftest.py',
     'syn/yosys/{flow}.sh staged with a fixture input and a chosen enforcement helper, which the guard self-test '
     'runs to prove both flows refuse active guards; ' + NOTHING + '.'),
    (r'/tmp/dp-srcs-selftest[^/]*/authority-[^/]+/syn/yosys/run\.sh$', 'syn/ooc/dp_srcs.py',
     'A mutated copy of syn/yosys/run.sh, the source-list authority, which the dp_srcs self-test asks for its read '
     'set; ' + NOTHING + '.'),
    (r'/syn/yosys/\.selftest-\d+-(?P<flow>ooc|run)\.sh$', 'scripts/check_rtl_source_lists.py',
     'syn/yosys/{flow}.sh with one source token dropped, which the source-list gate runs to prove the drift is '
     'caught; ' + NOTHING + '.'),
    (r'/tmp/act-ci-capture-signal-selftest[^/]*/entry-bin/gh$', 'scripts/act_ci.py',
     "The act runner self-test's gh stand-in: a non-cooperative process tree the capture must contain; "
     + NOTHING + '.'),
    (r'/tmp/act-ci-capture-signal-selftest[^/]*/noncooperative-tree\.py$', 'scripts/act_ci.py',
     "The act runner self-test's non-cooperative process tree, which a signal must contain; " + NOTHING + '.'),
    (r'/tmp/act-ci-capture-signal-selftest[^/]*/git-exec/git-remote-https$', 'scripts/act_ci.py',
     "The act runner self-test's Git remote helper stand-in: a non-cooperative process tree; " + NOTHING + '.'),
    (r'/tmp/act-ci-flat-selftest[^/]*/act_ci\.py$', 'scripts/act_ci.py',
     "scripts/act_ci.py installed flat by the act runner self-test, which runs it without its repository; "
     + NOTHING + '.'),
    (r'/tmp/ctrl-boundary[^/]*/controls/(?P<n>\d+)/run/builder/planted_builder\.py$',
     'sw/firmware/ctrl/test/ctrl_plants.py',
     "Control {n}'s planted Python builder, which the firmware boundary gate runs under its compiler capture to "
     'prove a compile is caught; it compiles the copy\'s sources and ' + NOTHING + '.'),
    (r'/tmp/ctrl-boundary[^/]*/pins/no_simulator\.py$', 'sw/firmware/ctrl/test/ctrl_pin_bench.py',
     "The pin bench's Verilator stand-in: it writes a no-op simulator stub where a build expects one; "
     + NOTHING + '.'),
    (r'/tmp/tmp[a-z0-9_]{8}/bin/fixture-python$', 'sw/builder/test_builder.py',
     "The builder self-test's fixture interpreter: it emulates one LiteX output and runs the image's Python for "
     'everything else; ' + NOTHING + '.'),
    (r'/tmp/tmp[a-z0-9_]{8}/bin/openFPGALoader$', 'sw/builder/test_builder.py',
     "The builder self-test's programmer stand-in: it records the flash it is asked for; " + NOTHING + '.'),
    (r'/tmp/tmp[a-z0-9_]{8}/(?P<case>[a-z-]+)/(?P<tool>cp|mktemp)$', 'sw/builder/test_builder.py',
     "The builder self-test's PATH shim that breaks one {tool} of build.sh's preservation ('{case}') and delegates "
     'every other call to the real tool; ' + NOTHING + '.'),
]
