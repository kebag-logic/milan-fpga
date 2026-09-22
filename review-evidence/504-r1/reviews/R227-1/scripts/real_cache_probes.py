import contextlib,hashlib,json,pathlib,sys
from unittest.mock import patch
ROOT=pathlib.Path('$VALIDATION_STORAGE/reviews/r227-504-r1'); OUT=pathlib.Path('$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-r1-r227');sys.path.insert(0,str(ROOT/'scripts'))
import ci_rv32_sdk as sdk
prefix=OUT/'sdk-trial/host';receipt=prefix/sdk.RECEIPT;original=receipt.read_bytes(); sdk.verify(prefix)
(OUT/'raw/sdk-install-receipt.json').write_bytes(original)
for label in ('bad-provenance','truncated-receipt','missing-receipt','support-file-bytes','compiler-link'):
 restore=None
 try:
  if label=='bad-provenance':
   data=json.loads(original);data['provenance']['archive_sha256']='0'*64;receipt.write_text(json.dumps(data))
  elif label=='truncated-receipt':receipt.write_text('{')
  elif label=='missing-receipt':receipt.unlink()
  elif label=='support-file-bytes':
   file=prefix/'share/buildroot/sdk-location';content=file.read_bytes();file.write_bytes(b'/incorrect/prefix\n');restore=lambda:file.write_bytes(content)
  else:
   file=prefix/sdk.COMPILER;link=file.readlink();file.unlink();file.symlink_to('/bin/false')
   def restore():file.unlink();file.symlink_to(link)
  with patch.object(sdk.subprocess,'run') as run:
   try:sdk.install(prefix)
   except (ValueError,FileNotFoundError) as exc:
    run.assert_not_called();print(json.dumps({'probe':label,'verdict':'REFUSED_BEFORE_TOOL_EXECUTION','reason':str(exc)}))
   else:raise AssertionError(label+' accepted')
 finally:
  if restore:restore()
  receipt.write_bytes(original)
sdk.verify(prefix);print('Pristine restored SDK verified after all five real-cache fault probes')
