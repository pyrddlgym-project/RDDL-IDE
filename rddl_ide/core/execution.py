from threading import Thread
from tkinter import messagebox 

import pyRDDLGym
from pyRDDLGym.core.policy import BaseAgent

    
def evaluate_policy_fn(domain_file, inst_file, policy_file):
    
    # compile policy from given class
    with open(policy_file, 'r') as f:
        source = '\n'.join(f.readlines())
        compiled = compile(source, '', 'exec')
    exec(compiled, globals())
        
    class DynamicAgent(BaseAgent):
        
        def sample_action(self, state):
            return sample_action(self, state)
    
        def reset(self):
            return reset(self)
    
    # evaluation handle
    def target(out):
        try:
            env = pyRDDLGym.make(domain=domain_file,
                                 instance=inst_file,
                                 enforce_action_constraints=True)
            policy = DynamicAgent()   
            policy.evaluate(env, episodes=1, verbose=True, render=True)
        except Exception as e:
            out[0] = e
    
    err = [None] * 1
    thread = Thread(target=target, args=(err,))
    thread.start()
    thread.join()
    if err[0] is not None:
        messagebox.showerror('RDDL error', err[0])
        raise err[0]
