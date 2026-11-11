#!/usr/bin/env python3
"""Reviewer probes for PR #881 (issue #871): planted defects in the firmware's REBOOT code that the
author's tables do not plant, and one behaviour probe, each built and run by the repository's own arms.

    python3 -B fw_probes.py PROBE_CLONE OUT_DIR [NAME ...]

PROBE_CLONE is a disposable clone of the exact head with its tsn-c-stack and lwSRP submodules. Each
probe edits that clone, runs one arm, records which tests failed with which words, and restores the
file byte for byte. Results go to OUT_DIR/results.json and one log per probe.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
ONLY = set(sys.argv[3:])
TEST = CLONE / 'sw/firmware/ctrl/test'
sys.path.insert(0, str(TEST))
sys.path.insert(0, str(CLONE / 'sw/firmware/gtest'))

import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import CTRL, STACK, Refusal, Tree  # noqa: E402

AECP = 'sw/firmware/ctrl/aecp/aecp.c'
CMDS = 'sw/firmware/ctrl/aecp/aecp_commands.c'
PLAT = 'sw/firmware/ctrl/plat/ctrl_plat.c'
BOOT_TEST = 'sw/firmware/ctrl/test/test_plat_boot.cpp'

#: The behaviour probe: an ACMP command that reaches the mailbox after the REBOOT's SUCCESS has left, and
#: before the reset port fires. The processor takes no command after the SUCCESS and sends nothing after the
#: final ENTITY_DEPARTING (protocol-processor 06_aecp_engine.md 6.11, REQ-FWX-001). Each EXPECT states the
#: processor's behaviour; a failure records where the split's firmware differs.
PROBE_TEST = r'''
TEST_F(Boot, ReviewProbeAcmpAfterTheRebootSuccess) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    const std::size_t from = frames.size();
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 500 && aecp_frames(from, 42).empty(); ++k) pass_ms();
    ASSERT_EQ(aecp_frames(from, 42).size(), 1u) << "PROBE the SUCCESS has left";
    ASSERT_TRUE(reboot_writes().empty()) << "PROBE the port has not fired yet";
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0));
    const std::size_t sent_from = frames.size();
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    ASSERT_EQ(reboot_writes().size(), 1u) << "PROBE the port fires";
    acmp_sink_view sink{};
    ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, 0, &sink));
    EXPECT_FALSE(sink.bound) << "PROBE a BIND_RX after the REBOOT's SUCCESS is not applied";
    std::size_t acmp = 0, first_departing = frames.size(), after_departing = 0;
    for (std::size_t k = sent_from; k < frames.size(); ++k) {
        const auto& f = frames[k].frame;
        if (f.channel == MBX_CH_ACMP) ++acmp;
        if (f.channel == MBX_CH_ADP && (f.bytes[15] & 0x0fu) == 1u && first_departing == frames.size())
            first_departing = k;
    }
    for (std::size_t k = first_departing; k < frames.size(); ++k)
        if (frames[k].frame.channel != MBX_CH_ADP) ++after_departing;
    EXPECT_EQ(acmp, 0u) << "PROBE a BIND_RX after the REBOOT's SUCCESS is not answered";
    EXPECT_EQ(after_departing, 0u) << "PROBE no frame but ADP's leaves after ENTITY_DEPARTING";
    std::printf("PROBE-OBSERVED acmp_frames_after_success=%zu sink_bound=%d frames_after_departing=%zu "
                "first_departing_index=%zu total_frames=%zu\n", acmp, int(sink.bound), after_departing,
                first_departing - sent_from, frames.size() - sent_from);
}

// The same command once ENTITY_DEPARTING has left the mailbox, if the port has not fired by then: whatever
// it makes the entity send leaves after the DEPARTING.
TEST_F(Boot, ReviewProbeAcmpAfterTheDeparting) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    const std::size_t from = frames.size();
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 500 && departing(from).empty() && reboot_writes().empty(); ++k) pass_ms();
    const bool window = !departing(from).empty() && reboot_writes().empty();
    std::printf("PROBE-OBSERVED departing_left_before_the_port=%d\n", int(window));
    if (!window) return;
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0));
    const std::size_t sent_from = frames.size();
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    std::size_t acmp = 0;
    for (std::size_t k = sent_from; k < frames.size(); ++k) acmp += frames[k].frame.channel == MBX_CH_ACMP;
    EXPECT_EQ(acmp, 0u) << "PROBE no frame but ADP's leaves after ENTITY_DEPARTING";
    std::printf("PROBE-OBSERVED acmp_frames_after_departing=%zu port_writes=%zu\n", acmp, reboot_writes().size());
}
'''

#: The end of the last REBOOT test, where the behaviour probe is appended
B18_END = ('    for (const auto* d : gone) EXPECT_LE(d->plat, writes[0]) << "B18 ENTITY_DEPARTING leaves before the '
           'reset";\n}\n')

#: name -> (file, old, new, arm, the test that should fail, the words it should fail on)
PROBES = {
    'end-one-early': (AECP, '\t\t\ta->reboot_end = a->tx_cookie;\n', '\t\t\ta->reboot_end = a->tx_cookie - 1u;\n',
                      'aecp', 'Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete',
                      'not due before the notification has left'),
    'older-completion-moves-back': (AECP, '\tif (ahead != 0u && ahead < 0x80000000u) {\n',
                                    '\tif (ahead != 0u) {\n', 'aecp',
                                    'Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete',
                                    'an older completion does not hold the reset back'),
    'due-without-the-reentry-guard': (AECP, '\treturn aecp_enter(a) && a->reboot == 2u &&',
                                      '\treturn a->reboot == 2u &&', 'aecp',
                                      'Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete',
                                      "a port's call cannot read the release"),
    'lock-before-the-index': (CMDS,
                              '\tif (wire_be16(in + 2) != 0u) {\n\t\treturn AECP_NO_SUCH_DESCRIPTOR;\n\t}\n'
                              '\tif (aecp_foreign_lock(a)) {\n\t\treturn AECP_ENTITY_LOCKED;\n\t}\n',
                              '\tif (aecp_foreign_lock(a)) {\n\t\treturn AECP_ENTITY_LOCKED;\n\t}\n'
                              '\tif (wire_be16(in + 2) != 0u) {\n\t\treturn AECP_NO_SUCH_DESCRIPTOR;\n\t}\n',
                              'aecp', 'Core.RebootRefusalsLeaveTheEntityInService', ''),
    'refusing-ignored': (CMDS, '\tif (aecp_foreign_lock(a)) {\n\t\treturn AECP_ENTITY_LOCKED;\n\t}\n\ta->notify = true;\n',
                         '\tif (aecp_other_lock(a)) {\n\t\treturn AECP_ENTITY_LOCKED;\n\t}\n\ta->notify = true;\n',
                         'aecp', 'Core.RebootRefusalsLeaveTheEntityInService',
                         'ENTITY_MISBEHAVING while a change waits for the platform'),
    'quiet-without-the-face-poll': (PLAT, '\t(void)aecp_face_poll(&p->face);\n\t(void)ctrl_plat_console_poll(&p->console);\n}\n',
                                    '\t(void)ctrl_plat_console_poll(&p->console);\n}\n', 'platboot',
                                    'Boot.B16ARebootDuringTheJournalWriteKeepsTheChange',
                                    'the drain ends because the write completed'),
    'drained-reads-the-aecp-ring': (PLAT, 'MBX_CH_BASE + MBX_CH_ADP * MBX_CH_STRIDE;\n\treturn',
                                    'MBX_CH_BASE + MBX_CH_AECP * MBX_CH_STRIDE;\n\treturn', 'platboot',
                                    'Boot.B12TheResetWaitsForTheResponseToLeave',
                                    'no reset while the mailbox holds ENTITY_DEPARTING'),
    'shutdown-before-due': (PLAT, '\t\tif (!aecp_reboot_due(&p->aecp.core)) {\n',
                            '\t\tif (p->aecp.core.reboot == 0u) {\n', 'platboot',
                            'Boot.B12TheResetWaitsForTheResponseToLeave', 'nor is ADP shut down'),
    'behaviour-acmp-after-success': (BOOT_TEST, B18_END, B18_END + PROBE_TEST,
                                     'platboot', 'Boot.ReviewProbeAcmpAfterTheRebootSuccess', ''),
}


def run_arm(arm: str, tree: Tree, selected: str):
    if arm == 'aecp':
        config = CLONE / 'configs/endstation_ax7101_1x1_tdm8.yaml'
        return aecp_arms.core_arm(tree, config, 2, 'app', selected)
    return plat_arms.arm_platboot(tree, 1)


def failed(log: str) -> list[str]:
    return [ln.strip() for ln in log.splitlines() if '[FAIL]' in ln]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for name, (rel, old, new, arm, test, words) in PROBES.items():
        if ONLY and name not in ONLY:
            continue
        target = CLONE / rel
        original = target.read_bytes()
        text = original.decode()
        if text.count(old) != 1:
            results.append({'name': name, 'error': f'anchor occurs {text.count(old)} times'})
            continue
        target.write_text(text.replace(old, new, 1))
        try:
            tree = Tree(CTRL, OUT / 'build' / name, OUT / 'reuse', fw_gtest.Build(jobs=4), STACK)
            outcome = run_arm(arm, tree, test.split('.', 1)[0] + '.*' if arm == 'aecp' else '*')
            log = outcome.log
            rc = outcome.rc
        except Refusal as exc:
            log, rc = f'REFUSED: {exc}', 2
        finally:
            target.write_bytes(original)
        (OUT / f'{name}.log').write_text(log)
        fails = failed(log)
        hit = [f for f in fails if test in f and words in f]
        observed = re.findall(r'PROBE-OBSERVED .*', log)
        results.append({'name': name, 'file': rel, 'arm': arm, 'rc': rc, 'expected_test': test,
                        'expected_words': words, 'caught_by_expected': bool(hit), 'fail_lines': fails[:40],
                        'observed': observed})
        print(f'{name}: rc={rc} caught_by_expected={bool(hit)} fails={len(fails)} {observed}', flush=True)
    (OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
