import contextlib,io,json,pathlib,sys,types,unittest
ROOT=pathlib.Path('$VALIDATION_STORAGE/reviews/r227-504-r1'); sys.path.insert(0,str(ROOT/'scripts'))
import ci_rv32_sdk_selftest as fixtures
source=(ROOT/'scripts/ci_rv32_sdk.py').read_text()
changes=[('omit-extraction','    destination.mkdir(parents=True)','    return\n    destination.mkdir(parents=True)'),('omit-relocation','    subprocess.run(argv, cwd=destination, check=True)','    pass'),('ignore-provenance','    if receipt["provenance"] != provenance(destination):','    if False:'),('ignore-inventory','    if not actual or receipt["inventory"] != actual:','    if False:'),('ignore-tool-version','    if values["gcc_version"] != "14.3.0":','    if False:'),('ignore-tool-target','    if values["target"] != "riscv32-buildroot-linux-gnu":','    if False:'),('ignore-tool-receipt','    if receipt["tools"] != identify(destination):','    if False:')]
for label,old,new in changes:
 assert source.count(old)==1
 module=types.ModuleType('review_sdk_fault'); module.__file__=str(ROOT/'scripts/ci_rv32_sdk.py'); exec(compile(source.replace(old,new),module.__file__,'exec'),module.__dict__)
 fixtures.sdk=module; suite=unittest.defaultTestLoader.loadTestsFromModule(fixtures); stream=io.StringIO()
 with contextlib.redirect_stdout(io.StringIO()): result=unittest.TextTestRunner(stream=stream,verbosity=0).run(suite)
 record={'fault':label,'tests_run':result.testsRun,'failures':[t.id() for t,_ in result.failures],'errors':[t.id() for t,_ in result.errors]}; print(json.dumps(record)); assert not result.wasSuccessful(),label
print('7 in-memory installer omission/identity mutants killed by actual shipped fixture suite')
