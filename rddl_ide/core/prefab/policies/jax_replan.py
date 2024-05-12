from pyRDDLGym_jax.core.planner import (
     _parse_config_string, _load_config, 
     JaxBackpropPlanner, JaxOnlineController
)
     
PARAMETERS = """
    [Model]
    logic='FuzzyLogic'
    logic_kwargs={'weight': 10}
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
    epochs=1000
    train_seconds=2
"""

def build_policy(env):
    config, args = _parse_config_string(PARAMETERS)
    planner_args, plan_kwargs, train_args = _load_config(config, args)    
    policy_hyperparams = {action: 1.0 for action in env.model.action_fluents}
    planner = JaxBackpropPlanner(rddl=env.model, **planner_args)
    return JaxOnlineController(planner, policy_hyperparams=policy_hyperparams, **train_args)

def required_env_args():
    return {'vectorized': True}