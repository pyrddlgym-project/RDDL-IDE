from threading import Thread
from tkinter import messagebox, END

import pyRDDLGym
from pyRDDLGym.core.policy import BaseAgent

    
def evaluate_policy_fn(domain_file, inst_file, policy_editor, viz, vectorized):
    
    # compile policy from given class
    policy_source = policy_editor.get(1.0, END)
    try:
        compiled = compile(policy_source, '', 'exec')
        exec(compiled, globals())
    except Exception as e:
        messagebox.showerror('Python error', e)
        raise e
        
    # evaluation handle
    def target():
        try:
            env = pyRDDLGym.make(domain=domain_file,
                                 instance=inst_file,
                                 enforce_action_constraints=True, 
                                 vectorized=vectorized)
            env.set_visualizer(viz)
            policy = build_policy(env) 
            policy.evaluate(env, episodes=1, verbose=True, render=True)
            env.close()
            return None
        except Exception as e:
            return e
    
    err = target()
    if err is not None:
        messagebox.showerror('pyRDDLGym error', err)
        raise err
