// Issue 117 (A200): non-interactive la_avdecc discovery and full enumeration.
//
// Creates one la_avdecc controller on <interface> (PCap transport), does NOT
// advertise it, lets the library discover and fully enumerate every entity for
// <seconds>, then prints per entity: online/offline, compatibility flags, the
// Milan info, every compatibility change with its spec clause, diagnostics and
// the enumeration query errors; every library log line at Warn or above is
// printed as a COMPLAINT line. Each online entity's model is also written as
// JSON (static, dynamic, state, statistics, Milan, compatibility, diagnostics).
//
// The library only issues read commands plus REGISTER_UNSOLICITED_NOTIFICATION
// during enumeration; nothing is acquired, locked, bound or set.
//
// usage: a200_enum <interface> <seconds> <json_out_dir>

#include <la/avdecc/controller/avdeccController.hpp>
#include <la/avdecc/logger.hpp>
#include <la/avdecc/utils.hpp>

#include <chrono>
#include <cstdio>
#include <map>
#include <mutex>
#include <set>
#include <string>
#include <thread>
#include <vector>

using namespace std::chrono_literals;
namespace ctl = la::avdecc::controller;

namespace
{
std::mutex g_lock;

std::string hex(la::avdecc::UniqueIdentifier const id)
{
	return la::avdecc::utils::toHexString(id, true, false);
}

std::string ver(la::avdecc::entity::model::MilanVersion const& v)
{
	return std::to_string(v.getMajorVersion()) + "." + std::to_string(v.getMinorVersion()) + "." + std::to_string(v.getPatchVersion()) + "." + std::to_string(v.getBuildVersion());
}

std::string flags(ctl::ControlledEntity::CompatibilityFlags const f)
{
	std::string s;
	auto const add = [&](ctl::ControlledEntity::CompatibilityFlag fl, char const* n) {
		if (f.test(fl))
		{
			s += (s.empty() ? "" : "|");
			s += n;
		}
	};
	add(ctl::ControlledEntity::CompatibilityFlag::IEEE17221, "IEEE17221");
	add(ctl::ControlledEntity::CompatibilityFlag::Milan, "Milan");
	add(ctl::ControlledEntity::CompatibilityFlag::IEEE17221Warning, "IEEE17221Warning");
	add(ctl::ControlledEntity::CompatibilityFlag::MilanWarning, "MilanWarning");
	add(ctl::ControlledEntity::CompatibilityFlag::Misbehaving, "Misbehaving");
	return s.empty() ? "None" : s;
}

class Obs final : public ctl::Controller::DefaultedObserver, public la::avdecc::logger::Logger::Observer
{
public:
	std::set<la::avdecc::UniqueIdentifier> online{};
	std::map<la::avdecc::UniqueIdentifier, std::vector<int>> queryErrors{};
	int complaints{ 0 };

	void onLogItem(la::avdecc::logger::Level const level, la::avdecc::logger::LogItem const* const item) noexcept override
	{
		auto const lvl = la::avdecc::logger::Logger::getInstance().levelToString(level);
		std::lock_guard<std::mutex> const lg{ g_lock };
		if (level >= la::avdecc::logger::Level::Warn)
		{
			++complaints;
			std::printf("COMPLAINT [%s] %s\n", lvl.c_str(), item->getMessage().c_str());
		}
		else
		{
			std::printf("LOG [%s] %s\n", lvl.c_str(), item->getMessage().c_str());
		}
		std::fflush(stdout);
	}
	void onTransportError(ctl::Controller const* const) noexcept override
	{
		std::lock_guard<std::mutex> const lg{ g_lock };
		std::printf("EVENT transport-error\n");
	}
	void onEntityQueryError(ctl::Controller const* const, ctl::ControlledEntity const* const entity, ctl::Controller::QueryCommandError const error) noexcept override
	{
		std::lock_guard<std::mutex> const lg{ g_lock };
		auto const id = entity->getEntity().getEntityID();
		queryErrors[id].push_back(static_cast<int>(error));
		std::printf("EVENT query-error %s code=%d\n", hex(id).c_str(), static_cast<int>(error));
	}
	void onEntityOnline(ctl::Controller const* const, ctl::ControlledEntity const* const entity) noexcept override
	{
		std::lock_guard<std::mutex> const lg{ g_lock };
		auto const id = entity->getEntity().getEntityID();
		online.insert(id);
		std::printf("EVENT online %s\n", hex(id).c_str());
		std::fflush(stdout);
	}
	void onEntityOffline(ctl::Controller const* const, ctl::ControlledEntity const* const entity) noexcept override
	{
		std::lock_guard<std::mutex> const lg{ g_lock };
		std::printf("EVENT offline %s\n", hex(entity->getEntity().getEntityID()).c_str());
	}
	void onCompatibilityChanged(ctl::Controller const* const, ctl::ControlledEntity const* const entity, ctl::ControlledEntity::CompatibilityFlags const f, la::avdecc::entity::model::MilanVersion const& mv) noexcept override
	{
		std::lock_guard<std::mutex> const lg{ g_lock };
		std::printf("EVENT compatibility %s flags=%s milan=%s\n", hex(entity->getEntity().getEntityID()).c_str(), flags(f).c_str(), ver(mv).c_str());
	}
};
} // namespace

int main(int argc, char** argv)
{
	if (argc != 4)
	{
		std::fprintf(stderr, "usage: %s <interface> <seconds> <json_out_dir>\n", argv[0]);
		return 2;
	}
	if (!la::avdecc::isCompatibleWithInterfaceVersion(la::avdecc::InterfaceVersion))
	{
		std::printf("ABI: interface version mismatch\n");
		return 3;
	}
	std::printf("LIB la_avdecc %s, controller %s\n", la::avdecc::getVersion().c_str(), la::avdecc::controller::getVersion().c_str());
	for (auto const& info : la::avdecc::getCompileOptionsInfo())
		std::printf("LIB option %s\n", info.longName.c_str());
	for (auto const& info : la::avdecc::controller::getCompileOptionsInfo())
		std::printf("LIB controller-option %s\n", info.longName.c_str());

	Obs obs;
	la::avdecc::logger::Logger::getInstance().registerObserver(&obs);
	la::avdecc::logger::Logger::getInstance().setLevel(la::avdecc::logger::Level::Info);
	int rc = 0;
	{
		auto controller = ctl::Controller::create(la::avdecc::protocol::ProtocolInterface::Type::PCap, argv[1], 0x0A20, la::avdecc::UniqueIdentifier{ 0x001BC50000000A20ull }, "en", nullptr, std::nullopt, nullptr);
		controller->registerObserver(&obs);
		std::this_thread::sleep_for(std::chrono::seconds(std::stoi(argv[2])));

		std::set<la::avdecc::UniqueIdentifier> ids;
		{
			std::lock_guard<std::mutex> const lg{ g_lock };
			ids = obs.online;
		}
		auto const jflags = la::avdecc::entity::model::jsonSerializer::Flags{ la::avdecc::entity::model::jsonSerializer::Flag::ProcessADP, la::avdecc::entity::model::jsonSerializer::Flag::ProcessCompatibility, la::avdecc::entity::model::jsonSerializer::Flag::ProcessDiagnostics, la::avdecc::entity::model::jsonSerializer::Flag::ProcessDynamicModel, la::avdecc::entity::model::jsonSerializer::Flag::ProcessMilan, la::avdecc::entity::model::jsonSerializer::Flag::ProcessState, la::avdecc::entity::model::jsonSerializer::Flag::ProcessStaticModel, la::avdecc::entity::model::jsonSerializer::Flag::ProcessStatistics };
		for (auto const id : ids)
		{
			auto guard = controller->getControlledEntityGuard(id);
			if (!guard)
			{
				std::printf("ENTITY %s guard-unavailable\n", hex(id).c_str());
				rc = 4;
				continue;
			}
			auto const& e = *guard;
			std::lock_guard<std::mutex> const lg{ g_lock };
			std::printf("ENTITY %s model=%s flags=%s milanRedundant=%d cacheable=%d\n", hex(id).c_str(), hex(e.getEntity().getEntityModelID()).c_str(), flags(e.getCompatibilityFlags()).c_str(), e.isMilanRedundant() ? 1 : 0, e.isEntityModelValidForCaching() ? 1 : 0);
			if (auto const mi = e.getMilanInfo())
				std::printf("ENTITY %s milanInfo protocolVersion=%u certificationVersion=%s specificationVersion=%s\n", hex(id).c_str(), mi->protocolVersion, ver(mi->certificationVersion).c_str(), ver(mi->specificationVersion).c_str());
			else
				std::printf("ENTITY %s milanInfo absent\n", hex(id).c_str());
			for (auto const& ev : e.getCompatibilityChangedEvents())
				std::printf("ENTITY %s compat-change %s -> %s clause=\"%s\" message=\"%s\"\n", hex(id).c_str(), flags(ev.previousFlags).c_str(), flags(ev.newFlags).c_str(), ev.specClause.c_str(), ev.message.c_str());
			auto const& d = e.getDiagnostics();
			std::printf("ENTITY %s diagnostics redundancyWarning=%d controlsOutOfBounds=%zu streamInputOverLatency=%zu\n", hex(id).c_str(), d.redundancyWarning ? 1 : 0, d.controlCurrentValueOutOfBounds.size(), d.streamInputOverLatency.size());
			auto const it = obs.queryErrors.find(id);
			std::printf("ENTITY %s query-errors %zu\n", hex(id).c_str(), it == obs.queryErrors.end() ? std::size_t{ 0 } : it->second.size());
			auto const path = std::string{ argv[3] } + "/entity_" + hex(id) + ".json";
			auto const [err, msg] = controller->serializeControlledEntityAsJson(id, path, jflags, "issue 117 A200 enumeration");
			std::printf("ENTITY %s json %s %s\n", hex(id).c_str(), !!err ? "FAILED" : "written", !!err ? msg.c_str() : path.c_str());
		}
		std::printf("SUMMARY online=%zu complaints=%d\n", ids.size(), obs.complaints);
		std::fflush(stdout);
	}
	la::avdecc::logger::Logger::getInstance().unregisterObserver(&obs);
	return rc;
}
