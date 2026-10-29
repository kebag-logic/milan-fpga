# The reviewers' probes, copied unchanged from their packets, run against the working tree's fixed mover

- r712: `probe_dma_length.py` (R712-1), its bench copy with a 1,024-word ring, lengths 4092 to 4095 both directions, pinned Verilator 5.050: rc 0
- r711: `dma_reviewer_plants.py` (R711-1), ten plants against the tree's bench: 10 of 10 caught
- r711: `dma_len_probe.cpp` (R711-1), 22 moves, pinned Verilator 5.050: 0 hang

sha256 of the probe sources as run:
2b6696be5aed430590d52e0bc3de3ff1dc42a1f7a8a4f7cef675986b75c3820f  r712/probe_dma_length.py
a842805de50b3871ebbe53768b746882faba355351e01a0f1ae232a7f3b43798  r711/dma_reviewer_plants.py
daed85573b26013fff79928e0504bf9ba2084d3524106198cbc0124ac3df5919  r711/dma_len_probe.cpp
2b6696be5aed430590d52e0bc3de3ff1dc42a1f7a8a4f7cef675986b75c3820f  665s2b-r712-1/probe_dma_length.py
a842805de50b3871ebbe53768b746882faba355351e01a0f1ae232a7f3b43798  665s2b-r711-1/scripts/dma_reviewer_plants.py
daed85573b26013fff79928e0504bf9ba2084d3524106198cbc0124ac3df5919  665s2b-r711-1/scripts/dma_len_probe.cpp
