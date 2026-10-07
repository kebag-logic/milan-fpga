import hashlib,json,pathlib,re,sys
p=pathlib.Path(sys.argv[1]).resolve(); raw=p/'scratch/raw-receipts'; raw.mkdir(exist_ok=True)
changes=[]
for f in sorted((p/'receipts').glob('*')):
 if not f.is_file():continue
 original=f.read_bytes();data=original
 data=re.sub(rb'/home/[^/\s]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff/usr/share/verilator',b'<SIM_INSTALL>',data)
 data=re.sub(rb'/home/[^/\s]+',b'~',data)
 if data!=original:
    (raw/f.name).write_bytes(original);f.write_bytes(data)
    changes.append(dict(file=str(f.relative_to(p)),original_sha256=hashlib.sha256(original).hexdigest(),published_sha256=hashlib.sha256(data).hexdigest(),change='Local home/install prefixes only; diagnostic and result text unchanged'))
(p/'receipts/path-redactions.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Path-only redactions:',len(changes))
