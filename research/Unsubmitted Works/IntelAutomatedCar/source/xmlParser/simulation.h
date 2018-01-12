#pragma once

#include <cstdio>
#include <cstring>
#include <vector>
#include <map>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <assert.h>

#include "tinyxml2.h"

#include "userCar.h"
#include "sumoCar.h"

using namespace std;

class Simulation
{
public:
	Simulation();
	~Simulation();

	// Read the log file file and uses it to set the raw data of all the elements of the simulation 
	int ReadFile(const char *file, vector<int>& collision_vct, vector<pair<double,bool>>& giraffe_vct);

	int ReadCollision(const char *file, vector<int>& collision_vct);
	int ReadGiraffe(const char *file, vector<pair<double,bool>>& giraffe_vct);

	// Time Stamp value.
	int time_stamp_;
	// absolut time for each step
	std::vector<double> time_;
	//Returns the total duration of the simulation
	double Duration();
	
	//Collisions : timestamps
	std::vector<int> collision_times;

	// Car driven by the user
	UserCar user_;
	// At each time step, lists all the visible sumo cars
	std::vector<std::vector<SumoCar *>> visible_cars_;
	// Find a pointer to a Sumo car thanks to its id.
	std::map<std::string, SumoCar *> cars_;

	// Compute all the statistics relative to this simulations
	void Initialize();

	// Y value of the three lanes
	std::array<double, 3> lanes_Y_;
	// Lanes' width
	double lanes_width_;
	// Lanes' width/2
	double lanes_half_width_;

	// Checks the user current lane
	// Returns true if the car with Y coordinate yCar is on the lane lane.
	bool IsOnLane(double yCar, int lane);
	// Set the lane on which the user car is for each time step.
	void SetUserOnLane();

	// returns the sumo car directly in front of the user (on the same lane)
	SumoCar * InFrontOfUser(int inst, int lane);
	// returns the sumo car directly behind the user (on the same lane)
	SumoCar * BehindUser(int inst, int lane);
	// Sets the cars in front and behind the user for each time step
	void setCarsAroundUser();

	// Print the statistics calculated in a CSV file named filename.
    void PrintCSV(const char* userid, const char* mode, const char* d_dataPath, const char* d_collisionPath);
};

