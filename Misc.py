import pandas as pd
ore_df = pd.read_csv('policy_elas0.5_0422.csv',index_col = False)
ore_df['Total High Ore Volume'] = ore_df.apply(lambda row: row['Total High']*(1/0.65), axis = 1) #1/0.65
ore_df['Total Medium Ore Volume'] = ore_df.apply(lambda row: row['Total Medium']*(1/0.62), axis = 1) #1/0.62
ore_df['Total Low Ore Volume'] = ore_df.apply(lambda row: row['Total Low']*(1/0.58), axis = 1) #1/0.58
ore_df['Total Ore Volume'] = ore_df.apply(lambda row: row['Total Low Ore Volume'] + row['Total Medium Ore Volume'] + row['Total High Ore Volume'], axis = 1)
ore_df.to_csv("policy_elas0.5_updated_ore.csv")