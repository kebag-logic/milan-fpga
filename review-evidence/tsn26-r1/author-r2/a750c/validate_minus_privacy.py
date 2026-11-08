# Diagnostic: run the clone's own scripts/validate.py unchanged except that the single
# ('privacy', 'check_privacy.py', []) entry is removed, so the fail-fast stop does not
# skip the build, mutation and graph gates. privacy is run and reported separately.
import sys
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
path = clone / 'scripts' / 'validate.py'
src = path.read_text()
old = "        ('privacy-selftest', 'check_privacy.py', ['--selftest']),\n        ('privacy', 'check_privacy.py', [])):"
new = "        ('privacy-selftest', 'check_privacy.py', ['--selftest']),\n        ):"
assert src.count(old) == 1, 'unexpected validate.py text'
sys.argv = [str(path)] + sys.argv[2:]
exec(compile(src.replace(old, new), str(path), 'exec'), {'__file__': str(path), '__name__': '__main__'})
