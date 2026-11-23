# Firmware gate after relearning the hot list

Command in each independent clean clone:
`python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard k/4 --jobs 2`

shard 0/4: 631dc544ce4ac0221f2a9cc7363838e3a22961f3
shard 1/4: 631dc544ce4ac0221f2a9cc7363838e3a22961f3
shard 2/4: 631dc544ce4ac0221f2a9cc7363838e3a22961f3
shard 3/4: 631dc544ce4ac0221f2a9cc7363838e3a22961f3

Four shards completed, rc=0. Control campaign: 826/826 caught. gptp and gptp_ubsan: 63 tests each.
ctrl_hot.py: 286 entries, two passing controls and ten caught plants, including the two new LINKED controls.
Full logs exceeding 200 KB remain outside this packet; LARGE.txt records size and sha256.
Only prose changed after this head: two design pages and ctrl_memory.py's explanatory string.
