import traceback
from tkinter import messagebox, END

import pyRDDLGym
from pyRDDLGym.core.policy import BaseAgent
from pyRDDLGym.core.visualizer.movie import MovieGenerator

    
def evaluate_policy_fn(domain_file, inst_file, policy_editor, viz, record):
    
    # compile policy from given class
    policy_source = policy_editor.get(1.0, END)
    try:
        compiled = compile(policy_source, '', 'exec')
        exec(compiled, globals())
    except Exception as e:
        print(traceback.format_exc())
        messagebox.showerror('Python error', e)
        
    # evaluation handle
    def target():
        try:
            env_args = required_env_args()
            env = pyRDDLGym.make(domain=domain_file, instance=inst_file, **env_args)
            if record is not None:
                movie_gen = MovieGenerator(record, env.model.domain_name, 9999)
            else:
                movie_gen = None
            env.set_visualizer(viz, movie_gen=movie_gen)
            policy = build_policy(env) 
            policy.evaluate(env, episodes=1, verbose=True, render=True)
            env.close()
            return None
        except Exception as e:
            print(traceback.format_exc())
            return e
    
    # error handler
    err = target()
    if err is not None:
        messagebox.showerror('pyRDDLGym error', err)
    
    err = str(err)
    if '>>' in err:
        start = err.index('>>')
        if 'Please check expression' in err:
            end = err.index('Please check expression')
        else:
            end = len(err) - 1
        message = err[start:end].strip()
    else:
        message = None
    return message
    
