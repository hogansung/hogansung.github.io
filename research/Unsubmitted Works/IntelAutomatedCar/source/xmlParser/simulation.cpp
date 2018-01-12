#include "simulation.h"
#include <time.h>

using namespace std;
using namespace tinyxml2;

Simulation::Simulation()
{
	time_ = std::vector<double>();
	cars_ = std::map<string, SumoCar *>();
	visible_cars_ = std::vector<std::vector<SumoCar*>>();

	lanes_width_ = 4.1;
	lanes_Y_[0] = -10.25;
	lanes_Y_[1] = -6.15;
	lanes_Y_[2] = -2.05;
	lanes_half_width_ = lanes_width_ * 0.5;
}


Simulation::~Simulation()
{
}

#ifndef XMLCheckResult
#define XMLCheckResult(a_eResult) if (a_eResult != XML_SUCCESS) { printf("Error: %i\n", a_eResult); return a_eResult; }
#endif

int Simulation::ReadFile(const char *file, vector<int>& collision_vct, vector<pair<double,bool>>& giraffe_vct)
{
	//Open the document
	XMLDocument xmlDoc;
	XMLError eResult = xmlDoc.LoadFile(file);
	XMLCheckResult(eResult);

	XMLNode * timeRoot = xmlDoc.FirstChild();
	if (timeRoot == nullptr) return XML_ERROR_FILE_READ_ERROR;

	//get the TimeStamp
	XMLCheckResult(eResult);

	XMLElement * pElement = xmlDoc.FirstChildElement();
	if (pElement == nullptr) return XML_ERROR_PARSING_ELEMENT;
	eResult = pElement->QueryIntAttribute("timeStamp", &time_stamp_);
	XMLCheckResult(eResult);

	// read all steps
	XMLElement * step = pElement->FirstChildElement("step");
	double tmp;
	int time_step = 0;

	vector<int>::iterator c_it = collision_vct.begin();
    vector<pair<double,bool>>::iterator g_it = giraffe_vct.begin();

	while (step != nullptr)
	{
		//read the time
		eResult = step->QueryDoubleAttribute("time", &tmp);
		time_.push_back(tmp);
		
		//read the user car
		pElement = step->FirstChildElement("UserCar");

		double posX, posY, posZ, rotX, rotY, rotZ, velX, velY, velZ, steer, throttle, brake;
		bool b_collision = false;
		bool b_giraffe_st = false;
		bool b_giraffe_ed = false;

		eResult = pElement->QueryDoubleAttribute("PositionX", &posX);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("PositionY", &posY);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("PositionZ", &posZ);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("RotationX", &rotX);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("RotationY", &rotY);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("RotationZ", &rotZ);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("VelocityX", &velX);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("VelocityY", &velY);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("VelocityZ", &velZ);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("Steer", &steer);
		XMLCheckResult(eResult);
		eResult = pElement->QueryDoubleAttribute("Throttle", &throttle);
        //XMLCheckResult(eResult);
		if (eResult != 0) {
            eResult = pElement->QueryDoubleAttribute("Acceleration", &throttle);
        }
        XMLCheckResult(eResult);

        // find out all collision frame
        if (c_it != collision_vct.end()) {
            int sec = difftime(*c_it, time_stamp_);
            if (sec <= tmp && tmp < sec + 1) {
                b_collision = true;
            }
            else if (sec + 1 <= tmp) {
                c_it += 1;
            }
        }

        // find out on / off giraffe view
        if (g_it != giraffe_vct.end()) {
            double sec = g_it->first;
            if (sec <= tmp) {
                if (g_it->second == true) {
                    b_giraffe_st = true;
                }
                else {
                    b_giraffe_ed = true;
                }
                g_it += 1;    
            }
        }

		user_.AddTimestep(posX, posZ, rotX, rotY, rotZ, velX, velZ, steer, throttle, b_collision, b_giraffe_st, b_giraffe_ed);

		//Read all the Sumo generated cars
		visible_cars_.push_back(std::vector<SumoCar*>());
		pElement = step->FirstChildElement("SumoCar");
		unsigned int i = 0;
		while (pElement != nullptr) {
			const char *id = nullptr;
			id = pElement->Attribute("id");
			if (id == nullptr) return XML_ERROR_PARSING_ATTRIBUTE;
			double x, y;
			eResult = pElement->QueryDoubleAttribute("x", &x);
			XMLCheckResult(eResult);
			eResult = pElement->QueryDoubleAttribute("y", &y);
			XMLCheckResult(eResult);
			const char* type=nullptr;
			type = pElement->Attribute("type");
			if (type == nullptr) type = "CR7";
			SumoCar *car_to_add = cars_[id];
			if (car_to_add == NULL){
				car_to_add = new SumoCar(type);
				cars_[id] = car_to_add;
			}
			(visible_cars_[time_step]).push_back(car_to_add);
			car_to_add->AddPosition(time_step, x, y);

			pElement = pElement->NextSiblingElement("SumoCar");
			++i;
		}
		time_step++;
		step = step->NextSiblingElement("step");

	}
	return 0;
}

int Simulation::ReadCollision(const char *file, vector<int>& collision_vct) {
	//Open the document
	XMLDocument xmlDoc;
	XMLError eResult = xmlDoc.LoadFile(file);
	XMLCheckResult(eResult);

	XMLNode * Root = xmlDoc.FirstChild();
	if (Root == nullptr) return XML_ERROR_FILE_READ_ERROR;

	XMLElement * pElement = xmlDoc.FirstChildElement();
	if (pElement == nullptr) return XML_ERROR_PARSING_ELEMENT;

	XMLElement * col = pElement->FirstChildElement("Collision");
	if (col == nullptr) return XML_ERROR_PARSING_ELEMENT;

	int tmp;
	while (col != nullptr){
		eResult = col->QueryIntAttribute("timeStamp", &tmp);
		XMLCheckResult(eResult);
		collision_times.push_back(tmp);
		col = col->NextSiblingElement("Collision");

        // push into vector
		collision_vct.push_back(tmp);
	}
}

// not use for now
int Simulation::ReadGiraffe(const char *file, vector<pair<double,bool>> &giraffe_vct) {
    //Open the document
	XMLDocument xmlDoc;
	XMLError eResult = xmlDoc.LoadFile(file);
	XMLCheckResult(eResult);

	XMLNode * Root = xmlDoc.FirstChild();
	if (Root == nullptr) return XML_ERROR_FILE_READ_ERROR;

	XMLElement * pElement = xmlDoc.FirstChildElement();
	if (pElement == nullptr) return XML_ERROR_PARSING_ELEMENT;

	XMLElement * col = pElement->FirstChildElement("GiraffeView");
	if (col == nullptr) return XML_ERROR_PARSING_ELEMENT;

    const char* type = nullptr;
    const char* action = nullptr;
	double tmp;
	while (col != nullptr){
        type = pElement->Attribute("type");
        action = pElement->Attribute("action");
		eResult = col->QueryDoubleAttribute("timeStamp", &tmp);
		XMLCheckResult(eResult);
		collision_times.push_back(tmp);
		col = col->NextSiblingElement("GiraffeView");

        // push into vector
		// giraffe_vct.push_back(tmp);
	}
}

void Simulation::Initialize() {
	// On the simulation level
	SetUserOnLane();
	setCarsAroundUser();

	for (const auto sumo : cars_)
		sumo.second->ComputeVelocity(time_);

	user_.Initialize(time_);
}

double Simulation::Duration(){
	return time_[time_.size() - 1] - time_[0];
}

bool Simulation::IsOnLane(double yCar, int lane)
{
	double yLane = lanes_Y_[lane];
	if ((lane == 0) && (yCar < yLane + lanes_half_width_))
		return true;

	if ((lane == 2) && (yCar > yLane - lanes_half_width_))
		return true;

	return (yCar > yLane - lanes_half_width_ && yCar < yLane + lanes_half_width_);
}

void Simulation::SetUserOnLane()
{
	double all_y[3];
	for (int i = 0; i < user_.position_.size(); i++) {
		double ycenter = (user_.position_[i])[1];
		all_y[0] = ycenter; all_y[1] = ycenter - 0.8; all_y[2] = ycenter + 0.8;
		for (int i = 0; i < 3; i++){
			double y = all_y[i];
			if (IsOnLane(y, 0))
				user_.on_lane_[i].push_back(0);
			else if (IsOnLane(y, 1))
				user_.on_lane_[i].push_back(1);
			else if (IsOnLane(y, 2))
				user_.on_lane_[i].push_back(2);
			else // not on any of the three lanes --> bug?
				user_.on_lane_[i].push_back(-1);
		}
	}
}

SumoCar * Simulation::InFrontOfUser(int inst, int lane)
{
    if (lane < 0 || lane > 2) return NULL;

	double carX = 1000000000;
	SumoCar *car = NULL;
	SumoCar *cur;
	double curX;
	for (int c = 0; c < (visible_cars_[inst]).size(); c++) {
		cur = (visible_cars_[inst])[c];
		curX = cur->GetPositionX(inst);
		if (curX < (user_.position_[inst])[0])
			continue;
		if (IsOnLane(cur->GetPositionY(inst), lane)) {
			if (car == NULL || curX < carX){
				car = cur;
				carX = curX;
			}
		}
	}
	return car;
}

SumoCar * Simulation::BehindUser(int inst, int lane)
{
    if (lane < 0 || lane > 2) return NULL;

	double carX = 0;
	SumoCar *cur;
	SumoCar *car= NULL;
	double curX;
	for (int c = 0; c < (visible_cars_[inst]).size(); c++) {
		cur = (visible_cars_[inst])[c];
		curX = cur->GetPositionX(inst);
		if (curX > (user_.position_[inst])[0])
			continue;
		if (IsOnLane(cur->GetPositionY(inst), lane)) {
			if (car == NULL || curX > carX){
				car = cur;
				carX = curX;
			}
		}
	}
	return car;
}

void Simulation::setCarsAroundUser()
{
	for (int i = 0; i < user_.position_.size(); i++) {
        int lane = user_.on_lane_[0][i];

		user_.in_front_.push_back(InFrontOfUser(i, lane));
		user_.behind_.push_back(BehindUser(i, lane));

		user_.in_front_l.push_back(InFrontOfUser(i, lane - 1));
		user_.behind_l.push_back(BehindUser(i, lane - 1));

		user_.in_front_r.push_back(InFrontOfUser(i, lane + 1));
		user_.behind_r.push_back(BehindUser(i, lane + 1));
	}
	return;
}


/* Note that mode 0 means normal; mode 1 means aggressive */
void Simulation::PrintCSV(const char* userid, const char* mode, const char* d_dataPath, const char* d_collisionPath)
{

	ofstream output(d_dataPath);
	if (!output.is_open()) {
		fprintf(stderr, "ERROR, unable to create ouput file.\n");
		return;
	}

    output << time_stamp_ << "," << userid << "," << mode << std::endl;
	output << "Time,X,Y,Current Lane,Lane Left,Lane Right,Velocity,Acceleration,Rotation X,Rotation Y,Rotation Z,Pedal,Steer,Dist to Front,Dist to Back,Dist to Left-Front,Dist to Left-Back,Dist to Right-Front,Dist to Right-Back,Speed Front,Speed Front Left,Speed Front Right,Speed Back,Speed Back Left,Speed Back Right,b_collision,b_giraffe_st,b_giraffe_ed,SumoCars\n";

	for (int i = 0; i < time_.size(); i++) {
		output << time_[i]<<",";
		output << (user_.position_[i])[0] << "," << (user_.position_[i])[1] << ",";
		output << (user_.on_lane_[0])[i] << "," << (user_.on_lane_[1])[i] << "," << (user_.on_lane_[2])[i] << ",";
		output << user_.velocity_norm_[i] << "," << user_.acceleration_[i] << ",";
		output << user_.rotation_x_[i] << "," << user_.rotation_[i] << "," << user_.rotation_z_[i] << ",";
		output << user_.pedal_[i] << "," << user_.steer_[i] << ",";
		output << user_.dist_front_[i] << "," << user_.dist_back_[i] << ",";
		output << user_.dist_front_l[i] << "," << user_.dist_back_l[i] << ",";
		output << user_.dist_front_r[i] << "," << user_.dist_back_r[i] << ",";
		output << user_.velo_front_[i] << "," << user_.velo_back_[i] << ",";
		output << user_.velo_front_l[i] << "," << user_.velo_back_l[i] << ",";
		output << user_.velo_front_r[i] << "," << user_.velo_back_r[i] << ",";
		output << user_.collision_[i] << "," << user_.giraffe_st[i] << "," << user_.giraffe_ed[i] << ",";

        /* load all sumo cars into one string */
        /* string: (x_y);(x_y)...(x_y)*/
        string str;
        for (SumoCar* sumoCar : visible_cars_[i]) {
            double x = sumoCar->GetPositionX(i);
            double y = sumoCar->GetPositionY(i);
            double h = sumoCar->GetLength();
            double w = sumoCar->GetWidth();
            
            char tmp[110];
            sprintf(tmp, "%f_%f_%f_%f;", x, y, h, w);
            str += tmp;
        }
        if (str.size() > 0) {
            str.pop_back(); // delete last ';'
        }

        output << str << "\n";
	}
	output.close();
	
	
	ofstream output_col(d_collisionPath);
	if (!output_col.is_open()) {
		fprintf(stderr, "ERROR, unable to create collision file.\n");
		return;
	}

	output_col << "Timestamp\n";
	for (int i = 0; i < collision_times.size(); i++) {
		output_col << collision_times[i] << endl;
	}
	output_col.close();
	return;
}	
