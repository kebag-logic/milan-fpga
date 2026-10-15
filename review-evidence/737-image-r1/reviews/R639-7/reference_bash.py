#!/usr/bin/env python3
"""Extract the base image's Bash version from the public distribution package."""
import gzip, hashlib, json, subprocess, urllib.request
from pathlib import Path
p=Path(__file__).resolve().parent
base='https://archive.ubuntu.com/ubuntu/'
data=urllib.request.urlopen(base+'dists/noble/main/binary-amd64/Packages.gz').read()
paragraph=next(x for x in gzip.decompress(data).decode().split('\n\n') if x.startswith('Package: bash\n'))
fields=dict(line.split(': ',1) for line in paragraph.splitlines() if ': ' in line and not line.startswith(' '))
assert fields['Version']=='5.2.21-2ubuntu4'
body=urllib.request.urlopen(base+fields['Filename']).read()
assert hashlib.sha256(body).hexdigest()==fields['SHA256']
archive=p/'scratch/bash.deb'; archive.write_bytes(body)
target=p/'scratch/reference-bash'
target.mkdir(exist_ok=True)
member=next(x for x in subprocess.check_output(['ar','t',str(archive)],text=True).splitlines() if x.startswith('data.tar'))
payload=p/'scratch'/member
payload.write_bytes(subprocess.check_output(['ar','p',str(archive),member]))
subprocess.run(['tar','-xf',str(payload),'-C',str(target)],check=True)
binary=next(x for x in [target/'bin/bash',target/'usr/bin/bash'] if x.is_file())
version=subprocess.check_output([str(binary),'--version'],text=True).splitlines()[0]
record={'version':version,'package':fields['Version'],'package_sha256':fields['SHA256'],'url':base+fields['Filename'],'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'matches_image_base_package':True}
(p/'reference-bash.json').write_text(json.dumps(record,indent=2)+'\n')
print(version)
