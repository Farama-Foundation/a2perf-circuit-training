# coding=utf-8
# Copyright 2021 The Circuit Training Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A class to store the observation shape and sizes."""

from typing import Dict
from typing import List
from typing import Optional
from typing import Text
from typing import Tuple
from typing import Union

import gin
import gym
import numpy as np
import tensorflow as tf

TensorType = Union[np.ndarray, tf.Tensor]
FeatureKeyType = Union[List[Text], Tuple[Text, ...]]

HARD_MACRO = 1
SOFT_MACRO = 2
PORT_CLUSTER = 3

NETLIST_METADATA = (
    'normalized_num_edges',
    'normalized_num_hard_macros',
    'normalized_num_soft_macros',
    'normalized_num_port_clusters',
    'total_horizontal_routes_k',
    'total_vertical_routes_k',
    'total_macro_horizontal_routes_k',
    'total_macro_vertical_routes_k',
    'grid_cols',
    'grid_rows',
    'canvas_width',
    'canvas_height',
)

GRAPH_ADJACENCY_MATRIX = (
    'sparse_adj_i',
    'sparse_adj_j',
    'sparse_adj_weight',
    'edge_counts',
)

NODE_STATIC_FEATURES = (
    'macros_w',
    'macros_h',
    'node_types',
)

NETLIST_INDEX = ('netlist_index',)

STATIC_OBSERVATIONS = (
    NETLIST_METADATA
    + GRAPH_ADJACENCY_MATRIX
    + NODE_STATIC_FEATURES
    + NETLIST_INDEX
)

DYNAMIC_OBSERVATIONS = (
                           'locations_x',
                           'locations_y',
                           'is_node_placed',
                           'current_node',
                           'fake_net_heatmap',
                           'mask',
                       ) + NETLIST_INDEX

ALL_OBSERVATIONS = STATIC_OBSERVATIONS + DYNAMIC_OBSERVATIONS


@gin.configurable
class ObservationConfig(object):
  """A class that contains shared configs for observation."""

  # The default numbers are the maximum number of nodes, edges, and grid size
  # on a set of TPU blocks.
  # Large numbers may cause GPU/TPU OOM during training.
  def __init__(
      self,
      max_num_nodes: int = 3_500,
      max_num_edges: int = 42_000,
      max_grid_size: int = 128,
  ):
    self.max_num_edges = max_num_edges
    self.max_num_nodes = max_num_nodes
    self.max_grid_size = max_grid_size

  @property
  def dynamic_observation_space(self) -> gym.spaces.Space:
    """Env Dynamic Observation space."""
    return gym.spaces.Dict({
        'is_node_placed': gym.spaces.Box(
            low=0, high=1, shape=(self.max_num_nodes,), dtype=np.int32
        ),
        'locations_x': gym.spaces.Box(
            low=0, high=1, shape=(self.max_num_nodes,)
        ),
        'locations_y': gym.spaces.Box(
            low=0, high=1, shape=(self.max_num_nodes,)
        ),
        'current_node': gym.spaces.Box(
            low=0, high=self.max_num_nodes - 1, shape=(1,), dtype=np.int32
        ),
        'fake_net_heatmap': gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=(self.max_grid_size ** 2,),
            dtype=np.float32,
        ),
        'mask': gym.spaces.Box(
            low=0, high=1, shape=(self.max_grid_size ** 2,), dtype=np.int32
        ),
        # high is set to 0 intentionally, so when we sample obs for creating
        # the model parameter, we sample 0 for netlist_index.
        'netlist_index': gym.spaces.Box(
            low=0, high=0, shape=(1,), dtype=np.int32
        ),
    })

  @property
  def observation_space(self) -> gym.spaces.Space:
    """Env Observation space."""
    return gym.spaces.Dict({
        'normalized_num_edges': gym.spaces.Box(low=0, high=1, shape=(1,)),
        'normalized_num_hard_macros': gym.spaces.Box(low=0, high=1, shape=(1,)),
        'normalized_num_soft_macros': gym.spaces.Box(low=0, high=1, shape=(1,)),
        'normalized_num_port_clusters': gym.spaces.Box(
            low=0, high=1, shape=(1,)
        ),
        'total_horizontal_routes_k': gym.spaces.Box(
            low=0, high=1000, shape=(1,)
        ),
        'total_vertical_routes_k': gym.spaces.Box(low=0, high=1000, shape=(1,)),
        'total_macro_horizontal_routes_k': gym.spaces.Box(
            low=0, high=1000, shape=(1,)
        ),
        'total_macro_vertical_routes_k': gym.spaces.Box(
            low=0, high=1000, shape=(1,)
        ),
        'sparse_adj_weight': gym.spaces.Box(
            low=0, high=1000, shape=(self.max_num_edges,)
        ),
        'sparse_adj_i': gym.spaces.Box(
            low=0,
            high=self.max_num_nodes - 1,
            shape=(self.max_num_edges,),
            dtype=np.int32,
        ),
        'sparse_adj_j': gym.spaces.Box(
            low=0,
            high=self.max_num_nodes - 1,
            shape=(self.max_num_edges,),
            dtype=np.int32,
        ),
        'edge_counts': gym.spaces.Box(
            low=0,
            high=self.max_num_edges - 1,
            shape=(self.max_num_nodes,),
            dtype=np.int32,
        ),
        'node_types': gym.spaces.Box(
            low=0, high=3, shape=(self.max_num_nodes,), dtype=np.int32
        ),
        'is_node_placed': gym.spaces.Box(
            low=0, high=1, shape=(self.max_num_nodes,), dtype=np.int32
        ),
        'macros_w': gym.spaces.Box(low=0, high=1, shape=(self.max_num_nodes,)),
        'macros_h': gym.spaces.Box(low=0, high=1, shape=(self.max_num_nodes,)),
        'locations_x': gym.spaces.Box(
            low=0, high=1, shape=(self.max_num_nodes,)
        ),
        'locations_y': gym.spaces.Box(
            low=0, high=1, shape=(self.max_num_nodes,)
        ),
        'grid_cols': gym.spaces.Box(low=0, high=1, shape=(1,)),
        'grid_rows': gym.spaces.Box(low=0, high=1, shape=(1,)),
        'canvas_width': gym.spaces.Box(low=0, high=1, shape=(1,)),
        'canvas_height': gym.spaces.Box(low=0, high=1, shape=(1,)),
        'current_node': gym.spaces.Box(
            low=0, high=self.max_num_nodes - 1, shape=(1,), dtype=np.int32
        ),
        'fake_net_heatmap': gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=(self.max_grid_size ** 2,),
            dtype=np.float32,
        ),
        'mask': gym.spaces.Box(
            low=0, high=1, shape=(self.max_grid_size ** 2,), dtype=np.int32
        ),
        'netlist_index': gym.spaces.Box(
            low=0, high=0, shape=(1,), dtype=np.int32
        ),
    })


def _to_dict(
    flatten_obs: TensorType,
    keys: FeatureKeyType,
    observation_config: Optional[ObservationConfig] = None,
) -> Dict[Text, TensorType]:
  """Unflatten the observation to a dictionary."""
  if observation_config:
    obs_space = observation_config.observation_space
  else:
    obs_space = ObservationConfig().observation_space
  splits = [obs_space[k].shape[0] for k in keys]
  split_obs = tf.split(flatten_obs, splits, axis=-1)
  return {k: o for o, k in zip(split_obs, keys)}


def _flatten(
    dict_obs: Dict[Text, TensorType], keys: FeatureKeyType
) -> TensorType:
  out = [np.asarray(dict_obs[k]) for k in keys]
  return np.concatenate(out, axis=-1)


def flatten_static(dict_obs: Dict[Text, TensorType]) -> TensorType:
  return _flatten(dict_obs=dict_obs, keys=STATIC_OBSERVATIONS)


def flatten_dynamic(dict_obs: Dict[Text, TensorType]) -> TensorType:
  return _flatten(dict_obs=dict_obs, keys=DYNAMIC_OBSERVATIONS)


def flatten_all(dict_obs: Dict[Text, TensorType]) -> TensorType:
  return _flatten(dict_obs=dict_obs, keys=ALL_OBSERVATIONS)


def to_dict_static(
    flatten_obs: TensorType,
    observation_config: Optional[ObservationConfig] = None,
) -> Dict[Text, TensorType]:
  """Convert the flattend numpy array of static observations back to a dict.

  Args:
    flatten_obs: a numpy array of static observations.
    observation_config: Optional observation config.

  Returns:
    A dict representation of the observations.
  """
  return _to_dict(
      flatten_obs=flatten_obs,
      keys=STATIC_OBSERVATIONS,
      observation_config=observation_config,
  )


def to_dict_dynamic(
    flatten_obs: TensorType,
    observation_config: Optional[ObservationConfig] = None,
) -> Dict[Text, TensorType]:
  """Convert the flattend numpy array of dynamic observations back to a dict.

  Args:
    flatten_obs: a numpy array of dynamic observations.
    observation_config: Optional observation config.

  Returns:
    A dict representation of the observations.
  """
  return _to_dict(
      flatten_obs=flatten_obs,
      keys=DYNAMIC_OBSERVATIONS,
      observation_config=observation_config,
  )


def to_dict_all(
    flatten_obs: TensorType,
    observation_config: Optional[ObservationConfig] = None,
) -> Dict[Text, TensorType]:
  """Convert the flattend numpy array of observations back to a dict.

  Args:
    flatten_obs: a numpy array of observations.
    observation_config: Optional observation config.

  Returns:
    A dict representation of the observations.
  """
  return _to_dict(
      flatten_obs=flatten_obs,
      keys=ALL_OBSERVATIONS,
      observation_config=observation_config,
  )
