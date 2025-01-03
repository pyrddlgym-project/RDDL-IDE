from pyRDDLGym_jax.core.planner import (
     _parse_config_string, _load_config, 
     JaxBackpropPlanner, JaxOnlineController
)
     
PARAMETERS = """
    [Model]
    logic='FuzzyLogic'
    tnorm='ProductTNorm'
    tnorm_kwargs={}
    
    [Optimizer]
    method='JaxStraightLinePlan'
    method_kwargs={}
    optimizer='rmsprop'
    optimizer_kwargs={'learning_rate': 0.01}
    batch_size_train=32
    batch_size_test=32
    rollout_horizon=5
    
    [Training]
    key=42
    epochs=5000
    train_seconds=2
    policy_hyperparams=2.0
"""

def build_policy(env):
    config, args = _parse_config_string(PARAMETERS)
    planner_args, _, train_args = _load_config(config, args)
    planner = JaxBackpropPlanner(rddl=env.model, **planner_args)
    return JaxOnlineController(planner, **train_args)

def required_env_args():
    return {'vectorized': True}