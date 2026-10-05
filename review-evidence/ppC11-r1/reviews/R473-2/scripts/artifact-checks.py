#!/usr/bin/env python3
import pathlib,subprocess,re,json,hashlib,os
p=pathlib.Path(__file__).resolve().parents[1];root=p/'scratch/tree'
def content(ref,path):return subprocess.check_output(['git','-C',str(root),'show',ref+':'+path],text=True)
ports=set()
for f in (root/'hdl').rglob('*.sv'):
 s=re.sub(r'//[^\n]*|/\*.*?\*/','',f.read_text(),flags=re.S if False else 0)
 for line in s.splitlines():
  if re.search(r'\b(input|output|inout)\b',line):ports.update(re.findall(r'\b\w+_[io]\b',line))
top=(root/'hdl/top/protocol_processor_top.sv').read_text()
top_ports=set()
for line in top.splitlines():
 if re.match(r'\s*(input|output|inout)\b',line):top_ports.update(re.findall(r'\b\w+_[io]\b',line.split('//')[0]))
missing=[];allnames=set()
for f in (root/'docs/architecture').glob('*.md'):
 names=set(re.findall(r'\b[A-Za-z][A-Za-z0-9_]*_[io]\b',f.read_text()));allnames|=names
 for n in sorted(names-ports):missing.append((str(f.relative_to(root)),n))
print('Architecture port names',len(allnames),'missing',missing);assert not missing
face=(root/'docs/architecture/02_interfaces.md').read_text()
names=set(re.findall(r'\b[A-Za-z][A-Za-z0-9_]*_[io]\b',face))
print('02 names',len(names),'missing from top',sorted(names-top_ports));assert not names-top_ports
assert 'rx_err_i' not in ports and 'rx_ready_o' not in top_ports
print('Independent missing-name control: rx_err_i absent; rx_ready_o not a top port')
base=content('c050d971','docs/architecture/02_interfaces.md');hist=(root/'docs/history/02-class-a-word-stream.md').read_text()
old_prose=base.split('Word-oriented stream,')[1].split('The RX stream carries')[0]
assert ('Word-oriented stream,'+old_prose).strip() in hist
for anchor in ['fig-02-rxwave','fig-02-txwave']:
 block=base.split('<a id="'+anchor+'"></a>')[1].split('```wavedrom\n')[1].split('```')[0]
 assert block in hist
print('Historical word-stream prose/table/two waveform sources: verbatim at c050d971')
assert all('docs/history' in (root/f).read_text() or 'history/02-class-a-word-stream.md' in (root/f).read_text() for f in ['README.md','docs/README.md','docs/architecture/02_interfaces.md'])
for stem in ['rxwave','txwave','memwave']:
 name='fig-02-'+stem
 subprocess.run(['rsvg-convert','-w','1600','-o',str(p/'scratch'/(name+'.png')),str(root/'docs/diagrams/wavedrom'/(name+'.svg'))],check=True)
 print('Rendered',name)
for name,cmd in [('simulator identity',['$VALIDATION_TOOLS/pinned-verilator-5.050/verilator','--version']),('diagram cli',['mmdc','--version']),('renderer',[str(p/'scratch/venv/bin/python'),'-c','import importlib.metadata as m; print(m.version("wavedrom"))'])]:
 print(name,subprocess.check_output(cmd,text=True).strip())
f=pathlib.Path('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator');print('simulator entry SHA256',hashlib.sha256(f.read_bytes()).hexdigest())
