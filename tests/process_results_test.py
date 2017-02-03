from ue_solver.process_results import *

def results_to_geojson_test():
	results_f = 'resources/results/sf_secondary/demand_1p5_gap100.txt'
	network_geojson = 'resources/network/sf_secondary/network.geojson'
	geojson_outf = 'resources/results/sf_secondary/demand_1p5_gap100.geojson'
	results_to_geojson(results_f, network_geojson, geojson_outf)