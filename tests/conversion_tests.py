from ue_solver.conversions import *

# def graph_to_network_file_test():
#      graph_to_network_file(graph='resources/network/sf_freeway/network_graph.txt', 
#                            filepath='resources/network/sf_freeway/network_file.txt')


# def networkx_to_geojson_test():
#      networkx_to_geojson(graph='resources/network/sf_secondary/network_graph.txt',
#                          geojson_f ='resources/network/sf_secondary/network.geojson', 
#                          simple_geom=False)


def test_geojson_to_networkx():
     g = geojson_to_networkx(geojson_f ='resources/network/testnetwork/selection.geojson', 
                         graph_f='resources/network/testnetwork/selection_graph.txt')
     #check that number of lines in geojson is the same as text 
     geojson_f = 'resources/network/testnetwork/selection.geojson'
     graph_f= 'resources/network/testnetwork/selection_graph.txt'
     num_lines_gjf = sum(1 for line in open(geojson_f))
     geojson = gpd.read_file(geojson_f).shape[0]
     num_edges = g.number_of_edges()
     assert geojson == num_edges
    

     #g.number_of_edges()
     #network to geojson 
     #test if graphs are equal

     