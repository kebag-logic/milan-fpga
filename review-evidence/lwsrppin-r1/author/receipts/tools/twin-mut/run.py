import importlib.util, sys
src_dir, path = sys.argv[1], sys.argv[2]
sys.path.insert(0, src_dir)
spec = importlib.util.spec_from_file_location("twin_mrp_mut", path); m = importlib.util.module_from_spec(spec)
sys.modules["twin_mrp_mut"] = m; spec.loader.exec_module(m)
print(path.rsplit("/",1)[1], m.selftest() or "ALL PASS")
