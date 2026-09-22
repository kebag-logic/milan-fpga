import hashlib,json,pathlib,urllib.request
OUT=pathlib.Path('$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-r1-r227')
archive=pathlib.Path('$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz')
url='https://toolchains.bootlin.com/downloads/releases/toolchains/riscv32-ilp32d/tarballs/riscv32-ilp32d--glibc--stable-2025.08-1.sha256'
authority=urllib.request.urlopen(url,timeout=30).read();digest=hashlib.file_digest(archive.open('rb'),'sha256').hexdigest();assert archive.stat().st_size==102597892;assert digest=='d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f' and digest in authority.decode()
print(json.dumps({'archive':str(archive),'size':archive.stat().st_size,'sha256':digest,'authority_url':url,'published_checksum':authority.decode()}))
