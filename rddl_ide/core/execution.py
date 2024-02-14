from threading import Thread
from tkinter import messagebox, END

import pyRDDLGym
from pyRDDLGym.core.policy import BaseAgent

    
def evaluate_policy_fn(domain_file, inst_file, policy_editor):
    
    # compile policy from given class
    policy_source = policy_editor.get(1.0, END)
    compiled = compile(policy_source, '', 'exec')
    exec(compiled, globals())
    
    # evaluation handle
    def target(out):
        try:
            env = pyRDDLGym.make(domain=domain_file,
                                 instance=inst_file,
                                 enforce_action_constraints=True)
            policy = Policy(action_space=env.action_space,
                            num_actions=env.max_allowed_actions)   
            policy.evaluate(env, episodes=1, verbose=True, render=True)
            env.close()
        except Exception as e:
            out[0] = e
    
    err = [None] * 1
    if err[0] is not None:
        messagebox.showerror('RDDL error', err[0])
        raise err[0]
    target(err)
