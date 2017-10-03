#include "kalman_filter.h"
#include <iostream>
using namespace std;

using Eigen::MatrixXd;
using Eigen::VectorXd;

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
  x_ = x_in;
  P_ = P_in;
  F_ = F_in;
  H_ = H_in;
  R_ = R_in;
  Q_ = Q_in;
}

void KalmanFilter::Predict() {
  /**
  TODO:DONE
    * predict the state
  */
	x_ = F_ * x_;
	MatrixXd Ft = F_.transpose();
	P_ = (F_ * P_ * Ft) + Q_;
}

void KalmanFilter::Update(const VectorXd &z) {
  /**
  TODO:DONE
    * update the state by using Kalman Filter equations
  */
	VectorXd z_pred = H_ * x_;
	VectorXd y = z - z_pred;
	MatrixXd Ht = H_.transpose();
	MatrixXd S = H_ * P_ * Ht + R_;
	MatrixXd Si = S.inverse();
	MatrixXd PHt = P_ * Ht;
	MatrixXd K = PHt * Si;

	//new estimate
	x_ = x_ + (K * y);
	long x_size = x_.size();
	MatrixXd I = MatrixXd::Identity(x_size, x_size);
	P_ = (I - K * H_) * P_;
}

void KalmanFilter::UpdateEKF(const VectorXd &z) {
  /**
  TODO:DONE
    * update the state by using Extended Kalman Filter equations
  */
	//preparation values
	float px, py, vx, vy;
	px = x_(0); py = x_(1); vx = x_(2); vy = x_(3);
	//h(x') = (rho, phi, rho dot)
	float ro = sqrt((px*px)+(py*py));//rho,range predection  = sqrt(px^2 + py^2)
	//float phi = atan((py/px));//phi,bearing predection = arctan(py/px) 
	float phi = atan2(py, px);
	if (ro == 0)
		cout << "ERROR: Divide by 0 @ UpdateEKF";
	float ro_dot = ((px*vx)+(py*vy))/ro;//rho,radial velocity predection = (pxvx+pyvy)/sqrt(px^2 + py^2)
	
	VectorXd z_pred = VectorXd(3);//h(x');
	z_pred << ro, phi, ro_dot;
	VectorXd y = z - z_pred;//z - h(x')
	//normlize phi 
	y(1) = atan2(sin(y(1)), cos(y(1)));

//TODO, refactor from here, and also Update() function , extract code to unified function as it the same code.
	MatrixXd Ht = H_.transpose();
	MatrixXd S = H_ * P_ * Ht + R_;
	MatrixXd Si = S.inverse();
	MatrixXd PHt = P_ * Ht;
	MatrixXd K = PHt * Si;

	//new estimate
	x_ = x_ + (K * y);
	long x_size = x_.size();
	MatrixXd I = MatrixXd::Identity(x_size, x_size);
	P_ = (I - K * H_) * P_;
}
