#!/usr/bin/env python3
"""Create disposable, content-pinned simulation inputs below PACKET/scratch."""
import io, os, pathlib, subprocess, tarfile
packet=pathlib.Path(__file__).resolve().parent.parent
checkout=pathlib.Path(os.environ['CHECKOUT']).resolve()
assert subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()=='0ded1f269a44d107498f177c8276665656e07d30'
for target,source,ref in [('mailbox-source',checkout,'HEAD'),('processor-if2',checkout/'protocol-processor','c9f74b6866a63dd3c0e4534724bfc07a86ad142b')]:
    out=packet/'scratch'/target
    out.mkdir(parents=True,exist_ok=False)
    data=subprocess.check_output(['git','-C',str(source),'archive',ref])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(out,filter='data')
