import os
import gymnasium as gym
import pkg_resources


def register_circuit_env(id_suffix, netlist_name):
    netlist_file_path = pkg_resources.resource_filename(
        "a2perf",
        f"domains/circuit_training/circuit_training/environment/test_data/{netlist_name}/netlist.pb.txt",
    )
    init_placement_file_path = pkg_resources.resource_filename(
        "a2perf",
        f"domains/circuit_training/circuit_training/environment/test_data/{netlist_name}/initial.plc",
    )
    plc_wrapper_main = pkg_resources.resource_filename(
        "a2perf", "domains/circuit_training/bin/plc_wrapper_main"
    )
    # Fallback to global installation path
    if not os.path.exists(plc_wrapper_main):
        plc_wrapper_main = "/usr/local/bin/plc_wrapper_main"

    gym.envs.register(
        id=f"CircuitTraining-{id_suffix}-v0",
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


register_circuit_env("Ariane", "ariane")
register_circuit_env("ToyMacro", "toy_macro_stdcell")
