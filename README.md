# flowAroundTriangles
This is a small example project, that showcases the possibility of using a surrogate model to estimate the drag coefficient of arbitrary triangles.

The project is divided in four parts:
1. Mesh creation
2. CFD calculation
3. Neural network model training
4. Dash app for data exploration

The basic idea is to use OpenFOAM to calculate the flow around many differently shaped triangles at different Reynolds numbers and obtain the resulting drag coefficient. These results are then used to train a neural network. Finally the neural network can be used to estimate the drag coefficient for arbitrary triangles.

## Prerequisites
Tested with the following set-up:
* OpenFoam-6
* Python 3.8
  * Tensorflow 2.5.0
  * Scikit-learn 0.23.1
  * Pandas 1.0.5
  * Numpy 1.19.5
  * Matplotlib 3.2.2
  * Plotly 4.14.1
  * Dash 1.18.1

## Mesh creation
The bash script `runCases.sh` first creates the required mesh for each case using the set-up in the `mesh` folder. By changing the `blockMeshDict` in the `mesh/system` folder meshes for a large number of triangles are craeted. `blockMesh` creates a structured mesh of hexahedral blocks. One resulting mesh is shown in the image below.

<img src="https://github.com/axelfiedler/flowAroundTriangles/blob/main/mesh_example.PNG" alt="Example of an automatically generated hex mesh around a triangle" width="300"/>

## CFD calculation ##
After a mesh for one triangle is created, it will be copied from the `mesh` folder to the `simple_laminar` folder. There the inlet velocity in `0/U` as well as the velocity at infinity in `system/controlDict` will be updated according to the current Reynolds number. After that the case will be decomposed for parallel computing. The default number of processors in `runCases.sh` is 4, this can be changed in line `101` and `104` if a system with more processors is used. The mesh is renumbered after decomposition for speed-up and a `simpleFoam` calculation is started. After the simulation is finished the resulting `forceCoeffs.dat` file, that contains the drag coefficient is copied to the results folder `C_D` and the next calculation is started by generating the next mesh. E.g. for the mesh that was shown above the resulting velocity field is shown below.

<img src="https://github.com/axelfiedler/flowAroundTriangles/blob/main/flow_example.PNG" alt="Example of calculated velocity field" width="300"/>

## Neural network model training ##
First `read_files.py` is used to store the simulation data in a Pandas DataFrame, that can easily be used in the further steps.
