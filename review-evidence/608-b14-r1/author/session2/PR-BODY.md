[A578] B14 bench lane on dev 5603c353: STOP after the identity gate (resume session)

Refs #608 #645 #647 #667 #682 #686 #691

This session proposes no pull request. Branch `608-b14-bench` is unchanged at dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`, with no commit, and no findings page has been written yet.

- The controller host came back at 04:45 UTC. Every host was re-checked.
- Item 1, the identity gate, passes:
  - entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0", serial "AX7101-0001";
  - CSR ID `4d494c4e` and VERSION `00020060`;
  - AEM CRC `5ba355eb` over the QSPI bytes and the RAM copy.
- The SoC board's serial console then answered with a login prompt instead of the root shell. The bench rule is to stop there and leave the login to the manager.
- No bench state changed. Only read-only console, AECP and ADP reads ran under the bench lock, which is free.
- Two decisions for the resume:
  - item 6's RX error counters need an RMON snapshot write, which this lane's rules forbid;
  - item 7 cannot observe a fresh MAAP acquisition without a power cycle or a register write.

The lane continues from item 2 on the same image once the console is logged in or the check is ruled out of scope.
