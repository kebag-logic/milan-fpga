from pathlib import Path
import hashlib, re, shutil
root=Path('<scratch>')
out=Path('<management>/920-a786/round3')
receipts=out/'receipts'
large=[]
def scrub(text):
    text=text.replace(str(root), '<scratch>')
    text=text.replace('<lane-scratch>', '<lane-scratch>')
    text=text.replace('<source>', '<source>')
    text=text.replace('<management>', '<management>')
    text=re.sub(r'<home>/\s]+', '<home>', text)
    text=re.sub(r'<other-scratch>/\s]+', '<other-scratch>', text)
    text=re.sub(r'$VALIDATION_STORAGE/(?:tools|scratch)/[^\s`"<>]+', '<installed-tool>', text)
    text=text.replace('<review-packet>', '<review-packet>')
    return text
def copy(p, dest):
    if not p.is_file(): return
    b=p.read_bytes()
    if len(b)>200000:
        large.append(f'{p.relative_to(root)} {len(b)} B sha256 {hashlib.sha256(b).hexdigest()}')
        lines=b.decode(errors='replace').splitlines()
        text='Full log omitted (size limit); sha256 and size in large-files.txt.\n'+ '\n'.join(lines[:6]+['[middle omitted]']+lines[-80:])+'\n'
        if dest.exists(): dest.unlink()
        dest=dest.with_suffix('.excerpt.txt')
    else:
        text=b.decode()
    if len(text.encode())>190000:
        text=text[:85000]+'\n[excerpt further shortened to fit packet limit]\n'+text[-85000:]
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(scrub(text))
for p in (root/'logs').glob('*'):
    copy(p,receipts/'gates'/p.name)
for p in (root/'docs/logs').glob('*'):
    copy(p,receipts/'docs'/p.name)
for p in (root/'scripts').glob('*'):
    copy(p,receipts/'reproduction'/p.name)
for p in receipts.rglob('*'):
    if p.is_file():
        t=p.read_text(); s=scrub(t)
        if s!=t: p.write_text(s)
if large:
    (receipts/'large-files.txt').write_text('\n'.join(large)+'\n')
files=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='INDEX.md')
assert all(p.stat().st_size<=200000 for p in files)
rows=['# Round 3 packet index', '', 'Generated from the sanitized files present. SHA-256 hashes describe the packaged bytes.', '', '| File | Bytes | SHA-256 |','|---|---:|---|']
for p in files:
    rel=p.relative_to(out).as_posix(); data=p.read_bytes()
    rows.append(f'| [{rel}]({rel}) | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |')
(out/'INDEX.md').write_text('\n'.join(rows)+'\n')
print(f'Indexed {len(files)} sanitized files; none exceeds 200 KB.')
