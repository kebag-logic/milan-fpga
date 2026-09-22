#!/usr/bin/env python3
import json,sys
from pathlib import Path
rows=json.loads(Path(sys.argv[1]).read_text())
verdicts=[]
for r in rows:
    before=all(e and e[0][1]&16 for e in r['owned_pidfd_events_while_blocked'].values())
    after=all(e and e[0][1]&16 for e in r['owned_pidfd_events_after_drain'].values())
    assert after and r['exit_after_drain']==(-15 if r['signal']=='SIGTERM' else -2),'draining positive control failed'
    verdicts.append(before)
    print(r['signal'], 'cancellation_before_consumer_drain='+str(before), 'draining_positive_control='+str(after))
raise SystemExit(0 if all(verdicts) else 1)
