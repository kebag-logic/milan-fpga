import subprocess,sys,types,runpy
from pathlib import Path
root=Path('$CHECKOUT')
# Evaluate only the original generator modules in memory; no second checkout.
for name,path in [('aem_specs','avdecc/aem_specs.py'),('endstation_builder','sw/builder/endstation_builder.py')]:
 sys.path.insert(0,str((root/path).parent))
 source=subprocess.check_output(['git','show','99a003cc:'+path],cwd=root,text=True)
 module=types.ModuleType(name);module.__file__=str(root/path);sys.modules[name]=module
 exec(compile(source,str(root/path),'exec'),module.__dict__)
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
runpy.run_path(str(root/'sw/firmware/ctrl/test/ctrl_plat_image.py'),run_name='__main__')
