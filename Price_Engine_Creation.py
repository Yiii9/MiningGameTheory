from Player_Creation import *

initial_high_price = 80
initial_medium_price = 70
initial_low_price = 60
initial_prices = [initial_high_price, initial_medium_price, initial_low_price]

baseline_high_cagr = 1.024
baseline_medium_cagr = 1.024
baseline_low_cagr = 1.024
baseline_cagrs = [baseline_high_cagr, baseline_medium_cagr, baseline_low_cagr]

elasticity_elastic = 0.5

high_elasticities = [-0.2*elasticity_elastic, -0.1*elasticity_elastic, -0.1*elasticity_elastic]
medium_elasticities = [-0.1*elasticity_elastic, -0.2*elasticity_elastic, -0.1*elasticity_elastic]
low_elasticities = [-0.1*elasticity_elastic, -0.1*elasticity_elastic, -0.2*elasticity_elastic]
total_elasticities = [0, 0, 0]

all_elasticities = [high_elasticities, medium_elasticities, low_elasticities]

def baseline_qualities(amount, cagr):
    baseline_totals = []
    for quality in amount:
        temp  = []
        for i in range(31):
            if i < 10:
                temp.append(quality*cagr**i)
            else:
                temp.append(quality*cagr**10)
        baseline_totals.append(temp)
    return (baseline_totals)

baseline_total_volumes = baseline_qualities(totals, baseline_low_cagr)
# baseline_high_volumes = baseline_qualities(player_a, baseline_high_cagr)
# baseline_medium_volumes = baseline_qualities(player_b, baseline_medium_cagr)
# baseline_low_volumes = baseline_qualities(player_c, baseline_low_cagr)

players = all_players(players,cagrs)

def get_price_multipliers(players, baseline, high_e, medium_e, low_e, initial_price):
    all_multipliers = {}

    #player_a, player_b, player_c, and player_d are keys 
    for player_a in players[0]: 
        for player_b in players[1]:
            for player_c in players[2]:
                for player_d in players[3]:
                    key = str(player_a) + str(player_b) + str(player_c) + str(player_d)
                    low_quality_total = []
                    medium_quality_total = []
                    high_quality_total = []
                    for i in range(31):
                        high_quality_total.append(players[0][player_a][0][i] + players[1][player_b][0][i] + players[2][player_c][0][i] + players[3][player_d][0][i])
                        medium_quality_total.append(players[0][player_a][1][i] + players[1][player_b][1][i] + players[2][player_c][1][i] + players[3][player_d][1][i])
                        low_quality_total.append(players[0][player_a][2][i] + players[1][player_b][2][i] + players[2][player_c][2][i] + players[3][player_d][2][i])
                    high_multipliers = []
                    medium_multipliers = []
                    low_multipliers = []
                    for i in range(31):
                        high_multipliers.append(initial_price[0]*(high_quality_total[i]/baseline[0][i])**high_e[0] 
                            *(medium_quality_total[i]/baseline[1][i])**high_e[1] * 
                                (low_quality_total[i]/baseline[2][i])**high_e[2] )
                        medium_multipliers.append(initial_price[1]*(high_quality_total[i]/baseline[0][i])**medium_e[0] 
                            *(medium_quality_total[i]/baseline[1][i])**medium_e[1] * 
                                (low_quality_total[i]/baseline[2][i])**medium_e[2] )
                        low_multipliers.append(initial_price[2]*(high_quality_total[i]/baseline[0][i])**low_e[0] 
                            *(medium_quality_total[i]/baseline[1][i])**low_e[1] * 
                                (low_quality_total[i]/baseline[2][i])**low_e[2] )
                    all_multipliers[key] = [high_multipliers,medium_multipliers, low_multipliers]
    return (all_multipliers)

multipliers = get_price_multipliers(players, baseline_total_volumes, high_elasticities, medium_elasticities, low_elasticities, initial_prices)

# print (len(multipliers))
# print (multipliers['1111'])