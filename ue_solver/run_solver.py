import sys
import subprocess
import os
import time



def run_solver(network_file, demand_file, output_file, distance_factor=0, 
               toll_factor=0, gap=10.0):
    
    distance_factor = str(distance_factor)
    toll_factor = str(toll_factor)
    gap = str(gap)

    #TODO test inputs!! make sure file inputs are right format!
    # print appropriate error messages.
    
    solver_command = " ".join(["M_Steel_Solver/GEF",
                               network_file,
                               demand_file,
                               output_file,
                               distance_factor,
                               toll_factor,gap])

    start = time.time()
    print 'started at', start

    #create and write the .sh file
    writeSolverSh = open("Solver.sh", "w")
    writeSolverSh.write(solver_command)
    writeSolverSh.close()

    # Open bash to run FW algorithm
    print 'Running FW algorithm'
    result = subprocess.check_output(["/bin/bash", "Solver.sh"])
    print 'done in', time.time()-start, 'sec'

from ue_solver.modify_network import add_virtual_nodes
from ue_solver.conversions import graph_to_network_file
from ue_solver.map_demand import demand_to_virtual_node

def run_solver_full(network_graph, taz_demand_f, output_file, taz_shapefile,
                    demand_scale=1.5, distance_factor=0, toll_factor=0, gap=10.0):
    
    # 1. add virtual nodes to network graph (saves taz_dict)
    G, taz_dict = add_virtual_nodes(network_graph, taz_shapefile, n_neighbors=5)

    # 2. convert to network file and save
    network_file = 'resources/network/solver_network_file.txt'
    graph_to_network_file(G, network_file)
    
    # 3. distribute demand
    demand_file = 'resources/demand/solver_demand_file.txt'
    demand_to_virtual_node(taz_demand_f, taz_dict, scale=demand_scale, 
                           demand_outf=demand_file)

    # 4. run solver:
    run_solver(network_file, demand_file, output_file, distance_factor, toll_factor, gap)


