import os

import gym as legacy_gym
import gymnasium as gym
import pkg_resources

netlist_file_path = pkg_resources.resource_filename(
    "a2perf",
    "domains/circuit_training/circuit_training/environment/test_data/ariane/netlist.pb.txt",
)

init_placement_file_path = pkg_resources.resource_filename(
    "a2perf",
    "domains/circuit_training/circuit_training/environment/test_data/ariane/initial.plc",
)

plc_wrapper_main = pkg_resources.resource_filename(
    "a2perf", "domains/circuit_training/bin/plc_wrapper_main"
)

# Fallback to global installation path
if not os.path.exists(plc_wrapper_main):
    plc_wrapper_main = "/usr/local/bin/plc_wrapper_main"

gym.envs.register(
    id="CircuitTraining-v0",
    apply_api_compatibility=False,
    disable_env_checker=False,
    entry_point="a2perf.domains.circuit_training.circuit_training.environment.environment:create_circuit_environment",
    kwargs=dict(
        netlist_file=netlist_file_path,
        init_placement=init_placement_file_path,
        plc_wrapper_main=plc_wrapper_main,
        netlist_index=0,
        use_legacy_step=False,
        use_legacy_reset=False,
    ),
)

legacy_gym.envs.register(
    id="CircuitTraining-v0",
    entry_point="a2perf.domains.circuit_training.circuit_training.environment.environment:create_circuit_environment",
    kwargs=dict(
        use_legacy_step=True,
        use_legacy_reset=True,
        netlist_file=netlist_file_path,
        init_placement=init_placement_file_path,
        plc_wrapper_main=plc_wrapper_main,
        netlist_index=0,
    ),
)
