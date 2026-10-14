import pathlib,sys,tarfile,hashlib,json
p=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(pathlib.Path(sys.argv[1])/'ci/image'));import image_archive
path=p/'scratch/image/cold-a.tar';_,m,_=image_archive.metadata(path,'linux/amd64');result=[]
with tarfile.open(path) as outer:
 for layer in m['layers']:
  with image_archive.blob(outer,layer['digest']) as s,tarfile.open(fileobj=s,mode='r|*') as t:
   for item in t:
    if item.name.removeprefix('./')=='usr/bin/make' and item.isfile():
     data=t.extractfile(item).read();out=p/'scratch/reference/bin/make';out.write_bytes(data);out.chmod(0o755)
     result.append({'sha256':hashlib.sha256(data).hexdigest(),'layer':layer['digest']})
(p/'reference-make.json').write_text(json.dumps(result,indent=2)+'\n')
