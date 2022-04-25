## Desired features from conversation:
* control the wrapper with command line args through ```argparse```
* print user's config params into output directory through ```json dump```
* visualize results through ```pygmt```
* visualize 1D Earth model as graph of bulk modulus, viscosity, etc.
* depend on "VISCO1D-v3" from Fred's Github, not any other version

## First-draft Specifics:

### 1. Code inputs
* Fault model file with input slip scenario
* Earth model file
* Results directory name?

### 2. Interface with visco1d
* possibly in UUID or scratch directory

### 3. Code outputs
* displacements and time series, Fred's format and/or modern format
* plots of things
* reporting on user parameters, arg json, earth model


### Kathryn's design notes
* Would love to keep visualization functions as separate as possible from the rest of the code. Cleanest: depends only on Fred's original output files.  
