# ue_solver

### Introduction

This UE Solver takes an origin-destination demand input (origin, destination, number of cars taking this path) and a road 
network and assigns a path for each trip such that **no traveler can decrease travel time by shifting to a new path.** 
* * *
The solver is finding the [static user equilibrium](https://en.wikipedia.org/wiki/Route_assignment#Equilibrium_assignment) 
network flows. The travel time per road segment (link) is assumed to be a function of the link's flow/capacity and is set 
according to the Bureau of Public Roads (BPR) link congestion function:

![equation](http://latex.codecogs.com/gif.latex?TT_a%20%3D%20TT_%7Ba%2Cfree-flow%7D%20%5Cleft%28%20%7B1%20&plus;%200.15%5Cleft%28%20%7B%5Cfrac%7B%7Bv_a%20%7D%7D%7B%7Bc_a%20%7D%7D%7D%20%5Cright%29%5E4%20%7D%20%5Cright%29)

where ![equation](http://latex.codecogs.com/gif.latex?TT_a) = Average Travel time on link a; ![equation](http://latex.codecogs.com/gif.latex?TT_%7Ba%2Cfree-flow%7D) = Free flow travel time on link a; ![equation](http://latex.codecogs.com/gif.latex?v_a) = volume of traffic on link a per unit of time (somewhat more accurately: flow attempting to use link a); and ![equation](http://latex.codecogs.com/gif.latex?c_a) = capacity of link a per unit of time. 

* * *

In addition to finding the network static user equilibrium network flows, this UE Solver package has several methods 
to simulate alternative road networks. Reasons for altering the road network include increasing/decreasing road capacity, 
simulating road closures, floods, or any sort of disruption in the original road network. 

Processing the results will convert the assigned travel to a geojson file. In addition, processing results can calculate 
VMT, VHT, and delay.

### Resources
* See [UE_processes.ipynb](https://github.com/mads14/ue_solver/blob/master/UE_processes.ipynb) for a walk-through of the
features in this sovler. 
* See [the documenatation](https://mads14.github.io/ue_solver/build/html/index.html#) for more details on the methods in this package.
* And [sample Bay Area input files](https://paper.dropbox.com/doc/Bay-Area-UE-Solver-resources-W9SLplNM8J3ljws9VFZaF)

The image below represent the baseline morning commute congestion in the San Francisco Bay Area, as determined by the UE solver.

<img src="https://www.dropbox.com/s/hu3u7kyawc408jw/ue_result.png?raw=1" alt="Drawing" style="width: 400px;"/>
