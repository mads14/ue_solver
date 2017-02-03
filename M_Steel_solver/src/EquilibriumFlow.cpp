/*
    Copyright 2008, 2009 Matthew Steel.

    This file is part of EF.

    EF is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    EF is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with EF.  If not, see <http://www.gnu.org/licenses/>.
*/


#include <utility> //For Pair
#include <iostream>
#include <fstream>
#include <cstdlib> //For EXIT_SUCCESS
#include <sstream>
#include <string>
#include <fstream>

#include "MTimer.hpp"
#include "AlgorithmBSolver.hpp"
#include "BarGeraImporter.hpp"
#include "InputGraph.hpp"

using namespace std;

void general(const char* netString, const char* tripString, const char* outputString, double distanceFactor=0.0, double tollFactor=0.0, double gap = 1e-13)
{
    ifstream network(netString), trips(tripString);
    BarGeraImporter bgi(distanceFactor, tollFactor);
	InputGraph ig;
	MTimer timer3;
	bgi.readInGraph(ig, network, trips);
	cout << timer3.elapsed() << endl;
    

	MTimer timer1;

	AlgorithmBSolver abs(ig);
	double time=0.0;
	cout << (time += timer1.elapsed()) << endl;//*/
//*/
	double thisGap;
	for(thisGap = abs.averageExcessCost(); thisGap > gap; thisGap = abs.averageExcessCost()) {
		cout << time << ' ' << thisGap << endl;
		MTimer t2;
		
        // to save the output at each iteratation:
        std::ostringstream ss;
        ss << thisGap;
        std::string s(ss.str());
        std::string c = std::string("resources/temp/output") + s + ".txt";
        ////Output a file with all the flows
        ofstream myfile;
        myfile.open (c.c_str());
        myfile << abs;
        myfile.close();
        
        abs.solve(12);
        time += t2.elapsed();

	}
	cout << time << ' ' << thisGap << endl;
	cout << "flag_here" << endl;
	cout << abs << endl;
        ////Output a file with all the flows
        ofstream myfile;
        myfile.open (outputString);
        myfile << abs;
        myfile.close();
//*/
}

class func {
	public:
		func(double first, double second) : first(first), second(second) {}
		double operator()(double d) { return d*second + first; }
	private:
		double first, second;
};

int main (int argc, char **argv)
{
//	general("networks/ChicagoSketch_net.txt", "networks/ChicagoSketch_trips.txt", 0.04, 0.02);
//	general("networks/Braess/Braess_net.txt", "networks/Braess/Braess_trips.txt");
//	general("networks/OSM_medium/OSM_medium_net_orig.txt", "networks/OSM_medium/OSM_medium_trips_.txt", 0.0, 0.0, 1e-4);
    
// TODO: add error check on argv and info on format?
//    char *pNet = argv[1]
//    char *pTrp = argv[2]
//    char *pOut = argv[3]

    cout << "flag_start" << endl;
    general(argv[1], argv[2], argv[3], atof(argv[4]), atof(argv[5]), atof(argv[6]));

    
    
	// general("networks/Toy_3D/Toy_3D_net.txt", "networks/Toy_3D/Toy_3D_trips.txt", 0.0, 1.0);
	 //Braess' network paradox
/*	InputGraph g;
	g.setNodes(5);
	g.addEdge(0, 1, func(0.5,0));
	g.addEdge(0, 4, func(0.5,0));
	g.addEdge(0, 2, func(1.5,0));
	g.addEdge(0, 3, func(2.5,0));
	g.addEdge(1, 4, func(0.5,3));
	g.addEdge(2, 4, func(0.5,1));
	g.addEdge(3, 4, func(0.5,2));
	
	g.addDemand(0, 4, 20.0);
	AlgorithmBSolver abs(g);
	cout << abs << endl;
	abs.solve(1);
	cout << abs << endl;
	//*/
}
