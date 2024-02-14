import os
import tkinter as tk
from tkinter import END, Menu
import tkinter.filedialog as fd

from core.execution import evaluate_policy_fn


def load_policy(name):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(abs_path, 'policies', name + '.py'), 'r') as file:
        content = file.read()
    return content    


def assign_menubar_functions(domain_window, inst_window, policy_window,
                             domain_editor, inst_editor, policy_editor):
    domain_file, inst_file, viz = None, None, None
    
    # load template RDDL
    abs_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(abs_path, 'domain.rddl'), 'r') as dom_txt:
        DOMAIN_TEMPLATE = dom_txt.read()
    with open(os.path.join(abs_path, 'instance.rddl'), 'r') as inst_txt:
        INSTANCE_TEMPLATE = inst_txt.read()
    
    # FILE functions
    def create_domain():
        global domain_file, viz
        domain_file, viz = None, None
        domain_window.title('[Domain] Untitled')
        domain_editor.delete(1.0, END)
        domain_editor.insert(1.0, DOMAIN_TEMPLATE)
        
    def create_instance():
        global inst_file
        inst_file = None
        inst_window.title('[Instance] Untitled')
        inst_editor.delete(1.0, END)
        inst_editor.insert(1.0, INSTANCE_TEMPLATE)
    
    def _window_from_file(window, editor, caption, file_path):
        if file_path is not None:
            window.title(f'[{caption}] {os.path.basename(file_path)}')
            editor.delete(1.0, END)
            with open(file_path, 'r') as new_file:
                editor.insert(1.0, new_file.read())
                new_file.close()
        
    def open_domain():
        global domain_file, viz    
        domain_file = fd.askopenfilename(defaultextension='.rddl',
                                         filetypes=[('RDDL File', '*.rddl*')])
        viz = None
        if domain_file == '': domain_file = None            
        _window_from_file(domain_window, domain_editor, 'Domain', domain_file)
    
    def open_instance():
        global inst_file        
        inst_file = fd.askopenfilename(defaultextension='.rddl',
                                       filetypes=[('RDDL File', '*.rddl*')])
        if inst_file == '': inst_file = None            
        _window_from_file(inst_window, inst_editor, 'Instance', inst_file)
    
    def open_from_dialog():
        global domain_file, inst_file, viz
        master = tk.Tk()
        master.resizable(False, False)
        
        tk.Label(master, text="Domain").grid(row=0)
        tk.Label(master, text="Instance").grid(row=1)
        e1 = tk.Entry(master)
        e2 = tk.Entry(master)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        
        def close_me():
            master.quit()      
            master.destroy()   
            
        def select_problem():
            global domain_file, inst_file, viz
            domain, instance = e1.get(), e2.get()
            
            from rddlrepository.core.manager import RDDLRepoManager
            manager = RDDLRepoManager()
            info = manager.get_problem(domain)
            domain_file = info.get_domain()
            inst_file = info.get_instance(instance)
            viz = info.get_visualizer()
            
            _window_from_file(domain_window, domain_editor, 'Domain', domain_file)
            _window_from_file(inst_window, inst_editor, 'Instance', inst_file) 
              
            close_me()
        
        tk.Button(master, text='Load', command=select_problem).grid(
            row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Close', command=close_me).grid(
            row=3, column=1, sticky=tk.W, pady=4)
        
    def save_domain():
        global domain_file        
        if domain_file is None:
            domain_file = fd.asksaveasfilename(initialfile='domain.rddl',
                                               defaultextension='.rddl',
                                               filetypes=[('RDDL File', '*.rddl*')])
            if domain_file == '': domain_file = None            
        if domain_file is not None: 
            with open(domain_file, 'w') as new_file:
                new_file.write(domain_editor.get(1.0, END))
                new_file.close()
            domain_window.title(f'[Domain] {os.path.basename(domain_file)}')
        
    def save_instance():
        global inst_file        
        if inst_file is None:
            inst_file = fd.asksaveasfilename(initialfile='instance.rddl',
                                             defaultextension='.rddl',
                                             filetypes=[('RDDL File', '*.rddl*')])
            if inst_file == '': inst_file = None            
        if inst_file is not None: 
            with open(inst_file, 'w') as new_file:
                new_file.write(inst_editor.get(1.0, END))
                new_file.close()
            inst_window.title(f'[Instance] {os.path.basename(inst_file)}')
    
    def save_domain_as():
        global domain_file        
        domain_file = None
        save_domain()
    
    def save_instance_as():
        global inst_file        
        inst_file = None
        save_instance()
        
    def exit_application():
        domain_window.destroy() 
        inst_window.destroy() 
    
    # EDIT functions
    def copy_domain_text():
        domain_editor.event_generate('<<Copy>>')
    
    def copy_instance_text():
        inst_editor.event_generate('<<Copy>>')
    
    def cut_domain_text():
        domain_editor.event_generate('<<Cut>>')
        
    def cut_instance_text():
        inst_editor.event_generate('<<Cut>>')
    
    def paste_domain_text():
        domain_editor.event_generate('<<Paste>>')
        
    def paste_instance_text():
        inst_editor.event_generate('<<Paste>>')
    
    # policy SELECT functions
    def _fill_policy_window(policy_name, caption):
        policy_editor.delete(1.0, END)
        policy_editor.insert(1.0, load_policy(policy_name))
        policy_window.title(f'[Policy] {caption}')
    
    def load_noop():
        _fill_policy_window('noop', 'NoOp')
    
    load_noop()
        
    def load_random(): 
        _fill_policy_window('random', 'Random')
    
    def load_jax_slp():
        _fill_policy_window('jax_slp', 'JAX-SLP')
        
    def load_jax_replan():
        _fill_policy_window('jax_replan', 'JAX-SLP-Replan')
        
    def load_jax_drp():
        _fill_policy_window('jax_drp', 'JAX-DRP')
        
    def load_gurobi_replan():
        _fill_policy_window('gurobi_replan', 'Gurobi-SLP-Replan')
        
    def load_sb3_ppo():
        _fill_policy_window('sb3_ppo', 'StableBaselines3-PPO')
        
    # policy RUN functions
    def _evaluate(record):
        global domain_file, inst_file, viz
        save_domain()
        save_instance()
        if domain_file is not None and inst_file is not None:
            evaluate_policy_fn(domain_file, inst_file, policy_editor, viz, record)
    
    def evaluate():
        _evaluate(None)
    
    def record():
        _evaluate(fd.askdirectory())
        
    # create menu bars
    domain_menu = Menu(domain_window)
    inst_menu = Menu(inst_window)
    policy_menu = Menu(policy_window)
    
    # domain file menu
    domain_file_menu = Menu(domain_menu, tearoff=False, activebackground='DodgerBlue')
    domain_file_menu.add_command(label='New Domain', command=create_domain)
    domain_file_menu.add_separator()
    domain_file_menu.add_command(label='Load Domain from Repository...', command=open_from_dialog)
    domain_file_menu.add_command(label='Load Domain from File...', command=open_domain)
    domain_file_menu.add_separator()
    domain_file_menu.add_command(label='Save Domain', command=save_domain)
    domain_file_menu.add_command(label='Save Domain As...', command=save_domain_as)
    domain_file_menu.add_separator()
    domain_file_menu.add_command(label='Exit', command=exit_application)
    domain_menu.add_cascade(label='File', menu=domain_file_menu)
    
    # domain edit menu
    domain_edit_menu = Menu(domain_menu, tearoff=False, activebackground='DodgerBlue')
    domain_edit_menu.add_command(label='Copy', command=copy_domain_text)
    domain_edit_menu.add_command(label='Cut', command=cut_domain_text)
    domain_edit_menu.add_command(label='Paste', command=paste_domain_text)
    domain_menu.add_cascade(label='Edit', menu=domain_edit_menu)
    
    # instance file menu
    inst_file_menu = Menu(inst_menu, tearoff=False, activebackground='DodgerBlue')
    inst_file_menu.add_command(label='New Instance', command=create_instance)
    inst_file_menu.add_separator()
    inst_file_menu.add_command(label='Load Instance from File...', command=open_instance)
    inst_file_menu.add_separator()
    inst_file_menu.add_command(label='Save Instance', command=save_instance)
    inst_file_menu.add_command(label='Save Instance As...', command=save_instance_as)
    inst_menu.add_cascade(label='File', menu=inst_file_menu)
    
    # instance edit menu
    inst_edit_menu = Menu(inst_menu, tearoff=False, activebackground='DodgerBlue')
    inst_edit_menu.add_command(label='Copy', command=copy_instance_text)
    inst_edit_menu.add_command(label='Cut', command=cut_instance_text)
    inst_edit_menu.add_command(label='Paste', command=paste_instance_text)
    inst_menu.add_cascade(label='Edit', menu=inst_edit_menu)
    
    # policy load menu
    policy_load_menu = Menu(policy_menu, tearoff=False, activebackground='DodgerBlue')
    policy_load_menu.add_command(label='No-Op', command=load_noop)
    policy_load_menu.add_command(label='Random', command=load_random)
    policy_load_menu.add_separator()
    policy_load_menu.add_command(label='JAX Planner (SLP)', command=load_jax_slp)
    policy_load_menu.add_command(label='JAX Planner (SLP+Replan)', command=load_jax_replan)
    policy_load_menu.add_command(label='JAX Planner (DRP)', command=load_jax_drp)
    policy_load_menu.add_separator()
    policy_load_menu.add_command(label='Gurobi Planner (SLP+Replan)', command=load_gurobi_replan)
    policy_load_menu.add_separator()
    policy_load_menu.add_command(label='Stable-Baselines3 (PPO)', command=load_sb3_ppo)
    policy_menu.add_cascade(label='Select', menu=policy_load_menu)
    
    # policy run menu
    policy_run_menu = Menu(policy_menu, tearoff=False, activebackground='DodgerBlue')
    policy_run_menu.add_command(label='Evaluate', command=evaluate)
    policy_run_menu.add_command(label='Record', command=record)
    policy_menu.add_cascade(label='Run', menu=policy_run_menu)
    
    # assign menu bar to window
    domain_window.config(menu=domain_menu)
    inst_window.config(menu=inst_menu)
    policy_window.config(menu=policy_menu)

