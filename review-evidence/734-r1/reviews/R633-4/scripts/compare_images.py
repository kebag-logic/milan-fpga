#!/usr/bin/env python3
"""Compare every linked image byte and bind the source/input claim to the reviewed tree."""
import hashlib,json,pathlib,subprocess
packet=pathlib.Path(__file__).resolve().parents[1]
root=packet/'scratch/linked-images-accepted/images'
shapes=['endstation_arty_4x4','endstation_arty_8ch','endstation_arty_current','endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8']
rows=[]
for shape in shapes:
    before=(root/'base'/shape/'ctrl_app.elf').read_bytes()
    after=(root/'head'/shape/'ctrl_app.elf').read_bytes()
    assert before==after,shape
    rows.append({'shape':shape,'bytes':len(after),'sha256_base':hashlib.sha256(before).hexdigest(),'sha256_head':hashlib.sha256(after).hexdigest(),'equal':True})
changed=subprocess.check_output(['git','diff','--name-only','a0f39ad4..HEAD','--','sw','configs','hdl','syn','protocol-processor','gptp-processor','third_party','.gitmodules'],text=True)
assert not changed
out={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'base':'a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0','build_receipt':'receipts/linked-images-accepted.log','sdk_archive_sha256':'d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f','image_inputs_unchanged':True,'pairs':rows,'limit':'Desk linked-image equality only; physical calibration NOT RUN.'}
(packet/'receipts/image-comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
