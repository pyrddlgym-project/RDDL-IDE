from pyRDDLGym_jax.core.planner import (
     _parse_config_string, _load_config, 
     JaxBackpropPlanner, JaxOfflineController
)
     
PARAMETERS = """
    [Model]
    logic='FuzzyLogic'
    logic_kwargs={'weight': 20}
    tnorm='ProductTNorm'
    tnorm_kwargs={}
    
    [Optimizer]
    method='JaxStraightLinePlan'
    method_kwargs={}
    optimizer='rmsprop'
    optimizer_kwargs={'learning_rate': 0.01}
    batch_size_train=32
    batch_size_test=32
    
    [Training]
    key=42
    epochs=30000
    train_seconds=60    
    policy_hyperparams=2.0
    plot_step=50
"""

def build_policy(env):
    config, args = _parse_config_string(PARAMETERS)
    planner_args, _, train_args = _load_config(config, args)
    planner = JaxBackpropPlanner(rddl=env.model, **planner_args)
    return JaxOfflineController(planner, **train_args)

def required_env_args():
    return {'vectorized': True}