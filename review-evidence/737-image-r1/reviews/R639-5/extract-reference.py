import pathlib,sys,json,tarfile,hashlib,os
p=pathlib.Path(__file__).resolve().parent;root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'ci/image'));import image_archive
archive=p/'scratch/image/cold-a.tar';dest=p/'scratch/reference';dest.mkdir(exist_ok=True)
_,manifest,config=image_archive.metadata(archive,'linux/amd64');rows=[]
with tarfile.open(archive) as outer:
 for layer in manifest['layers']:
  with image_archive.blob(outer,layer['digest']) as stream,tarfile.open(fileobj=stream,mode='r|*') as t:
   for m in t:
    n=m.name.removeprefix('./')
    selected=n=='usr/bin/python3.12' or n.startswith(('usr/lib/python3.12/','usr/lib/x86_64-linux-gnu/libpython3.12','opt/python/lib/python3.12/site-packages/'))
    if not selected or not m.isfile():continue
    out=dest/n;out.parent.mkdir(parents=True,exist_ok=True)
    data=t.extractfile(m).read();out.write_bytes(data);out.chmod(m.mode)
    rows.append({'path':n,'sha256':hashlib.sha256(data).hexdigest(),'layer':layer['digest']})
(p/'reference-extraction.json').write_text(json.dumps(rows,indent=2)+'\n')
print('extracted',len(rows),'reference files')
bin=dest/'bin';bin.mkdir(exist_ok=True)
script='#!/bin/sh\nexport PYTHONHOME="'+str(dest/'usr')+'"\nexport PYTHONPATH="'+str(dest/'opt/python/lib/python3.12/site-packages')+'"\nexec "'+str(dest/'usr/bin/python3.12')+'" "$@"\n'
(bin/'python3').write_text(script);(bin/'python3').chmod(0o755)
