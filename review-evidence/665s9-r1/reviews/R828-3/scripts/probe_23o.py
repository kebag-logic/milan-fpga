"""Gate 23o probe. argv: plant|clean. Runs test_builder.py --gates test_placement_recipe from the
current checkout; with `plant`, the split placement's nvm_split.json differs from the all-fabric
build's (one block's count +1) while every other artifact is untouched."""
import copy, runpy, sys
from pathlib import Path
mode = sys.argv[1]
sys.path.insert(0, str(Path('sw/builder').resolve()))
sys.path.insert(0, str(Path('avdecc').resolve())); sys.path.insert(0, str(Path('scripts').resolve()))
sys.path.insert(0, str(Path('sw/litex').resolve()))
import endstation_builder as eb
if mode == 'plant':
    real = eb._derive_artifacts
    def planted(config_path, placement=None):
        art = real(config_path, placement)
        if placement == 'split':
            ns = copy.deepcopy(getattr(art, 'nvm_split', None))
            assert ns is not None, 'this tree has no nvm_split artifact: the plant has nothing to change'
            ns['blocks'][0]['count'] += 1
            art = copy.copy(art); object.__setattr__(art, 'nvm_split', ns)
        return art
    eb._derive_artifacts = planted
    print('PLANT: split nvm_split.json block 0 count +1', flush=True)
sys.argv = ['sw/builder/test_builder.py', '--gates', 'test_placement_recipe']
runpy.run_path('sw/builder/test_builder.py', run_name='__main__')
