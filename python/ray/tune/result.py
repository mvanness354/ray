import os
from pathlib import Path

# Importing for Backward Compatibility
from ray.air.constants import (  # noqa: F401
    TIMESTAMP,
    TIME_THIS_ITER_S,
    TRAINING_ITERATION,
    EXPR_PARAM_FILE,
    EXPR_PARAM_PICKLE_FILE,
    EXPR_PROGRESS_FILE,
    EXPR_RESULT_FILE,
    EXPR_ERROR_PICKLE_FILE,
    EXPR_ERROR_FILE,
)


# fmt: off
# __sphinx_doc_begin__
# (Optional/Auto-filled) training is terminated. Filled only if not provided.
DONE = "done"

# (Optional) Enum for user controlled checkpoint
SHOULD_CHECKPOINT = "should_checkpoint"

# (Auto-filled) The hostname of the machine hosting the training process.
HOSTNAME = "hostname"

# (Auto-filled) The auto-assigned id of the trial.
TRIAL_ID = "trial_id"

# (Auto-filled) The auto-assigned id of the trial.
EXPERIMENT_TAG = "experiment_tag"

# (Auto-filled) The node ip of the machine hosting the training process.
NODE_IP = "node_ip"

# (Auto-filled) The pid of the training process.
PID = "pid"

# (Optional) Default (anonymous) metric when using tune.report(x)
DEFAULT_METRIC = "_metric"

# (Optional) Mean reward for current training iteration
EPISODE_REWARD_MEAN = "episode_reward_mean"

# (Optional) Mean loss for training iteration
MEAN_LOSS = "mean_loss"

# (Optional) Mean accuracy for training iteration
MEAN_ACCURACY = "mean_accuracy"

# Number of episodes in this iteration.
EPISODES_THIS_ITER = "episodes_this_iter"

# (Optional/Auto-filled) Accumulated number of episodes for this trial.
EPISODES_TOTAL = "episodes_total"

# Number of timesteps in this iteration.
TIMESTEPS_THIS_ITER = "timesteps_this_iter"

# (Auto-filled) Accumulated number of timesteps for this entire trial.
TIMESTEPS_TOTAL = "timesteps_total"

# (Auto-filled) Accumulated time in seconds for this entire trial.
TIME_TOTAL_S = "time_total_s"

# __sphinx_doc_end__
# fmt: on

DEFAULT_EXPERIMENT_INFO_KEYS = ("trainable_name", EXPERIMENT_TAG, TRIAL_ID)

DEFAULT_RESULT_KEYS = (
    TRAINING_ITERATION,
    TIME_TOTAL_S,
    MEAN_ACCURACY,
    MEAN_LOSS,
)

# Metrics that don't require at least one iteration to complete
DEBUG_METRICS = (
    TRIAL_ID,
    "experiment_id",
    "date",
    TIMESTAMP,
    PID,
    HOSTNAME,
    NODE_IP,
    "config",
)

# Make sure this doesn't regress
AUTO_RESULT_KEYS = (
    TRAINING_ITERATION,
    TIME_TOTAL_S,
    EPISODES_TOTAL,
    TIMESTEPS_TOTAL,
    NODE_IP,
    HOSTNAME,
    PID,
    TIME_TOTAL_S,
    TIME_THIS_ITER_S,
    TIMESTAMP,
    "date",
    "time_since_restore",
    "timesteps_since_restore",
    "iterations_since_restore",
    "config",
    # TODO(justinvyu): Move this stuff to train to avoid cyclical dependency.
    "checkpoint_dir_name",
)

# __duplicate__ is a magic keyword used internally to
# avoid double-logging results when using the Function API.
RESULT_DUPLICATE = "__duplicate__"

# __trial_info__ is a magic keyword used internally to pass trial_info
# to the Trainable via the constructor.
TRIAL_INFO = "__trial_info__"

# __stdout_file__/__stderr_file__ are magic keywords used internally
# to pass log file locations to the Trainable via the constructor.
STDOUT_FILE = "__stdout_file__"
STDERR_FILE = "__stderr_file__"


def _get_defaults_results_dir() -> str:
    return (
        # This can be overwritten by our libraries
        os.environ.get("RAY_AIR_LOCAL_CACHE_DIR")
        # This is a directory provided by Bazel automatically
        or os.environ.get("TEST_TMPDIR")
        # This is the old way to specify the results dir
        # Deprecate: Remove in 2.6
        or os.environ.get("TUNE_RESULT_DIR")
        # Default
        or Path("~/ray_results").expanduser().as_posix()
    )


# Where Tune writes result files by default
DEFAULT_RESULTS_DIR = _get_defaults_results_dir()

DEFAULT_EXPERIMENT_NAME = "default"

# Meta file about status under each experiment directory, can be
# parsed by automlboard if exists.
JOB_META_FILE = "job_status.json"

# Meta file about status under each trial directory, can be parsed
# by automlboard if exists.
EXPR_META_FILE = "trial_status.json"

# Config prefix when using ExperimentAnalysis.
CONFIG_PREFIX = "config"
