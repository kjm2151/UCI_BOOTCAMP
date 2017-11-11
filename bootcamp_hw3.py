# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:20:19 2017

@author: Device Admin
"""

import os

#define file path
csvpath_1 = os.path.join('Resources','budget_data_1.csv')
csvpath_2 = os.path.join('Resources','budget_data_2.csv')



import csv

# Lists to store data
rev_budget_1 = []
rev_budget_2 = []
rev_budget = []

#define variables
tot_month = 0
tot_rev = 0
tot_month_1 = 0
tot_month_2 = 0



#read csv files
with open(csvpath_1) as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    budget_data_1 = csv.reader(csvfile, delimiter=',')

    #  Each row is read as a row
    for budget_1 in budget_data_1:
        rev_budget_1.append(budget_1[1])
        rev_budget_1[0] = 0
    tot_month_1 = len(rev_budget_1) -1
    rev_budget_1 = [int(i) for i in rev_budget_1]
    rev_budget_1.remove(0)


with open(csvpath_2) as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    budget_data_2 = csv.reader(csvfile, delimiter=',')

    #  Each row is read as a row
    for budget_2 in budget_data_2:
        rev_budget_2.append(budget_2[1])
        rev_budget_2[0] = 0
    tot_month_2 = len(rev_budget_2) -1
    rev_budget_2 = [int(i) for i in rev_budget_2]
    rev_budget_2.remove(0)


rev_budget = rev_budget_1 + rev_budget_2
tot_month = tot_month_1 + tot_month_2





def sum(numbers):
    total = 0
    for x in numbers:
        total += x
    return total
        
tot_rev = sum(rev_budget)


diff = [rev_budget[i+1]-rev_budget[i] for i in range(len(rev_budget)-1)]

tot_avg_diff = sum(diff)/tot_month


print("Total Months: " + str(tot_month))
print("Total Revenue: " + str(tot_rev))
print("Average Revenue Change: " + "$"+str(tot_avg_diff))
print("Greatest Increase in Revenue: " + "$"+str(max(diff)))
print("Greatest Decrease in Revenue: " + "$"+str(min(diff)))
