from psyflow import StimUnit
from functools import partial
from psyflow import StimUnit
from functools import partial

def run_trial(win,kb,settings,condition,stim_bank,trigger_sender=None,):
    """
    General-purpose run_trial function for psyflow-based tasks.

    This function outlines a typical trial flow:

      1. digit presentation
      2. ITI
    """

    # === Trial data container ===
    trial_data = {"condition": condition}
    _match = condition.split("_")[0]
    _digit = condition.split("_")[1]
    correct_key = settings.match_key if _match == "match" else settings.nomatch_key

    # === Helper for creating StimUnits ===
    make_unit = partial(StimUnit, win=win, triggersender=trigger_sender)

    # 1. digit presentation  ===
    make_unit(unit_label="cue") \
        .add_stim(stim_bank.rebuild('stim_digit', text=_digit)) \
        .capture_response(
            keys=settings.key_list,
            correct=correct_key,
            duration=settings.cue_duration,
            onset_trigger=settings.triggers.get(f'{_match}_onset'),
            response_trigger=settings.triggers.get('key_press'),
            timeout_trigger=settings.triggers.get('no_response'),
            terminate_on_timeout=True
        )
    # 2. ITI ===
    make_unit(unit_label="iti") \
        .add_stim(stim_bank.get('iti')) \
        .show(settings.iti_duration)

    return trial_data
