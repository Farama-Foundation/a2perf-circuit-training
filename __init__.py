import gym as legacy_gym
import gymnasium as gym

# Register the environments with the relative path
gym.envs.register(
    id='QuadrupedLocomotion-v0',
    apply_api_compatibility=True,
    entry_point='a2perf.domains.quadruped_locomotion.motion_imitation.envs.env_builder:build_imitation_env',
    kwargs={
    }
)

legacy_gym.envs.register(
    id='QuadrupedLocomotion-v0',
    entry_point='a2perf.domains.quadruped_locomotion.motion_imitation.envs.env_builder:build_imitation_env',
    kwargs={
    }
)
