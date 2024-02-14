from stable_baselines3 import PPO
from pyRDDLGym_rl.core.env import SimplifiedActionRDDLEnv
from pyRDDLGym_rl.core.agent import StableBaselinesAgent

def build_policy(env):
    model = PPO('MultiInputPolicy', env, verbose=1)    
    model.learn(total_timesteps=200000)
    return StableBaselinesAgent(model)

def required_env_args():
    return {'vectorized': True, 'base_class': SimplifiedActionRDDLEnv}