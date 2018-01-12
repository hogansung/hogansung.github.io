#include <assert.h>
#include "simulation.h"

using namespace std;

int main(int argc, char **argv) {
	string dataPath;
	string collisionPath;
	string giraffePath;
    string userID;
    string userMode;
	string d_dataPath;
	string d_collisionPath;
  
	if (argc == 7) {
	    dataPath = argv[1];
	    collisionPath = argv[2];
	    giraffePath = "";
	    userID = argv[3];
	    userMode = argv[4];
	    d_dataPath = argv[5];
	    d_collisionPath = argv[6];
    }
    else if (argc == 8) {
	    dataPath = argv[1];
	    collisionPath = argv[2];
	    giraffePath = argv[3];
	    userID = argv[4];
	    userMode = argv[5];
	    d_dataPath = argv[6];
	    d_collisionPath = argv[7];
    }
    else if (argc == 6) {
    }
    else {
		std::cout << "ERROR. Usage : ./Main dat.xml col.xml [giraffe.xml] userID userMode d_dat.xml d_col.xml, " << std::endl;
		exit(EXIT_FAILURE);
	}

    vector<int> collision_vct;
    vector<pair<double,bool>> giraffe_vct;

	Simulation simu;
	simu.ReadCollision(collisionPath.c_str(), collision_vct);
	if (giraffePath != "") {
	    simu.ReadGiraffe(giraffePath.c_str(), giraffe_vct);
    }
	simu.ReadFile(dataPath.c_str(), collision_vct, giraffe_vct);
	simu.Initialize();
	simu.PrintCSV(userID.c_str(), userMode.c_str(), d_dataPath.c_str(), d_collisionPath.c_str());
	
	return 0;
}   

