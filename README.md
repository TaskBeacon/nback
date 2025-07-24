# N-Back Task

| Field | Value |
|---|---|
| Name | N-Back Task |
| Version | main (1.0) |
| URL / Repository | https://github.com/TaskBeacon/nback |
| Short Description | An N-Back task with 1-back and 2-back conditions. |
| Created By | zh1peng |
| Date Updated | 2025/07/24 |
| PsyFlow Version |0.1.0|
| PsychoPy Version |2025.1.1              |
| Modality     |Behavior/EEG                  |

## 1. Task Overview
This task is a classic N-Back cognitive test. Participants are shown a sequence of digits and must determine if the current digit matches the one presented 'N' trials ago. The task includes two blocks: a 1-Back block and a 2-Back block.

## 2. Task Flow
### Block-Level Flow
| Step | Description |
|---|---|
| 1. Instruction | For each block (1-Back then 2-Back), instructions are displayed. The first half of the blocks are 1-Back, the second half are 2-Back. |
| 2. Trial Execution | The block runs for a set number of trials, as defined in `config.yaml`. |
| 3. Block Break | After each block, a break screen is shown with the accuracy for the 'match' trials in that block. |
| 4. Goodbye | After all blocks are complete, a "goodbye" message is displayed. |

### Trial-Level Flow
| Step | Description |
|---|---|
| 1. Digit Presentation | A digit is presented on the screen for the duration specified by `cue_duration`. The participant can respond during this time. |
| 2. Inter-Trial Interval (ITI) | A blank screen is shown for the duration specified by `iti_duration`. |

### Other Logic
| Function | Description |
|---|---|
| `generate_nback_conditions` | This function generates the sequence of trials for each block. It ensures a specific ratio of 'match' to 'non-match' trials, and controls for the number of consecutive 'match' trials. |

## 3. Configuration Summary
### a. Subject Info
| Field | Meaning |
|---|---|
| subject_id | Subject Identifier |
| subname | Subject Name |
| age | Age |
| gender | Gender |

### b. Window Settings
| Parameter | Value |
|---|---|
| size | [1920, 1080] |
| units | deg |
| screen | 1 |
| bg_color | gray |
| fullscreen | True |
| monitor_width_cm | 60 |
| monitor_distance_cm | 72 |

### c. Stimuli
| Name | Type | Description |
|---|---|---|
| stim_digit | text | The digit presented to the participant. |
| stim_iti | text | A blank stimulus for the inter-trial interval. |
| instruction_1back | textbox | Instructions for the 1-Back block. |
| instruction_2back | textbox | Instructions for the 2-Back block. |
| block_break | text | Feedback shown between blocks. |
| good_bye | textbox | Final message at the end of the task. |

### d. Timing
| Phase | Duration |
|---|---|
| cue_duration | 0.8 |
| iti_duration | [1.2] |

### e. Triggers
| Event | Code |
|---|---|
| exp_onset | 98 |
| exp_end | 99 |
| block_onset | 100 |
| block_end | 101 |
| match_onset | 2 |
| nomatch_onset | 3 |
| key_press | 4 |
| no_response | 5 |

## 4. Methods
Participants perform an N-Back task, a continuous performance paradigm used to measure working memory. The experiment is divided into two blocks: a 1-Back and a 2-Back condition. In each trial, a digit (1-9) is presented on the screen. Participants are instructed to press the spacebar if the current digit is identical to the digit presented N trials previously (a "match").

The task begins with a 1-Back block, followed by a 2-Back block. Each block consists of 20 trials. The sequence of stimuli is pseudo-randomly generated to contain approximately 30% match trials. A digit is displayed for 800ms, during which a response can be made. This is followed by a 1200ms inter-trial interval. Feedback on accuracy for match trials is provided at the end of each block.