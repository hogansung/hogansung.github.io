#include "sumoCar.h"
#include <iostream>
#include <assert.h>

SumoCar::SumoCar(const char *type)
{
	position_ = std::map<int, std::array<double, 2>>();

	if (strncmp("Truck", type, 5) == 0){
		length = 4.2;
		width = 2.0;
	}
	else if (strncmp("MP4", type, 3) == 0){
		length = 3.9;
		width = 1.8;
	}
	else if (strncmp("F360", type, 4) == 0){ // with id
		length = 3.6;
		width = 1.6;
	}
	else if (strncmp("R34", type, 3) == 0){ // with id
		length = 3.9;
		width = 1.4;
	}
	else if (strncmp("Bus", type, 3) == 0){
		length = 10.5;
		width = 2.3;
	}
	else if (strncmp("Coupe", type, 5) == 0){
		length = 3.5;
		width = 1.4;
	}
	else if (strncmp("SUV", type, 3) == 0){
		length = 4.2;
		width = 2.1;
	}
	else if (strncmp("Cio", type, 3) == 0){
		length = 3.2;
		width = 1.4;
	}
	else if (strncmp("CR7", type, 3) == 0){ // with id
		length = 3.6;
		width = 1.6;
	}
	else if (strncmp("Catamount", type, 9) == 0){
		length = 4.1;
		width = 1.7;
	}
	else if (strncmp("Saloon", type, 6) == 0){
		length = 4.3;
		width = 1.9;
	}
	else if (strncmp("School Bus", type, 10) == 0){
		length = 11.0;
		width = 2.4;
	}
	else if (strncmp("Ambulance", type, 9) == 0){
		length = 5.0;
		width = 2.1;
	}
	else if (strncmp("Police", type, 6) == 0){
		length = 4.3;
		width = 1.4;
	}
	else if (strncmp("Pickup", type, 6) == 0){
		length = 5.3;
		width = 1.8;
	}
	else if (strncmp("Blue Sedan", type, 10) == 0){
		length = 3.3;
		width = 1.5;
	}
	else {
        assert(false);
    }
}


SumoCar::~SumoCar()
{
}

void SumoCar::AddPosition(int timestep, double position_x, double position_y) {
	std::array<double, 2> pos = { position_x, position_y };
	position_[timestep] = pos;
	//position_.insert(std::pair<int, std::array<double, 2> >(timestep, pos));
}

void SumoCar::ComputeVelocity(std::vector<double> &time) {
	int prev = -10;
	std::vector<int> non_set = std::vector<int>();
	for (const auto &it_pos : position_){
		int frame = it_pos.first;
		if (it_pos.first > prev + 1){
			non_set.push_back(it_pos.first);
		}
		else{
			std::array<double, 2> cur_pos = it_pos.second;
			std::array<double, 2> pre_pos = position_[prev];

			double norm_diff = sqrt((pre_pos[0] - cur_pos[0])*(pre_pos[0] - cur_pos[0]) + (pre_pos[1] - cur_pos[1])*(pre_pos[1] - cur_pos[1]));
			double delta = time[it_pos.first] - time[prev];
			velocity_[it_pos.first]=norm_diff/delta;
		}
		prev = it_pos.first;
	}

	for (const auto &it_f : non_set){
	    if (velocity_.count(it_f + 1) == 0) {
			velocity_[it_f] = -1;
        }
        else {
            velocity_[it_f] = velocity_[it_f + 1];
        }
	}
}


double SumoCar::GetPositionX(int timestep){
	return (position_.at(timestep))[0];
}
double SumoCar::GetPositionY(int timestep){
	return (position_.at(timestep))[1];
}
double SumoCar::GetVelocity(int timestep){
	return velocity_[timestep];
}

double SumoCar::GetLength(){
	return length;
}
double SumoCar::GetWidth(){
    return width;
}
