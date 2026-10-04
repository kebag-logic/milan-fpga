// Lane B11 (#653, new): a minimal controller probe on the bench's la_avdecc 4.3.1 build.
// One process, two local controller entities on the same AVB interface:
//   * the session: la::avdecc::controller::Controller (the library's high-level controller,
//     the one a controller application uses). It enumerates the DUT and the reference peer,
//     registers for their unsolicited notifications (the library does this on enumeration),
//     tracks their models, and reports through its Observer: Milan compatibility changes
//     (with the library's clause and message), diagnostics, counters, connection changes.
//     Every bind and unbind goes through it (connectStream / disconnectStream).
//   * the aux entity: a low-level ControllerEntity (another ProgID). It reads the talker's and
//     the listener's current stream format live before each bind (the binding rule), and sends
//     the control cycle's own GET_COUNTERS before the unbind. It never binds, never sets.
// The only command that writes is SET_STREAM_FORMAT on the LISTENER (the DUT's STREAM_INPUT),
// sent only if the live formats differ; the talker is never changed.
// At quit the session is destroyed, then a short-lived entity with the session's ProgID sends
// DEREGISTER_UNSOLICITED_NOTIFICATION to both entities if its EntityID equals the session's.
//
// usage: o653_probe <iface> <dut_eid> <peer_eid> <session_progid> <aux_progid>
// stdin, one command per line:
//   cycle <tag> <talker_out_idx> <listener_in_idx> <ctl 0|1> <hold_ms> <post_ms> <lock_timeout_ms>
//   state
//   quit
// stdout: one JSON object per line, each with "t" (this host's system clock, microseconds).
#include <la/avdecc/avdecc.hpp>
#include <la/avdecc/controller/avdeccController.hpp>
#include <la/avdecc/executor.hpp>

#include <array>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <set>
#include <sstream>
#include <string>
#include <thread>

using namespace std::chrono;
namespace la_ctl = la::avdecc::controller;
namespace la_ent = la::avdecc::entity;
namespace la_em = la::avdecc::entity::model;
using SICF = la_ent::StreamInputCounterValidFlag;
using CF = la_ctl::ControlledEntity::CompatibilityFlag;

static std::mutex g_out;
static std::uint64_t DUT = 0, PEER = 0;

static long long nowUs()
{
	return duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
}

static std::string esc(std::string const& s)
{
	std::string o;
	for (unsigned char c : s)
	{
		if (c == '"' || c == '\\')
		{
			o += '\\';
			o += static_cast<char>(c);
		}
		else if (c < 0x20)
		{
			char b[8];
			std::snprintf(b, sizeof(b), "\\u%04x", c);
			o += b;
		}
		else
			o += static_cast<char>(c);
	}
	return o;
}

static std::string hex64(std::uint64_t v)
{
	char b[24];
	std::snprintf(b, sizeof(b), "%016llx", static_cast<unsigned long long>(v));
	return b;
}

// The library's status strings read "Success." for success
static bool isOk(std::string const& s)
{
	return s.rfind("Success", 0) == 0;
}

static void emit(std::string const& body)
{
	std::lock_guard<std::mutex> l(g_out);
	std::printf("{\"t\":%lld,%s}\n", nowUs(), body.c_str());
	std::fflush(stdout);
}

static std::string who(std::uint64_t eid)
{
	return eid == DUT ? "dut" : eid == PEER ? "peer" : hex64(eid);
}

static std::string flagsStr(la_ctl::ControlledEntity::CompatibilityFlags const f)
{
	std::ostringstream o;
	o << "\"compat\":\"0x" << std::hex << static_cast<unsigned>(f.value()) << std::dec << "\",\"compat_names\":\"";
	bool first = true;
	for (auto const& [flag, name] : std::initializer_list<std::pair<CF, char const*>>{ { CF::IEEE17221, "IEEE17221" }, { CF::Milan, "Milan" }, { CF::IEEE17221Warning, "IEEE17221Warning" }, { CF::MilanWarning, "MilanWarning" }, { CF::Misbehaving, "Misbehaving" } })
	{
		if (f.test(flag))
		{
			o << (first ? "" : "|") << name;
			first = false;
		}
	}
	o << "\"";
	return o.str();
}

static char const* connName(la_em::StreamInputConnectionInfo::State const s)
{
	switch (s)
	{
		case la_em::StreamInputConnectionInfo::State::NotConnected:
			return "NotConnected";
		case la_em::StreamInputConnectionInfo::State::FastConnecting:
			return "FastConnecting";
		case la_em::StreamInputConnectionInfo::State::Connected:
			return "Connected";
	}
	return "?";
}

static std::array<std::pair<SICF, char const*>, 12> const kCtr{ { { SICF::MediaLocked, "ML" }, { SICF::MediaUnlocked, "MU" }, { SICF::StreamInterrupted, "SI" }, { SICF::SeqNumMismatch, "SEQ" }, { SICF::MediaReset, "MRST" }, { SICF::TimestampUncertain, "TU" }, { SICF::TimestampValid, "TSV" }, { SICF::TimestampNotValid, "TSNV" }, { SICF::UnsupportedFormat, "UF" }, { SICF::LateTimestamp, "LATE" }, { SICF::EarlyTimestamp, "EARLY" }, { SICF::FramesRx, "FRX" } } };

static std::string ctrJson(la_em::StreamInputCounters const& c)
{
	std::ostringstream o;
	o << "{";
	bool first = true;
	for (auto const& [flag, name] : kCtr)
	{
		auto it = c.find(flag);
		if (it == c.end())
			continue;
		o << (first ? "" : ",") << "\"" << name << "\":" << it->second;
		first = false;
	}
	o << "}";
	return o.str();
}

static std::uint32_t ctrGet(la_em::StreamInputCounters const& c, SICF f)
{
	auto it = c.find(f);
	return it == c.end() ? 0xffffffffu : it->second;
}

static std::string eventsJson(la_ctl::ControlledEntity const& e, size_t from)
{
	auto const& ev = e.getCompatibilityChangedEvents();
	std::ostringstream o;
	o << "[";
	for (size_t i = from; i < ev.size(); ++i)
	{
		auto const& x = ev[i];
		o << (i == from ? "" : ",") << "{\"i\":" << i << ",\"prev\":\"0x" << std::hex << static_cast<unsigned>(x.previousFlags.value()) << "\",\"new\":\"0x" << static_cast<unsigned>(x.newFlags.value()) << std::dec << "\",\"prev_milan\":" << x.previousMilanVersion.getValue() << ",\"new_milan\":" << x.newMilanVersion.getValue() << ",\"clause\":\"" << esc(x.specClause) << "\",\"msg\":\"" << esc(x.message) << "\",\"ts_us\":" << duration_cast<microseconds>(x.timestamp.time_since_epoch()).count() << "}";
	}
	o << "]";
	return o.str();
}

static std::string diagJson(la_ctl::ControlledEntity::Diagnostics const& d)
{
	std::ostringstream o;
	o << "{\"redundancyWarning\":" << (d.redundancyWarning ? "true" : "false") << ",\"controlOutOfBounds\":" << d.controlCurrentValueOutOfBounds.size() << ",\"streamInputOverLatency\":[";
	bool first = true;
	for (auto const i : d.streamInputOverLatency)
	{
		o << (first ? "" : ",") << i;
		first = false;
	}
	o << "]}";
	return o.str();
}

// State shared between the library's callbacks and the command loop
struct Shared
{
	std::mutex m;
	std::condition_variable cv;
	std::set<std::uint64_t> online{};
	std::set<std::uint64_t> auxOnline{};
	std::map<std::uint16_t, std::array<std::uint32_t, 2>> dutCtr{}; // STREAM_INPUT index -> (ML, MU) last reported by the library
	std::map<std::uint16_t, int> dutCtrUpdates{};
};
static Shared S;

class Obs final : public la_ctl::Controller::DefaultedObserver
{
	bool mine(la_ctl::ControlledEntity const* e) const
	{
		auto const v = e->getEntity().getEntityID().getValue();
		return v == DUT || v == PEER;
	}
	std::string w(la_ctl::ControlledEntity const* e) const
	{
		return who(e->getEntity().getEntityID().getValue());
	}

public:
	void onTransportError(la_ctl::Controller const*) noexcept override
	{
		emit("\"ev\":\"transport_error\"");
	}
	void onEntityQueryError(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_ctl::Controller::QueryCommandError const err) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"query_error\",\"who\":\"" + w(e) + "\",\"error\":" + std::to_string(static_cast<int>(err)));
	}
	void onEntityOnline(la_ctl::Controller const*, la_ctl::ControlledEntity const* e) noexcept override
	{
		if (!mine(e))
			return;
		std::ostringstream o;
		o << "\"ev\":\"online\",\"who\":\"" << w(e) << "\"," << flagsStr(e->getCompatibilityFlags()) << ",\"milan\":" << e->getMilanCompatibilityVersion().getValue() << ",\"subscribed\":" << (e->isSubscribedToUnsolicitedNotifications() ? "true" : "false") << ",\"unsol_supported\":" << (e->areUnsolicitedNotificationsSupported() ? "true" : "false") << ",\"events\":" << eventsJson(*e, 0) << ",\"diag\":" << diagJson(e->getDiagnostics());
		emit(o.str());
		{
			std::lock_guard<std::mutex> l(S.m);
			S.online.insert(e->getEntity().getEntityID().getValue());
		}
		S.cv.notify_all();
	}
	void onEntityOffline(la_ctl::Controller const*, la_ctl::ControlledEntity const* e) noexcept override
	{
		if (!mine(e))
			return;
		emit("\"ev\":\"offline\",\"who\":\"" + w(e) + "\"");
		{
			std::lock_guard<std::mutex> l(S.m);
			S.online.erase(e->getEntity().getEntityID().getValue());
		}
		S.cv.notify_all();
	}
	void onUnsolicitedRegistrationChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, bool const sub, bool const byEntity) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"unsol_registration\",\"who\":\"" + w(e) + "\",\"subscribed\":" + (sub ? "true" : "false") + ",\"by_entity\":" + (byEntity ? "true" : "false"));
	}
	void onCompatibilityChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_ctl::ControlledEntity::CompatibilityFlags const f, la_em::MilanVersion const& mv) noexcept override
	{
		if (!mine(e))
			return;
		auto const& ev = e->getCompatibilityChangedEvents();
		emit("\"ev\":\"compat_changed\",\"who\":\"" + w(e) + "\"," + flagsStr(f) + ",\"milan\":" + std::to_string(mv.getValue()) + ",\"last_event\":" + eventsJson(*e, ev.empty() ? 0 : ev.size() - 1));
	}
	void onStreamInputConnectionChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::StreamIndex const idx, la_em::StreamInputConnectionInfo const& info, bool const byOther) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"si_connection\",\"who\":\"" + w(e) + "\",\"idx\":" + std::to_string(idx) + ",\"state\":\"" + connName(info.state) + "\",\"talker\":\"" + hex64(info.talkerStream.entityID.getValue()) + "\",\"talker_idx\":" + std::to_string(info.talkerStream.streamIndex) + ",\"by_other\":" + (byOther ? "true" : "false"));
	}
	void onStreamInputFormatChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::StreamIndex const idx, la_em::StreamFormat const f) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"si_format\",\"who\":\"" + w(e) + "\",\"idx\":" + std::to_string(idx) + ",\"format\":\"" + hex64(f.getValue()) + "\"");
	}
	void onStreamInputDynamicInfoChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::StreamIndex const idx, la_em::StreamDynamicInfo const&) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"si_dynamic_info\",\"who\":\"" + w(e) + "\",\"idx\":" + std::to_string(idx));
	}
	void onStreamInputStarted(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::StreamIndex const idx) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"si_started\",\"who\":\"" + w(e) + "\",\"idx\":" + std::to_string(idx));
	}
	void onStreamInputStopped(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::StreamIndex const idx) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"si_stopped\",\"who\":\"" + w(e) + "\",\"idx\":" + std::to_string(idx));
	}
	void onClockSourceChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::ClockDomainIndex const cd, la_em::ClockSourceIndex const cs) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"clock_source\",\"who\":\"" + w(e) + "\",\"domain\":" + std::to_string(cd) + ",\"source\":" + std::to_string(cs));
	}
	void onClockDomainCountersChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::ClockDomainIndex const cd, la_em::ClockDomainCounters const& c) noexcept override
	{
		if (!mine(e))
			return;
		std::ostringstream o;
		o << "\"ev\":\"cd_counters\",\"who\":\"" << w(e) << "\",\"domain\":" << cd << ",\"counters\":{";
		bool first = true;
		for (auto const& [flag, v] : c)
		{
			o << (first ? "" : ",") << "\"0x" << std::hex << static_cast<unsigned>(flag) << std::dec << "\":" << v;
			first = false;
		}
		o << "}";
		emit(o.str());
	}
	void onStreamInputCountersChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_em::StreamIndex const idx, la_em::StreamInputCounters const& c) noexcept override
	{
		if (!mine(e))
			return;
		std::string conn = "?";
		try
		{
			conn = connName(e->getSinkConnectionInformation(idx).state);
		}
		catch (...)
		{
		}
		std::ostringstream o;
		o << "\"ev\":\"si_counters\",\"who\":\"" << w(e) << "\",\"idx\":" << idx << ",\"counters\":" << ctrJson(c) << ",\"lib_conn\":\"" << conn << "\"," << flagsStr(e->getCompatibilityFlags()) << ",\"n_events\":" << e->getCompatibilityChangedEvents().size();
		emit(o.str());
		if (e->getEntity().getEntityID().getValue() == DUT)
		{
			{
				std::lock_guard<std::mutex> l(S.m);
				S.dutCtr[idx] = { ctrGet(c, SICF::MediaLocked), ctrGet(c, SICF::MediaUnlocked) };
				S.dutCtrUpdates[idx] += 1;
			}
			S.cv.notify_all();
		}
	}
	void onAemAecpUnsolicitedCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"unsol_count\",\"who\":\"" + w(e) + "\",\"value\":" + std::to_string(v));
	}
	void onAemAecpUnsolicitedLossCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"unsol_loss\",\"who\":\"" + w(e) + "\",\"value\":" + std::to_string(v));
	}
	void onAecpTimeoutCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"aecp_timeout\",\"who\":\"" + w(e) + "\",\"value\":" + std::to_string(v));
	}
	void onAecpUnexpectedResponseCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"aecp_unexpected\",\"who\":\"" + w(e) + "\",\"value\":" + std::to_string(v));
	}
	void onDiagnosticsChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, la_ctl::ControlledEntity::Diagnostics const& d) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"diagnostics\",\"who\":\"" + w(e) + "\",\"diag\":" + diagJson(d));
	}
};

class AuxDelegate final : public la_ent::controller::DefaultedDelegate
{
public:
	void onEntityOnline(la_ent::controller::Interface const*, la::avdecc::UniqueIdentifier const eid, la_ent::Entity const&) noexcept override
	{
		{
			std::lock_guard<std::mutex> l(S.m);
			S.auxOnline.insert(eid.getValue());
		}
		S.cv.notify_all();
	}
};

// Waits for a completion flag set by a handler
template<class T>
struct Waiter
{
	std::mutex m;
	std::condition_variable cv;
	bool done{ false };
	T value{};
	void set(T v)
	{
		{
			std::lock_guard<std::mutex> l(m);
			value = std::move(v);
			done = true;
		}
		cv.notify_all();
	}
	bool wait(milliseconds const to)
	{
		std::unique_lock<std::mutex> l(m);
		return cv.wait_for(l, to, [this] { return done; });
	}
};

struct AemResult
{
	std::string status{};
	std::uint64_t fmt{ 0 };
	std::array<std::uint32_t, 32> ctr{};
	std::uint32_t valid{ 0 };
	long long tDone{ 0 };
};

static bool waitOnline(std::set<std::uint64_t> Shared::*which, milliseconds const to)
{
	std::unique_lock<std::mutex> l(S.m);
	return S.cv.wait_for(l, to, [which] { return (S.*which).count(DUT) && (S.*which).count(PEER); });
}

static std::string libSnapshot(la_ctl::Controller const& c, std::uint64_t eid, std::uint16_t idx, size_t eventsFrom, size_t* eventsNow)
{
	auto g = c.getControlledEntityGuard(la::avdecc::UniqueIdentifier{ eid });
	if (!g.get())
		return "{\"present\":false}";
	std::ostringstream o;
	o << "{\"present\":true," << flagsStr(g->getCompatibilityFlags()) << ",\"milan\":" << g->getMilanCompatibilityVersion().getValue() << ",\"subscribed\":" << (g->isSubscribedToUnsolicitedNotifications() ? "true" : "false") << ",\"diag\":" << diagJson(g->getDiagnostics()) << ",\"unsol_count\":" << g->getAemAecpUnsolicitedCounter() << ",\"events_new\":" << eventsJson(*g, eventsFrom);
	if (eventsNow)
		*eventsNow = g->getCompatibilityChangedEvents().size();
	if (eid == DUT)
	{
		try
		{
			auto const cfg = g->getCurrentConfigurationIndex();
			auto const& n = g->getStreamInputNode(cfg, idx);
			o << ",\"si\":" << idx << ",\"lib_format\":\"" << hex64(n.dynamicModel.streamFormat.getValue()) << "\",\"lib_conn\":\"" << connName(g->getSinkConnectionInformation(idx).state) << "\",\"lib_counters\":" << (n.dynamicModel.counters ? ctrJson(*n.dynamicModel.counters) : std::string("null"));
		}
		catch (std::exception const& ex)
		{
			o << ",\"si_error\":\"" << esc(ex.what()) << "\"";
		}
	}
	o << "}";
	return o.str();
}

int main(int argc, char** argv)
{
	if (argc != 6)
	{
		std::fprintf(stderr, "usage: %s <iface> <dut_eid> <peer_eid> <session_progid> <aux_progid>\n", argv[0]);
		return 2;
	}
	std::string const iface = argv[1];
	DUT = std::stoull(argv[2], nullptr, 16);
	PEER = std::stoull(argv[3], nullptr, 16);
	auto const progID = static_cast<std::uint16_t>(std::stoul(argv[4]));
	auto const auxProgID = static_cast<std::uint16_t>(std::stoul(argv[5]));
	auto const modelID = la_em::makeEntityModelID(0x001B92, 0x00, 0x0653B110);
	emit("\"ev\":\"start\",\"lib\":\"" + esc(la::avdecc::getVersion()) + "\",\"ctl_lib\":\"" + esc(la_ctl::getVersion()) + "\",\"iface\":\"" + esc(iface) + "\",\"dut\":\"" + hex64(DUT) + "\",\"peer\":\"" + hex64(PEER) + "\",\"progid\":" + std::to_string(progID) + ",\"aux_progid\":" + std::to_string(auxProgID));

	auto auxExec = la::avdecc::ExecutorManager::getInstance().registerExecutor("b11aux", la::avdecc::ExecutorWithDispatchQueue::create("b11aux"));
	AuxDelegate auxDlg;
	auto auxES = la::avdecc::EndStation::create(la::avdecc::protocol::ProtocolInterface::Type::PCap, iface, std::string{ "b11aux" });
	auto* aux = auxES->addControllerEntity(auxProgID, modelID, nullptr, &auxDlg);

	Obs obs;
	auto ctl = la_ctl::Controller::create(la::avdecc::protocol::ProtocolInterface::Type::PCap, iface, progID, modelID, "en", nullptr, std::nullopt, nullptr);
	auto const sessionEID = ctl->getControllerEID().getValue();
	emit("\"ev\":\"entities\",\"session_eid\":\"" + hex64(sessionEID) + "\",\"aux_eid\":\"" + hex64(aux->getEntityID().getValue()) + "\"");
	ctl->registerObserver(&obs);
	ctl->discoverRemoteEntities();
	aux->discoverRemoteEntities();
	for (int i = 0; i < 9 && !waitOnline(&Shared::online, seconds(10)); ++i)
	{
		ctl->discoverRemoteEntities();
		aux->discoverRemoteEntities();
	}
	bool const up = waitOnline(&Shared::online, milliseconds(1)) && waitOnline(&Shared::auxOnline, seconds(5));
	emit(std::string("\"ev\":\"both_online\",\"ok\":") + (up ? "true" : "false"));
	size_t evDut = 0, evPeer = 0;
	emit("\"ev\":\"snapshot\",\"tag\":\"session-start\",\"dut\":" + libSnapshot(*ctl, DUT, 0, 0, &evDut) + ",\"dut_si1\":" + libSnapshot(*ctl, DUT, 1, evDut, nullptr) + ",\"peer\":" + libSnapshot(*ctl, PEER, 0, 0, &evPeer));

	auto auxFormat = [&](bool output, std::uint64_t eid, std::uint16_t idx) {
		auto w = std::make_shared<Waiter<AemResult>>();
		auto h = [w](la_ent::controller::Interface const*, la::avdecc::UniqueIdentifier const, la_ent::LocalEntity::AemCommandStatus const st, la_em::StreamIndex const, la_em::StreamFormat const f) {
			AemResult r;
			r.status = la_ent::LocalEntity::statusToString(st);
			r.fmt = f.getValue();
			r.tDone = nowUs();
			w->set(r);
		};
		if (output)
			aux->getStreamOutputFormat(la::avdecc::UniqueIdentifier{ eid }, idx, h);
		else
			aux->getStreamInputFormat(la::avdecc::UniqueIdentifier{ eid }, idx, h);
		if (!w->wait(seconds(3)))
			return AemResult{ "NO_ANSWER" };
		return w->value;
	};
	auto auxCounters = [&](std::uint16_t idx) {
		auto w = std::make_shared<Waiter<AemResult>>();
		aux->getStreamInputCounters(la::avdecc::UniqueIdentifier{ DUT }, idx, [w](la_ent::controller::Interface const*, la::avdecc::UniqueIdentifier const, la_ent::LocalEntity::AemCommandStatus const st, la_em::StreamIndex const, la_ent::StreamInputCounterValidFlags const valid, la_em::DescriptorCounters const& c) {
			AemResult r;
			r.status = la_ent::LocalEntity::statusToString(st);
			r.valid = valid.value();
			r.ctr = c;
			r.tDone = nowUs();
			w->set(r);
		});
		if (!w->wait(seconds(3)))
			return AemResult{ "NO_ANSWER" };
		return w->value;
	};

	std::string line;
	while (std::getline(std::cin, line))
	{
		std::istringstream in(line);
		std::string cmd;
		in >> cmd;
		if (cmd == "quit")
			break;
		if (cmd == "state")
		{
			emit("\"ev\":\"snapshot\",\"tag\":\"state\",\"dut\":" + libSnapshot(*ctl, DUT, 0, evDut, nullptr) + ",\"dut_si1\":" + libSnapshot(*ctl, DUT, 1, evDut, nullptr) + ",\"peer\":" + libSnapshot(*ctl, PEER, 0, evPeer, nullptr));
			continue;
		}
		if (cmd != "cycle")
		{
			emit("\"ev\":\"bad_command\",\"line\":\"" + esc(line) + "\"");
			continue;
		}
		std::string tag;
		unsigned tIdx = 0, lIdx = 0, ctlRead = 0, holdMs = 0, postMs = 0, lockMs = 0;
		in >> tag >> tIdx >> lIdx >> ctlRead >> holdMs >> postMs >> lockMs;
		auto const T = static_cast<std::uint16_t>(tIdx), L = static_cast<std::uint16_t>(lIdx);
		emit("\"ev\":\"cycle_begin\",\"tag\":\"" + esc(tag) + "\",\"talker_out\":" + std::to_string(T) + ",\"listener_in\":" + std::to_string(L) + ",\"control\":" + std::to_string(ctlRead) + ",\"hold_ms\":" + std::to_string(holdMs) + ",\"post_ms\":" + std::to_string(postMs));
		std::string result = "OK";
		// Binding rule: read both formats live; the listener adapts to the talker
		auto tf = auxFormat(true, PEER, T);
		auto lf = auxFormat(false, DUT, L);
		emit("\"ev\":\"formats\",\"tag\":\"" + esc(tag) + "\",\"talker_status\":\"" + tf.status + "\",\"talker_format\":\"" + hex64(tf.fmt) + "\",\"listener_status\":\"" + lf.status + "\",\"listener_format\":\"" + hex64(lf.fmt) + "\",\"equal\":" + (tf.fmt == lf.fmt ? "true" : "false"));
		if (!isOk(tf.status) || !isOk(lf.status))
			result = "FORMAT_READ_FAILED";
		else if (tf.fmt != lf.fmt)
		{
			auto w = std::make_shared<Waiter<std::string>>();
			ctl->setStreamInputFormat(la::avdecc::UniqueIdentifier{ DUT }, L, la_em::StreamFormat{ tf.fmt }, [w](la_ctl::ControlledEntity const*, la_ent::LocalEntity::AemCommandStatus const st) { w->set(la_ent::LocalEntity::statusToString(st)); });
			auto const ok = w->wait(seconds(3));
			auto lf2 = auxFormat(false, DUT, L);
			emit("\"ev\":\"set_listener_format\",\"tag\":\"" + esc(tag) + "\",\"status\":\"" + (ok ? w->value : std::string("NO_ANSWER")) + "\",\"readback\":\"" + hex64(lf2.fmt) + "\"");
			if (lf2.fmt != tf.fmt)
				result = "LISTENER_CANNOT_TAKE_TALKER_FORMAT";
		}
		if (result != "OK")
		{
			emit("\"ev\":\"cycle_end\",\"tag\":\"" + esc(tag) + "\",\"result\":\"" + result + "\"");
			continue;
		}
		size_t evDutPre = 0, evPeerPre = 0;
		emit("\"ev\":\"snapshot\",\"tag\":\"" + esc(tag) + "-pre\",\"dut\":" + libSnapshot(*ctl, DUT, L, evDut, &evDutPre) + ",\"peer\":" + libSnapshot(*ctl, PEER, 0, evPeer, &evPeerPre));
		evDut = evDutPre;
		evPeer = evPeerPre;
		std::uint32_t preML = 0;
		int preUpdates = 0;
		{
			std::lock_guard<std::mutex> l(S.m);
			preML = S.dutCtr.count(L) ? S.dutCtr[L][0] : 0;
			preUpdates = S.dutCtrUpdates[L];
		}
		// Bind
		auto wb = std::make_shared<Waiter<std::string>>();
		auto const tBind = nowUs();
		ctl->connectStream({ la::avdecc::UniqueIdentifier{ PEER }, T }, { la::avdecc::UniqueIdentifier{ DUT }, L }, [wb](la_ctl::ControlledEntity const*, la_ctl::ControlledEntity const*, la_em::StreamIndex const, la_em::StreamIndex const, la_ent::ControllerEntity::ControlStatus const st) { wb->set(la_ent::LocalEntity::statusToString(st)); });
		bool const bAns = wb->wait(seconds(5));
		emit("\"ev\":\"bind\",\"tag\":\"" + esc(tag) + "\",\"t_cmd\":" + std::to_string(tBind) + ",\"status\":\"" + (bAns ? wb->value : std::string("NO_ANSWER")) + "\"");
		if (!bAns || !isOk(wb->value))
		{
			emit("\"ev\":\"cycle_end\",\"tag\":\"" + esc(tag) + "\",\"result\":\"BIND_FAILED\"");
			continue;
		}
		// Wait for MEDIA_LOCKED as the library reports it: a counters update after the bind with
		// MEDIA_LOCKED above MEDIA_UNLOCKED (the DUT resets the input's counters at the bind)
		bool locked = false;
		{
			std::unique_lock<std::mutex> l(S.m);
			locked = S.cv.wait_for(l, milliseconds(lockMs), [&] { return S.dutCtrUpdates[L] > preUpdates && S.dutCtr.count(L) && S.dutCtr[L][0] > S.dutCtr[L][1]; });
		}
		emit("\"ev\":\"lock_wait\",\"tag\":\"" + esc(tag) + "\",\"locked\":" + (locked ? "true" : "false") + ",\"ms\":" + std::to_string((nowUs() - tBind) / 1000) + ",\"pre_ml\":" + std::to_string(preML));
		if (!locked)
			result = "NO_LOCK_REPORTED";
		std::this_thread::sleep_for(milliseconds(holdMs));
		if (ctlRead)
		{
			auto const t0 = nowUs();
			auto r = auxCounters(L);
			emit("\"ev\":\"control_get_counters\",\"tag\":\"" + esc(tag) + "\",\"t_cmd\":" + std::to_string(t0) + ",\"t_rsp\":" + std::to_string(r.tDone) + ",\"status\":\"" + r.status + "\",\"valid\":\"0x" + [&] { char b[16]; std::snprintf(b, sizeof(b), "%x", r.valid); return std::string(b); }() + "\",\"ML\":" + std::to_string(r.ctr[0]) + ",\"MU\":" + std::to_string(r.ctr[1]) + ",\"SI\":" + std::to_string(r.ctr[2]) + ",\"FRX\":" + std::to_string(r.ctr[11]));
		}
		// Unbind
		auto wu = std::make_shared<Waiter<std::string>>();
		auto const tUnbind = nowUs();
		ctl->disconnectStream({ la::avdecc::UniqueIdentifier{ PEER }, T }, { la::avdecc::UniqueIdentifier{ DUT }, L }, [wu](la_ctl::ControlledEntity const*, la_em::StreamIndex const, la_ent::ControllerEntity::ControlStatus const st) { wu->set(la_ent::LocalEntity::statusToString(st)); });
		bool const uAns = wu->wait(seconds(5));
		emit("\"ev\":\"unbind\",\"tag\":\"" + esc(tag) + "\",\"t_cmd\":" + std::to_string(tUnbind) + ",\"status\":\"" + (uAns ? wu->value : std::string("NO_ANSWER")) + "\"");
		if (!uAns || !isOk(wu->value))
			result = "UNBIND_FAILED";
		std::this_thread::sleep_for(milliseconds(postMs));
		size_t evDutPost = 0, evPeerPost = 0;
		emit("\"ev\":\"snapshot\",\"tag\":\"" + esc(tag) + "-post\",\"dut\":" + libSnapshot(*ctl, DUT, L, evDut, &evDutPost) + ",\"peer\":" + libSnapshot(*ctl, PEER, 0, evPeer, &evPeerPost));
		evDut = evDutPost;
		evPeer = evPeerPost;
		emit("\"ev\":\"cycle_end\",\"tag\":\"" + esc(tag) + "\",\"result\":\"" + result + "\"");
	}

	emit("\"ev\":\"snapshot\",\"tag\":\"session-end\",\"dut\":" + libSnapshot(*ctl, DUT, 0, 0, nullptr) + ",\"dut_si1\":" + libSnapshot(*ctl, DUT, 1, 0, nullptr) + ",\"peer\":" + libSnapshot(*ctl, PEER, 0, 0, nullptr));
	ctl->unregisterObserver(&obs);
	ctl.reset();
	emit("\"ev\":\"session_destroyed\"");
	auxES.reset();

	// Deregister with an entity carrying the session's ProgID, only if it gets the session's EntityID
	{
		auto ex = la::avdecc::ExecutorManager::getInstance().registerExecutor("b11dereg", la::avdecc::ExecutorWithDispatchQueue::create("b11dereg"));
		AuxDelegate dlg;
		{
			std::lock_guard<std::mutex> l(S.m);
			S.auxOnline.clear();
		}
		auto es = la::avdecc::EndStation::create(la::avdecc::protocol::ProtocolInterface::Type::PCap, iface, std::string{ "b11dereg" });
		auto* c = es->addControllerEntity(progID, modelID, nullptr, &dlg);
		auto const eid = c->getEntityID().getValue();
		emit("\"ev\":\"dereg_entity\",\"eid\":\"" + hex64(eid) + "\",\"equal_to_session\":" + (eid == sessionEID ? "true" : "false"));
		if (eid == sessionEID)
		{
			c->discoverRemoteEntities();
			bool const seen = waitOnline(&Shared::auxOnline, seconds(10));
			for (auto const target : { DUT, PEER })
			{
				auto w = std::make_shared<Waiter<std::string>>();
				c->unregisterUnsolicitedNotifications(la::avdecc::UniqueIdentifier{ target }, [w](la_ent::controller::Interface const*, la::avdecc::UniqueIdentifier const, la_ent::LocalEntity::AemCommandStatus const st) { w->set(la_ent::LocalEntity::statusToString(st)); });
				bool const ok = w->wait(seconds(3));
				emit("\"ev\":\"deregister\",\"who\":\"" + who(target) + "\",\"seen\":" + (seen ? "true" : "false") + ",\"status\":\"" + (ok ? w->value : std::string("NO_ANSWER")) + "\"");
			}
		}
		es.reset();
	}
	emit("\"ev\":\"exit\"");
	return 0;
}
