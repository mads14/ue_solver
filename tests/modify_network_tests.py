
from ue_solver.modify_network import *
from ue_solver.conversions import *


# def add_virtual_nodes_test():
#     networkx_f = 'resources/network/sf_secondary/network_graph.txt'
#     taz_shpf = 'resources/shapefiles/bay_area_tazs'
#     n_neighbors = 5
#     G, taz_dict = add_virtual_nodes(networkx_f, taz_shpf, n_neighbors)
#     # add some tests here

def test_label_road_network():
    ca_cities_shp = 'resources/shapefiles/ca_cities_2014'
    geojson_starter = 'resources/network/testnetwork/new_selection_without_cities.geojson'
    road_network_geojson = 'resources/network/testnetwork/new_function_result.geojson'
    label_road_network(ca_cities_shp, geojson_starter, 'NAME', road_network_geojson, 'city')
    append_city_geojson = 'resources/network/testnetwork/old_function_result.geojson'
    append_city_names(ca_cities_shp, geojson_starter, append_city_geojson)
    geojson_new = gpd.read_file(road_network_geojson).shape[0]
    geojson_old = gpd.read_file(append_city_geojson).shape[0]
    assert geojson_new == geojson_old 

# def test_append_city_names():
#     ca_cities_shp = 'resources/shapefiles/ca_cities_2014'
#     geojson_f = 'resources/network/sf_secondary_all_roads_0p8/network.geojson'
#     append_city_names(ca_cities_shp, geojson_f)
    

# def update_capacity_test():
#     attr_dict = {'county': ['Alameda']}
#     percent_cap = .5
#     geojson_inf = 'resources/network/sf_secondary/network.geojson'
#     geojson_outf = 'resources/network/sf_secondary_alameda_0p5/network.geojson'
#     graph_outf = 'resources/network/sf_secondary_alameda_0p5/network_graph.txt'
#     update_capacity(attr_dict, percent_cap, geojson_inff, 
#                     geojson_outf, graph_outf)


# def remove_duplicate_links_test():
    
#     geojson_inf = 'resources/network/sf_secondary_all/network.geojson'
#     geojson_outf = 'resources/network/sf_secondary_all/network.geojson'
#     remove_duplicate_links(geojson_in, geojson_out)

# def cut_links_test():
#     geojson_inf = 'resources/network/sf_secondary_all_roads_0p8/network.geojson'
#     links_f = 'resources/cut_links/SLR025_KT_cutlinks.csv'
#     geojson_outf = 'resources/network/sf_secondary_SLR025_KT_cutlinks/network.geojson'
#     graph_outf = 'resources/network/sf_secondary_SLR025_KT_cutlinks/network_graph.txt'
#     cut_links(geojson_infile, links_f, geojson_outf, graph_outf)