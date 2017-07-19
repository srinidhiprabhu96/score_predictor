import sys
import os
import numpy as np
import scipy.stats

# Function that takes the situation of the match, and predicts the final score.
def get_predicted_score(curr_score,num_overs,balls,runs,runs_var,wickets,players):	
	estimate = [0.0,0.0,0.0]
	variance = [0.0,0.0,0.0]
	max_balls = [36,54,30]
	#Pre-process
	for wicket in wickets:
		balls[players.index(wicket)] = 0
		
	for i in range(0,3):
		balls[:,i] = balls[:,i]/balls[:,i].sum()
		estimate[i] = np.multiply(runs[:,i],balls[:,i]).sum()*max_balls[i] 
		variance[i] = np.multiply(0.1*runs_var[:,i],balls[:,i]).sum()*max_balls[i]
		
	# Predict, using a Gaussian Distribution
	if num_overs < 6:
		additional = (curr_score - float(num_overs)*estimate[0]/6)*((6-num_overs)*variance[0]/6+variance[1]+variance[2])/(float(num_overs)*variance[0]/6) + (6-num_overs)*estimate[0]/6+estimate[1]+estimate[2]
	elif num_overs < 15:
		additional = (curr_score - estimate[0]-float(num_overs-6)*estimate[1]/9)*((15-num_overs)*variance[1]/9+variance[2])/(variance[0]+float(num_overs-6)*variance[1]/9) + (15-num_overs)*estimate[1]/9 + estimate[2]
	else:
		additional = (curr_score - estimate[0]-estimate[1]-float(num_overs-15)*estimate[2]/5)*((20-num_overs)*variance[2]/5)/(variance[0]+variance[1]+float(num_overs-15)*variance[2]/5) + (20-num_overs)*estimate[2]/5
		
	return int(curr_score + additional)

softmax_scaler = 0.3 # May need tuning, if more data becomes available
players = []
fp = open("team_players.txt","r")
for line in fp:
	players.append(line.strip())

fp.close()
balls = []
runs = []
matches = []
runs_var = []
for player in players:
	balls.append([0.0,0.0,0.0])
	runs.append([0.0,0.0,0.0])
	matches.append(0.0)
	runs_var.append([0.0,0.0,0.0])
	
fp = open("database.txt","r")
for line in fp:
	line = line.strip().split()
	line[0] = " ".join(line[0].split("_"))
	if line[0] in players:
		j = players.index(line[0])
		matches[j] = float(line[1])
		for i in range(2,5):
			runs[j][i-2] = float(line[i])
		for i in range(5,8):
			runs_var[j][i-5] = float(line[i])
		for i in range(8,11):
			balls[j][i-8] = float(line[i])

fp.close()

for i in range(0,len(balls)):
	for j in range(0,3):
		if balls[i][j]!=0:
			runs[i][j] = np.divide(runs[i][j],balls[i][j])
			runs_var[i][j]= np.divide(runs_var[i][j],balls[i][j]) - runs[i][j]**2
		else:
			balls[i][j] = -float("inf")
	balls[i] = np.array(balls[i])/float(matches[i])
	
balls = softmax_scaler*np.array(balls)
runs = np.array(runs)
runs_var = np.array(runs_var)
balls = np.exp(balls)

match = sys.argv[1]+".csv"
fp = open(match,"r")
curr_score = 0
curr_wickets = 0
wickets = []
total_score = 0
innings = "1"
prev_over = -1
for line in  fp:
	line = line.strip().split(",")
	if line[0]=="ball" and line[1]==innings:
		over = int(line[2].split(".")[0])
		if over != prev_over:
			if prev_over != -1:	
				predicted = get_predicted_score(curr_score,over,balls,runs,runs_var,wickets,players)
				print "Score after "+str(over)+" overs: "+str(curr_score) +"/"+str(curr_wickets)+" and predicted score is: "+str(predicted)
			prev_over = over			
		curr_score += int(line[7])+int(line[8])
		total_score += int(line[7])+int(line[8])
		if line[10] != '""':
			curr_wickets += 1
			wickets.append(line[10])

print "\n Final score: "+str(total_score) + "/"+str(curr_wickets)
