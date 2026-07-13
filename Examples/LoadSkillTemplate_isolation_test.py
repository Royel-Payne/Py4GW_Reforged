"""Diagnostic isolation test, see Claude_Coop/COOP_RELAY.md (attribState assert crash).

Fires ONLY GLOBAL_CACHE.SkillBar.LoadSkillTemplate() -- nothing else -- to test whether the
attribState assert crash (ChCliAttrib.cpp:212) reproduces from a bare call, standing idle, with
no Botting FSM, no leveler, no other game calls. Deliberately uses GLOBAL_CACHE.SkillBar (the
GlobalCache/SkillbarCache.py wrapper that queues onto ActionQueueManager("ACTION")), NOT the
Skillbar.py static SkillBar class, because GLOBAL_CACHE.SkillBar is the actual call path the
Nightfall leveler crashes on (Routines.Yield.Skills.LoadSkillbar -> behaviourtrees_src/skills.py ->
GLOBAL_CACHE.SkillBar.LoadSkillTemplate) -- confirmed against the crash dump's own Python stack.

Same shape as LeaveGH_isolation_test.py, the script that isolated the issue #3 crash.

Usage: load and run via Script Runner (or the in-game "Select Python Script" dialog) while standing
idle in an outpost (e.g. Chahbek Village), NOT running any bot/leveler. The action is queued once
on first main() tick, then the queue is drained every frame same as any other Py4GW script (the
always-running Environment Upkeeper widget also drains it independently).
"""
from Py4GWCoreLib import *

MODULE_NAME = "LoadSkillTemplate Isolation Test"

# Same template that crashed Shade (Mesmer, level 2) inside EquipSkillBar -- see COOP_RELAY.md.
TEMPLATE = "OQBDAhITAoohAAAAAAAA"

_fired = False


def main():
    global _fired
    if not _fired:
        _fired = True
        ConsoleLog(MODULE_NAME, f"Firing GLOBAL_CACHE.SkillBar.LoadSkillTemplate('{TEMPLATE}') now -- this is the only action this script takes.")
        GLOBAL_CACHE.SkillBar.LoadSkillTemplate(TEMPLATE)

    ActionQueueManager().ProcessQueue("ACTION")


if __name__ == "__main__":
    main()
