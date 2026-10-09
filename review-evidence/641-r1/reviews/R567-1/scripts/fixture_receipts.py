#!/usr/bin/env python3
"""Recompute media and grading independently from the published trace bytes."""
import hashlib, json, pathlib, subprocess, sys, tempfile
root=pathlib.Path.cwd()
packet=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tb/verilator/fw_service_budget'))
import run
oracle=json.loads((run.HERE/'oracle.json').read_text())
old=json.loads(subprocess.check_output(['git','show','5603c353:tb/verilator/fw_service_budget/oracle.json']))
for row, prior, name in zip(oracle,old,('1X1-ALL','8X8-ALL','1X1-PACED')):
    public=json.loads((packet/'public/review-evidence/641-r1/author'/f'MEASUREMENT-{name}.json').read_text())
    for section in ('input_hashes', 'build_hashes'):
        for filename, digest in public[section].items():
            source=root/filename
            if not pathlib.Path(filename).is_absolute() and source.is_file():
                assert hashlib.sha256(source.read_bytes()).hexdigest()==digest, filename
    assert row['raw_log']==public['raw_log']
    assert hashlib.sha256(row['raw_log'].encode()).hexdigest()==row['log_sha256']==public['log_sha256']
    assert set(row['media'])=={'populated','plan','slots_sha256'}, row['media']
    with tempfile.TemporaryDirectory() as directory:
        media=run.oracle_media(pathlib.Path(directory),row['shape'],row['media'])
        assert media==public['media'],(media,public['media'])
        graded=run.grade(row['raw_log'],media)
        for key in ('rows','budget_findings','heartbeat','liveness'):
            assert graded[key]==row[key]==public[key],key
        wrong=dict(media,image_bytes=media['image_bytes']+1)
        try: run.grade(row['raw_log'],wrong)
        except RuntimeError as error: assert str(error)=='flash operation census'
        else: raise AssertionError('byte-count mutation escaped')
        print(json.dumps(dict(trace=name,media=media,raw_log_matches_public=True,grading_matches=True,findings=row['budget_findings'],prior_findings=prior['budget_findings'],wrong_size_refused=True)))
