from mujoco_py import load_model_from_path, MjSim, MjViewer
import numpy as np
from numpy import matlib
from scipy import signal
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
#import pickle
import os
from copy import deepcopy
from all_functions import *

def calculate_closeloop_inputkinematics(step_number, real_attempt_positions, desired_kinematics, K, gradient_edge_order=1, timestep=.005):
	q_desired =  desired_kinematics[step_number, np.ix_([0,3])][0]
	q_dot_desired = desired_kinematics[step_number, np.ix_([1,4])][0]
	q_error = q_desired - real_attempt_positions[step_number-1,:]
	q_dot_in = q_dot_desired + K*q_error
	q_double_dot_in = [
		np.gradient(desired_kinematics[step_number-gradient_edge_order:step_number+1,1],edge_order=gradient_edge_order)[-1]/timestep,
		np.gradient(desired_kinematics[step_number-gradient_edge_order:step_number+1,4],edge_order=gradient_edge_order)[-1]/timestep]
		#desired_kinematics[step_number, np.ix_([2,5])][0]#
	desired_kinematics = [q_desired[0], q_dot_in[0], q_double_dot_in[0], q_desired[1], q_dot_in[1], q_double_dot_in[1]]
	return desired_kinematics

def closeloop_run_fcn(model, desired_kinematics, K, plot_outputs=True, Mj_render=False, chassis_fix=True, timestep=.005):
	est_activations = estimate_activations_fcn(model, desired_kinematics)
	number_of_task_samples = desired_kinematics.shape[0]
	chassis_pos=np.zeros(number_of_task_samples,)
	input_kinematics = np.zeros(desired_kinematics.shape)
	real_attempt_positions = np.zeros([number_of_task_samples,2])
	real_attempt_activations = np.zeros([number_of_task_samples,3])

	if chassis_fix:
		Mj_model = load_model_from_path("./models/nmi_leg_w_chassis_fixed.xml")
	else:
		Mj_model = load_model_from_path("./models/nmi_leg_w_chassis_walk.xml")
	sim = MjSim(Mj_model)

	if Mj_render:
		viewer = MjViewer(sim)

	sim_state = sim.get_state()
	control_vector_length=sim.data.ctrl.__len__()
	print("control_vector_length: "+str(control_vector_length))

	sim.set_state(sim_state)
	gradient_edge_order = 1
	for ii in range(number_of_task_samples):
		if ii < gradient_edge_order:
			print(ii)
			input_kinematics[ii,:] = desired_kinematics[ii,:]
		else:
			input_kinematics[ii,:] = calculate_closeloop_inputkinematics(
				step_number=ii,
				real_attempt_positions=real_attempt_positions,
				desired_kinematics=desired_kinematics,
				K=K,
				gradient_edge_order=gradient_edge_order,
				timestep=timestep)
		est_activations[ii,:] = model.predict([input_kinematics[ii,:]])[0,:]
		sim.data.ctrl[:] = est_activations[ii,:]
		sim.step()
		chassis_pos[ii]=sim.data.get_geom_xpos("Chassis_frame")[0]
		current_positions_array = sim.data.qpos[-2:]
		real_attempt_positions[ii,:] = current_positions_array
		real_attempt_activations[ii,:] = sim.data.ctrl
		if Mj_render:
			viewer.render()
	real_attempt_kinematics = positions_to_kinematics_fcn(
		real_attempt_positions[:,0],
		real_attempt_positions[:,1],
		timestep=timestep)
	error0 = error_cal_fcn(desired_kinematics[:,0], real_attempt_kinematics[:,0])
	error1 = error_cal_fcn(desired_kinematics[:,3], real_attempt_kinematics[:,3])
	average_error = 0.5*(error0+error1)
	if plot_outputs:
		plt.figure()
		plt.subplot(2, 1, 1)
		plt.plot(range(desired_kinematics.shape[0]), desired_kinematics[:,0], range(desired_kinematics.shape[0]), real_attempt_kinematics[:,0])
		plt.ylabel("q0 desired vs. simulated")
		plt.subplot(2, 1, 2)
		plt.plot(range(desired_kinematics.shape[0]), desired_kinematics[:,3], range(desired_kinematics.shape[0]), real_attempt_kinematics[:,3])
		plt.ylabel("q1  desired vs. simulated")
		plt.xlabel("Sample #")
		plt.show(block=True)
	return average_error

def openloop_run_fcn(model, desired_kinematics, plot_outputs=False, Mj_render=False):
	est_activations = estimate_activations_fcn(model, desired_kinematics)
	[real_attempt_kinematics, real_attempt_activations, chassis_pos] = run_activations_fcn(est_activations, chassis_fix=True, timestep=0.005, Mj_render=Mj_render)
	error0 = error_cal_fcn(desired_kinematics[:,0], real_attempt_kinematics[:,0])
	error1 = error_cal_fcn(desired_kinematics[:,3], real_attempt_kinematics[:,3])
	average_error = 0.5*(error0+error1)
	if plot_outputs:
		plt.figure()
		plt.subplot(2, 1, 1)
		plt.plot(range(desired_kinematics.shape[0]), desired_kinematics[:,0], range(desired_kinematics.shape[0]), real_attempt_kinematics[:,0])
		plt.ylabel("q0 desired vs. simulated")
		plt.subplot(2, 1, 2)
		plt.plot(range(desired_kinematics.shape[0]), desired_kinematics[:,3], range(desired_kinematics.shape[0]), real_attempt_kinematics[:,3])
		plt.ylabel("q1  desired vs. simulated")
		plt.xlabel("Sample #")
		plt.show(block=True)
	return average_error