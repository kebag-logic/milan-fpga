# The first runs of the held groups, at 3fed27b3 (the legs were stopped: their image was replaced by 22fc99f7)

## The held-load refusal (N-A1 at 3fed27b3, the SET_NAME took one of the AECP bucket's tokens)
REFUSED save-held: its receive channels committed {'adp': 464, 'acmp': 924, 'aecp': 928, 'maap': 231, 'srp': 2304} from its change, the held load offered {'adp': 464, 'acmp': 924, 'aecp': 929, 'maap': 231, 'srp': 2304}; refused frames [(267453916, 0, '-', 60)]
REFUSED save-starved: its receive channels committed {'adp': 464, 'acmp': 924, 'aecp': 928, 'maap': 231, 'srp': 2304} from its change, the held load offered {'adp': 464, 'acmp': 924, 'aecp': 929, 'maap': 231, 'srp': 2304}; refused frames [(267453916, 0, '-', 60)]

## The pass over the share, 1 ms after the change (8x8, each leg's held groups at 3fed27b3)
N-A8 save-held: PASS at sys 271608161: 210740 CPU cycles; 
N-A8 save-starved: PASS at sys 271608161: 213496 CPU cycles; 
N-B8 save-held: PASS at sys 271595600: 205471 CPU cycles; 
N-B8 save-starved: PASS at sys 271595600: 208488 CPU cycles; 
D-A8 save-held: 
D-A8 save-starved: 

## Its modules (N-A8 save-starved at 3fed27b3): nvm_klj2 is the two walks of the records
mods=aecp_mbx:1604,ctrl_app_aecp:6788,mbx:13750,srp_mbx:16632,ctrl_loop:3324,adp_mbx:443,adp:1604,acmp_mbx:411,acmp:41797,maap_mbx:2784,ctrl_mem:36248,ctrl_app_srp:2851,ctrl_aecp_image:189,maap:6371,aecp:7441,aecp_nvm:576,mrp_mad:26677,mbx_plat_mmio:84,timer:386,nvm_store:1133,nvm_flash_litespi:352,rt_lshrdi3:6037,aecp_commands:1303,msrp:3362,shlan_port:235,ctrl_pool:3405,mrp_pdu:5077,aecp_face:544,nvm_klj2:22088,
