"""Report the current foreground builder mode and its latest completed checks."""
from pathlib import Path
for name in ('driver', 'present-with-firmware-census', 'absent'):
    p=Path('/tmp/a385-final-builder-'+name+'.log')
    if p.exists():
        print(name)
        print('\n'.join(p.read_text(errors='replace').splitlines()[-5:]))
