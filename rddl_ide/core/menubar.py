import os
import tkinter as tk
from tkinter import END, Menu
import tkinter.filedialog as fd

from core.execution import evaluate_policy_fn

DOMAIN_TEMPLATE = '''
domain Untitled {
        
    types {
    };
            
    pvariables {
    };
        
    cpfs {
    };
                
    reward = ;        
}
'''

INSTANCE_TEMPLATE = '''
non-fluents nf_Untitled {

    domain = Untitled;
    
    objects {
    };
    
    non-fluents {
    };
}

instance Untitled_inst {

    domain = Untitled;

    non-fluents = nf_Untitled;
    
    init-state {
    };

    max-nondef-actions = pos-inf;
    horizon = 100;
    discount = 1.0;
}
'''


def load_policy(name):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    file = open(os.path.join(abs_path, 'policies', name + '.py'), 'r')
    content = file.read()
    file.close()
    return content    


def assign_menubar_functions(domain_window, inst_window, policy_window,
                             domain_editor, inst_editor, policy_editor):
    domain_file, inst_file, viz, vectorized = None, None, None, False
    
    # FILE functions
    def create_domain():
        global domain_file, viz
        domain_file, viz = None, None
        domain_window.title('[Domain] Untitled.rddl')
        domain_editor.delete(1.0, END)
        domain_editor.insert(1.0, DOMAIN_TEMPLATE)
        
    def create_instance():
        global inst_file
        inst_file = None
        inst_window.title('[Instance] Untitled.rddl')
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
            domain_file = fd.asksaveasfilename(initialfile='Untitled.rddl',
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
            inst_file = fd.asksaveasfilename(initialfile='Untitled.rddl',
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
    
    def load_noop():
        global vectorized
        vectorized = False
        policy_editor.delete(1.0, END)
        policy_editor.insert(1.0, load_policy('noop'))
        policy_window.title('[Policy] NoOp')
    
    load_noop()
    
    def load_random(): 
        global vectorized
        vectorized = False
        policy_editor.delete(1.0, END)
        policy_editor.insert(1.0, load_policy('random'))
        policy_window.title('[Policy] Random')
    
    def load_jax_slp():
        global vectorized
        vectorized = True
        policy_editor.delete(1.0, END)
        policy_editor.insert(1.0, load_policy('jax_slp'))
        policy_window.title('[Policy] JAX-SLP')
        
    def load_jax_drp():
        global vectorized
        vectorized = True
        policy_editor.delete(1.0, END)
        policy_editor.insert(1.0, load_policy('jax_drp'))
        policy_window.title('[Policy] JAX-DRP')
        
    # RUN functions
    def evaluate():
        global domain_file, inst_file, viz, vectorized
        save_domain()
        save_instance()
        if domain_file is not None and inst_file is not None:
            evaluate_policy_fn(domain_file, inst_file, policy_editor, viz, None, vectorized)
    
    def record():
        global domain_file, inst_file, viz, vectorized
        save_domain()
        save_instance()
        if domain_file is not None and inst_file is not None:
            record = fd.askdirectory()
            evaluate_policy_fn(domain_file, inst_file, policy_editor, viz, record, vectorized)
        
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
    policy_load_menu.add_command(label='Load No-Op', command=load_noop)
    policy_load_menu.add_command(label='Load Random', command=load_random)
    policy_load_menu.add_separator()
    policy_load_menu.add_command(label='Load JAX Planner (SLP)', command=load_jax_slp)
    policy_load_menu.add_command(label='Load JAX Planner (DRP)', command=load_jax_drp)
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

