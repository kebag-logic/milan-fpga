import sys,json
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'tb/verilator/nvm_capture_cpu'))
from run import _compile
build = Path('$VALIDATION_STORAGE/559-a307-capture-8x8')
_compile(build, json.loads((build / 'sources.json').read_text()))
