#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# 
# > In this project I'll explore "Soccer Database", which contains differnt tables with data about top european leagues teams, matches and player, in the period of season 2008/2009 to season 2015/2016.
# The dataset was provided in SQLite format and have been checked in DB browser, and later on imported and extracted into python by "sqlalchemy" library.
# 

# #### By the end of the project the following questions should be answered : 
# 
# <ol>
#     <li><a href="#oldest">Oldest players</a></li>
#     <li><a href="#youngest">Youngest players</a></li>
#     <li><a href="#shortest">Shortest players</a></li>
#     <li><a href="#tallest">Tallest players</a></li>
#     <li><a href="#best">Best rated players</a></li>
#     <li><a href="#potential">Best potential rated players</a></li>
#     <li><a href="#apperances">Players with most appearances</a></li>
#     <li><a href="#season">Team scored most goals in a single season</a></li>
#     <li><a href="#team_goals">Team scored most goals</a></li>
#     <li><a href="#season_goals">Total number of goals for each season</a></li>  
#     <li><a href="#league_goals">Total number of goals for each League</a></li>
#     <li><a href="#team_improve">What teams improved the most over the time period?</a></li>    
#     <li><a href="#best_teams_attr">What team attributes lead to the most victories?</a></li>
#     <li><a href="#win_home_away">Relation between home and away wins</a></li>
#     <li><a href="#best_teams">Team with most wins</a></li>
#     <li><a href="#away_wins">Team with most away wins</a></li>
#     <li><a href="#home_wins">Team with most home wins</a></li>
# </ol>

# ## Importing libraries
# ### Importing data and converting sqlite files to CSV

#  

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from IPython.display import Image
get_ipython().run_line_magic('matplotlib', 'inline')


# #### Extract tables from 'sqlite' dataframe
# #### Then saving extracted tables into differnt CSV table to use later

# In[2]:


engine = create_engine('sqlite:///database.sqlite')
engine.table_names()


# In[3]:


conn = engine.connect()


# In[4]:


country = pd.read_sql_query('SELECT * FROM Country', engine)
country.to_csv('country.csv', index=False)


# In[5]:


league = pd.read_sql_query('SELECT * FROM League', engine)
league.to_csv('league.csv', index=False)


# In[6]:


match = pd.read_sql_query('SELECT * FROM Match', engine)
match.to_csv('match.csv', index=False)


# In[7]:


player = pd.read_sql_query('SELECT * FROM Player', engine)
player.to_csv('player.csv', index=False)


# In[8]:


player_attributes = pd.read_sql_query('SELECT * FROM Player_Attributes', engine)
player_attributes.to_csv('player_attributes.csv', index=False)


# In[9]:


team = pd.read_sql_query('SELECT * FROM Team', engine)
team.to_csv('team.csv', index=False)


# In[10]:


team_attributes = pd.read_sql_query('SELECT * FROM Team_Attributes', engine)
team_attributes.to_csv('team_attributes.csv', index=False)


#  

# # Data wrangling & Exploratory data analysis

#  

#  

# ## Players

# In[11]:


player = pd.read_csv('player.csv')
player.head()


# In[12]:


df_player = player.copy()
df_player.info()


# >#### Table has no Na values and datatypes of the columns are the right type except for the birthday which is a string and will convert it to datetime format and drop 'player_fifa_api_id' column because we don't need it for our analysis

# In[13]:


df_player.drop('player_fifa_api_id', axis = 1, inplace = True)
df_player['birthday'] = pd.to_datetime(df_player['birthday'], format = '%Y-%m-%d')


# In[14]:


df_player.head()


# ##### Create 4 different tables for oldest, youngest, shortest, tallest players and droping columns not going to use in the findings

# In[15]:


oldest_player = df_player.sort_values(by = 'birthday').head(10)
oldest_player.drop(['id','player_api_id','weight', 'height'], axis = 1, inplace = True)
oldest_player.to_csv('oldest_player.csv', index=False)

youngest_player = df_player.sort_values(by = 'birthday', ascending = False).head(10)
youngest_player.drop(['id','player_api_id','weight', 'height'], axis = 1, inplace = True)
youngest_player.to_csv('youngest_player.csv', index=False)

shortest_player = df_player.sort_values(by = 'height').head(10)
shortest_player.drop(['id','player_api_id','weight', 'birthday'], axis = 1, inplace = True)
shortest_player.to_csv('shortest_player.csv', index=False)

tallest_player = df_player.sort_values(by = 'height', ascending = False).head(10)
tallest_player.drop(['id','player_api_id','weight', 'birthday'], axis = 1, inplace = True)
tallest_player.to_csv('tallest_player.csv', index=False)


# <a id= 'oldest'></a>
# 
# ## Find the oldest players

# >#### A table been created with the oldest 20 players based on their birthday
# With the oldest player in the list *'Alberto Fontana'*

# In[16]:


oldest_player


# <a id= 'youngest'></a>
# 
# ## Find the youngest players

# >#### A table been created with the youngest 20 players based on their birthday
# With the youngest player in the list *'Jonathan Leko'*

# In[17]:


youngest_player


# <a id= 'shortest'></a>
# 
# # Find the shortest player

# >#### A table been created with the shortest 10 players based on their reported height
# With the shortest player in the list *'Juan Quero'*

# In[18]:


shortest_player


# <a id= 'tallest'></a>
# # Find the tallest player

# >#### A table been created with the tallest 10 players based on their reported height
# With the tallest player in the list *'Kristof van Hout'*

# In[19]:


tallest_player


# In[20]:


player_attributes = pd.read_csv('player_attributes.csv')
player_attributes.head()


# In[21]:


player_attributes.info()


# > player_attributes has 41 columns most of them not going to use during this analysis so I picked 3 coulmns('player_api_id','overall_rating','potential) that we are going to use in our next analysis and disregard the rest but only in a copy of the orginal table because we might need the orginal df later on, and checked the table for Nan values and found none

# In[22]:


player_attributes_1 = player_attributes[['player_api_id','overall_rating','potential']]
player_attributes_1


# In[23]:


player_attributes_1.info()


# 

# In[24]:


df_player.drop(['id','birthday','height','weight'], axis = 1, inplace = True)
df_player


# > We drop 4 more coulmns from copied player table because we are done with them for now and only need player name and ID to use it later to merge with other tables

# In[25]:


player_attributes_1 = pd.merge(left=df_player, right=player_attributes_1, left_on='player_api_id', right_on='player_api_id')
player_attributes_1


# In[26]:


player_attributes_1.drop('player_api_id', axis = 1, inplace = True)
player_attributes_1 = round(player_attributes_1.groupby('player_name').mean('overall_rating'), 2)
player_attributes_1


# > We drop player Id columns because we are not going to need it for our analysis and round up the average rating and potential to 2 decimal places for convenience.

# In[27]:


top_players = player_attributes_1.sort_values(by = 'overall_rating', ascending = False). head(10)
top_players.to_csv('top_players.csv')

top_players_potential = player_attributes_1.sort_values(by = 'potential', ascending = False). head(10)
top_players.to_csv('top_players.csv')


# <a id= 'best'></a>
# 
# # Top players with the best average overall rating

# >#### A table been created with the best rated 10 players based on their average performance
# With the best player in the list *'Lionel Messi'* with average rating 92.19

# In[28]:


top_players


# <a id= 'potential'></a>
# 
# # Top players with the best average potential rating

# >#### A table been created with the best potential rating 10 players based on their average performance
# With the best player in the list *'Lionel Messi'* with average potential rating 95.23

# In[29]:


top_players_potential


#  

# In[30]:


match = pd.read_csv('match.csv')
match.head()


# In[31]:


match.columns


# > Match table have 115 coulmns we can't do analysis on that much coulmns at the same time, so we only choose coulmns we going  to need for the next analysis which is players id in starting 11 in home and away teams and make a copy of that table to use then check if the table has NaN and drop them if their is any, then reshape the table from wide table to long table for our next analysis, then drop another column we created during melting the table and rename the column for convenience and prepare it for next merging step

# In[32]:


match_players = match[['home_player_1', 'home_player_2', 'home_player_3',
       'home_player_4', 'home_player_5', 'home_player_6', 'home_player_7',
       'home_player_8', 'home_player_9', 'home_player_10', 'home_player_11',
       'away_player_1', 'away_player_2', 'away_player_3', 'away_player_4',
       'away_player_5', 'away_player_6', 'away_player_7', 'away_player_8',
       'away_player_9', 'away_player_10', 'away_player_11']]
match_players


# In[33]:


match_players = match_players.melt()
match_players = match_players.dropna()
match_players.head()


# In[34]:


match_players.drop('variable', axis = 1, inplace = True)


# In[35]:


match_players.rename(columns = {'value':'player_id'}, inplace = True)


# In[36]:


player.drop(['id', 'player_fifa_api_id', 'birthday', 'height', 'weight'], axis = 1, inplace = True)


# In[37]:


appearance = pd.merge(left=player, right=match_players, left_on='player_api_id', right_on='player_id')
appearance


# In[38]:


appearance = appearance.groupby('player_name').count().sort_values(by = 'player_api_id',ascending = False)
appearance.drop('player_id', axis = 1,inplace = True)
appearance.rename(columns = {'player_api_id':'apperances'}, inplace = True)
appearance = appearance.head(10)
appearance.to_csv('player_most_appearances.csv')


# > Merge the player table and modfied match table into one table and count the number of apperances for each player in the least and drop id column because we have the player names now and rename 'player_api_id' column into 'apperances' for readabilty

# <a id= 'apperances'></a>
# 
# # Players with most apperances

# >#### A table been created with 10 players with the most apperances
# With the player with most appearances is *'Marcelo'* with with total of 513 apperances

# In[39]:


appearance


#  
#  

#  

# # Teams

#  

#  

# In[40]:


match = pd.read_csv('match.csv')
match.head()


# > Again with the match table has a lot of columns that we not going to use for analysis so we pick only the columns we going to need and check data types of the columns and if they have any NaN

# In[41]:


goal = match[['league_id','season', 'home_team_api_id', 'away_team_api_id','home_team_goal', 'away_team_goal']]
goal.head()


# In[42]:


goal.info()


# In[43]:


team = pd.read_csv('team.csv')
team.head()


# > With the team table we only need the team id and name so we drop the rest and check data type of the columns and check if their is any Nan's

# In[44]:


team.drop(['id','team_fifa_api_id','team_short_name'],axis = 1, inplace = True)
team.head()


# In[45]:


team.info()


# > For next analysis we going to duplicate the team tables twice(home and away) and rename their coulumns into (home and away columns) to preparete it for merge with match table and and find which team came up winning or a draw, then drop columns from league table that we are not going to use and rename the column into league name for readability then check data type and if the league table have any NaN's and then merged it into the newly created match results table, final drop of unnecessary and repeated coulmns and then rearange the columns for better readability.

# In[46]:


home_team = team.copy()
away_team = team.copy()


# In[47]:


home_team.rename(columns = {'team_api_id' : 'home_team_api_id','team_long_name': 'home_team'}, inplace = True)
away_team.rename(columns = {'team_api_id' : 'away_team_api_id','team_long_name': 'away_team'}, inplace = True)


# In[48]:


goal_home = pd.merge(left=goal, right=home_team, left_on='home_team_api_id', right_on='home_team_api_id')


# In[49]:


goal_home_away = pd.merge(left=goal_home, right=away_team, left_on='away_team_api_id', right_on='away_team_api_id')


# In[50]:


conditions = [goal_home_away['home_team_goal'] > goal_home_away['away_team_goal'],
              goal_home_away['home_team_goal'] < goal_home_away['away_team_goal']]
choices = [goal_home_away['home_team'], goal_home_away['away_team']]
goal_home_away['winner'] = np.select(conditions, choices, default = 'Draw')

goal_home_away.head()


# In[51]:


league = pd.read_csv('league.csv')
league.head()


# In[52]:


league.drop('id', axis = 1, inplace = True)
league.rename(columns = {'name':'league_name'}, inplace = True)


# In[53]:


league.info()


# In[54]:


goal_home_away_league = pd.merge(left=goal_home_away, right=league, left_on='league_id', right_on='country_id')
goal_home_away_league.head()


# In[55]:


goal_home_away_league.drop(['league_id', 'home_team_api_id', 'away_team_api_id', 'country_id'],axis = 1, inplace = True)
goal_home_away_league = goal_home_away_league.reindex(columns = ['league_name', 'season', 'home_team', 'away_team',
                                                                 'home_team_goal', 'away_team_goal','winner'])
goal_home_away_league.head()


# In[56]:


team_season_goals = goal_home_away_league.copy()


# In[57]:


home_goals = team_season_goals[['season','league_name', 'home_team', 'home_team_goal']].groupby(['season','league_name','home_team'], as_index = False)['home_team_goal'].sum().sort_values(by = 'home_team_goal',ascending = False)
away_goals = team_season_goals[['season','league_name', 'away_team', 'away_team_goal']].groupby(['season','league_name','away_team'], as_index = False)['away_team_goal'].sum().sort_values(by = 'away_team_goal',ascending = False)


# In[58]:


team_season_goals = pd.merge(left=home_goals, right=away_goals, left_on=['home_team','season'], right_on=['away_team','season'])
team_season_goals.head()


# In[59]:


team_season_goals.rename(columns = {'league_name_x':'league_name', 'home_team':'team'}, inplace = True)
team_season_goals['goals'] = team_season_goals['home_team_goal'] + team_season_goals['away_team_goal']
team_season_goals.drop(['league_name_y','away_team','home_team_goal','away_team_goal'],axis = 1, inplace = True)
team_season_goals = team_season_goals.sort_values(by = 'goals', ascending = False)


# > Merge teams goals after calulating the home and away goals for each club for each season and droping repeated coulmns and rename columns for better readability and finally sort the table by number of goals in descending manner.

# <a id= 'season'></a>
# # Most goals soccered in a season by a team

# >#### A table been created with top 20 clubs with most goals in a single season
# With the club with the most goals *'Real Madrid CF'* with 121 goals in season 2011/2012

# In[60]:


team_season_goals.head(20)


# In[125]:


def plt_attr(x_label,title):
    plt.xticks(fontsize=16)
    plt.xlabel(x_label, fontsize = 24)
    plt.title(title, fontsize=24);


# In[ ]:


plt.xticks(fontsize=16)
plt.xlabel('Teams', fontsize = 24)
plt.title('Teams with most goals in a single season', fontsize=24);


# In[126]:


team_season_goals.head(20).plot(x = 'team', y = 'goals', figsize = (14,8),width = 0.75, kind='bar', color = '#8DB600')
plt_attr('Teams','Teams with most goals in a single season')


# >#### The bar graph shows total number of goals scorred by teams in different seasons.

# In[62]:


team_season_goals.to_csv('team_season_goals.csv')


# In[63]:


team_goals = team_season_goals.groupby('team', as_index = False).sum('goals').sort_values(by = 'goals', ascending = False)


# <a id= 'team_goals'></a>
# 
# # Most goals scored by a team

# >#### A table been created with top 10 clubs with most goals in 6 seasons
# With the club with the most goals *'FC Barcelona'* with total 849 goals in 6 seasons

# In[64]:


team_goals.head(20)


# In[127]:


team_goals.head(20).plot(x = 'team', y = 'goals', figsize = (14,8),width = 0.75, kind='bar', color = '#8DB600')
plt_attr('Teams','Teams with most goals');


# >#### The bar graph shows total number of goals scorred by teams in all seasons.

# In[66]:


season_goals = team_season_goals.groupby('season', as_index = False).sum('goals').sort_values(by = 'goals', ascending = False)


# <a id= 'season_goals'></a>
# 
# # Total goals scored per season

# >#### A table been created with total goals socred in each season among all leagues
# With season 2015/2016 with most goals 9162

# In[67]:


season_goals


# In[129]:


season_goals.head(20).plot(x = 'season', y = 'goals', figsize = (14,8),width = 0.75, kind='bar', color = '#8DB600')
plt_attr('Seasons','Total number of goals socored each season')


# >#### The bar graph shows total number of goals scorred in different seasons.

# In[69]:


season_goals.to_csv('season_goals.csv')


# In[70]:


league_goals = team_season_goals.groupby('league_name', as_index = False).sum('goals').sort_values(by = 'goals', ascending = False)


# <a id= 'league_goals'></a>
# 
# # Total goals scored by league

# >#### A table been created with total goals socred in each league for all seasons
# With 'Spain LIGA BBVA' league with most goals 8412

# In[71]:


league_goals


# In[131]:


league_goals.head(20).plot(x = 'league_name', y = 'goals', figsize = (14,8),width = 0.75, kind='bar', color = '#8DB600')
plt_attr('Leagues','Total number of goals scored in each league')


# >#### The bar graph shows total number of goals scorred in different leagues.

# In[73]:


league_goals.to_csv('league_goals.csv')


# In[74]:


team_season_goals


# In[75]:


team_improve = pd.pivot(team_season_goals, columns='season', index=['league_name', 'team'], values='goals')
team_improve.head()


# In[76]:


team_improve.info()


# In[77]:


float_columns = ['2008/2009','2009/2010','2010/2011','2011/2012','2012/2013','2013/2014','2014/2015','2015/2016']
for x in float_columns:
    team_improve[x] = team_improve[x].astype('Int32')


# In[78]:


team_improve.info()


# In[79]:


team_improve = team_improve.dropna()
team_improve['differnce'] = team_improve['2015/2016'] - team_improve['2008/2009']
team_improve = team_improve.sort_values(by = 'differnce', ascending = False).head(8)


# >To find team improvement progress we converted team goals table into wide table with seasons as coulmns and teams as rows and checked the data types and turns out to be floats number and goals don't need to be float, so I converted all the columns into ints datatype, and some rows has na result for some seasons which could means that team has been relegated into lower tier league in that year so I choose to drop all clubs with na values to maintain data integrity, and then we calculated how much each team scored in first and last season and find the difference between them.

# In[80]:


team_improve.to_csv('team_improve.csv')


# In[81]:


team_improve = pd.read_csv('team_improve.csv')


# <a id= 'team_improve'></a>
# 
# # Best improved team in scoring goals

# >#### A table been created with difference between total goals scored in season 2008/2009 and season 2015/2016 to find the team improved in scoring goals the most between those 2 seasons and *'Paris Saint-Germain'* came first among these teams with 53 more golas scored (Over the double of number goals).

# In[82]:


team_improve


# ![title](best_improved_clubs.png)

# >The line graph shows best improved teams in number of goals over the 6 seasons period and it shows that Paris Saint-Germain shows the best steady improvement even if it did not score the most goals

# In[83]:


best_teams = goal_home_away_league.copy()


# >To calculate the cound of teams win we reuse best_teams table with only differnce that we going to drop all draw results since we not going to need it to calculate most wins and then count every team wins and drop repeated and unnecessary columns and rename tables for readability.

# In[84]:


best_teams = best_teams[best_teams.winner != 'Draw']
best_teams.head()


# In[85]:


best_teams = best_teams.groupby('winner', as_index = False).count().sort_values(by='league_name', ascending = False)
best_teams


# In[86]:


best_teams.drop(['season','home_team','away_team','home_team_goal','away_team_goal'], inplace = True, axis = 1)
best_teams.rename(columns = {'winner':'team', 'league_name':'wins'}, inplace = True)
best_teams = best_teams.head(10)


# <a id= 'best_teams'></a>
# 
# ### Teams with most wins

# >#### A table been created with top 10 clubs with most win in 6 seasons
# With the club with the most win *'FC Barcelona'* with total 234 wins in 6 seasons

# In[87]:


best_teams


# In[88]:


best_teams = pd.merge(left = team, right = best_teams, left_on = 'team_long_name', right_on = 'team')
best_teams


# In[89]:


best_teams.drop(['team_long_name','wins'], axis = 1, inplace = True)
best_teams


# In[90]:


team_attributes = pd.read_csv('team_attributes.csv')
team_attributes.head()


# In[91]:


team_attributes.info()


# > With team attributes table we only need numeric team attributes values so we drop all object/string columns and then find the average attribute rating for each team based on all matches played and round the number to 2 decimal places for convenience and then 'lef merge' the table with best teams table since we only want to see what the best teams have in commen not what all teams have on common.

# In[92]:


team_attributes.drop(['id','team_fifa_api_id','date','buildUpPlaySpeedClass','buildUpPlayDribblingClass',
                      'buildUpPlayPassingClass','buildUpPlayPositioningClass','chanceCreationPassingClass','chanceCreationCrossingClass',
                     'chanceCreationShootingClass','chanceCreationPositioningClass','defencePressureClass','defenceAggressionClass',
                      'defenceTeamWidthClass','defenceDefenderLineClass'], axis = 1, inplace = True)
team_attributes = round(team_attributes.groupby('team_api_id').mean(), 2)
team_attributes


# In[93]:


team_attributes.info()


# In[94]:


team_attributes = round(team_attributes.groupby('team_api_id').mean(), 2)
team_attributes


# In[95]:


best_teams_attr = pd.merge(left = best_teams, right = team_attributes, how = 'left', left_on = 'team_api_id', right_on = 'team_api_id')


# <a id= 'best_teams_attr'></a>
# 
# # Best teams attributes on average

# >#### A table been created with top 10 teams with most wins average attributes, and each team has different playing style and there is no single attribute can be linked to winning, but 'defence Aggression' attribute is the most consistant one on average among the best teams

# In[96]:


best_teams_attr


# ![title](best_teams_attr.png)

# >Line graph shows average attributes for best teams in european leagues based on number of wins

# In[97]:


best_teams_attr.to_csv('best_teams_attr.csv')


# > we use the goals table again but this time to find the teams with home or away win and count the wins either home or away and drop unnecessary columns and rearrange table coulmns for convenience.

# In[98]:


conditions = [goal_home_away['home_team_goal'] > goal_home_away['away_team_goal'],
              goal_home_away['home_team_goal'] < goal_home_away['away_team_goal']]
choices = ['home_team','away_team']
goal_home_away['winner'] = np.select(conditions, choices, default = 'Draw')

goal_home_away.head()


# In[99]:


win_home_away_teams = pd.merge(left=goal_home_away, right=league, left_on='league_id', right_on='country_id')
win_home_away_teams.head()


# In[100]:


win_home_away = win_home_away_teams.copy()


# In[101]:


win_home_away.drop(['league_id', 'home_team_api_id', 'away_team_api_id', 'country_id'],axis = 1, inplace = True)
win_home_away.head()


# In[102]:


win_home_away = win_home_away.reindex(columns = ['league_name', 'season', 'home_team', 'away_team', 
                                                 'home_team_goal', 'away_team_goal','winner'])
win_home_away.head()


# In[103]:


win_home_away = win_home_away.groupby(['league_name', 'winner'], as_index = False).count()


# In[104]:


win_home_away.head(6)


# <a id= 'win_home_away'></a>
# 
# ## Ratio of home to away wins in different leagues

# In[105]:


win_home_away.drop(['home_team','away_team','home_team_goal','away_team_goal'], axis = 1, inplace = True)
win_home_away.rename(columns = {'season':'total'}, inplace = True)
win_home_away


# In[134]:


win_home_away.pivot('league_name', 'winner', 'total').plot(color = ['yellow', 'red', 'limegreen'], figsize = (14,8),width = 0.75, kind='bar')
plt_attr('European Leagues','Home team win ratio to away win ratio in the different european laegues')


# >#### A table been created with the number of wins to compare between win ratio in home and away venues amon different leagues, among all leagues there's significant edge in playing home than away with the most signficant in 'Italy Serie A' and 'Scotland Premier League' has the least signficant difference among all reported european leagues

# In[107]:


bigest_difference =  win_home_away.query('league_name == "Italy Serie A"')
least_difference = win_home_away.query('league_name == "Scotland Premier League"')


# In[108]:


least_difference


# In[109]:


bigest_difference


# In[110]:


labels = ['draw', 'away win', 'home win']
colors = ['yellow', 'red', 'green']


# In[111]:


plt.pie(bigest_difference['total'], labels = labels, colors = colors, autopct='%.0f%%', 
        textprops={'fontsize': 14},radius = 1);
plt.xticks(fontsize=20)
plt.xlabel('Italy Serie A', fontsize = 20)
plt.title('Home-away win ratio in Italy Serie A', fontsize=24);


# >Pie chart shows percentage of home-away win ration in Italy Serie A

# In[112]:


plt.pie(least_difference['total'], labels = labels, colors = colors, autopct='%.0f%%', 
        textprops={'fontsize': 14},radius = 1);
plt.xticks(fontsize=20)
plt.xlabel('Scotland Premier League', fontsize = 20)
plt.title('Home-away win ratio in Scotland Premier League', fontsize=24);


# >Pie chart shows percentage of home-away win ration in Scotland Premier League

# In[113]:


win_home_away_teams.drop(['league_id', 'home_team_api_id', 'away_team_api_id', 'country_id','home_team_goal','away_team_goal'],axis = 1, inplace = True)
win_home_away_teams.head(20)


# In[114]:


win_home_away_teams = win_home_away_teams[win_home_away_teams.winner != 'Draw']
win_home_away_teams.head()


# In[115]:


win_home_away_teams = win_home_away_teams.groupby(['home_team', 'winner'], as_index = False).count()
win_home_away_teams


# In[116]:


win_home_away_teams.drop(['away_team', 'league_name'], axis = 1, inplace = True)
win_home_away_teams.rename(columns = {'winner':'win_as','season':'wins'}, inplace = True)
win_home_away_teams


# In[117]:


away_wins = win_home_away_teams[win_home_away_teams['win_as'] == 'away_team'].sort_values(by = 'wins', ascending = False)
away_wins.drop('win_as', inplace = True, axis = 1)
away_wins.rename(columns = {'wins':'away_wins'},inplace = True)


# <a id= 'away_wins'></a>
# 
# # Teams with the most away wins

# >#### A table been created with top 20 clubs with most away wins in 6 seasons
# With the club with the most away wins *'Kilmarnock'* with total 72 away wins in 6 seasons

# In[118]:


away_wins.head(20)


# In[132]:


away_wins.head(20).plot(x = 'home_team', y = 'away_wins', figsize = (14,8),width = 0.75, kind='bar', color = '#A7F432')
plt_attr('Teams','Teams with most away wins')


# >Bar chart for teams with best record in winning in away venues

# In[120]:


away_wins.to_csv('away_wins.csv')


# In[121]:


home_wins = win_home_away_teams[win_home_away_teams['win_as'] == 'home_team'].sort_values(by = 'wins', ascending = False)
home_wins.drop('win_as', inplace = True, axis = 1)
home_wins.rename(columns = {'wins':'home_wins'},inplace = True)


# <a id= 'home_wins'></a>
# 
# # Teams with the most home wins

# >#### A table been created with top 20 clubs with most home wins in 6 seasons
# With the club with the most home wins *'FC Barcelona'* with total 131 home wins in 6 seasons

# In[122]:


home_wins.head(20)


# In[133]:


home_wins.head(20).plot(x = 'home_team', y = 'home_wins', figsize = (14,8),width = 0.75, kind='bar', color = '#A7F432')
plt_attr('Teams','Teams with most home wins')


# >Bar chart for teams with best record in winning in home venues

# In[124]:


home_wins.to_csv('home_wins.csv')


#  

# ## Conclusions
# 
# > Best improved team: Based on improvement in number of goals scored each season, Paris Saint-Germain is the best improved team in the past 8 seasons 
# 
# > Home to away win ratio based on different leagues: with all leagues their are more home wins than away wins in total but you can see a gap differnce between home-away win ratio in different leagues with the Scotland Premier League	has the least home-away win ratio, while Italy Serie A has the most gap between home and away wins
# 
# >What team attributes lead to the most victories: Best teams(Based on total number of wins) have different playing styles and no only one single attribute can be pointed to be the cause of victries, but among the best teams 'defence Aggression' is the most average stat among the best team

# ## Data limitation
# 
# > Some tables has too many columns (115 in match table), which making wrangling hideous sometimes
# 
# > Some columns have ver long, scrambled, unclear data that is very hard to understand and wrangle
# 
# > A new table for transfers could be useful
