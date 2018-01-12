#pragma once

#include <vector>
#include <array>
#include <iostream>
#include <algorithm>

#include "sumoCar.h"

class UserCar
{
public:
	UserCar();
	~UserCar();

	/*** RAW DATA ***/
	std::vector <std::array<double, 2> > position_; //2D position of the car
	std::vector <double > rotation_;
	std::vector <double > rotation_x_,rotation_z_;

	std::vector <std::array<double, 2> > velocity_; // Rotation in the 2D plan

	std::vector<double> steer_;
	std::vector<double> pedal_; // Throttle pedal when >0, Brake pedal when <0.
    std::vector<bool> collision_;
    std::vector<bool> giraffe_st;
    std::vector<bool> giraffe_ed;

	// Adds the information (=Raw data) from a new timestep
	void AddTimestep(double position_x, double position_z, double rotation_x, double rotation_y, double rotation_z, double velocity_x, double velocity_z, double steer, double throttle, bool b_collision, bool b_giraffe_st, bool b_giraffe_ed);

	void Initialize(std::vector<double> &time);

	/*** PROCESSED DATA ***/

	// Velocity of the car. (norm)
	std::vector<double> velocity_norm_;
	// Acceleration of the car (norm)
	std::vector<double> acceleration_;

	// Computes the velocity of the car
	void set_velocity_norm();
	// Computes the acceleration_ of the car.
	void set_acceleration(std::vector<double> &time);


	// On which lane is the car.
	std::vector<int> on_lane_[3];
	// Which car is directly in front of/behind the user (left/right).
	std::vector<SumoCar *> in_front_, behind_;
	std::vector<SumoCar *> in_front_l, behind_l;
	std::vector<SumoCar *> in_front_r, behind_r;
	// Distance with the precedding/next car (left/right).
	std::vector<double> dist_front_, dist_back_;
	std::vector<double> dist_front_l, dist_back_l;
	std::vector<double> dist_front_r, dist_back_r;
	// Speed of the preceding/next car (left/right).
	std::vector<double> velo_front_, velo_back_;
	std::vector<double> velo_front_l, velo_back_l;
	std::vector<double> velo_front_r, velo_back_r;

	// Measure the distance to the cars in front
	void set_dist_front();
	// Measure the distance to the cars behind
	void set_dist_back();
	// Measure the speed of the cars in front
	void set_velo_front();
	// Measure the speed of the cars behind
	void set_velo_back();

};

