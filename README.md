# Analyzing Compilable State for a CS1 Course

This repository contains a data pipeline and notebook to analyze keystroke data from a CS 1 University Course.
The data pipeline can be run by calling `pipe.sh` in the root of the repository after copying down the keystroke data from the Harvard Dataverse to the respective folders under `source_data`:
- 2019 data https://doi.org/10.7910/DVN/6BPCXN
- 2021 data https://doi.org/10.7910/DVN/BVOF7S

This will take a while to run but should only need to be run once before using the notebook.

The notebook can be run using jupyter lab using the command `jupyter-lab` from the notebooks folder after setting up a python environment and installing the dependencies listed in `requirements.txt`.
