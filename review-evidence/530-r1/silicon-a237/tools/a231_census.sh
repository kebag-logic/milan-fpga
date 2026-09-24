set -u
T=/tmp/a231/avdecc_ro.py
PEER=3cc0c60102030000; PMAC=3c:c0:c6:01:02:03; DUT=020000fffe000001; DMAC=02:00:00:00:00:01
Z=0000000000000000
for i in 0 1 2 3 4 5 6 7 8 9; do sudo -n timeout 8 python3 $T acmp ens10 get_rx_state $Z 0 $PEER $i; done
for i in 0 1 2 3; do sudo -n timeout 8 python3 $T acmp ens10 get_tx_state $PEER $i $Z 0; done
for i in 0 1; do sudo -n timeout 8 python3 $T acmp ens10 get_rx_state $Z 0 $DUT $i; done
for i in 0 1; do sudo -n timeout 8 python3 $T acmp ens10 get_tx_state $DUT $i $Z 0; done
sudo -n timeout 40 python3 $T aem ens10 $PEER $PMAC 0x0017 00240000 0x0004 0000000000050000 0x0004 0000000000050001 0x0004 0000000000050008 0x0004 0000000000050009 0x0004 0000000000060000 0x0004 0000000000060002 0x0009 00050000 0x0009 00050008 0x0015 00020000
sudo -n timeout 20 python3 $T aem ens10 $DUT $DMAC 0x0004 0000000000000000 0x0007 00000000 0x0017 00240000 0x0027 00090000 0x0028 00000000
sudo -n timeout 20 python3 $T aem ens10 $PEER $PMAC 0x0007 00000000 0x0015 00020000 0x0017 00240000 0x0009 00050008 0x0004 0000000000000000
