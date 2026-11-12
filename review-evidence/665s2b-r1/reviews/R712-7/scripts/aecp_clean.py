"""Run the AECP core arm on the clean tree for the round's named tests.  usage: python3 -B aecp_clean.py <root> <work>"""
import sys, shutil
from pathlib import Path
root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_arms, fw_gtest
from ctrl_build import CTRL, ROOT, Tree
from aecp_mutants import STACK
src = work / 'work/ctrl'; shutil.copytree(CTRL, src, dirs_exist_ok=True)
shutil.copytree(CTRL.parent / 'ctrl_nvm', src.parent / 'ctrl_nvm', dirs_exist_ok=True)
tree = Tree(src, work / 'work/build', work / 'work/reuse', fw_gtest.Build(jobs=4), STACK)
sel = ':'.join(('Core.ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain', 'Core.ANoticeIsAddressedToEachRecipientAlone',
                'Mailbox.ANoticeWithNoRoomStaysOwed', 'Mailbox.FullTransmitRingAndCompletionQueueKeepTheirOwedResponse',
                'Mailbox.ANoticeThroughTheFanPortIsAddressedToEachRecipientAlone'))
r = aecp_arms.core_arm(tree, ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml', 2, 'app', sel)
print('\n'.join(l for l in r.log.splitlines() if l.startswith('[')))
sys.exit(r.rc)
