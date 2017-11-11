# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 02:34:12 2017

@author: Device Admin
"""

import os

#define file path
csvpath = os.path.join('Resources','election_data_2.csv')



import csv

# Lists to store data

voter = []
county = []
candidate = []
unique_candidate = []


#define variables
tot_voter = 0

#read csv files
with open(csvpath) as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    election_data = csv.reader(csvfile, delimiter=',')

    #  create voter list
    for election in election_data:
        voter.append(election[0])
        voter[0] = 0
    voter.remove(0)


#read csv files
with open(csvpath) as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    election_data = csv.reader(csvfile, delimiter=',')

    #  create county list
    for election in election_data:
        county.append(election[1])
        county[0] = 0
    county.remove(0)

#read csv files
with open(csvpath) as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    election_data = csv.reader(csvfile, delimiter=',')

    #  create candidate list
    for election in election_data:
        candidate.append(election[2])
        candidate[0] = 0
    candidate.remove(0)
    

tot_voter = len(voter)

for i in candidate:
    if i not in unique_candidate:
        unique_candidate.append(i)

candidate_1 = []
candidate_2 = []
candidate_3 = []
candidate_4 = []

for item in candidate:
    if item == str(unique_candidate[0]):
        candidate_1.append(item)
    elif item == str(unique_candidate[1]):
        candidate_2.append(item)
    elif item == str(unique_candidate[2]):
        candidate_3.append(item)
    elif item == str(unique_candidate[3]):
        candidate_4.append(item)


tot_vote_cand1 = len(candidate_1)
tot_vote_cand2 = len(candidate_2)
tot_vote_cand3 = len(candidate_3)
tot_vote_cand4 = len(candidate_4)

avg_vote_cand1 = (float(tot_vote_cand1) / tot_voter) * 100
avg_vote_cand2 = (float(tot_vote_cand2) / tot_voter) * 100
avg_vote_cand3 = (float(tot_vote_cand3) / tot_voter) * 100
avg_vote_cand4 = (float(tot_vote_cand4) / tot_voter) * 100



if tot_vote_cand1 > tot_vote_cand2:
    winner = unique_candidate[0]
elif tot_vote_cand1 > tot_vote_cand3:
    winner = unique_candidate[0]
elif tot_vote_cand1 > tot_vote_cand4:
    winner = unique_candidate[0]
elif tot_vote_cand2 > tot_vote_cand3:
    winner = unique_candidate[1]
elif tot_vote_cand2 > tot_vote_cand4:
    winner = unique_candidate[1]
elif tot_vote_cand3 > tot_vote_cand4:
    winner = unique_candidate[2]
else:
    winner = unique_candidate[3]
    
    
  
print("Election Results")
print("-------------------------")
print("Total Votes: "+str(tot_voter))
print("-------------------------")
print(str(unique_candidate[0])+": "+str(avg_vote_cand1)+"% "+str(tot_vote_cand1))
print(str(unique_candidate[1])+": "+str(avg_vote_cand2)+"% "+str(tot_vote_cand2))
print(str(unique_candidate[2])+": "+str(avg_vote_cand3)+"% "+str(tot_vote_cand3))
print(str(unique_candidate[3])+": "+str(avg_vote_cand4)+"% "+str(tot_vote_cand4))
print("-------------------------")
print("Wineer: "+winner)
print("-------------------------")







