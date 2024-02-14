from threading import Thread
from tkinter import messagebox, END

import pyRDDLGym
from pyRDDLGym.core.policy import BaseAgent
from pyRDDLGym.core.visualizer.movie import MovieGenerator

    
def evaluate_policy_fn(domain_file, inst_file, policy_editor, 
                       viz, record, vectorized, base_class):
    
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
            env = pyRDDLGym.make(domain=domain_file, instance=inst_file, 
                                 vectorized=vectorized,
                                 base_class=base_class)
            movie_gen = None
            if record is not None:
                movie_gen = MovieGenerator(record, env.model.domain_name, 9999)
            env.set_visualizer(viz, movie_gen=movie_gen)
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
