from pathlib import Path
import hashlib
root=Path('<lane-scratch>')
for d in sorted((root/'r3/images').iterdir()):
    if not d.is_dir(): continue
    assert (d/'rc').read_text().strip()=='0', d.name
    old=root/'r3/baseline-images'/d.name
    for f in ['image/ctrl_app.elf', 'loadable.bin']:
        a=(d/f).read_bytes(); b=(old/f).read_bytes()
        assert a==b, f'{d.name}/{f} differs'
        print(f'IDENTICAL {d.name}/{f} {len(a)} B sha256 {hashlib.sha256(a).hexdigest()}')
