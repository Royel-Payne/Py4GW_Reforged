"""TASK I in Claude_Coop/COOP_RELAY.md -- is it the polling steps, or the framework's per-frame
machinery itself?

Every prior test (LeaveGH, LeaveGH-only, Travel_To_Random_District) had the bot's OWN routine
actively polling map/agent state (Map.IsMapLoading, GetInstanceUptime, IsMapIDMatch, etc.) during
the transition. All three crashed. This test removes that variable entirely: the bot just sits on
bot.Wait.ForTime(), doing no map polling of any kind -- Update() still runs every frame (still
ticking _start_coroutines() and ~25 managed upkeep coroutines per App Claude's note), but the
routine itself never touches map state. YOU trigger the map change by hand while it's running.

- CRASHES  -> not the polling steps at all. The framework's per-frame coroutine machinery itself
              faults on any transition, regardless of what the routine is actually doing. Deeper
              bug, different fix location.
- SURVIVES -> the polling steps (_coro_until_on_outpost / _coro_for_map_to_change) are the actual
              culprits and need map-ready guards. Everything up to this point stands.

Usage: run via Script Runner on Rogue (already in Chahbek Village outpost, no fresh character
needed). Once it's running (status shows "Running"), manually travel/change district yourself
while it's still active.
"""
from Py4GWCoreLib import *

MODULE_NAME = "Idle Framework Test"

bot = Botting("Idle Framework")


def routine(bot: Botting) -> None:
    bot.Wait.ForTime(600000)


bot.SetMainRoutine(routine)

_started = False


def main():
    global _started
    bot.Update()
    if not _started and bot.config.initialized:
        _started = True
        bot.Start()


if __name__ == "__main__":
    main()
