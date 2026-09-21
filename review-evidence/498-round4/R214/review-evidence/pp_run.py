import os,subprocess,sys,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent;tmp=Path(os.environ['REVIEW_TMP'])
srcs=subprocess.check_output(['make','-s','-C',str(root/'tb/verilator/milan_dp'),'print-srcs'],text=True).strip()
assert srcs and 'pp_adp_pkg.sv' in srcs
(tmp/'pp-derived-sources.txt').write_text(srcs+'\n')
cmd=['make','-C',str(tmp/'pp-stage/tb/verilator/pp_shadow'),'-j8','run','DP_SRCS='+srcs]+sys.argv[1:]
(tmp/('pp-command-'+('mutant' if sys.argv[1:] else 'baseline')+'.json')).write_text(json.dumps(cmd,indent=2))
sys.exit(subprocess.run(cmd).returncode)
