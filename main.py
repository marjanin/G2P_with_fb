import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import pickle
from warnings import simplefilter
from all_functions import *
from feedback_functions import *

simplefilter(action='ignore', category=FutureWarning)

# # [babbling_kinematics, babbling_activations] = babbling_fcn(simulation_minutes=5)
# # model = inverse_mapping_fcn(kinematics=babbling_kinematics, activations=babbling_activations)
# # cum_kinematics = babbling_kinematics
# # cum_activations = babbling_activations



# # pickle.dump([model,cum_kinematics, cum_activations],open("results/mlp_model.sav", 'wb'))

[model,cum_kinematics, cum_activations] = pickle.load(open("results/mlp_model.sav", 'rb')) # loading the model
np.random.seed(0)

P = np.array([10, 15])/
I = np.array([2, 6])/
trial_number = 25

experiments_switch=[0, 0, 0, 0, 0, 0, 0, 0, 0]#[1, 1, 1, 1, 1, 1, 1, 1] 
for ii in range(len(experiments_switch)):
	globals()["exp{}_average_error".format(ii+1)]=np.zeros([2,1])
	exp6_average_error = np.zeros([3,1])
	exp7_average_error = np.zeros([3,1])
	exp9_average_error = np.zeros([3,1,1])
	
if experiments_switch[0] ==1: # as a function of cycle period
	features=np.ones(10,)
	cycle_durations = np.linspace(.1,10,trial_number)
	test1_no = cycle_durations.shape[0]
	exp1_average_error = np.zeros([2,test1_no]) # first row open-loop and second row close-loop
	#cycle length experiment
	for cycle_duration_in_seconds, ii in zip(cycle_durations, range(test1_no)):
		[q0_filtered, q1_filtered]  = feat_to_positions_fcn(features, timestep=0.005, cycle_duration_in_seconds = cycle_duration_in_seconds, show=False)
		q0_filtered_10 = np.tile(q0_filtered,10)
		q1_filtered_10 = np.tile(q1_filtered,10)
		desired_kinematics = positions_to_kinematics_fcn(q0_filtered_10, q1_filtered_10, timestep = 0.005)
		exp1_average_error[0,ii], _, _ = openloop_run_fcn(model=model, desired_kinematics=desired_kinematics, plot_outputs=False, Mj_render=False)
		exp1_average_error[1,ii], _, _ = closeloop_run_fcn(model=model, desired_kinematics=desired_kinematics, P=P, I=I, plot_outputs=False, Mj_render=False) # K = [10, 15]

if experiments_switch[1] ==1: # cyclical on air
	test2_no = trial_number
	exp2_average_error = np.zeros([2,test2_no])
	for ii in range(test2_no):
		features = np.random.rand(10)*.8+.2
		[q0_filtered, q1_filtered]  = feat_to_positions_fcn(features, timestep=0.005, cycle_duration_in_seconds = 2.5, show=False)
		#import pdb; pdb.set_trace()
		q0_filtered_10 = np.tile(q0_filtered,10)
		q1_filtered_10 = np.tile(q1_filtered,10)
		desired_kinematics = positions_to_kinematics_fcn(q0_filtered_10, q1_filtered_10, timestep = 0.005)
		exp2_average_error[0,ii], _, _ = openloop_run_fcn(model=model, desired_kinematics=desired_kinematics, plot_outputs=False, Mj_render=False)
		exp2_average_error[1,ii], _, _ = closeloop_run_fcn(model=model, desired_kinematics=desired_kinematics, P=P, I=I, plot_outputs=False, Mj_render=False) # K = [10, 15]
		#print("error_without: ", exp2_average_error[0,0], "error with: ", exp2_average_error[1,0])

if experiments_switch[2] ==1: # p2p
	test3_no = trial_number
	exp3_average_error = np.zeros([2,test3_no])
	for ii in range(test3_no):
		q0 = p2p_positions_gen_fcn(low=-np.pi/3, high=np.pi/3, number_of_positions=10, duration_of_each_position=2.5, timestep=.005)
		q1 = p2p_positions_gen_fcn(low=-np.pi/2, high=0, number_of_positions=10, duration_of_each_position=2.5, timestep=.005)
		desired_kinematics = positions_to_kinematics_fcn(q0, q1, timestep = 0.005)
		exp3_average_error[0,ii], _, _ = openloop_run_fcn(model=model, desired_kinematics=desired_kinematics, plot_outputs=False, Mj_render=False)
		exp3_average_error[1,ii], _, _ = closeloop_run_fcn(model=model, desired_kinematics=desired_kinematics,  P=P, I=I, plot_outputs=False, Mj_render=False) # K = [10, 15]

if experiments_switch[3] ==1:	# standing up against weight
	test4_no = 1
	exp4_average_error = np.zeros([2,test4_no])
	q0 = p2p_positions_gen_fcn(low=np.pi/3, high=np.pi/3, number_of_positions=1, duration_of_each_position=1, timestep=.005)
	q0 = np.append(q0,p2p_positions_gen_fcn(low=0, high=0, number_of_positions=1, duration_of_each_position=14, timestep=.005))
	q1 = p2p_positions_gen_fcn(low=-np.pi/2, high=-np.pi/2, number_of_positions=1, duration_of_each_position=1, timestep=.005)
	q1 = np.append(q1,p2p_positions_gen_fcn(low=0, high=0, number_of_positions=1, duration_of_each_position=14, timestep=.005))
	desired_kinematics = positions_to_kinematics_fcn(q0, q1, timestep = 0.005)
	exp4_average_error[0,:], _, _ = openloop_run_fcn(model=model, desired_kinematics=desired_kinematics, model_ver=3, plot_outputs=False, Mj_render=False)

	q0 = p2p_positions_gen_fcn(low=np.pi/3, high=np.pi/3, number_of_positions=1, duration_of_each_position=1, timestep=.005)
	q0 = np.append(q0,p2p_positions_gen_fcn(low=0, high=0, number_of_positions=1, duration_of_each_position=4, timestep=.005))
	q1 = p2p_positions_gen_fcn(low=-np.pi/2, high=-np.pi/2, number_of_positions=1, duration_of_each_position=1, timestep=.005)
	q1 = np.append(q1,p2p_positions_gen_fcn(low=0, high=0, number_of_positions=1, duration_of_each_position=4, timestep=.005))
	desired_kinematics = positions_to_kinematics_fcn(q0, q1, timestep = 0.005)
	exp4_average_error[1,:], _, _ = closeloop_run_fcn(model=model, desired_kinematics=desired_kinematics,  P=P, I=I, model_ver=3, plot_outputs=False, Mj_render=False)

if experiments_switch[4] == 1: # walking; contact dynamics
	test5_no = trial_number
	exp5_average_error = np.zeros([2,test5_no])
	for ii in range(test5_no):
		##########################
		features = np.random.rand(10)*.8+.2
		[q0_filtered, q1_filtered]  = feat_to_positions_fcn(features, timestep=0.005, cycle_duration_in_seconds = 2.5, show=False)
		q0_filtered_10 = np.tile(q0_filtered,10)
		q1_filtered_10 = np.tile(q1_filtered,10)
		desired_kinematics = positions_to_kinematics_fcn(q0_filtered_10, q1_filtered_10, timestep = 0.005)
		exp5_average_error[0,ii], _, _ = openloop_run_fcn(model=model, desired_kinematics=desired_kinematics, model_ver=2, plot_outputs=False, Mj_render=False)
		exp5_average_error[1,ii], _, _ = closeloop_run_fcn(model=model, desired_kinematics=desired_kinematics, model_ver=2, P=P, I=I, plot_outputs=False, Mj_render=False) # K = [10, 15]

if experiments_switch[5] == 1: # everlearn ones
	np.random.seed(0)
	[babbling_kinematics_1min, babbling_activations_1min] = babbling_fcn(simulation_minutes=1)
	model_1min = inverse_mapping_fcn(kinematics=babbling_kinematics_1min, activations=babbling_activations_1min)
	cum_kinematics_ol = deepcopy(babbling_kinematics_1min)
	cum_activations_ol = deepcopy(babbling_activations_1min)
	exp6_model_ol = deepcopy(model_1min)
	cum_kinematics_cl = deepcopy(babbling_kinematics_1min)
	cum_activations_cl = deepcopy(babbling_activations_1min)
	exp6_model_cl = deepcopy(model_1min)
	test6_no = trial_number
	exp6_average_error = np.zeros([3,test6_no])
	for ii in range(test6_no):
		features = np.ones(10,)
		print(features)
		[q0_filtered, q1_filtered]  = feat_to_positions_fcn(features, timestep=0.005, cycle_duration_in_seconds = 2.5, show=False) #1sec also fine
		q0_filtered_10 = np.tile(q0_filtered,10)
		q1_filtered_10 = np.tile(q1_filtered,10)
		desired_kinematics = positions_to_kinematics_fcn(q0_filtered_10, q1_filtered_10, timestep = 0.005)

		exp6_average_error[0,ii], real_attempt_kinematics_ol, real_attempt_activations_ol = openloop_run_fcn(model=exp6_model_ol, desired_kinematics=desired_kinematics, model_ver=0, plot_outputs=False, Mj_render=False)
		cum_kinematics_ol, cum_activations_ol = concatinate_data_fcn( cum_kinematics_ol, cum_activations_ol, real_attempt_kinematics_ol, real_attempt_activations_ol, throw_percentage = 0.20)
		exp6_model_ol = inverse_mapping_fcn(cum_kinematics_ol, cum_activations_ol, prior_model = exp6_model_ol)

		exp6_average_error[1,ii], real_attempt_kinematics_cl, real_attempt_activations_cl = closeloop_run_fcn(model=exp6_model_cl, desired_kinematics=desired_kinematics, model_ver=0, P=P, I=I, plot_outputs=False, Mj_render=False)
		exp6_average_error[2,ii], _, _ = openloop_run_fcn(model=exp6_model_cl, desired_kinematics=desired_kinematics, model_ver=0, plot_outputs=False, Mj_render=False)
		cum_kinematics_cl, cum_activations_cl = concatinate_data_fcn( cum_kinematics_cl, cum_activations_cl, real_attempt_kinematics_cl, real_attempt_activations_cl, throw_percentage = 0.20)
		exp6_model_cl = inverse_mapping_fcn(cum_kinematics_cl, cum_activations_cl, prior_model = exp6_model_cl)

if experiments_switch[6] == 1: # everlearn random
	np.random.seed(0)
	[babbling_kinematics_1min, babbling_activations_1min] = babbling_fcn(simulation_minutes=1)
	model_1min = inverse_mapping_fcn(kinematics=babbling_kinematics_1min, activations=babbling_activations_1min)
	cum_kinematics_ol = deepcopy(babbling_kinematics_1min)
	cum_activations_ol = deepcopy(babbling_activations_1min)
	exp7_model_ol = deepcopy(model_1min)
	cum_kinematics_cl = deepcopy(babbling_kinematics_1min)
	cum_activations_cl = deepcopy(babbling_activations_1min)
	exp7_model_cl = deepcopy(model_1min)
	test7_no = trial_number
	exp7_average_error = np.zeros([3,test7_no])
	for ii in range(test7_no):
		print(ii)
		features = np.random.rand(10)*.8+.2
		print(features)
		[q0_filtered, q1_filtered]  = feat_to_positions_fcn(features, timestep=0.005, cycle_duration_in_seconds = 2.5, show=False) #1sec also fine
		q0_filtered_10 = np.tile(q0_filtered,10)
		q1_filtered_10 = np.tile(q1_filtered,10)
		desired_kinematics = positions_to_kinematics_fcn(q0_filtered_10, q1_filtered_10, timestep = 0.005)

		exp7_average_error[0,ii], real_attempt_kinematics_ol, real_attempt_activations_ol = openloop_run_fcn(model=exp7_model_ol, desired_kinematics=desired_kinematics, model_ver=0, plot_outputs=False, Mj_render=False)
		cum_kinematics_ol, cum_activations_ol = concatinate_data_fcn( cum_kinematics_ol, cum_activations_ol, real_attempt_kinematics_ol, real_attempt_activations_ol, throw_percentage = 0.20)
		exp7_model_ol = inverse_mapping_fcn(cum_kinematics_ol, cum_activations_ol, prior_model = exp7_model_ol)

		exp7_average_error[1,ii], real_attempt_kinematics_cl, real_attempt_activations_cl = closeloop_run_fcn(model=exp7_model_cl, desired_kinematics=desired_kinematics, model_ver=0, P=P, I=I, plot_outputs=False, Mj_render=False)
		exp7_average_error[2,ii], _, _ = openloop_run_fcn(model=exp7_model_cl, desired_kinematics=desired_kinematics, model_ver=0, plot_outputs=False, Mj_render=False)
		cum_kinematics_cl, cum_activations_cl = concatinate_data_fcn( cum_kinematics_cl, cum_activations_cl, real_attempt_kinematics_cl, real_attempt_activations_cl, throw_percentage = 0.20)
		exp7_model_cl = inverse_mapping_fcn(cum_kinematics_cl, cum_activations_cl, prior_model = exp7_model_cl)

if experiments_switch[7] ==1: # delay
	test8_no = trial_number
	all_delays = np.arange(0, 21, 2)
	exp8_average_error = np.zeros([all_delays.shape[0]+1,test8_no])
	for ii in range(test8_no):
		features = np.random.rand(10)*.8+.2
		[q0_filtered, q1_filtered]  = feat_to_positions_fcn(features, timestep=0.005, cycle_duration_in_seconds = 2.5, show=False)
		#import pdb; pdb.set_trace()
		q0_filtered_10 = np.tile(q0_filtered,10)
		q1_filtered_10 = np.tile(q1_filtered,10)
		desired_kinematics = positions_to_kinematics_fcn(q0_filtered_10, q1_filtered_10, timestep = 0.005)
		for delay_timesteps, jj in zip(all_delays, range(all_delays.shape[0])):
			if jj==0: # 0 is for the open loop
				exp8_average_error[jj,ii], _, _ = openloop_run_fcn(model=model, desired_kinematics=desired_kinematics, plot_outputs=False, Mj_render=False)
			exp8_average_error[jj+1,ii], _, _ = closeloop_run_fcn(model=model, desired_kinematics=desired_kinematics, P=P, I=I, delay_timesteps=delay_timesteps, plot_outputs=False, Mj_render=False) # K = [10, 15]
		#print("error_without: ", exp2_average_error[0,0], "error with: ", exp2_average_error[1,0])

if experiments_switch[8] == 1: # everlearn random mesh
	test9_no = trial_number
	babbling_times = np.array([1, 2.5, 5])
	num_babbling_cases = babbling_times.shape[0]

	#import pdb; pdb.set_trace()
	exp9_average_error = np.zeros([3,test9_no,num_babbling_cases])
	for babbling_time, jj in zip(babbling_times, range(num_babbling_cases)):
		np.random.seed(0)
		[babbling_kinematics_1min, babbling_activations_1min] = babbling_fcn(simulation_minutes=babbling_time)
		model_1min = inverse_mapping_fcn(kinematics=babbling_kinematics_1min, activations=babbling_activations_1min)
		cum_kinematics_ol = deepcopy(babbling_kinematics_1min)
		cum_activations_ol = deepcopy(babbling_activations_1min)
		exp9_model_ol = deepcopy(model_1min)
		cum_kinematics_cl = deepcopy(babbling_kinematics_1min)
		cum_activations_cl = deepcopy(babbling_activations_1min)
		exp9_model_cl = deepcopy(model_1min)
		for ii in range(test9_no):
			features = np.ones(10,)#np.random.rand(10)*.8+.2
			print(features)
			[q0_filtered, q1_filtered]  = feat_to_positions_fcn(features, timestep=0.005, cycle_duration_in_seconds = 2.5, show=False) #1sec also fine
			q0_filtered_10 = np.tile(q0_filtered,10)
			q1_filtered_10 = np.tile(q1_filtered,10)
			desired_kinematics = positions_to_kinematics_fcn(q0_filtered_10, q1_filtered_10, timestep = 0.005)

			exp9_average_error[0,ii,jj], real_attempt_kinematics_ol, real_attempt_activations_ol = openloop_run_fcn(model=exp9_model_ol, desired_kinematics=desired_kinematics, model_ver=0, plot_outputs=False, Mj_render=False)
			cum_kinematics_ol, cum_activations_ol = concatinate_data_fcn( cum_kinematics_ol, cum_activations_ol, real_attempt_kinematics_ol, real_attempt_activations_ol, throw_percentage = 0.20)
			exp9_model_ol = inverse_mapping_fcn(cum_kinematics_ol, cum_activations_ol, prior_model = exp9_model_ol)

			exp9_average_error[1,ii,jj], real_attempt_kinematics_cl, real_attempt_activations_cl = closeloop_run_fcn(model=exp9_model_cl, desired_kinematics=desired_kinematics, model_ver=0, P=P, I=I, plot_outputs=False, Mj_render=False)
			exp9_average_error[2,ii,jj], _, _ = openloop_run_fcn(model=exp9_model_cl, desired_kinematics=desired_kinematics, model_ver=0, plot_outputs=False, Mj_render=False)
			cum_kinematics_cl, cum_activations_cl = concatinate_data_fcn( cum_kinematics_cl, cum_activations_cl, real_attempt_kinematics_cl, real_attempt_activations_cl, throw_percentage = 0.20)
			exp9_model_cl = inverse_mapping_fcn(cum_kinematics_cl, cum_activations_cl, prior_model = exp9_model_cl)

errors_all = [exp1_average_error, exp2_average_error, exp3_average_error, exp4_average_error, exp5_average_error, exp6_average_error, exp7_average_error, exp8_average_error]
#pickle.dump([errors_all],open("results/P_I/feedback_errors_P_I_9.sav", 'wb')) # saving the results with only P
#pickle.dump([exp9_average_error],open("results/P_I/feedback_errors_P_I_V2.sav", 'wb')) # saving the results with only P
[exp9_average_error] = pickle.load(open("results/P_I/feedback_errors_P_I_V2.sav", 'rb')) # loading the results with only P
#[errors_all] = pickle.load(open("results/P_I/feedback_errors_P_I_9.sav", 'rb')) # loading the results with only P
#import pdb; pdb.set_trace()
# plt.figure()
# plt.plot(exp6_average_error[0,:])
# plt.plot(exp6_average_error[1,:])
# plt.show(block=True)
# plt.figure()
# plt.plot(exp7_average_error[0,:])
# plt.plot(exp7_average_error[1,:])
# plt.show(block=True)
plot_comparison_figures_fcn(errors_all)
trial_number = 25

babbling_times = np.array([1, 2.5, 5])
num_babbling_cases = babbling_times.shape[0]
	#plt 8: delay
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.05)
exp9_average_error
trials_num = trial_number
babblings_num = num_babbling_cases
X_1 = np.linspace(0,trials_num,trials_num)
X = np.tile(X_1, [babblings_num, 1]).transpose()
Y_1 = np.array([1, 2.5, 5])
Y = np.tile(Y_1, [trials_num, 1])
Z = exp9_average_error[0,:,:]
# Plot a basic wireframe.

#ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.YlGnBu_r, alpha=.5)
ax.plot_wireframe(X, Y, Z, rstride=100, cstride=1, color='C0', alpha=1)
ax.set_xlabel('Trial #')
ax.set_ylabel('Babbling length minute')
ax.set_zlim(0,.2)

#ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.05)
exp9_average_error
X_1 = np.linspace(0,trials_num,trials_num)
X = np.tile(X_1, [babblings_num, 1]).transpose()
Y_1 = np.array([1, 2.5, 5])
Y = np.tile(Y_1, [trials_num, 1])
Z = exp9_average_error[1,:,:]
# Plot a basic wireframe.

#ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.Oranges, alpha=.5)
ax.plot_wireframe(X, Y, Z, rstride=100, cstride=1, color = 'C1', alpha=.5)
ax.set_xlabel('Trial #')
ax.set_ylabel('Babbling length minute')
ax.set_zlim(0,.5)

#ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.05)
exp9_average_error
X_1 = np.linspace(0,trials_num,trials_num)
X = np.tile(X_1, [babblings_num, 1]).transpose()
Y_1 = np.array([1, 2.5,  5])
Y = np.tile(Y_1, [trials_num, 1])
Z = exp9_average_error[2,:,:]
# Plot a basic wireframe.

#ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.YlGn, alpha=.5)
ax.plot_wireframe(X, Y, Z, rstride=100, cstride=1, color='C2', alpha=.5)
ax.set_xlabel('Trial #')
ax.set_ylabel('Babbling length minute')
ax.set_zlim(0,.2)
# Z_ol_1 = exp9_average_error[0,:]
# Z_ol = np.tile(Z_ol_1,[11,1])
# ax.plot_wireframe(X, Y, Z_ol, rstride=5, cstride=10, color="lightcoral", alpha=.7)
# ax.view_init(elev=21., azim=-114.)
# ax.set_xlabel('delays (ms)')
# ax.set_ylabel('trial #')
# ax.set_zlabel('mean error (rads)')
# plt.title('Error for a set of cyclical trials as a function of delay')
# plt.savefig('./results/P_I/exp8.png')
plt.show()
