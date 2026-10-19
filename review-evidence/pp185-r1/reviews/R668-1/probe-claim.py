#!/usr/bin/env python3
import pathlib,subprocess,os,sys,difflib
p=pathlib.Path(__file__).resolve().parent
source=p/'scratch/source'
f=source/'tb/aecp_notify/sim_main.cpp'
original=subprocess.check_output(['git','show','b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad:tb/aecp_notify/sim_main.cpp'],cwd=sys.argv[1],text=True)
s=original.replace('bool lock_op(uint64_t eid, bool unlock, uint32_t flags) {','bool lock_op(uint64_t eid, bool unlock, uint32_t flags, int settle = 2) {')
s=s.replace('d->rgy_flags_i = 0;\n    idle(2);','d->rgy_flags_i = 0;\n    idle(settle);')
needle='  d->uns_done_i = 1;\n}\n\n// SC1:'
probe=r"""
  for (uint32_t flags : {0u, 0x00010000u}) {
    for (int settle : {0, 1}) {
      warm_reset();
      d->uns_done_i = 0;
      now = 100000;
      register_row(EID_C, MAC_C, false);
      const bool took4 = lock_op(EID_X, false, flags, settle);
      // settle 0: expiry before returning idle; settle 1: expiry at the claim.
      now += 60000;
      expire(LOCK_SLOT, OWN_LOCK);
      const UnsJob clash = job_presented(now + WALK_MS);
      printf("PROBE settle=%d command_flags=%08x took=%u held=%u holder=%016llx kind=%u flags=%04x%04x\n",
             settle, flags, took4, unsigned(d->lock_held_o),
             (unsigned long long)d->lock_ctlr_o,
             unsigned(clash.kind), unsigned(clash.arg1), unsigned(clash.arg0));
      if (clash.ms) (void)retire();
      const UnsJob later = job_presented(now + WALK_MS);
      printf("PROBE follow-up: present=%u kind=%u flags=%04x%04x\n", later.ms != 0,
             unsigned(later.kind), unsigned(later.arg1), unsigned(later.arg0));
      CHECK(took4 && !d->lock_held_o && clash.ms && clash.kind == KIND_LOCK
                && clash.arg1 == 0 && clash.arg0 == 1,
            "PROBE: expiry before/at round claim must notify UNLOCK (settle=%d, command=%08x)",
            settle, flags);
    }
  }
  d->uns_done_i = 1;
}

// SC1:"""
assert needle in s
s=s.replace(needle,probe)
f.write_text(s)
(p/'claim-collision.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='a/tb/aecp_notify/sim_main.cpp',tofile='b/tb/aecp_notify/sim_main.cpp')))
env=os.environ.copy(); env['TMPDIR']=str(p/'scratch/tmp'); env['MAKEFLAGS']='-j16'; env['VERILATOR']=str(p/'bounded-sim.py'); env['REVIEW_BUILD_JOBS']='8'
with (p/'receipts/claim-collision.log').open('w') as log:
 rc=subprocess.run(['make','-j16','-C','tb/aecp_notify','collision'],cwd=source,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 # Reuse the default build, but run the default test path including the added probe.
 if rc==0:
  rc=subprocess.run(['./obj_dir/Vaecp_notify_sim'],cwd=source/'tb/aecp_notify',env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'receipts/claim-collision.rc').write_text(str(rc)+'\n')
f.write_text(original)
print('Probe exit:',rc)
