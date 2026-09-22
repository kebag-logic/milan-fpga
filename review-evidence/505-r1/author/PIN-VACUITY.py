"""Focused #407 controls; changes only an imported module in memory."""
import collections
import copy
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd() / 'scripts'))
import ci_events as c

world = c.parse_world(c.read_tree(Path.cwd()))
arms = c._carrier_script_arms(world)
all_arms = c._mutations(world)
assert len({name for name, _, _ in all_arms}) == len(all_arms)
print('unique mutation labels: PASS')
print('all workflow mutations:', len(all_arms))
print('carrier mutation levers:', dict(collections.Counter(
    name.rsplit(' ', 1)[1] for name, _, _ in arms)))
for jid in ('docs-check', 'wire-accountability', 'docs-check-no-git', 'elaborate'):
    print(jid, dict(collections.Counter(name.rsplit(' ', 1)[1]
          for name, _, _ in arms if name.startswith(f'carrier-script-407 {jid} '))))

body_arms = [arm for arm in arms if not arm[0].endswith('continue-on-error')]
original = c.check_carrier_script
c.check_carrier_script = lambda *args: None
try:
    for name, mutate, want in body_arms:
        changed = copy.deepcopy(world)
        mutate(changed)
        assert not any(want in f for f in c.check(changed).findings), name
    print('focused vacuity: disabling only check_carrier_script fails all',
          len(body_arms), 'body assertions with specialized checks still active')
finally:
    c.check_carrier_script = original

print('focused carrier controls: PASS')
