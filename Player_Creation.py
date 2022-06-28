import math

expand_cagr = 1.06
hold_cagr = 1.00
decline_cagr = 0.97
cagrs = [expand_cagr, hold_cagr, decline_cagr]

medium_cagr_fixed = 1.00

player_a = [175,1,175]
player_b = [175,1,175]
player_c = [112.5,1,112.5]
player_d = [112.5,1,112.5]
totals = [575,4,575]
players = [player_a, player_b, player_c, player_d]

def get_cases(high, medium, low, high_cagr, medium_cagr, low_cagr):
    high_volumes = []
    medium_volumes = []
    low_volumes = []

    for i in range(0,31):
        if i < 10:
            high_volumes.append(high*high_cagr**i)
            medium_volumes.append(medium*medium_cagr**i)
            low_volumes.append(low*low_cagr**i)
        else:
            high_volumes.append(high*high_cagr**10)
            medium_volumes.append(medium*medium_cagr**10)
            low_volumes.append(low*low_cagr**10)
    
    return [high_volumes, medium_volumes, low_volumes]

# print(get_cases(players[0][0], players[0][1], players[0][2], 1.06, medium_cagr_fixed, 0.97))

def player_cases(player, cagrs):
    player_cases = {}
    count = 1 
    for a in cagrs:
        for b in cagrs:
            player_cases[count] = get_cases(player[0], player[1], player[2], a, medium_cagr_fixed, b)
            count += 1 
    return player_cases

def all_players(players,cagrs):
    player_a_cases = player_cases(players[0], cagrs)
    player_b_cases = player_cases(players[1], cagrs)
    player_c_cases = player_cases(players[2], cagrs)
    player_d_cases = player_cases(players[3], cagrs)
    return (player_a_cases, player_b_cases, player_c_cases, player_d_cases)

result = all_players(players,cagrs)

# print (result[0])


# tuple of dictionaries, each key represents a strategy 
# strategies 
# 1: expand expand 2: expand sustain 3: expand decline 
# 4: sustain expand 5: sustain sustain 6: sustain decline 
# 7: decline expand 8: decline sustain 9: decline decline 

# Mapping from mine to Rich's 
# 1:1, 2:2, 3:5, 4:3, 5:8, 6:4, 7:7, 8:6, 9:9
      

