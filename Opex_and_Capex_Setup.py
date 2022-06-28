from Player_Creation import *

cases = all_players(players,cagrs)

opex_elasticity = 1
# opex_low = 1
opex_low = 1.3
# opex_high = 1
opex_high = 0.9

opex_player_a = [32.50*opex_elasticity*opex_high,31*opex_elasticity,29*opex_elasticity*opex_low]
opex_player_b = [26*opex_elasticity*opex_high,24.8*opex_elasticity,23.20*opex_elasticity*opex_low]
opex_player_c = [32.50*opex_elasticity*opex_high,31*opex_elasticity,29*opex_elasticity*opex_low]
opex_player_d = [26*opex_elasticity*opex_high,24.8*opex_elasticity,23.20*opex_elasticity*opex_low]
opexs = [opex_player_a, opex_player_b, opex_player_c, opex_player_d]

other_player_a = [0,0,0]
other_player_b = [0,0,0]
other_player_c = [0,0,0]
other_player_d = [0,0,0]
others = [other_player_a, other_player_b, other_player_c, other_player_d]

capex_all = 1
capex_low = 1
capex_high = 1
# add new growth and sustaining capex
growth_player_a = [22.75*capex_all*capex_high,21.70*capex_all,20.30*capex_all*capex_low]
growth_player_b = [45.50*capex_all*capex_high,43.40*capex_all,40.60*capex_all*capex_low]
growth_player_c = [22.75*capex_all*capex_high,21.70*capex_all,20.30*capex_all*capex_low]
growth_player_d = [45.50*capex_all*capex_high,43.40*capex_all,40.60*capex_all*capex_low]
growths = [growth_player_a, growth_player_b, growth_player_c, growth_player_d]

sus_player_a = [11.375*capex_all*capex_high,10.85*capex_all,10.15*capex_all*capex_low]
sus_player_b = [22.75*capex_all*capex_high,21.70*capex_all,20.30*capex_all*capex_low]
sus_player_c = [11.375*capex_all*capex_high,10.85*capex_all,10.15*capex_all*capex_low]
sus_player_d = [22.75*capex_all*capex_high,21.70*capex_all,20.30*capex_all*capex_low]
suss = [sus_player_a, sus_player_b, sus_player_c, sus_player_d]

high_concentration = 0.65
medium_concentration = 0.62
low_concentration = 0.58
concentrations = [high_concentration, medium_concentration, low_concentration]

def total_variable_players(opexs, others, concentrations):
    player_total_variable_opex = []
    # why is this opex (check again too)
    for i in range(len(opexs)):
        temp = []
        for h in range(len(opexs[i])):
            temp.append((opexs[i][h]+others[i][h])/concentrations[h])
        player_total_variable_opex.append(temp)
    return player_total_variable_opex

def growth_players(growths, concentrations):
    player_growth_capex = []
    for i in growths:
        temp = []
        for h in range(len(i)):
                temp.append(i[h]/concentrations[h])
        player_growth_capex.append(temp)
    return player_growth_capex

def sus_players(sustainings, concentrations):
    player_sustaining_capex = []
    for i in sustainings:
        temp = []
        for h in range(len(i)):
                temp.append(i[h]/concentrations[h])
        player_sustaining_capex.append(temp)
    return player_sustaining_capex

growth_cost = growth_players(growths, concentrations)
sus_cost = sus_players(suss, concentrations)
total_var_cost = total_variable_players(opexs, others, concentrations)

# print (growth_cost)
# print (sus_cost)
# print (total_var_cost)

