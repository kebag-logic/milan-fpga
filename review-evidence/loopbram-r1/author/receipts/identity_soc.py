import sys,types,subprocess
from pathlib import Path
root=Path('$CHECKOUT');mode=sys.argv.pop(1)
sys.path.insert(0,str(root/'sw/litex'))
source=(subprocess.check_output(['git','show','99a003cc:sw/litex/milan_soc.py'],cwd=root,text=True) if mode=='baseline' else (root/'sw/litex/milan_soc.py').read_text())
m=types.ModuleType('milan_soc');m.__file__=str(root/'sw/litex/milan_soc.py');sys.modules['milan_soc']=m
exec(compile(source,m.__file__,'exec'),m.__dict__)
m._builder_out=lambda directory,name:str(Path(directory)/name)
m.main()
