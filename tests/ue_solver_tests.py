from nose.tools import *
import ue_solver
from ue_solver import run_solver

def setup():
    print "SETUP!"

# def run_solver_test():
#     network_file = 'resources/network/sf_freeway_virtual/network_file.txt'
#     demand_file = 'resources/demand/sf_freeway_virtual/demand_scale_5p0.txt'
#     output_file = 'resources/results/sf_freeway_virtual/demand_5p0_gap100.txt'

#     run_solver.run_solver(network_file, demand_file, output_file, distance_factor=0, 
#                           toll_factor=0, gap = 100.0)
def run_solver_full_test():
    # network_graph = 'resources/network/sf_secondary/network_graph.txt'
    # taz_demand_f = 'resources/demand/TAZ_sf_demand.csv'
    # output_file = 'resources/results/sf_secondary/demand_1p5_gap100.txt'
    network_graph = 'resources/network/sf_secondary_SLR025_KT_cutlinks/network_graph.txt'
    taz_demand_f = 'resources/demand/TAZ_sf_demand.csv'
    output_file = 'resources/results/sf_secondary_SLR025_KT_cutlinks/demand_1p5_gap100.txt'

    run_solver.run_solver_full(network_graph, taz_demand_f, output_file, 
                               taz_shapefile='resources/shapefiles/bay_area_tazs',
                               demand_scale = 1.5, distance_factor=0, toll_factor=0, 
                               gap = 100.0)


def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"