B=$1
set -- $(python3 -c 'import json, sys; d = json.load(open(sys.argv[1]))
print("xc" + d["bitstream_fpga_part"],
      hex([i for i in d["images"] if i["name"] == "aem"][0]["offset"]),
      hex(d["flash_jedec_id"]))' "$B/flashboot_layout.json")
P=$1 O=$2
echo "part $P, entity model at $O, flash ID $3"
