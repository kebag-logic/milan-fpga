#!/usr/bin/env python3
"""Build the unchanged reviewed RTL in a disposable tree and run two judges."""
import hashlib, io, json, os, pathlib, shutil, subprocess, sys, tarfile, time
packet = pathlib.Path(__file__).resolve().parent
source = pathlib.Path(sys.argv[1]).resolve()
head = 'ebb1f0010bde76c38cc5270a6366ee9e3157ec54'
assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip() == head
scratch = packet/'scratch'/'disable-lap'
scratch.mkdir(parents=True,exist_ok=True)
archive = subprocess.check_output(['git','-C',str(source),'archive',head])
with tarfile.open(fileobj=io.BytesIO(archive)) as tf: tf.extractall(scratch,filter='data')
bench = scratch/'tb/acmp_talker'
cpp = bench/'sim_main.cpp'
s = cpp.read_text()
s = s.replace('  void tick() {', '  bool review_clock = false;\n  uint64_t review_ticks = 0;\n  uint32_t review_origin = 1000;\n  void tick() {\n    if (review_clock) d->now_ms_i = review_origin + uint32_t(review_ticks++ / 100000);')
s = s.replace('}  // namespace\n\nint main', (packet/'probe-disable-lap.inc').read_text()+'\n}  // namespace\n\nint main')
s = s.replace('  Hn h;\n  return h.run_suite();','  if (argc > 1 && std::string(argv[1]) == "--disable-lap") return probe_disable_lap();\n  Hn h;\n  return h.run_suite();')
cpp.write_text(s)
mk=bench/'Makefile'; mk.write_text(mk.read_text().replace('--build -j 0','--build -j 8'))
sim='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
identity=subprocess.check_output([sim,'--version'],text=True)
assert 'Verilator 5.050 ' in identity
(packet/'compiler-identity.txt').write_text(identity+'launcher_sha256='+hashlib.sha256(pathlib.Path(sim).read_bytes()).hexdigest()+'\n')
result={}
commands=[('golden',['make','-j16','run','VERILATOR='+sim]),('disable-lap',['./obj_dir/Vacmp_talker_sim','--disable-lap']),('slow-control',['./obj_dir/Vacmp_talker_sim','--disable-lap'])]
for name,cmd in commands:
    start=time.monotonic()
    with (packet/(name+'.log')).open('w') as out:
        env=os.environ.copy()
        if name=='slow-control': env['PROBE_SLOW']='1'
        rc=subprocess.run(cmd,cwd=bench,stdout=out,stderr=subprocess.STDOUT,timeout=480,env=env).returncode
    (packet/(name+'.rc')).write_text(str(rc)+'\n')
    result[name]={'command':cmd,'returncode':rc,'seconds':round(time.monotonic()-start,2)}
    print(name,rc,flush=True)
    if name=='golden' and rc: break
(packet/'probe-results.json').write_text(json.dumps(result,indent=2)+'\n')
