The ruling's report item: whether a declared Talker Advertise or Listener Ready is declared again after a link
bounce. A disposable tb/srp_top group `streamlink` (streamlink.tb.patch; applied to a scratch copy of the tree only,
never committed): DECLARE_TALKER source 0 on VID 2, DECLARE_LISTENER sink 0 on a peer Talker Advertise that
registers, 3 s, then the link down for 30 ms and up; case 1 the peer sends nothing after it, case 2 it declares its
Talker Advertise again 100 ms after LINK_UP. The group prints each value's messages from every MRPDU after LINK_UP.

probe.log is the run on the working tree whose hdl/ and tb/ equal the head's (before the commits);
head/probe.log is the same patch on a clean clone of the head 84f6d6a (identical output expected and recorded).
Findings (HANDOFF "Stream Applicants across a link bounce"): the Talker Advertise is not declared again with New
(JoinMt at the next periodic!, 872 ms after LINK_UP); the Listener Ready is withdrawn (Lv) with its sink
registration and declared again, New, New, JoinMt, once the peer's Talker Advertise registers again. Not changed.
