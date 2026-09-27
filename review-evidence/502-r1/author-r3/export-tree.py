import hashlib, io, json, pathlib, subprocess, tarfile
root=pathlib.Path('/tmp/502-a345')
lane=pathlib.Path('$LANES/502-pending-live-write')
export=root/'export'; export.mkdir(exist_ok=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=lane,text=True).strip()
projects=[('',head),('protocol-processor','870ff88ad35bbd532244e4c7e6d7661b9f6e1366'),('gptp-processor','5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d'),('third_party/verilog-axis','48ff7a7e2ef782cf778d47910cf85835c64b1bce')]
records=[]
for rel,rev in projects:
    repo=lane/rel; dest=export/rel; dest.mkdir(exist_ok=True,parents=True)
    data=subprocess.check_output(['git','archive',rev],cwd=repo)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive: archive.extractall(dest,filter='data')
    n=0
    for row in subprocess.check_output(['git','ls-tree','-rz',rev],cwd=repo).split(b'\0'):
        if not row: continue
        header,name=row.split(b'\t',1); mode,kind,oid=header.split()
        if kind!=b'blob': continue
        path=dest/name.decode()
        contents=str(path.readlink()).encode() if path.is_symlink() else path.read_bytes()
        digest=hashlib.sha1(b'blob '+str(len(contents)).encode()+b'\0'+contents).hexdigest()
        assert digest==oid.decode(),str(path)
        n+=1
    records.append(dict(path=rel,revision=rev,blobs=n))
# Include current first-party edits while area comparison is pending.
changed=subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=lane,text=True).splitlines()
for rel in changed:
    (export/rel).write_bytes((lane/rel).read_bytes())
(root/'export-verification.json').write_text(json.dumps(dict(base_head=head,projects=records,working_overlays=changed),indent=2)+'\n')
print((root/'export-verification.json').read_text())
