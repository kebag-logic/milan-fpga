#!/usr/bin/env python3
"""Round-2 reviewer mutants re-anchored to the round-3 source, plus verdict-metadata mutants.

usage: r3_extra.py <planner.py>   (same KILLED / CRASH-ONLY / SURVIVED rules as r3_mutants.py)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
M = [
 # round-2 C10/C20/C21/C15/C17/C18/C19 re-anchored (limit is now a named constant)
 ("C10r history accepts negative resolution", "or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):", "or not observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):"),
 ("C20r history limit admits equality", "or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):", "or not 0 <= observation_resolution_s <= RELEASE_TU_RESOLUTION_LIMIT_S):"),
 ("C21r history limit relaxed to 0.5", "or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):", "or not 0 <= observation_resolution_s < 0.5):"),
 ("C15r single tu limit from 0.5 s only", "    resolution_limit_s = RELEASE_TU_RESOLUTION_LIMIT_S\n", "    resolution_limit_s = 0.5\n"),
 ("C17r single tu verdict omits limit", "              \"resolution_limit_s\": resolution_limit_s}\n", "              }\n"),
 ("C18r mr verdict omits limit", "              \"resolution_limit_s\": resolution_limit_s,\n", ""),
 ("C19r history verdict omits limit", "              \"resolution_limit_s\": RELEASE_TU_RESOLUTION_LIMIT_S}", "              }"),
 # round-2 text mutants whose short anchors now collide with test phrases: full literal anchors
 ("T20r mr text 8 -> 7 AVTPDUs", "\"hold each new value for at least 8 AVTPDUs of that stream; \"", "\"hold each new value for at least 7 AVTPDUs of that stream; \""),
 ("T21r mr text window one-sided", "\"match causes within +/- observation_resolution_s of the toggle; \"", "\"match causes within observation_resolution_s after the toggle; \""),
 ("T22r tu text 0.25 -> 0.2", "\"GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity \"", "\"GM change + 0.2 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity \""),
 ("T24r mr text GM alone passes", "\"mapped to that stream's clock source; GM change alone fails; \"", "\"mapped to that stream's clock source; GM change alone passes; \""),
 # verdict-metadata ("Resolution appears in every timing verdict"; "every NOT RUN verdict records resolution_limit_s")
 ("V01 mr inner NOT RUN/FAIL returns evidence only", "    verdict, evidence = _release_mr_toggles(stream_pdus, stream_causes, observation_resolution_s)\n    detail.update(evidence)\n    if verdict != \"PASS\":\n        return verdict, detail", "    verdict, evidence = _release_mr_toggles(stream_pdus, stream_causes, observation_resolution_s)\n    detail.update(evidence)\n    if verdict != \"PASS\":\n        return verdict, evidence"),
 ("V02 mr media-reset verdict returns evidence only", "    verdict, evidence = _release_media_resets(reads, detail[\"toggles_s\"], observation_resolution_s)\n    detail.update(evidence)\n    return verdict, detail", "    verdict, evidence = _release_media_resets(reads, detail[\"toggles_s\"], observation_resolution_s)\n    detail.update(evidence)\n    return verdict, evidence"),
 ("V03 mr baseline-read NOT RUN drops detail", "        return \"NOT RUN\", dict(detail, why=\"MEDIA_RESET baseline and endpoint reads required\")", "        return \"NOT RUN\", dict(why=\"MEDIA_RESET baseline and endpoint reads required\")"),
 ("V04 mr capture-span NOT RUN drops detail", "        return \"NOT RUN\", dict(detail, why=\"capture does not span the counter-read window and PDUs\")", "        return \"NOT RUN\", dict(why=\"capture does not span the counter-read window and PDUs\")"),
 ("V05 mr invalid-record NOT RUN drops detail", "        return \"NOT RUN\", dict(detail, why=\"invalid recorded evidence\")", "        return \"NOT RUN\", dict(why=\"invalid recorded evidence\")"),
 ("V06 tu uncorrelated FAIL drops detail", "return \"FAIL\", {\"why\": \"uncorrelated tu fails\", **detail}", "return \"FAIL\", {\"why\": \"uncorrelated tu fails\"}"),
 ("V07 tu rise FAIL drops detail", "        return \"FAIL\", dict(detail, why=\"tu rises before its first recorded discontinuity\")", "        return \"FAIL\", dict(why=\"tu rises before its first recorded discontinuity\")"),
 ("V08 tu minimum FAIL drops detail", "        return \"FAIL\", dict(detail, why=\"tu shorter than the GM minimum\")", "        return \"FAIL\", dict(why=\"tu shorter than the GM minimum\")"),
 ("V09 tu upper verdict drops detail", "    return (\"PASS\" if latest_clear_s <= deadline_s else \"FAIL\", detail)", "    return (\"PASS\" if latest_clear_s <= deadline_s else \"FAIL\", {})"),
 ("V10 history uncovered-GM FAIL drops detail", "return \"FAIL\", dict(detail, why=\"GM change lacks a covering tu minimum\", gm_change_s=event)", "return \"FAIL\", dict(why=\"GM change lacks a covering tu minimum\", gm_change_s=event)"),
 ("V11 history PASS drops detail", "    return \"PASS\", dict(detail, intervals=len(intervals), gm_changes=len(gm_changes_s))", "    return \"PASS\", dict(intervals=len(intervals), gm_changes=len(gm_changes_s))"),
 ("V12 history finite-event NOT RUN drops detail", "        return \"NOT RUN\", dict(detail, why=\"finite event history required\")", "        return \"NOT RUN\", dict(why=\"finite event history required\")"),
 ("V13 single finite NOT RUN drops detail", "        return \"NOT RUN\", dict(detail, why=\"finite interval, events and resolution required\")", "        return \"NOT RUN\", dict(why=\"finite interval, events and resolution required\")"),
]
r3 = importlib.import_module("r3_mutants")
r3.M = M
r3.main()
