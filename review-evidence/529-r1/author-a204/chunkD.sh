set -e
echo "---- THE SHIPPING ALINX SHAPE: 1 stream x 8 wire channels, TDM8 master ----"
./obj_ax1x1/Vmilan_dp_ax1x1
echo "---- the same shape at the TRUE clk_audio ratio (391/1591) ----"
./obj_aclk/Vmilan_dp_aclk
