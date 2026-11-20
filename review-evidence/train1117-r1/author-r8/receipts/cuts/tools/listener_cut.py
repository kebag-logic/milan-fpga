"""listener_cut.py TREE: attempt 2's polls cut in TREE's ctrl_app_srp.c: SRP's delivery tells ACMP a source's Listener
presence only where ACMP's flag differs from it. Scratch writer of the committed change."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sw/firmware/ctrl/app/ctrl_app_srp.c'; t = p.read_text()
a = """        (void)acmp_listener_registered(&app->acmp.acmp,interface,source,present);
    }"""
b = """        // ACMP is told a Listener's presence where its flag differs: the call sets that flag and nothing else, so a
        // pass that changes no source's paid it for every source each pass (#665)
        if (app->acmp.acmp.sources[source].listener_registered != present) {
            (void)acmp_listener_registered(&app->acmp.acmp,interface,source,present);
        }
    }"""
assert t.count(a) == 1
p.write_text(t.replace(a, b))
print('listener cut written')
