# ue_solver

### Introduction

This UE Solver takes an origin-destination demand input (origin, destination, number of cars taking this path) and a road 
network and assigns a path for each trip such that **no traveler can decrease travel time by shifting to a new path.** 
* * *
The solver is finding the [static user equilibrium](https://en.wikipedia.org/wiki/Route_assignment#Equilibrium_assignment) 
network flows. The travel time per road segment (link) is assumed to be a function of the link's flow/capacity and is set 
according to the Bureau of Public Roads (BPR) link congestion function:

$$TT_a = TT_{a,free-flow} \left( {1 + 0.15\left( {\frac{{v_a }}{{c_a }}} \right)^4 } \right)$$

where $TT_a$ = Average Travel time on link a; $ TT_{free-flow}$ = Free flow travel time on link a; $v_a$ = volume of traffic on link a per unit of time (somewhat more accurately: flow attempting to use link a); and $c_a$ = capacity of link a per unit of time. 

* * *

In addition to finding the network static user equilibrium network flows, this UE Solver package has several methods 
to simulate alternative road networks. Reasons for altering the road network include increasing/decreasing road capacity, 
simulating road closures, floods, or any sort of disruption in the original road network. 

Processing the results will convert the assigned travel to a geojson file. In addition, processing results can calculate 
VMT, VHT, and delay.


See [the UE_processes.ipynb](https://github.com/mads14/ue_solver/blob/master/UE_processes.ipynb) for a walk-through of the
features in this sovler. 
Also see [the documenatation](https://mads14.github.io/ue_solver/build/html/index.html#).
And [sample Bay Area input files](https://paper.dropbox.com/doc/Bay-Area-UE-Solver-resources-W9SLplNM8J3ljws9VFZaF)

The image below represent the baseline morning commute congestion in the San Francisco Bay Area, as determined by the UE solver 
given the sample inputs

<img src="https://www.dropbox.com/s/hu3u7kyawc408jw/ue_result.png?raw=1" alt="Drawing" style="width: 500px;"/>
