from Player_Creation import *
from Opex_and_Capex_Setup import *
from Price_Engine_Creation import *
from solver import *
import numpy_financial as np
import csv
import pandas as pd


def sumproduct(list1, list2):
    total = 0
    for position in range(len(list1)):
        total += list1[position] * list2[position]
    return total


def get_opex(multipliers, volumes):
    opex = []
    for player in range(len(volumes)):
        player_opex = []
        for case in range(len(volumes[0])):
            case_opex = []
            for year in range(31):
                temp_opex_val = volumes[player][case + 1][0][year] * multipliers[player][0] + \
                                volumes[player][case + 1][1][year] * multipliers[player][1] + \
                                volumes[player][case + 1][2][year] * multipliers[player][2]
                case_opex.append(temp_opex_val)
            player_opex.append(case_opex)
        opex.append(player_opex)
    return opex


testing = get_opex(total_var_cost, result)


# print (testing[0][1])
# print (testing[0][2])
# print (testing[0][3])
# print (testing[0][4])
# growth and sustaining
def get_capex(multipliers_sus, multipliers_growth, volumes):
    capex = []
    for player in range(len(volumes)):
        player_capex = []
        for case in range(1, len(volumes[0]) + 1):
            case_capex = []
            for quality in range(3):
                quality_capex = []
                for year in range(31):
                    if year > 0:
                        if volumes[player][case][quality][year] * 0.97 > volumes[player][case][quality][year - 1]:
                            temp_capex_growth_val = (volumes[player][case][quality][year] -
                                                     volumes[player][case][quality][year - 1]) * \
                                                    multipliers_growth[player][quality]
                        if volumes[player][case][quality][year] >= volumes[player][case][quality][year - 1]:
                            if year > 10:
                                temp_capex_growth_val = 0
                            temp_capex_sus_val = 0.03 * volumes[player][case][quality][year - 1] * \
                                                 multipliers_sus[player][quality]
                    else:
                        temp_capex_growth_val = 0
                        temp_capex_sus_val = 0
                    quality_capex.append(temp_capex_growth_val + temp_capex_sus_val)
                case_capex.append(quality_capex)
            combined_quality_capex = []
            for i in range(31):
                combined_quality_capex.append(case_capex[0][i] + case_capex[1][i] + case_capex[2][i])
            player_capex.append(combined_quality_capex)
        capex.append(player_capex)
    return capex


temp_capex = get_capex(sus_cost, growth_cost, result)


# print (temp_capex[0][1])
# print (temp_capex[0][2])
# print (temp_capex[0][3])
# print (temp_capex[0][4])
# need to go through all the players 

def get_revenues(price, volumes):
    revenues = {}
    for player_a in players[0]:
        for player_b in players[1]:
            for player_c in players[2]:
                for player_d in players[3]:
                    key = str(player_a) + str(player_b) + str(player_c) + str(player_d)
                    player_a_revenues = []
                    player_b_revenues = []
                    player_c_revenues = []
                    player_d_revenues = []
                    for year in range(31):
                        player_a_revenues.append(
                            volumes[0][player_a][0][year] * multipliers[key][0][year] + volumes[0][player_a][1][year] *
                            multipliers[key][1][year] + volumes[0][player_a][2][year] * multipliers[key][2][year])

                        player_b_revenues.append(
                            volumes[1][player_b][0][year] * multipliers[key][0][year] + volumes[1][player_b][1][year] *
                            multipliers[key][1][year] + volumes[1][player_b][2][year] * multipliers[key][2][year])

                        player_c_revenues.append(
                            volumes[2][player_c][0][year] * multipliers[key][0][year] + volumes[2][player_c][1][year] *
                            multipliers[key][1][year] + volumes[2][player_c][2][year] * multipliers[key][2][year])

                        player_d_revenues.append(
                            volumes[3][player_d][0][year] * multipliers[key][0][year] + volumes[3][player_d][1][year] *
                            multipliers[key][1][year] + volumes[3][player_d][2][year] * multipliers[key][2][year])
                    revenues[key] = [player_a_revenues, player_b_revenues, player_c_revenues, player_d_revenues]

    return revenues


temp = get_revenues(multipliers, result)


# fcfs is the aggregation of revenue/opex/capex
def get_fcfs(revenues, opex, capex):
    fcfs = {}
    for case in revenues:
        player_a = int(case[0])
        player_b = int(case[1])
        player_c = int(case[2])
        player_d = int(case[3])
        player_a_fcfs = []
        player_b_fcfs = []
        player_c_fcfs = []
        player_d_fcfs = []
        for i in range(31):
            player_a_fcfs.append(revenues[case][0][i] - opex[0][player_a - 1][i] - capex[0][player_a - 1][i])
            player_b_fcfs.append(revenues[case][1][i] - opex[1][player_b - 1][i] - capex[1][player_b - 1][i])
            player_c_fcfs.append(revenues[case][2][i] - opex[2][player_c - 1][i] - capex[2][player_c - 1][i])
            player_d_fcfs.append(revenues[case][3][i] - opex[3][player_d - 1][i] - capex[3][player_d - 1][i])
        fcfs[case] = [player_a_fcfs, player_b_fcfs, player_c_fcfs, player_d_fcfs]
    return fcfs


free_case = get_fcfs(temp, testing, temp_capex)


# fcfs look like 1st level players, 2nd level strat, 3rd level years
def get_npv(fcfs):
    npvs = {}
    for case in fcfs:
        temp_npvs = []
        for player in fcfs[case]:
            temp_npvs.append(np.npv(0.1, [0] + player))
        npvs[case] = temp_npvs
    return npvs


npv = get_npv(free_case)


def industry_best(npv):
    best_case = 'test'
    large = 0
    for case in npv:
        temp = sum(npv[case])
        if temp > large:
            large = temp
            best_case = case
    return best_case


def get_all_data(best_case, npv, volumes, multipliers):
    player_a = int(best_case[0])
    player_b = int(best_case[1])
    player_c = int(best_case[2])
    player_d = int(best_case[3])
    breakdown = npv[best_case]
    total = 0
    for i in breakdown:
        total += i
    vol_a = [sum(volumes[0][player_a][0]), sum(volumes[0][player_a][1]), sum(volumes[0][player_a][2])]
    vol_b = [sum(volumes[1][player_b][0]), sum(volumes[1][player_b][1]), sum(volumes[1][player_b][2])]
    vol_c = [sum(volumes[2][player_c][0]), sum(volumes[2][player_c][1]), sum(volumes[2][player_c][2])]
    vol_d = [sum(volumes[3][player_d][0]), sum(volumes[3][player_d][1]), sum(volumes[3][player_d][2])]

    # vol_a = [volumes[0][player_a][0][10], volumes[0][player_a][1][10], volumes[0][player_a][2][10]]
    # vol_b = [volumes[1][player_b][0][10], volumes[1][player_b][1][10], volumes[1][player_b][2][10]]
    # vol_c = [volumes[2][player_c][0][10], volumes[2][player_c][1][10], volumes[2][player_c][2][10]]
    # vol_d = [volumes[3][player_d][0][10], volumes[3][player_d][1][10], volumes[3][player_d][2][10]]
    vols = [vol_a, vol_b, vol_c, vol_d]
    vol_total_qual = [0, 0, 0]
    vol_total = 0
    for i in range(len(vols)):
        for j in range(len(vols[0])):
            vol_total += vols[i][j]
            vol_total_qual[j] += vols[i][j]
    prices = (multipliers[best_case][0][10], multipliers[best_case][1][10], multipliers[best_case][2][10])
    return (
    best_case, total, breakdown[0], breakdown[1], breakdown[2], breakdown[3], vols[0][0], vols[0][1], vols[0][2],
    vols[1][0], vols[1][1], vols[1][2], vols[2][0], vols[2][1], vols[2][2], vols[3][0], vols[3][1], vols[3][2],
    vol_total_qual[0], vol_total_qual[1], vol_total_qual[2], vol_total, prices[0], prices[1], prices[2])


def convert_to_csv(npvs):
    csv_file = 'Rio Paper Models/test.csv'
    f = open(csv_file, 'w')
    CSV = ""
    CSV += 'Case' + ',' + 'RIO' + ',' + 'VALE' + ',' + 'FMG' + ',' + 'BHP' + "\n"
    count = 1
    for k, v in npv.items():
        line = str(count) + ',' + str(v[0]) + ',' + str(v[1]) + ',' + str(v[2]) + ',' + str(v[3]) + "\n"
        CSV += line
        count += 1
    # You can store this CSV string variable to file as below
    with open(csv_file, "w") as file:
        file.write(CSV)


convert_to_csv(npv)

run()

# best = industry_best(npv)
# best = str(1111)
# answer = get_all_data(best, npv, result, multipliers)

runs_csv = 'policy_elas0.5_0422.csv'
f = open(runs_csv, 'w')
line_to_add = ''
line_to_add += 'Industry Max Case' + ',' + 'Total NPV' + ',' + 'Player A NPV' + ',' + 'Player B NPV' + ',' + 'Player C NPV' + ',' + 'Player D NPV' + ',' + 'Player A High' + ',' + 'Player A Medium' + ',' + 'Player A Low' + ',' + 'Player B High' + ',' + 'Player B Medium' + ',' + 'Player B Low' + ',' + 'Player C High' + ',' + 'Player C Medium' + ',' + 'Player C Low' + ',' + 'Player D High' + ',' + 'Player D Medium' + ',' + 'Player D Low' + ',' + 'Total High' + ',' + 'Total Medium' + ',' + 'Total Low' + ',' + 'Total Vol' + ',' + 'High Price' + ',' + 'Medium Price' + ',' + 'Low Price' + "\n"
# string_answer = ''
# for i in answer:
#     string_answer += str(i) + ','
# line_to_add += string_answer + '\n'



# output all 6561 cases
nine_cases = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
for a in nine_cases:
    for b in nine_cases:
        for c in nine_cases:
            for d in nine_cases:
                best = a + b + c + d
                answer = get_all_data(best, npv, result, multipliers)
                string_answer = ''
                for j in answer:
                    string_answer += str(j) + ','
                line_to_add += string_answer + '\n'



with open(runs_csv, "w") as file:
    file.write(line_to_add)

# things to include from Liz's request
# industry maximing 
# npvs by player 
# 2030 high/med/low volume totals (IESDS and maxizing)
# 2030 high/med/low price (IESDS and maxizing)

# cases in the excel spreadsheet
# run template
