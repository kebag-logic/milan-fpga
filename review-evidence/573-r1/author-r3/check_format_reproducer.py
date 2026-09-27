"""Grade the unchanged historical reproducer's expected boundary refusal."""
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
script = '/tmp/573-a355/reviews/R340-2/scripts/r341-1/format_cap_length.py'
result = subprocess.run([sys.executable, '-B', script, '/tmp/573-a355/head'],
                        capture_output=True, text=True, timeout=900)
(out / 'format-reproducer-raw.log').write_text(result.stdout + result.stderr)
print('Unchanged reproducer raw exit:', result.returncode)
assert result.returncode == 1
assert 'final formats=46: loader ACCEPTED' in result.stdout
assert 'descriptor length 506 octets' in result.stdout
assert 'number_of_formats 46' in result.stdout
assert 'format count 47 exceeds 46' in result.stderr
assert 'ConfigError' in result.stderr
print('Expected 46-entry acceptance and named 47-entry refusal verified.')
