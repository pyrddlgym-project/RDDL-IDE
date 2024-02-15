# RDDL-IDE

Author: [Mike Gimelfarb](https://mike-gimelfarb.github.io)

Graphical integrated development environment for RDDL.

This directory provides:
1. an IDE specifically designed for reading and writing RDDL descriptions
2. comprehensive integration of the pyRDDLGym [ecosystem](https://github.com/pyrddlgym-project), 
supports training, evaluation and visualization of various planners 
(e.g. [JAX planner](https://github.com/pyrddlgym-project/pyRDDLGym-jax), [Gurobi planner](https://github.com/pyrddlgym-project/pyRDDLGym-gurobi), [RL](https://github.com/pyrddlgym-project/pyRDDLGym-rl)), and your own custom policies in a single mouse click!

## Contents
- [Installation](#installation)
- [Running the IDE](#running-the-ide)

## Installation

To install, you will need ``pyRDDLGym>=2.0`` from [here](https://github.com/pyrddlgym-project/pyRDDLGym) 
and``tk`` (tkinter). To run the various baselines, you will also need the 
[prerequisite packages](https://github.com/pyrddlgym-project). 

To install directly with pip into the current directory with all of its requirements:

```shell
pip install git+https://github.com/pyrddlgym-project/RDDL-IDE .
```

## Running the IDE

To launch the IDE, simply type:

```shell
python -m rddl_ide.run
```
