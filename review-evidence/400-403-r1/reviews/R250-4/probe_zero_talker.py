"""Check whether a configuration with no talkers is supported.

Usage (from a tree at the reviewed head): python3 -B <this>

The new builder comment says every supported configuration declares talkers
and so requires MAAP. This loads endstation_arty_current.yaml with an empty
streams.talkers list, with and without board.features.maap: false, and prints
whether load_config accepts it.
"""
import copy
from pathlib import Path
import sys
import tempfile

import yaml

sys.path.insert(0, 'sw/builder')
import endstation_builder as eb  # noqa: E402

raw = yaml.safe_load(open('configs/endstation_arty_current.yaml'))
print("streams keys:", list(raw['streams']))


def no_talkers(r):
    r['streams']['talkers'] = []


def no_talkers_no_maap(r):
    no_talkers(r)
    r['board']['features']['maap'] = False


for name, mutate in (("zero_talkers", no_talkers), ("zero_talkers_maap_false", no_talkers_no_maap)):
    r = copy.deepcopy(raw)
    mutate(r)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'c.yaml'
        p.write_text(yaml.safe_dump(r))
        try:
            eb.load_config(str(p))
            print(name, "ACCEPTED")
        except eb.ConfigError as e:
            print(name, "ConfigError:", str(e)[:220])
