import os
import site
import sys
import tarfile
from pathlib import Path

import gymnasium as gym
import pkg_resources
from absl import logging


def setup_dreamplace():
    package_path = Path(__file__).parent
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    dreamplace_file = f"dreamplace_python{python_version}.tar.gz"
    dreamplace_path = package_path / "dreamplace_builds" / dreamplace_file

    site_packages_path = site.getusersitepackages()
    dreamplace_dir = os.path.join(site_packages_path, "dreamplace")

    if not os.path.exists(dreamplace_dir):
        logging.info("Setting up Dreamplace...")
        os.makedirs(dreamplace_dir, exist_ok=True)

        # Extract Dreamplace
        with tarfile.open(dreamplace_path, "r:gz") as tar:
            tar.extractall(path=dreamplace_dir)

        # Create .pth files
        dreamplace_inner_dir = os.path.join(dreamplace_dir, "dreamplace")
        dreamplace_outer_pth = os.path.join(site_packages_path, "dreamplace.pth")
        with open(dreamplace_outer_pth, "w") as file:
            file.write(dreamplace_dir + "\n")

        dreamplace_inner_pth = os.path.join(
            site_packages_path, "dreamplace_dreamplace.pth"
        )
        with open(dreamplace_inner_pth, "w") as file:
            file.write(dreamplace_inner_dir + "\n")

        logging.info("Dreamplace setup completed.")
    else:
        logging.info("Dreamplace already set up.")

    # Ensure Dreamplace is in sys.path
    if dreamplace_dir not in sys.path:
        sys.path.append(dreamplace_dir)
    if os.path.join(dreamplace_dir, "dreamplace") not in sys.path:
        sys.path.append(os.path.join(dreamplace_dir, "dreamplace"))


def set_plc_wrapper_main_permissions():
    package_path = Path(__file__).parent.parent.parent
    binary_path = (
        package_path / "domains" / "circuit_training" / "bin" / "plc_wrapper_main"
    )

    if binary_path.exists():
        try:
            os.chmod(binary_path, 0o755)
            logging.info("Set permissions for plc_wrapper_main.")
        except Exception as e:
            logging.error(f"Failed to set permissions for plc_wrapper_main: {str(e)}")
    else:
        logging.error("plc_wrapper_main not found.")


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


setup_dreamplace()
set_plc_wrapper_main_permissions()

register_circuit_env("Ariane", "ariane")
register_circuit_env("ToyMacro", "toy_macro_stdcell")
