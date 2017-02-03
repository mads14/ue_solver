from ue_solver.map_demand import *


def map_demand_to_virtual_node_test():
	scale = 5.0
	scale_str = str(scale).replace('.','p')
	map_demand_to_virtual_node(taz_demand_csv='resources/demand/TAZ_sf_demand.csv', 
		                       taz_dict_f = 'resources/demand/sf_freeway_virtual/taz_dict.txt', 
		                       scale=scale, 
		                       demand_outf='resources/demand/sf_freeway_virtual/demand_scale_%s.txt'%scale_str)

