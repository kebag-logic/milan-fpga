# SPDX-License-Identifier: CERN-OHL-W-2.0
"""AECP planted controls: a named test must fail on its own diagnostic."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path

import aecp_arms
import fw_gtest
from ctrl_build import CTRL, ROOT, HERE, Tree, Refusal, Outcome


@dataclass(frozen=True)
class Defect:
    """One source edit and the independently required rejecting checks."""
    name: str
    path: str
    old: str
    new: str
    checks: tuple[tuple[str, str], ...]


def defect(name: str, file: str, old: str, new: str,
           check: tuple[str, str], *also: tuple[str, str]) -> Defect:
    """Keep the table's common AECP directory implicit."""
    path = file if "/" in file else "aecp/" + file
    return Defect(name, path, old, new, (check, *also))


DEFECTS = (
    defect('nosub-bypasses-running-only', 'aecp_commands.c',
           '\t\tif (info.running) {\n',
           '\t\tif ((wire_be32(in + 4) & 0xfaf80000u) == 0u && !aecp_foreign_lock(a)) {\n'
           '\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n'
           '\t\t\treturn AECP_SUCCESS;\n'
           '\t\t}\n'
           '\t\tif (info.running) {\n',
           ('Core.S1_NoSubcommandSetOnRunningOutputIsRefused',
            'STREAM_IS_RUNNING for a no-sub-command SET')),
    defect('nosub-bypasses-input-refusal', 'aecp_commands.c',
           '\t\tif (type == 5u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n',
           '\t\tif (type == 5u && (wire_be32(in + 4) & 0xfaf80000u) != 0u) {\n'
           '\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n',
           ('Core.S2_NoSubcommandSetOnInputIsNotSupported',
            'NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT')),
    defect('nosub-applies-request-latency', 'aecp_commands.c',
           '\t\tif ((requested & 0x20000000u) == 0u) {\n',
           '\t\tif ((requested & 0x20000000u) == 0u) {\n'
           '\t\t\ta->cfg.latency[index] = (uint32_t)wire_be32(in + 24); aecp_override(a, d, 2u);\n',
           ('Core.SetStreamInfoWithoutSubcommandPreservesState',
            'no subcommand preserves stored latency'),
           ('Core.SetStreamInfoWithoutSubcommandPreservesState',
            'no subcommand preserves saved override'),
           ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
            'ignored flags and no subcommand preserve latency')),
    defect('nosub-reports-request-latency', 'aecp_commands.c',
           '\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n',
           '\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4); memcpy(out + 24, in + 24, 4u);\n',
           ('Core.SetStreamInfoWithoutSubcommandPreservesState',
            'no subcommand reports current latency, not requested latency'),
           ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
            'SET latency follows Milan success and current refusal rules')),
    defect('nosub-notifies-change', 'aecp_commands.c',
           '\t\tif ((requested & 0x20000000u) == 0u) {\n',
           '\t\tif ((requested & 0x20000000u) == 0u) {\n'
           '\t\t\taecp_note(a, AECP_CHANGE_LATENCY, type, index);\n',
           ('Core.SetStreamInfoWithoutSubcommandPreservesState',
            'no subcommand emits no change notification'),
           ('Core.SetStreamInfoWithoutSubcommandPreservesState',
            'called more times than expected')),
    defect('retry-timer-lost', 'aecp.c',
           'e->retry_pending != 0u && (!armed || due(deadline, e->retry_at))',
           'e->retry_pending == 0u && (!armed || due(deadline, e->retry_at))',
           ('Core.CounterTimerArmsOnlyEligibleCompletedSnapshots',
            'Unexpected mock function call')),
    defect('entity-available-index-static', 'aecp_commands.c',
           'wire_put_be(out + 40, available, 4u);',
           '(void)available;',
           ('Core.EntityAvailableIndexUsesTheIngressObservation',
            'ENTITY reads current ADP available index'),
           ('App.EntityReadSeesTheRealAdpAdvertisementCount',
            'ENTITY sees N advertisements from the ADP owner')),
    defect('hdcp-data-length-echo', 'aecp.c',
           'wire_put_be(a->response + 36, 0u, 2);',
           'wire_put_be(a->response + 36, wire_be16(p + 22), 2);',
           ('Core.NonAemMessageTypesFollowTheirOwnContracts',
            'HDCP refusal clears data length')),
    defect('cross-instance-guard-removed', 'aecp.c',
           'port_owner != NULL || (a != NULL && a->in_port)',
           'a != NULL && a->in_port',
           ('Core.CrossInstanceInputsAreRefusedInsideRealCallbacks',
            'every cross-instance public input counts its refusal')),
    defect('unavailable-head-blocks-notices', 'aecp.c',
           'e->retry_at = a->now + 1u;',
           'e->retry_at = a->now + 1u; return true;',
           ('Core.UnavailableSnapshotsDoNotBlockIndependentNoticesOrSpin',
            'backpressure retains the built independent snapshot')),
    defect('unavailable-retry-spins', 'aecp.c',
           'e->retry_at = a->now + 1u;',
           'e->retry_at = a->now;',
           ('Core.UnavailableSnapshotsDoNotBlockIndependentNoticesOrSpin',
            'failed snapshots wait for a timed retry')),
    defect('stream-info-request-echo', 'aecp_commands.c',
           'memcpy(out + 8, d->value + 74, 8u);',
           'memcpy(out + 8, in + 8, len >= 16u ? 8u : 0u);',
           ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
            'SET response uses current format')),
    defect('stream-info-flags-echo', 'aecp_commands.c',
           'uint32_t flags = info.flags;',
           'uint32_t flags = (uint32_t)wire_be32(in + 4);',
           ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
            'SET response flags describe current state')),
    defect('stream-info-noop-refused', 'aecp_commands.c',
           '(requested & 0xdaf80000u) != 0u',
           'requested != 0x20000000u',
           ('Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal',
            'status for command')),
    defect('root-configuration-refused', 'aecp_commands.c',
           'if (type == 0u || type == 1u) {',
           'if (type == 0xffffu) {',
           ('Core.RootDescriptorConfigurationIsIgnored',
            'root descriptor ignores received configuration')),
    defect('identify-refusal-body-lost', 'aecp_commands.c',
           'memcpy(out, in, len < 4u ? len : 4u);',
           'memset(out, 0, 4u);',
           ('Core.UnsupportedAndAcquire',
            'identify refusal preserves descriptor fields')),
    defect('descriptor-last-byte', 'aecp_commands.c',
           'memcpy(out + 4, d->value, d->length);',
           'memcpy(out + 4, d->value, d->length); out[4] ^= 1u;',
           ('Core.EveryDescriptorAndReadFailures',
            'every READ_DESCRIPTOR is byte exact')),
    defect('unknown-body-lost', 'aecp_commands.c',
           'memcpy(out, in, len);',
           'memset(out, 0, len);',
           ('Core.UnsupportedAndAcquire',
            'unsupported command echoes its exact body')),
    defect('lock-long', 'aecp_commands.c',
           'a->now + 60000u',
           'a->now + 60001u',
           ('Core.LockQueriesAndExpiry',
            'lock expires at exactly sixty seconds')),
    defect('group-name-offset', 'aecp_commands.c',
           '48u + 132u * name',
           '48u + 64u * name',
           ('Core.GroupNameDoesNotOverwriteFirmwareVersion',
            'group_name changes only'),
           ('Core.NamesAndDescriptorOverlay',
            'READ_DESCRIPTOR uses the same name'),
           ('Nvm.ShapePoolsAndNameOrdinalsMatchSavedRecords',
            'b')),
    defect('scalar-refusal-reports-request', 'aecp_commands.c',
           'memcpy(out + 4, d->value + offset, width);\n\t}',
           'memcpy(out + 4, in + 4, len >= 4u + width ? width : 0u);\n\t}',
           ('Core.ScalarGetSetAndCurrentValueRefusals',
            'refused SET reports current value')),
    defect('default-is-not-override', 'aecp_commands.c',
           '!aecp_overridden(a, d, 1u) || memcmp',
           'memcmp',
           ('Core.AcceptedDefaultBecomesAnOverrideAndObservationFailureRefusesSet',
            'aecp_value_latch')),
    defect('restore-forgets-override', 'aecp_state.c',
           'aecp_override(a, d, bit);',
           '(void)bit;',
           ('Core.RestoreValuesValidateAndRollbackWithoutLiveEvents',
            'aecp_value_latch'),
           ('Nvm.ScalarRecordsUseSharedValidationAndReserveUnknownGroups',
            'owner.port.latch')),
    defect('boot-clip-boundary', 'aecp_maps.c',
           'm->rows[k].channel >= channels(wire_be64(d->value + 74))',
           'm->rows[k].channel > channels(wire_be64(d->value + 74))',
           ('Core.RestoreMapWholeSetClipAndDefaults',
            'm.count'),
           ('Nvm.AbsentMapClipsButRefusedMapRevertsItsFormat',
            'm.count')),
    defect('counter-last-word', 'aecp_commands.c',
           'n < 32u; ++n',
           'n < 31u; ++n',
           ('Core.ObservationsHaveFullWireForms',
            'coherent bank includes every counter')),
    defect('path-failure-success', 'aecp_commands.c',
           'if (!ok || count > AECP_PATH_ITEMS)',
           'if ((void)ok, count > AECP_PATH_ITEMS)',
           ('Core.ObservationRefusals',
            'status for command')),
    defect('latency-sign-accepted', 'aecp_commands.c',
           '(latency & 0x80000000u) != 0u',
           'latency == UINT32_MAX',
           ('Core.StreamInfoDirectionFlagsAndLatency',
            'status for command')),
    defect('owed-response-discarded', 'aecp.c',
           'if (a->response_owed) {',
           'if (a->response_owed && false) {',
           ('Core.BackpressureOrdersResponseBeforeNotice',
            'sent.size()')),
    defect('start-wait-ten-ms', 'aecp.c',
           'a->start_deadline = a->now + 8u;',
           'a->start_deadline = a->now + 10u;',
           ('Core.StartIsDeferredAndHasFailureDeadline',
            'sent.size()'),
           ('Latency.DeferredFailureAndTimerPathsUseTheirDueTime',
            'commits.size()')),
    defect('dynamic-unknown-status', 'aecp_commands.c',
           'status = AECP_NOT_SUPPORTED;',
           'status = AECP_SUCCESS;',
           ('Core.DynamicInfoWhitelistAndIndependentResults',
            'per-record NOT_SUPPORTED')),
    defect('registry-no-retry', 'aecp.c',
           'if (r->probing == 2u)',
           'if (r->probing == 1u)',
           ('Core.RegistryCapacityInterfaceKeysAndLiveness',
            'sent.size()')),
    defect('foreign-lock-ignored', 'aecp_commands.c',
           'return a->locked && a->lock_owner != a->requester;',
           'return a->locked && a->lock_owner == a->requester;',
           ('Core.ConfigurationAndLockedSetRefusals',
            'status for command')),
    defect('extra-name-accepted', 'aecp_commands.c',
           'return name == 0u ? 4u : 0u;',
           'return name <= 1u ? 4u : 0u;',
           ('Core.NameRefusalsAndNoOp',
            'status for command')),
    defect('identify-one-accepted', 'aecp_commands.c',
           'in[4] != 0u && in[4] != 255u',
           'in[4] > 1u && in[4] != 255u',
           ('Core.IdentifyCurrentValueAndRefusals',
            'status for command')),
    defect('clock-reserved-halfword-omitted', 'aecp_commands.c',
           'len < (set ? *bytes : 4u)',
           'len < (set ? 4u + width : 4u)',
           ('Core.ChangedScalarValuesAndDamagedLists',
            'status for command')),
    defect('dynamic-overflow-kept', 'aecp_commands.c',
           '*bytes + 8u + result_bytes <= 512u',
           '*bytes + 8u + result_bytes <= 1024u',
           ('Core.DynamicInfoSkipsOverflowAndKeepsLaterRecords',
            'out.size()')),
    defect('map-capacity-ignored', 'aecp_maps.c',
           'additions > m->capacity - m->count',
           'additions > 65535u',
           ('Core.MapsAreAtomicAndPaginated',
            'status for command')),
    defect('counter-spacing-short', 'aecp.c',
           'departure_ms + 1000u',
           'departure_ms + 999u',
           ('Core.CounterNoticesCoalesceAndWaitForEligibility',
            'sent.empty()'),
           ('Mailbox.OutputTailStartsCounterSpacingAfterAStall',
            'fabric.tx_sent')),
    defect('unsupported-events-queued', 'aecp.c',
           '(events & supported)',
           '(events | supported)',
           ('Core.FailedSnapshotRetriesAndUnsupportedEventsAreDiscarded',
            'pending')),
    defect('static-map-orphan-accepted', 'aecp_maps.c',
           'wire_be16(record) == index && wire_be16(record + 2) >= channels(format)',
           'wire_be16(record) == index && wire_be16(record + 2) > 1023u',
           ('Core.StaticMapsPreventOrphaningFormats',
            'status for command')),
    defect('output-owner-crossed', 'aecp_maps.c',
           'other->index == port->index',
           'other->index != port->index',
           ('Core.OutputMappingsHaveOneGlobalOwner',
            'another port already owns this stream channel')),
    defect('saved-latency-wrong-type', 'aecp_state.c',
           'if (v.type != 6u) return false;',
           'if (v.type != 5u && v.type != 6u) return false;',
           ('Core.SavedValuesRejectWrongFieldsAndDamagedDescriptors',
            'aecp_value_restore')),
    defect('empty-map-no-page', 'aecp_maps.c',
           'pages = 1u;',
           'pages = 0u;',
           ('Core.MapTopologyFailuresAndEmptyPartitions',
            'status for command'),
           ('Core.OutputPartitionGeometryUsesAllAdvertisedWidths',
            'status for command')),
    defect('boot-map-capacity-ignored', 'aecp_maps.c',
           'count > m->capacity) return AECP_BAD_ARGUMENTS;',
           'count > 65535u) return AECP_BAD_ARGUMENTS;',
           ('Core.BootMapFaultsCannotPartlyReplaceTheSet',
            'aecp_map_restore')),
    defect('probe-status-matters', 'aecp.c',
           'if (msg == 1u) {',
           'if (msg == 1u && (p[2] & 0xf8u) == 0u) {',
           ('Core.ProbeRepliesResetOnlyTheirOwnInterface',
            'probing')),
    defect('framing-version-ignored', 'aecp.c',
           '(p[1] & 0xf0u) != 0u',
           '(p[1] & 0xe0u) != 0u',
           ('Core.FramingRejectsInvalidIdentityAndTruncation',
            'a.malformed')),
    defect('reentry-uncounted', 'aecp.c',
           '++a->reentries;',
           '(void)a;',
           ('Core.ReentrantPortsCannotMutateState',
            'a.reentries')),
    defect('probe-sequence-ignored', 'aecp.c',
           'r->probe_sequence == wire_be16(p + 20)',
           'r->probe_sequence != UINT16_MAX',
           ('Core.ProbeIdentityAndSequenceMustBothMatch',
            'probing')),
    defect('counter-timer-during-output', 'aecp.c',
           'e->counter_sent && !e->awaiting_output &&',
           'e->counter_sent &&',
           ('Core.CounterTimerArmsOnlyEligibleCompletedSnapshots',
            'Unexpected mock function call')),
    defect('descriptor-configuration-ignored', 'aecp_commands.c',
           'd->configuration == cfg && d->type == type',
           '(void)cfg, d->type == type',
           ('Core.MetadataConfigurationKeysAndRepeatedOverrides',
            'status for command')),
    defect('map-cluster-channel-ignored', 'aecp_maps.c',
           'a->cluster_channel == b->cluster_channel;',
           '((void)a->cluster_channel, true);',
           ('Core.MapsCompareEveryCoordinateAndBothDirectionsOnRestore',
            'a distinct cluster channel is a distinct input key')),
    defect('no-interface-accepted', 'aecp.c',
           'cfg->interfaces == 0u ||',
           '',
           ('Core.InitRefusalsAndClosedService',
            'aecp_init')),
    defect('system-id-write-lost', 'aecp.c',
           'a->system_id = wire_be64(p + 32);',
           'a->system_id = 0;',
           ('Core.MilanVendorCommandsAndRefusals',
            'get(out,46,8)')),
    defect('completion-cookie-ignored', 'aecp.c',
           'e->cookie == cookie',
           '(e->cookie != UINT32_MAX || cookie == UINT32_MAX)',
           ('Core.NotificationBackpressureAndLatestCompletion',
            'an old completion cannot release a newer copy')),
    defect('stream-interface-bound-ignored', 'aecp_commands.c',
           'if (interface >= a->cfg.interfaces)',
           'if (interface > 65535u)',
           ('Core.DescriptorAndObservationBoundaryFailures',
            'status for command')),
    defect('nvm-hole-accepted', 'aecp_nvm.c',
           'if (unused) return refused(n, m);',
           'if (unused && false) return refused(n, m);',
           ('Nvm.WholeMapFramingAndEmptySetAreDistinct',
            'owner.port.apply')),
    defect('nvm-latency-dirty-lost', 'aecp_nvm.c',
           'mark(n, NVM_G_PTOF, index);',
           '(void)index;',
           ('Nvm.AcceptedStateSurvivesTheRealStorePowerCycle',
            'owner.port.latch'),
           ('Nvm.EveryChangeQueuesOnlyItsOwnedRecords',
            'owner.pending')),
    defect('nvm-partial-latch-writes', 'aecp_nvm.c',
           'len != m->capacity * 8u) return 0;',
           'len > m->capacity * 8u) return 0;',
           ('Nvm.MapRecordsRefuseMissingStorageAndNeverPartiallyLatch',
            'owner.port.latch')),
    defect('app-start-inverted', 'app/ctrl_app_aecp.c',
           'c->start_value = value;',
           'c->start_value = !value;',
           ('App.DeferredStartAndLockUseTheRealAcmpOwner',
            'v.started')),
    defect('app-notice-overtakes-unbind', 'app/ctrl_app_aecp.c',
           'if (acmp_change_pending(a, n)) pending = true;',
           'if (false) pending = true;',
           ('App.MediaUnlockedNoticeCannotPassAnOwedUnbindResponse',
            'response) < (notice')),
    defect('app-write-owner-lost', 'app/ctrl_app_aecp.c',
           'aecp_nvm_changed(c->state, kind, type, index);',
           '(void)c->state;',
           ('App.PhysicalObservationsAndAcceptedWritesRetainTheirOwner',
            'nvm_store_status()->dirty')),
    defect('app-failure-flags-lost', 'app/ctrl_app_aecp.c',
           's.registering_failed ? 0x08000040u : 0u',
           's.registering_failed ? 0u : 0u',
           ('App.InputInfoReflectsAcmpSettlementAndFailures',
            'v.flags')),
    defect('app-poll-space-short', 'app/ctrl_app_aecp.c',
           'app->loop.n_polls + 2u > CTRL_LOOP_MAX_POLLS',
           'app->loop.n_polls + 1u > CTRL_LOOP_MAX_POLLS',
           ('App.CompositionRefusalsLeaveExistingBindingsIntact',
            'ctrl_app_compose_aecp')),
    defect('app-expired-start-applies', 'app/ctrl_app_aecp.c',
           'if (c->aecp->core.start_pending) {',
           'if (true) {',
           ('App.ExpiredAndMissingStartRequestsCannotApplyLate',
            'sinks[0].started')),
    defect('app-unbound-start-refused', 'app/ctrl_app_aecp.c',
           '(!old.bound || acmp_set_started(a, c->start_index, c->start_value))',
           'acmp_set_started(a, c->start_index, c->start_value)',
           ('App.UnboundStartAndStopAreSuccessfulNoOps',
            'get(p->bytes+16,2)>>11')),
    defect('mailbox-interface-crossed', 'aecp_mbx.c',
           'aecp_rx(&m->core, f->interface, f->bytes, f->len);',
           'aecp_rx(&m->core, 0, f->bytes, f->len);',
           ('Mailbox.EveryInterfaceAndObservationPort',
            'fabric.tx_sent')),
    defect('mailbox-stale-tag-accepted', 'aecp_mbx.c',
           'e->timer_tag != m->tag',
           'e->timer_tag == m->tag',
           ('Mailbox.TimerIdentityAndAttachRefusals',
            'adapter.stale_expiries')),
    defect('mailbox-full-completions-overwritten', 'aecp_mbx.c',
           'm->completion_count == AECP_MBX_COMPLETIONS ||',
           'm->completion_count > AECP_MBX_COMPLETIONS ||',
           ('Mailbox.FullTransmitRingAndCompletionQueueKeepTheirOwedResponse',
            'adapter.ports.send')),
    defect('latency-response-missing', 'aecp_commands.c',
           'case 4: return descriptor(a, interface, in, len, out, bytes);',
           'case 4: a->start_pending = true; return descriptor(a, interface, in, len, out, bytes);',
           ('Latency.EveryCommandAndRefusalUsesOneArrivalBudget',
            'commits.size()')),
    defect('latency-budget-relaxed', 'test/aecp_latency_policy.hpp',
           '10000000;',
           '20000000;',
           ('Latency.NotificationFanoutAndStallsRetainTheirOriginalOrigin',
            'late output cannot restart the service clock')),
    defect('image-byte-corrupted', 'aecp_image.c',
           'memcpy(values + used, body, length);',
           'memcpy(values + used, body, length); values[used] ^= 1u;',
           ('Image.EveryDescriptor',
            'descriptor defaults survive the image load')),
    defect('image-crc-ignored', 'aecp_image.c',
           'crc32(image, bytes) == expected_crc',
           '(crc32(image, bytes) == expected_crc || true)',
           ('Image.RejectHeader',
            'image CRC rejects corrupted descriptor bytes')),
    defect('image-type-ignored', 'aecp_image.c',
           'wire_be16(body) != type ||',
           'wire_be16(body) == 0xfffeu ||',
           ('Image.RejectDirectory',
            'invalid descriptor directory is refused at its boundary')),
    defect('debug-guard-silent', 'aecp.c',
           'ctrl_reentry_assert("aecp");',
           '(void)a;',
           ('AecpDebug.EveryInputRejectsSynchronousPortDelivery',
            'died but not with expected exit code')),
)


def caught(test: str, words: str, result: Outcome) -> bool:
    """Require a completed failure and this test's full assertion diagnostic."""
    if result.rc != 1 or "verdict: FAIL (its tallies report" not in result.log:
        return False
    match = re.search(r"\[ RUN      \] " + re.escape(test) + r"\n(.*?)\[  FAILED  \] " +
                      re.escape(test) + r" \(", result.log, re.S)
    return match is not None and words in match[1]


def controls() -> None:
    """Refuse unowned checks and prove the diagnostic reader cannot grade a crash."""
    expected = set()
    for name in ("test_aecp.cpp", "test_aecp_image.cpp", "test_aecp_debug.cpp"):
        expected.update(a + "." + b for a, b in
                        re.findall(r"TEST(?:_F)?\((\w+),\s*(\w+)\)", (HERE / name).read_text()))
    claimed = {test for d in DEFECTS for test, _ in d.checks}
    if claimed != expected or len({d.name for d in DEFECTS}) != len(DEFECTS):
        raise Refusal(f"AECP plant table drift: missing={expected-claimed}, extra={claimed-expected}")
    log = ("[ RUN      ] Fixture.Check\nnamed failure\n[  FAILED  ] Fixture.Check (0 ms)\n"
           "verdict: FAIL (its tallies report 1 failure(s) across 1 checks, exit 1)")
    result = Outcome("reader", 1, log)
    assert caught("Fixture.Check", "named failure", result)
    assert not caught("Fixture.Other", "named failure", result)
    assert not caught("Fixture.Check", "other failure", result)
    assert not caught("Fixture.Check", "named failure", Outcome("reader", 0, log))
    assert not caught("Fixture.Check", "named failure", Outcome("reader", 1, log.split("verdict:")[0]))


def campaign(root: Path, jobs: int = 4, shard: tuple[int, int] = (0, 1)) -> bool:
    """Reuse one isolated copy; compile failures and missing diagnoses are escapes."""
    controls()
    root.mkdir(parents=True, exist_ok=True)
    src = root / "work/ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    tree = Tree(src, root / "work/build", root / "work/reuse", fw_gtest.Build(jobs=jobs))
    config = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
    receipts = []
    for d in DEFECTS[shard[0]::shard[1]]:
        target = src / d.path
        original = target.read_text()
        if original.count(d.old) != 1:
            raise Refusal(f"{d.name}: expected one planting site, got {original.count(d.old)}")
        target.write_text(original.replace(d.old, d.new))
        try:
            selected = ":".join(test for test, _ in d.checks)
            if d.checks[0][0].startswith("Image."):
                result = aecp_arms.image_arm(tree, config)
            else:
                debug = d.checks[0][0].startswith("AecpDebug.")
                result = aecp_arms.core_arm(tree, config, 2, "debug" if debug else "app", selected)
            ok = all(caught(test, words, result) for test, words in d.checks)
            (root / (d.name + ".log")).write_text(result.log)
        except Refusal as error:
            ok = False
            (root / (d.name + ".log")).write_text(str(error))
        finally:
            target.write_text(original)
        receipts.append({**asdict(d), "caught": ok})
        (root / "results.json").write_text(json.dumps(receipts, indent=2) + "\n")
        print(f"[{'ok' if ok else 'ESCAPED'}] {d.name}: {selected}", flush=True)
    return any(not r["caught"] for r in receipts)


def main() -> int:
    """A foreground-sized partition of the same table the firmware bank uses."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shard", type=int, nargs=2, default=(0, 1))
    args = parser.parse_args()
    if not 0 <= args.shard[0] < args.shard[1]:
        parser.error("shard requires 0 <= index < count")
    return int(campaign(args.output, shard=args.shard))


if __name__ == "__main__":
    raise SystemExit(main())
