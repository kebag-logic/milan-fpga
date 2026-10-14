import pathlib,sys,json,hashlib,shutil,tarfile,gzip
p=pathlib.Path(__file__).resolve().parent;root=pathlib.Path(sys.argv[1]).resolve();source=pathlib.Path(sys.argv[2])
sys.path.insert(0,str(root/'ci/image'));import image_archive,image_lock,build
work=p/'scratch/image';work.mkdir(parents=True,exist_ok=True)
rows=[]
for name in ('cold-a','cold-b'):
 src=source/name/'image.tar';dst=work/(name+'.tar');shutil.copyfile(src,dst)
 with dst.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 descriptor,manifest,config=image_archive.metadata(dst,'linux/amd64')
 rows.append({'name':name,'bytes':dst.stat().st_size,'sha256':digest,'manifest':descriptor,'config':manifest['config'],'layers':manifest['layers'],'diff_ids':config['rootfs']['diff_ids']})
 if name=='cold-a':(p/'image-config-history.json').write_text(json.dumps(config,indent=2)+'\n')
print('exports equal:',rows[0]['sha256']==rows[1]['sha256'],flush=True)
(p/'independent-exports.json').write_text(json.dumps(rows,indent=2)+'\n')
# Only authenticated, publicly pinned archive inputs, never lane notes or receipts.
(work/'context').symlink_to(source/'cold-a/context',target_is_directory=True)
(work/'base-locked.tar').symlink_to(source/'cold-a/base-locked.tar')
pins=json.loads((root/'ci/image/sources.lock.json').read_text());lock=json.loads((root/'ci/image/image.lock.json').read_text())
image_lock.validate(lock,pins,build.recipe_digest(),build.layer_records(pins))
artifact=build.checked_artifact(work/'cold-a.tar',work,pins)
image_lock.verify_artifact(lock,artifact)
shutil.copyfile(work/'privacy-report.json',p/'independent-image-audit.json')
print('PASS lock, config, every compressed layer, diff-id and full member privacy scan',flush=True)
