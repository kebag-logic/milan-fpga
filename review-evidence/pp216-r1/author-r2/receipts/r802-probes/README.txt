The second review's probes, applied as published (their patch files in that review's packet, unchanged) to a clean
clone of the head 84f6d6a by r802-probes.sh (beside this file):
- p09-note4-inverted, p12-txla-vp-stays, p19-txla-vp-sends-sj (the three that survived every group at 60094a2):
  each now fails tb/srp_encoder, 1659 checks: 1657 PASS, 2 FAIL (p09: DA6, VR12; p12, p19: DA7, VR13), rc 2.
- r802-link-bounce.tb.patch (its in-tree successor is tb/srp_top AP8), applied with patch -p1 to the moved lines:
  passes, 2 checks: 2 PASS, 0 FAIL; VID 2 after LINK_UP New@3801 New@4001 JoinMt@4201 JoinMt@5001 JoinMt@6001.
