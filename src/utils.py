import random
import numpy as np
from typing import List, Optional, Dict

def generate_nback_conditions(
    n_trial_list: int,
    condition_labels: Optional[List[str]] = None,  # e.g., ['match', 'no_match']
    digits: List[str] = None,                             # e.g., ['1','2',...,'9'] or ['A', 'B', ...]
    n_back: int = 2,
    match_ratio: float = 0.3,
    min_nonmatch_start: int = 3,
    max_match_run: int = 3,
    seed: Optional[int] = None
) -> np.ndarray:
    """
    Generate an n-back sequence of trial_list with controlled match and non-match conditions.

    Returns a list of dictionaries:
        {'condition': 'match_3'} or {'condition': 'no_match_7'}
    """
    if condition_labels is None:
        condition_labels = ['match', 'no_match']
    if digits is None:
        digits = [str(i) for i in range(1, 10)]
    assert len(condition_labels) == 2, "condition_labels must contain exactly two labels"
    
    match_label, no_match_label = condition_labels

    rng = random.Random(seed)
    trial_list = []
    digit_buffer = []
    match_streak = 0

    for i in range(n_trial_list):
        if i < max(n_back, min_nonmatch_start):
            # Force non-match in early trial_list
            digit = rng.choice(digits)
            while len(digit_buffer) >= n_back and digit == digit_buffer[-n_back]:
                digit = rng.choice(digits)
            label = f"{no_match_label}_{digit}"
            match_streak = 0
        else:
            is_match = (rng.random() < match_ratio) and (match_streak < max_match_run)
            if is_match:
                digit = digit_buffer[-n_back]
                label = f"{match_label}_{digit}"
                match_streak += 1
            else:
                digit = rng.choice(digits)
                while digit == digit_buffer[-n_back]:
                    digit = rng.choice(digits)
                label = f"{no_match_label}_{digit}"
                match_streak = 0

        digit_buffer.append(digit)
        trial_list.append(label)

    return np.array(trial_list, dtype=object)
