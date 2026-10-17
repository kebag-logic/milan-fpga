#!/usr/bin/env python3
"""Reviewer probe: resolve extra Make fixtures with the head's walker and with the host's GNU Make.

Usage: python3 probe_make_walker.py CHECKOUT OUTPUT.json
Requires CI_IMAGE_SHFMT (the pinned parser) and PyYAML. Uses ci_differential's own
build/walk/run/outcome, so the comparison is the harness's, only the fixtures differ.
"""
import json
import sys
import tempfile
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(checkout / 'scripts'))
if len(sys.argv) > 3:
    sys.path.insert(1, sys.argv[3])  # Optional directory holding PyYAML, for an isolated interpreter.
import ci_differential as d  # noqa: E402
from ci_differential_fixtures import make  # noqa: E402

PROBES = [
    # Control: the committed eval fixture form.
    make('ctl-eval', [], 'CASES = a b-c\n$(foreach case,$(CASES),$(eval R_$(case) = r-$(case)))\n'
         'all: ; zz_probe $(R_a) $(R_b-c)\n'),
    # The loop variable assigned by an eval in the body: make defines it globally, so it persists.
    make('loopvar-eval-persists', [], 'X = outer\n$(foreach X,a b,$(eval X := z$(X)))\n'
         'all: ; zz_probe "$(X)"\n'),
    # Within an iteration the loop variable shadows the eval'd global value.
    make('loopvar-eval-shadow', [], '$(foreach X,a,$(eval X := q)$(eval Y := $(X)))\n'
         'all: ; zz_probe "$(Y)"\n'),
    # A command-line variable overrides an eval'd assignment, as any makefile assignment.
    make('eval-vs-command-line', [], '$(foreach c,a,$(eval X := mk))\nall: ; zz_probe "$(X)"\n',
         run='make X=cmd\n'),
    # A name containing `-` assigned at column zero.
    make('dash-name', [], 'a-b = one\nall: ; zz_probe "$(a-b)"\n'),
    # Escaped number sign in a rule-line recipe and in a tab recipe.
    make('escaped-hash-rule-recipe', [], 'all: ; zz_probe "a\\#b"\n'),
    make('escaped-hash-tab-recipe', [], 'all:\n\tzz_probe "a\\#b"\n'),
    # Static pattern rule whose prerequisite pattern holds two `%`: only the first is the stem.
    make('static-two-percent', [], 'all: run-x\nrun-x: run-%: b-%-%\n\tzz_probe $@ $< $*\n'
         'b-%: ; zz_probe build $@\n'),
    # Computed name that resolves to a defined variable via a nested reference.
    make('computed-nested', [], 'A = B\nB = C\nC = deep\nall: ; zz_probe "$($($(A)))"\n'),
    # `$(or)` whose first argument is whitespace only.
    make('or-whitespace', [], 'all: ; zz_probe "[$(or  , x)]" "[$(or ,)]"\n'),
]


def main() -> int:
    results = {}
    for fixture in PROBES:
        with tempfile.TemporaryDirectory(prefix='r638-probe-') as directory:
            scratch = Path(directory)
            tree = scratch / 'tree'
            tree.mkdir()
            d.build(fixture, tree)
            walker = d.walk(fixture, tree)
            ran, statuses = d.run(fixture, tree, scratch)
        outcome = d.outcome(fixture, walker, ran)
        results[fixture['id']] = {'outcome': outcome, 'refusal': walker['refusal'], 'walker': walker['resolved'],
                                  'real': ran, 'statuses': statuses, 'makefile': fixture['files']['Makefile'],
                                  'run': fixture['run']}
        print(f"{fixture['id']}: {outcome} walker={walker['resolved'] or walker['refusal']} real={ran}")
    Path(sys.argv[2]).write_text(json.dumps(results, indent=1, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
