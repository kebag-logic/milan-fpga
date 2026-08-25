#!/usr/bin/env bash
# gptp_direct_cable.sh - RETIRED (#259, 2026-08-25).
#
# This bench flow validated the SOFTWARE gPTP owner (ptp4l on two Linux
# images over a direct cable). That owner and its images are retired: the
# product is bare-metal only and the fabric plane is the one gPTP owner, so
# there is no software-owner image left for this script to drive. The
# measured bring-up procedure it encoded is preserved in git history
# (pre-#259 revisions of this file); no executable form of it remains here,
# so nothing can start a retired daemon beside the fabric owner.
echo "RETIRED (#259): the software gPTP owner and its Linux images no longer exist;" >&2
echo "this bench script is preserved as history and refuses to run." >&2
exit 2
