#include "userCar.h"





UserCar::UserCar()
{
	position_ = std::vector<std::array<double, 2>>();
	rotation_ = std::vector<double>();
	velocity_ = std::vector<std::array<double, 2>>();
	steer_ = std::vector<double>();
	pedal_ = std::vector<double>();
	rotation_x_ = std::vector<double>();
	rotation_z_ = std::vector<double>();
	collision_ = std::vector<bool>();
	giraffe_st = std::vector<bool>();
	giraffe_ed = std::vector<bool>();
}


UserCar::~UserCar()
{
}

// Add a new step in the car position and state.
void UserCar::AddTimestep(double position_x, double position_z, double rotation_x, double rotation_y, double rotation_z, double velocity_x, double velocity_z, double steert, double throttlet, bool b_collision, bool b_giraffe_st, bool b_giraffe_ed)
{
	std::array<double, 2> pos; pos[0] = position_x; pos[1] = position_z;
	position_.push_back(pos);
	double rot; rot = rotation_y;
	rotation_.push_back(rot);
	rotation_x_.push_back(rotation_x);
	rotation_z_.push_back(rotation_z);
	std::array<double, 2> vel; vel[0] = velocity_x; vel[1] = velocity_z;
	velocity_.push_back(vel);

	steer_.push_back(steert);
	pedal_.push_back(throttlet);

	collision_.push_back(b_collision);
	giraffe_st.push_back(b_giraffe_st);
	giraffe_ed.push_back(b_giraffe_ed);
}



void UserCar::Initialize(std::vector<double> &time) {

	set_velocity_norm();
	set_acceleration(time);

	// Distance to the cars behind and in front
	set_dist_front();
	set_dist_back();
	set_velo_front();
	set_velo_back();
}

/*** DATA PREPROCESSING ***/

/* Compute the norm of the velocity*/
void UserCar::set_velocity_norm() {
	std::array<double, 2> vel;
	for (int i = 0; i < velocity_.size(); i++) {
		vel = velocity_[i];
		velocity_norm_.push_back(sqrt(vel[0] * vel[0] + vel[1] * vel[1]));
	}
}

/** Derivation functions **/
void UserCar::set_acceleration(std::vector<double>& time) {
	// initial aceleration is 0
	acceleration_.push_back(0);
	double cur = velocity_norm_[0];
	double prev;
	double delta;
	for (int i = 1; i < velocity_norm_.size(); i++) {
		prev = cur;
		cur = velocity_norm_[i];
		delta = time[i] - time[i - 1];
		acceleration_.push_back((cur - prev) / delta);
	}
}

void UserCar::set_dist_front() {
	for (int i = 0; i < in_front_.size(); i++){
		if (in_front_[i] == NULL) dist_front_.push_back(-1);
		else dist_front_.push_back((in_front_[i])->GetPositionX(i) - (position_[i])[0] - (in_front_[i])->GetLength());

		if (in_front_l[i] == NULL) dist_front_l.push_back(-1);
		else dist_front_l.push_back((in_front_l[i])->GetPositionX(i) - (position_[i])[0] - (in_front_l[i])->GetLength());

		if (in_front_r[i] == NULL) dist_front_r.push_back(-1);
		else dist_front_r.push_back((in_front_r[i])->GetPositionX(i) - (position_[i])[0] - (in_front_r[i])->GetLength());
	}
}

void UserCar::set_dist_back() {
	for (int i = 0; i < behind_.size(); i++){
		if (behind_[i] == NULL) dist_back_.push_back(-1);
		else dist_back_.push_back( (position_[i])[0] - (behind_[i])->GetPositionX(i) );

		if (behind_l[i] == NULL) dist_back_l.push_back(-1);
		else dist_back_l.push_back( (position_[i])[0] - (behind_l[i])->GetPositionX(i) );

		if (behind_r[i] == NULL) dist_back_r.push_back(-1);
		else dist_back_r.push_back( (position_[i])[0] - (behind_r[i])->GetPositionX(i) );
	}
}

void UserCar::set_velo_front(){
	for (int i = 0; i < in_front_.size(); i++){
		if (in_front_[i] == NULL) velo_front_.push_back(-1);
		else velo_front_.push_back((in_front_[i])->GetVelocity(i));

		if (in_front_l[i] == NULL) velo_front_l.push_back(-1);
		else velo_front_l.push_back((in_front_l[i])->GetVelocity(i));

		if (in_front_r[i] == NULL) velo_front_r.push_back(-1);
		else velo_front_r.push_back((in_front_r[i])->GetVelocity(i));
	}
}
void UserCar::set_velo_back(){
	for (int i = 0; i < behind_.size(); i++){
		if (behind_[i] == NULL) velo_back_.push_back(-1);
		else velo_back_.push_back((behind_[i])->GetVelocity(i));

		if (behind_l[i] == NULL) velo_back_l.push_back(-1);
		else velo_back_l.push_back((behind_l[i])->GetVelocity(i));

		if (behind_r[i] == NULL) velo_back_r.push_back(-1);
		else velo_back_r.push_back((behind_r[i])->GetVelocity(i));
	}

}

/*****Tools functions *****/

std::vector<double> derivation(std::vector<double> &l, std::vector<double> &time) {
	std::vector<double> der;
	der.push_back(0);
	double cur = l[0];
	double prev, delta;
	for (int i = 1; i < l.size(); i++) {
		prev = cur;
		cur = l[i];
		delta = time[i] - time[i - 1];
		der.push_back((cur - prev) / delta);
	}
	return der;
}
