Usage:
	python score_predictor.py <File name without csv extension>
	Eg: python score_predictor.py 1082611
	
#### 

This is a score predictor for IPL/T20 matches.
We use the domain knowledge of IPL matches(regarding the scoring rate) and past performances of players to determine the predicted score.

The csv files regarding the ball-by-ball score for the matches can be found at "http://cricsheet.org/". Download and paste the file in CSV format into the folder and run the program using the above command.

###

Output for the sample file included:

Score after 1 overs: 10/0 and predicted score is: 195
Score after 2 overs: 12/1 and predicted score is: 129
Score after 3 overs: 18/1 and predicted score is: 129
Score after 4 overs: 28/1 and predicted score is: 149
Score after 5 overs: 31/1 and predicted score is: 133
Score after 6 overs: 39/1 and predicted score is: 139
Score after 7 overs: 55/1 and predicted score is: 165
Score after 8 overs: 64/1 and predicted score is: 168
Score after 9 overs: 73/1 and predicted score is: 170
Score after 10 overs: 80/1 and predicted score is: 168
Score after 11 overs: 91/1 and predicted score is: 173
Score after 12 overs: 98/1 and predicted score is: 171
Score after 13 overs: 108/1 and predicted score is: 174
Score after 14 overs: 127/1 and predicted score is: 190
Score after 15 overs: 135/1 and predicted score is: 189
Score after 16 overs: 148/1 and predicted score is: 191
Score after 17 overs: 158/2 and predicted score is: 190
Score after 18 overs: 170/2 and predicted score is: 191
Score after 19 overs: 174/4 and predicted score is: 184

 Final score: 191/4
 
###
Remarks:
	1) In general, we see that the estimates are quite close to the final score, unless there is a drastic increase/decrease in scoring rate or sudden fall of wickets.
	2) The hyper-parameters may need to be updated, when more data is available.
	3) The predictor assumes that all remaining players will play till end of the 20th over.
	4) The performance has been tuned for IPL matches. Performance on T20 matches is not guaranteed. The predictor does not work on ODI matches.
	5) Future work - Consider the weightage for the current batsmen vs those who are left to bat, Use the number of wickets fallen to determine predicted score.
