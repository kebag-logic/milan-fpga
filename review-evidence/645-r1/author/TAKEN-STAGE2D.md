[A531] TAKEN
Branch: 645-ring-slip
Head: 535a710d3be73764fd0c951953565f462812bce8
Authoritative references: stage-2d ruling https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990646410; #645, #647 and the media-clock design.
Interpreted scope: merge dev fa450d30 with --no-ff, then grade the declared settle recentre at its decision PDU with both planted ordering controls, preserve all existing checks, and update the declared-discontinuity documentation.
Validation plan: rerun physical/accounting gPTP, arrival and INTERNAL campaigns, controls, full datapath/render/media-clock suites, builder, portability, source gates and the build-defined timing signoff at the merged head.
Blockers: none identified during initial verification; timing failures trigger STOP as ruled. No push.
