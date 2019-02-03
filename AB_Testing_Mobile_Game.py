import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('AB_Test_Mobile_Game.csv')
#let's check that we have approximately equal number of users in each of the AB-testing groups:
print(df.groupby(['version'])['userid'].count())
"""
#simply out of curiosity, let's plot the typical quantity of game rounds taken by the user (most users play very few game rounds):
game_rounds = df.groupby(['sum_gamerounds'])['userid'].count().head(100)
ax = game_rounds.plot()
ax.set_xlabel("Quantity of Game Rounds")
ax.set_ylabel("Number of Users");
"""
#let's check what the average 1-day and 7-day retention were, and also how it differed in the control and treatment groups
print(df.retention_1.mean(), df.retention_7.mean())
print(df.groupby(['version'])['retention_1'].mean())
print(df.groupby(['version'])['retention_7'].mean())
#let's control for sample selection by randomly generating sumsamples of the data and repeating the analysis
def bootstrap(retention):
    bootstrap_df = []
    for i in range(5000):
        bootstrap_df.append(df.sample(frac = 1, replace = True).groupby(['version'])[retention].mean())        
    bootstrap_df = pd.DataFrame(bootstrap_df)
    return bootstrap_df
bootstrap_1 = bootstrap('retention_1')
bootstrap_7 = bootstrap('retention_7')
"""
a1 = bootstrap_1.plot.kde()
a1.set_xlabel("1-day Retention Average of the Random Data Subsamples")
a1.set_ylabel("Kernel Density of the Random Data Subsamples");
a7 = bootstrap_7.plot.kde()
a7.set_xlabel("7-day Retention Average of the Random Data Subsamples")
a7.set_ylabel("Kernel Density of the Random Data Subsamples");
"""
def difference(bootstrap, day):
    bootstrap[day] = ((bootstrap['gate_30'] - bootstrap['gate_40']) / bootstrap['gate_40'])*100
    return bootstrap[day] 
bootstrap_1['1_day_difference'] = difference(bootstrap_1, '1_day_difference')
bootstrap_7['7_day_difference'] = difference(bootstrap_7, '7_day_difference')
"""
ad = bootstrap_1['1_day_difference'].plot.kde()
ad.set_xlabel("% Difference in the Two Groups' 1 Day Retention")
ad.set_ylabel("Kernel Density of the Random Data Subsamples");
av = bootstrap_7['7_day_difference'].plot.kde()
av.set_xlabel("% Difference in the Two Groups' 7 Day Retention")
av.set_ylabel("Kernel Density of the Random Data Subsamples");
"""
print( "{:.2%}".format((bootstrap_1['1_day_difference']>0).mean()) )
print( "{:.2%}".format((bootstrap_7['7_day_difference']>0).mean()) )