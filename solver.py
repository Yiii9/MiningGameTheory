import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import copy


# sets up the strategies, keys, choices, and npv output
def setup(cases, npv, pi, relative):
    strategies = {}
    keys = []
    choices = [[], [], [], []]
    for profile in range(0, len(cases)):
        profiles = profile + 1

        keys.append(profiles)
        strategies[profiles] = []

        strategies[profiles].append(int(cases['Rio'][profile]))
        strategies[profiles].append(int(cases['Vale'][profile]))
        strategies[profiles].append(int(cases['FMG'][profile]))
        strategies[profiles].append(int(cases['BHP'][profile]))

        choices[0].append(int(cases['Rio'][profile]))
        choices[1].append(int(cases['Vale'][profile]))
        choices[2].append(int(cases['FMG'][profile]))
        choices[3].append(int(cases['BHP'][profile]))

    # goes through the choices and eliminate duplicates
    choices_final = [[], [], [], []]
    for i in range(4):
        choices_final[i] = list(dict.fromkeys(choices[i]))
    for i in choices_final:
        i.sort()

    npv_outcome = {}
    pi_outcome = {}
    relative_outcome = {}

    for i in range(len(npv)):
        npv_outcome[i + 1] = [npv['RIO'][i], npv['VALE'][i], npv['FMG'][i], npv['BHP'][i]]
        pi_outcome[i + 1] = [pi['RIO'][i], pi['VALE'][i], pi['FMG'][i], pi['BHP'][i]]
        relative_outcome[i + 1] = [relative['RIO'][i], relative['VALE'][i], relative['FMG'][i], relative['BHP'][i]]

    return (strategies, keys, choices_final, npv_outcome, pi_outcome, relative_outcome)


def combine_dictionaries(strategies, outcome_npv, outcome_pi, outcome_relative):
    npv_result = {}
    pi_result = {}
    relative_result = {}
    for i in range(1, len(strategies) + 1):
        temp = strategies[i]
        npv_result[','.join(map(str, temp))] = outcome_npv[i]
        pi_result[','.join(map(str, temp))] = outcome_pi[i]
        relative_result[','.join(map(str, temp))] = outcome_relative[i]

    return npv_result, pi_result, relative_result


# if the NPV is within 2% of the max, then we let the tie metric be unchanged, otherwise 0
def preprocess_one_company(company, tolerance, choices, max_metric, tie_metric):
    comp = choices.pop(company)
    metric_processed = copy.deepcopy(tie_metric)
    for h in choices[0]:
        for i in choices[1]:
            for j in choices[2]:
                answer = 0
                maximum = -1000000
                for k in comp:
                    strat = [h, i, j]
                    strat.insert(company, k)
                    strat_str = ','.join(map(str, strat))
                    if max_metric[str(strat_str)][company] > maximum:
                        maximum = max_metric[strat_str][company]
                        answer = k
                for l in comp:
                    strat[company] = l
                    temp_strat_str = ','.join(map(str, strat))
                    if max_metric[str(temp_strat_str)][company] < maximum * (1 - tolerance) - 0.00000001:
                        metric_processed[str(temp_strat_str)][company] = 0
    choices.insert(company, comp)
    # print (metric_processed)

    return metric_processed


def best_response_one_company(company, tolerance, choices, max_metric):
    comp = choices.pop(company)
    dom_strats = []
    dom_strat_small = []
    dom_strat_dist = []
    dom_strat_dict = {}

    for h in choices[0]:
        for i in choices[1]:
            for j in choices[2]:
                answer = 0
                maximum = -10000000
                for k in comp:
                    strat = [h, i, j]
                    strat.insert(company, k)
                    strat_str = ','.join(map(str, strat))
                    if max_metric[str(strat_str)][company] > maximum:
                        maximum = max_metric[strat_str][company]
                        answer = k
                dom_strats.append(answer)
    for i in dom_strats:
        if i not in dom_strat_small:
            dom_strat_small.append(i)
            dom_strat_dict[i] = 1
        else:
            dom_strat_dict[i] += 1

    for i in dom_strat_dict:
        dom_strat_dist.append(dom_strat_dict[i])
    # dom_strat_small.sort()
    choices.insert(company, comp)

    return (dom_strat_small, dom_strat_dist)


def all_companies_one_round(tolerance, choices, rio_metric, vale_metric, fmg_metric, bhp_metric):
    rio_dom, rio_dist = best_response_one_company(0, tolerance, choices, rio_metric)
    vale_dom, vale_dist = best_response_one_company(1, tolerance, choices, vale_metric)
    fmg_dom, fmg_dist = best_response_one_company(2, tolerance, choices, fmg_metric)
    bhp_dom, bhp_dist = best_response_one_company(3, tolerance, choices, bhp_metric)
    print('Dominant Strategies:' + str(rio_dom) + str(vale_dom) + str(fmg_dom) + str(bhp_dom))
    print('Played Frequency: ' + str(rio_dist) + str(vale_dist) + str(fmg_dist) + str(bhp_dist))
    dom_list = [rio_dom, vale_dom, fmg_dom, bhp_dom]
    dom_dist = [rio_dist, vale_dist, fmg_dist, bhp_dist]
    return dom_list, dom_dist


def all_companies_all_rounds(tolerance, choices, rio_metric, vale_metric, fmg_metric, bhp_metric):
    one_dom, one_dist = all_companies_one_round(tolerance, choices, rio_metric, vale_metric, fmg_metric, bhp_metric)
    two_dom, two_dist = all_companies_one_round(tolerance, one_dom, rio_metric, vale_metric, fmg_metric, bhp_metric)
    three_dom, three_dist = all_companies_one_round(tolerance, two_dom, rio_metric, vale_metric, fmg_metric, bhp_metric)
    four_dom, four_dist = all_companies_one_round(tolerance, three_dom, rio_metric, vale_metric, fmg_metric, bhp_metric)
    five_dom, five_dist = all_companies_one_round(tolerance, four_dom, rio_metric, vale_metric, fmg_metric, bhp_metric)
    six_dom, six_dist = all_companies_one_round(tolerance, five_dom, rio_metric, vale_metric, fmg_metric, bhp_metric)
    seven_dom, seven_dist = all_companies_one_round(tolerance, six_dom, rio_metric, vale_metric, fmg_metric, bhp_metric)
    return [one_dom, two_dom, three_dom, four_dom, five_dom, six_dom, seven_dom], [one_dist, two_dist, three_dist,
                                                                                   four_dist, five_dist, six_dist,
                                                                                   seven_dist]


# given the starting points of the 4 companies, let each case evolve and append the result to a list
# s
def find_equilibria(dom_strat_list, rio_metric, vale_metric, fmg_metric, bhp_metric):
    dom_profile = []
    profile_values = {}
    for i in dom_strat_list[0]:
        for j in dom_strat_list[1]:
            for k in dom_strat_list[2]:
                for l in dom_strat_list[3]:
                    profile = [i, j, k, l]
                    strat_str = ','.join(map(str, profile))
                    value = [rio_metric[str(strat_str)][0], vale_metric[str(strat_str)][1],
                             fmg_metric[str(strat_str)][2], bhp_metric[str(strat_str)][3]]
                    dom_profile.append(profile)
                    profile_values[strat_str] = value

    def evolve(dom_profiles):
        new_profiles = []
        for i in range(len(dom_profiles)):
            old_profile = dom_profiles[i].copy()
            strat_str = ','.join(map(str, old_profile))
            old_values = profile_values[strat_str].copy()

            new_profile = dom_profiles[i].copy()
            for h in dom_strat_list[0]:
                temp_profile = dom_profiles[i].copy()
                temp_profile[0] = h
                temp_strat_str = ','.join(map(str, temp_profile))
                if profile_values[temp_strat_str][0] > old_values[0]:
                    old_values[0] = profile_values[temp_strat_str][0]
                    new_profile[0] = h

            for j in dom_strat_list[1]:
                temp_profile = dom_profiles[i].copy()
                temp_profile[1] = j
                temp_strat_str = ','.join(map(str, temp_profile))
                if profile_values[temp_strat_str][1] > old_values[1]:
                    old_values[1] = profile_values[temp_strat_str][1]
                    new_profile[1] = j

            for k in dom_strat_list[2]:
                temp_profile = dom_profiles[i].copy()
                temp_profile[2] = k
                temp_strat_str = ','.join(map(str, temp_profile))
                if profile_values[temp_strat_str][2] > old_values[2]:
                    old_values[2] = profile_values[temp_strat_str][2]
                    new_profile[2] = k

            for l in dom_strat_list[3]:
                temp_profile = dom_profiles[i].copy()
                temp_profile[3] = l
                temp_strat_str = ','.join(map(str, temp_profile))
                if profile_values[temp_strat_str][3] > old_values[3]:
                    old_values[3] = profile_values[temp_strat_str][3]
                    new_profile[3] = l
            new_profiles.append(new_profile)
        print(len(new_profiles))
        new_profiles_small = []
        for i in new_profiles:
            if i not in new_profiles_small:
                new_profiles_small.append(i)
        print(new_profiles)
        return (new_profiles)

    round_one = evolve(dom_profile)
    round_two = evolve(round_one)
    round_three = evolve(round_two)
    round_four = evolve(round_three)
    round_five = evolve(round_four)
    round_six = evolve(round_five)
    round_seven = evolve(round_six)
    round_eight = evolve(round_seven)
    round_nine = evolve(round_eight)
    temp_list = []
    for i in range(144):
        if round_six[i] == round_seven[i] == round_eight[i] == round_nine[i] == round_five[i]:
            print(round_six[i])
            print(i)
            if round_six[i] not in temp_list:
                temp_list.append(round_six[i])
    print(temp_list)
    # new_profiles_small = []
    # new_dom_strat_list = [[],[],[],[]]
    # for i in new_profiles:
    #     if i not in new_profiles_small:
    #         new_profiles_small.append(i)
    # for i in new_profiles_small:
    #     if i[0] not in new_dom_strat_list[0]:
    #         new_dom_strat_list[0].append(i[0])
    #     if i[1] not in new_dom_strat_list[1]:
    #         new_dom_strat_list[1].append(i[1])
    #     if i[2] not in new_dom_strat_list[2]:
    #         new_dom_strat_list[2].append(i[2])
    #     if i[3] not in new_dom_strat_list[3]:
    #         new_dom_strat_list[3].append(i[3])

    # print (new_profiles)
    # print ('halksjdkls')
    # print (new_profiles_small)
    # print ('halksjdklasdadaws')

    # print (new_dom_strat_list)
    # find_equilibria(new_dom_strat_list, rio_metric, vale_metric, fmg_metric, bhp_metric)


def run():
    npv_csv = pd.read_csv('Rio Paper Models/test.csv')
    pi_csv = pd.read_csv('Rio Paper Models/test.csv')
    relative_csv = pd.read_csv('Rio Paper Models/test.csv')
    cases = pd.read_csv('Rio Paper Models/1103_cases.csv')

    players = list(cases.columns[1:5])

    strategies, keys, choices, npv_r, pi_r, relative_r = setup(cases, npv_csv, pi_csv, relative_csv)
    npv_comb, pi_comb, rel_comb = combine_dictionaries(strategies, npv_r, pi_r, relative_r)

    def deal_with_inputs():
        tolerance = float(0)
        # tolerance = float(input('What tolerance from 0 to 1 do you want to run at? '))

        # rio_metric, vale_metric, bhp_metric, fmg_metric = npv_comb.copy(),npv_comb.copy(), npv_comb.copy(), npv_comb.copy()
        #print('Input \'pi\', \'rel\', or \'npv\' to change.')
        # rio = input('Rio: ')
        # vale = input('Vale: ')
        # fmg = input('FMG: ')
        # bhp = input('BHP: ')

        rio_metric = npv_comb.copy()
        vale_metric = npv_comb.copy()
        fmg_metric = npv_comb.copy()
        bhp_metric = npv_comb.copy()
        # preprocess_one_company(0,tolerance, choices, npv_comb, pi_comb)
        # preprocess_one_company(1,tolerance, choices, npv_comb, rel_comb)
        # if rio == 'pi':
        #     rio_metric = preprocess_one_company(0,tolerance, choices, npv_comb, pi_comb)
        # if rio == 'rel':
        #     rio_metric = preprocess_one_company(0,tolerance, choices, npv_comb, rel_comb)
        # if vale == 'pi':
        #     vale_metric = preprocess_one_company(1, tolerance, choices, npv_comb, pi_comb)
        # if vale == 'rel':
        #     vale_metric = preprocess_one_company(1, tolerance, choices, npv_comb, rel_comb)
        # if fmg == 'pi':
        #     fmg_metric = preprocess_one_company(2, tolerance, choices, npv_comb, pi_comb)
        # if fmg == 'rel':
        #     fmg_metric = preprocess_one_company(2, tolerance, choices, npv_comb, rel_comb)
        # if bhp == 'pi':
        #     bhp_metric = preprocess_one_company(3, tolerance, choices, npv_comb, pi_comb)
        # if bhp == 'rel':
        #     bhp_metric = preprocess_one_company(3, tolerance, choices, npv_comb, rel_comb)

        return rio_metric, vale_metric, bhp_metric, fmg_metric, tolerance

    rio_metric, vale_metric, bhp_metric, fmg_metric, tolerance = deal_with_inputs()

    dom, dist = all_companies_all_rounds(tolerance, choices, rio_metric, vale_metric, fmg_metric, bhp_metric)
    # find_equilibria([[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4],[1]],rio_metric, vale_metric, bhp_metric, fmg_metric)
    return dom, dist


dom, dist = run()
print (dom)
