// B12 controller probe, derived from B11. Named VLAN library; application counter rule.
// Commands: cycle TAG DIRECTION TIDX LIDX HOLD_MS POST_MS POLL_MS; state; quit.
// DIRECTION A: peer to DUT; B: DUT to peer. Holds start at successful bind response.
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
static std::mutex pushMutex;
static std::condition_variable pushCv;
static std::map<std::pair<std::uint64_t,std::uint16_t>,steady_clock::time_point> lastPush;

// Cache initialization, reset/wrap and increment behavior match the application.
struct ErrorInfo { std::uint32_t current{0}, clear{0}; };
static std::map<std::uint64_t, std::map<std::uint16_t, std::map<SICF, ErrorInfo>>> errors;
static std::mutex errorMutex;
static std::string errorUpdate(std::uint64_t eid, std::uint16_t idx,
                              la_em::StreamInputCounters const& c, std::string const& conn)
{
 std::lock_guard<std::mutex> lock(errorMutex);
 if (!errors.count(eid)) return "{}";
 auto& row=errors[eid][idx];
 la_em::StreamInputCounters increments, visible;
 for (auto const& [flag,v]:c) {
  bool selected=false;
  switch(flag) {
   case SICF::MediaUnlocked: selected=(conn=="Connected"); break;
   case SICF::StreamInterrupted: case SICF::SeqNumMismatch:
   case SICF::LateTimestamp: case SICF::EarlyTimestamp:
   case SICF::UnsupportedFormat: selected=true; break;
   default: break;
  }
  if (!selected) continue;
  auto& x=row[flag];
  if(v<x.current) x.clear=0;
  if(v>x.current) increments[flag]=v-x.current;
  x.current=v;
 }
 for(auto const& [flag,x]:row) if(x.current!=x.clear) visible[flag]=x.current-x.clear;
 return "\"increments\":"+ctrJson(increments)+",\"visible\":"+ctrJson(visible);
}

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
	void onTransportError(la_ctl::Controller const*, la_ctl::InterfaceType const) noexcept override
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
        {
          std::lock_guard<std::mutex> lock(errorMutex);
          auto eid=e->getEntity().getEntityID().getValue();
          errors[eid].clear();
          for(auto const& [idx,node]:e->getCurrentConfigurationNode().streamInputs)
            if(node.dynamicModel.counters)
              for(auto const& [flag,v]:*node.dynamicModel.counters) errors[eid][idx][flag]={v,v};
        }
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
        {std::lock_guard<std::mutex> lock(errorMutex); errors.erase(e->getEntity().getEntityID().getValue());}
		{
			std::lock_guard<std::mutex> l(S.m);
			S.online.erase(e->getEntity().getEntityID().getValue());
		}
		S.cv.notify_all();
	}
	void onUnsolicitedRegistrationChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, bool const sub, bool const byEntity, la_ctl::InterfaceType const) noexcept override
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
        {std::lock_guard<std::mutex> lock(pushMutex);lastPush[{e->getEntity().getEntityID().getValue(),idx}]=steady_clock::now();}
        pushCv.notify_all();
		std::string conn = "?";
		try
		{
			conn = connName(e->getSinkConnectionInformation(idx).state);
		}
		catch (...)
		{
		}
        auto rule=errorUpdate(e->getEntity().getEntityID().getValue(),idx,c,conn);
        if(rule!="{}") emit("\"ev\":\"hive_rule\",\"who\":\""+w(e)+"\",\"idx\":"+std::to_string(idx)+",\"lib_conn\":\""+conn+"\","+rule);
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
	void onAemAecpUnsolicitedCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v, la_ctl::InterfaceType const) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"unsol_count\",\"who\":\"" + w(e) + "\",\"value\":" + std::to_string(v));
	}
	void onAemAecpUnsolicitedLossCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v, la_ctl::InterfaceType const) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"unsol_loss\",\"who\":\"" + w(e) + "\",\"value\":" + std::to_string(v));
	}
	void onAecpTimeoutCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v, la_ctl::InterfaceType const) noexcept override
	{
		if (mine(e))
			emit("\"ev\":\"aecp_timeout\",\"who\":\"" + w(e) + "\",\"value\":" + std::to_string(v));
	}
	void onAecpUnexpectedResponseCounterChanged(la_ctl::Controller const*, la_ctl::ControlledEntity const* e, std::uint64_t const v, la_ctl::InterfaceType const) noexcept override
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
	if (eid == DUT || eid == PEER)
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
	auto const modelID = la_em::makeEntityModelID(0x001B92, 0x00, 0x0653B120);
	emit("\"ev\":\"start\",\"lib\":\"" + esc(la::avdecc::getVersion()) + "\",\"ctl_lib\":\"" + esc(la_ctl::getVersion()) + "\",\"iface\":\"" + esc(iface) + "\",\"dut\":\"" + hex64(DUT) + "\",\"peer\":\"" + hex64(PEER) + "\",\"progid\":" + std::to_string(progID) + ",\"aux_progid\":" + std::to_string(auxProgID));

	auto auxExec = la::avdecc::ExecutorManager::getInstance().registerExecutor("b12aux", la::avdecc::ExecutorWithDispatchQueue::create("b12aux"));
	AuxDelegate auxDlg;
	auto auxES = la::avdecc::EndStation::create(la::avdecc::protocol::ProtocolInterface::Type::PCap, iface, std::string{ "b12aux" });
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
	auto auxCounters = [&](std::uint64_t eid, std::uint16_t idx) {
		auto w = std::make_shared<Waiter<AemResult>>();
		aux->getStreamInputCounters(la::avdecc::UniqueIdentifier{ eid }, idx, [w](la_ent::controller::Interface const*, la::avdecc::UniqueIdentifier const, la_ent::LocalEntity::AemCommandStatus const st, la_em::StreamIndex const, la_ent::StreamInputCounterValidFlags const valid, la_em::DescriptorCounters const& c) {
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
		std::string tag, direction;
		unsigned tIdx=0,lIdx=0,holdMs=0,postMs=0,pollMs=0;
		in>>tag>>direction>>tIdx>>lIdx>>holdMs>>postMs>>pollMs;
		if(!in || (direction!="A" && direction!="B") || holdMs>610000) {
			emit("\"ev\":\"bad_command\""); continue;
		}
		int alignMs=0; in>>alignMs;
		auto talker=direction=="A"?PEER:DUT, listener=direction=="A"?DUT:PEER;
		auto T=static_cast<std::uint16_t>(tIdx),L=static_cast<std::uint16_t>(lIdx);
		emit("\"ev\":\"cycle_begin\",\"tag\":\""+tag+"\",\"direction\":\""+direction+"\",\"talker_out\":"+std::to_string(T)+",\"listener_in\":"+std::to_string(L)+",\"hold_ms\":"+std::to_string(holdMs));
		auto poll=[&](std::string const& phase) {
			auto t=nowUs(); auto r=auxCounters(listener,L);
			la_em::StreamInputCounters c;
			for(unsigned i=0;i<32;++i) if(r.valid&(1u<<i)) c[static_cast<SICF>(1u<<i)]=r.ctr[i];
			emit("\"ev\":\"poll\",\"tag\":\""+tag+"\",\"phase\":\""+phase+"\",\"t_cmd\":"+std::to_string(t)+",\"t_rsp\":"+std::to_string(r.tDone)+",\"status\":\""+r.status+"\",\"counters\":"+ctrJson(c));
			return isOk(r.status);
		};
		auto tf=auxFormat(true,talker,T), lf=auxFormat(false,listener,L);
		emit("\"ev\":\"formats\",\"tag\":\""+tag+"\",\"talker_status\":\""+tf.status+"\",\"listener_status\":\""+lf.status+"\",\"talker_format\":\""+hex64(tf.fmt)+"\",\"listener_format\":\""+hex64(lf.fmt)+"\"");
		if(!isOk(tf.status)||!isOk(lf.status)) {emit("\"ev\":\"cycle_end\",\"tag\":\""+tag+"\",\"result\":\"FORMAT_READ_FAILED\"");break;}
		if(tf.fmt!=lf.fmt) {
			auto w=std::make_shared<Waiter<std::string>>();
			ctl->setStreamInputFormat(la::avdecc::UniqueIdentifier{listener},L,la_em::StreamFormat{tf.fmt},[w](la_ctl::ControlledEntity const*,la_ent::LocalEntity::AemCommandStatus const st){w->set(la_ent::LocalEntity::statusToString(st));});
			bool ok=w->wait(seconds(3));auto rb=auxFormat(false,listener,L);
			emit("\"ev\":\"set_listener_format\",\"tag\":\""+tag+"\",\"status\":\""+(ok?w->value:"NO_ANSWER")+"\",\"readback\":\""+hex64(rb.fmt)+"\"");
			if(!ok||!isOk(w->value)||!isOk(rb.status)||rb.fmt!=tf.fmt) {emit("\"ev\":\"cycle_end\",\"tag\":\""+tag+"\",\"result\":\"LISTENER_CANNOT_TAKE_TALKER_FORMAT\"");break;}
		}
		if(!poll("pre-bind")) {emit("\"ev\":\"cycle_end\",\"tag\":\""+tag+"\",\"result\":\"POLL_FAILED\"");break;}
		auto wb=std::make_shared<Waiter<std::string>>();auto tBind=nowUs();auto bindStart=steady_clock::now();
		ctl->connectStream({la::avdecc::UniqueIdentifier{talker},T},{la::avdecc::UniqueIdentifier{listener},L},[wb](la_ctl::ControlledEntity const*,la_ctl::ControlledEntity const*,la_em::StreamIndex const,la_em::StreamIndex const,la_ent::ControllerEntity::ControlStatus const st){wb->set(la_ent::LocalEntity::statusToString(st));});
		bool bAns=wb->wait(seconds(5));auto bound=steady_clock::now();
		emit("\"ev\":\"bind\",\"tag\":\""+tag+"\",\"t_cmd\":"+std::to_string(tBind)+",\"status\":\""+(bAns?wb->value:"NO_ANSWER")+"\"");
		if(!bAns||!isOk(wb->value)) {emit("\"ev\":\"cycle_end\",\"tag\":\""+tag+"\",\"result\":\"BIND_FAILED\"");break;}
		std::string result="OK";
		for(auto ms:{20u,100u,250u}) if(ms<holdMs) {std::this_thread::sleep_until(bound+milliseconds(ms));if(!poll("first-pdus-"+std::to_string(ms))) result="POLL_FAILED";}
		if(pollMs) for(unsigned ms=pollMs;ms<holdMs;ms+=pollMs) {std::this_thread::sleep_until(bound+milliseconds(ms));if(!poll("hold-"+std::to_string(ms))) {result="POLL_FAILED";break;}}
		if(!alignMs) std::this_thread::sleep_until(bound+milliseconds(holdMs));
		if(pollMs) if(!poll("hold-final")) result="POLL_FAILED";
        if(alignMs) {
          std::unique_lock<std::mutex> lock(pushMutex);auto key=std::make_pair(listener,L);
          bool seen=pushCv.wait_for(lock,seconds(4),[&]{return lastPush.count(key)&&lastPush[key]>=bindStart;});
          if(seen) {
            auto anchor=lastPush[key], target=anchor+milliseconds(alignMs);
            while(target<steady_clock::now()) target+=seconds(1);
            lock.unlock();std::this_thread::sleep_until(target);
            emit("\"ev\":\"phase_target\",\"tag\":\""+tag+"\",\"offset_ms\":"+std::to_string(alignMs)+",\"actual_hold_us\":"+std::to_string(duration_cast<microseconds>(steady_clock::now()-bound).count()));
          } else {result="NO_PUSH_ANCHOR";}
        }

		auto wu=std::make_shared<Waiter<std::string>>();auto tUnbind=nowUs();
		ctl->disconnectStream({la::avdecc::UniqueIdentifier{talker},T},{la::avdecc::UniqueIdentifier{listener},L},[wu](la_ctl::ControlledEntity const*,la_em::StreamIndex const,la_ent::ControllerEntity::ControlStatus const st){wu->set(la_ent::LocalEntity::statusToString(st));});
		bool uAns=wu->wait(seconds(5));
		emit("\"ev\":\"unbind\",\"tag\":\""+tag+"\",\"t_cmd\":"+std::to_string(tUnbind)+",\"status\":\""+(uAns?wu->value:"NO_ANSWER")+"\"");
		if(!uAns||!isOk(wu->value)) result="UNBIND_FAILED";
		std::this_thread::sleep_for(milliseconds(postMs));poll("post-unbind");
		emit("\"ev\":\"snapshot\",\"tag\":\""+tag+"-post\",\"listener\":"+libSnapshot(*ctl,listener,L,0,nullptr));
		emit("\"ev\":\"cycle_end\",\"tag\":\""+tag+"\",\"result\":\""+result+"\"");
		if(result!="OK") break;
	}

	emit("\"ev\":\"snapshot\",\"tag\":\"session-end\",\"dut\":" + libSnapshot(*ctl, DUT, 0, 0, nullptr) + ",\"dut_si1\":" + libSnapshot(*ctl, DUT, 1, 0, nullptr) + ",\"peer\":" + libSnapshot(*ctl, PEER, 0, 0, nullptr));
	ctl->unregisterObserver(&obs);
	ctl.reset();
	emit("\"ev\":\"session_destroyed\"");
	auxES.reset();

	// Deregister with an entity carrying the session's ProgID, only if it gets the session's EntityID
	{
		auto ex = la::avdecc::ExecutorManager::getInstance().registerExecutor("b12dereg", la::avdecc::ExecutorWithDispatchQueue::create("b12dereg"));
		AuxDelegate dlg;
		{
			std::lock_guard<std::mutex> l(S.m);
			S.auxOnline.clear();
		}
		auto es = la::avdecc::EndStation::create(la::avdecc::protocol::ProtocolInterface::Type::PCap, iface, std::string{ "b12dereg" });
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
