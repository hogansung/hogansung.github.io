#pragma once

#include <vector>
#include <map>
#include <array>
#include <string>
#include <cstring>
#include <cmath>

class SumoCar
{
public:
	SumoCar(const char *type);
	~SumoCar();

	double length, width;

	//std::string id_;
	std::map <int, std::array<double, 2> > position_;
	std::map <int, double > velocity_;

	void AddPosition(int timestep, double position_x, double position_y);
	void ComputeVelocity(std::vector<double> &time);

	double GetPositionX(int timestep);
	double GetPositionY(int timestep);
	double GetVelocity(int timestep);

	double GetLength();
	double GetWidth();
};

