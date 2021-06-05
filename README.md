# flowAroundTriangles
This is a small example project, that showcases the possibility of using a surrogate model to estimate the drag coefficient of arbitrary triangles.

The project is divided in four parts:
1. Mesh creation
2. CFD calculation
3. Neural network model training
4. Dash app for data exploration

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
The bash script `runCases.sh` first creates for each cases the required mesh using the set-up in the `mesh` folder.
