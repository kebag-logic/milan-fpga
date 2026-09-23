set -e
./obj_dir/Vmilan_dp_sim
echo "---- Milan 5.4.5 notifications, TIMED on the compressed processor timebase ----"
./obj_notify/Vmilan_dp_notify
./obj_nxn/Vmilan_dp_nxn
echo "---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----"
./obj_nxndv/Vmilan_dp_nxndv
./obj_nxn8/Vmilan_dp_nxn8
echo "---- the shipping Arty shape: 4 streams x 4 wire channels ----"
./obj_nxn4c/Vmilan_dp_nxn4c
echo "---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----"
./obj_nolpf/Vmilan_dp_nolpf
echo "---- all six tier-1 blocks pruned ----"
./obj_prune/Vmilan_dp_prune
