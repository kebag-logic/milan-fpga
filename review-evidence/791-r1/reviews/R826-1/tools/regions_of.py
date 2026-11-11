"""regions_of.py <soc.json> <out.json>: a region-decode soc.json's memory_regions followed by its cpu_devices."""
import json, sys
d = json.load(open(sys.argv[1]))
json.dump(d['memory_regions'] + d['cpu_devices'], open(sys.argv[2], 'w'))
print(d['netlist'], d['mutant'])
