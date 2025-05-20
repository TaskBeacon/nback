from psyflow import BlockUnit,StimBank, StimUnit,SubInfo,TaskSettings,TriggerSender
from psyflow import load_config, initialize_exp
import pandas as pd
from psychopy import core
import serial

from src import run_trial, generate_nback_conditions

# Load experiment configuration from config.yaml
cfg = load_config()

# Collect subject/session info using SubInfo form
subform = SubInfo(cfg['subform_config'])
subject_data = subform.collect()

# Load task settings and merge with subject info
settings = TaskSettings.from_dict(cfg['task_config'])
settings.add_subinfo(subject_data)

# Initialize trigger sender (can be changed to real serial port)
settings.triggers = cfg['trigger_config']
ser = serial.serial_for_url("loop://", baudrate=115200, timeout=1)
trigger_sender = TriggerSender(
    trigger_func=lambda code: ser.write([1, 225, 1, 0, code]),
    post_delay=0,
    on_trigger_start=lambda: ser.open() if not ser.is_open else None,
    on_trigger_end=lambda: ser.close()
)

# Initialize PsychoPy window and input devices
win, kb = initialize_exp(settings)

# Load and preload all stimuli
stim_bank = StimBank(win, cfg['stim_config']).preload_all()

# Save settings to file (for logging and reproducibility)
settings.save_to_json()

# Run task blocks
all_data = []
for block_i in range(settings.total_blocks):
    half_point = settings.total_blocks // 2
    n_back = 1 if block_i < half_point else 2
    # Show corresponding instruction
    instruction_label = f"instruction_{n_back}back"
    StimUnit(win, instruction_label).add_stim(stim_bank.get(instruction_label)).wait_and_continue()
    block = BlockUnit(
        block_id=f"block_{block_i}",
        block_idx=block_i,
        settings=settings,
        window=win,
        keyboard=kb
    ).generate_conditions(func=generate_nback_conditions,
                          n_back=n_back) \
     .on_start(lambda b: trigger_sender.send(settings.triggers.get("block_onset", 100))) \
     .on_end(lambda b: trigger_sender.send(settings.triggers.get("block_end", 101))) \
     .run_trial(func=run_trial, stim_bank=stim_bank, n_back=n_back, trigger_sender=trigger_sender) \
     .to_dict(all_data)

    # Customize block-level feedback (hit rate, scores, etc.)
    match_trials = block.get_trial_data(key='condition', pattern='match',match_type='startswith')
    acc = sum(t.get("cue_hit", False) for t in match_trials) / len(match_trials)

    StimUnit(win, 'block').add_stim(stim_bank.get_and_format('block_break', 
                                                             block_num=block_i+1,
                                                             total_blocks=settings.total_blocks,
                                                             acc=acc)).wait_and_continue()

# Final screen (e.g., goodbye or total score)
StimUnit(win, 'block').add_stim(stim_bank.get('good_bye')).wait_and_continue(terminate=True)

# Save trial data to CSV
df = pd.DataFrame(all_data)
df.to_csv(settings.res_file, index=False)

# Clean up
core.quit()
