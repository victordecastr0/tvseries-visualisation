# %% codecell
#!pip install bertopic
#since this notebook was first made in Google Colab this line was necessary due
#to a issue with plotly

#the issue was found when trying to change hovering information, it raised
#"RuntimeError: dictionary changed size during iteration"
# %% codecell
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

data = {'season 1': [{'episodeNumber': '1', 'title': 'Pilot', 'released': '13 Sep. 2005', 'imDbRating': '8.7'}, {'episodeNumber': '2', 'title': 'Wendigo', 'released': '20 Sep. 2005', 'imDbRating': '8.0'}, {'episodeNumber': '3', 'title': 'Dead in the Water', 'released': '27 Sep. 2005', 'imDbRating': '8.1'}, {'episodeNumber': '4', 'title': 'Phantom Traveler', 'released': '4 Oct. 2005', 'imDbRating': '8.2'}, {'episodeNumber': '5', 'title': 'Bloody Mary', 'released': '11 Oct. 2005', 'imDbRating': '8.4'}, {'episodeNumber': '6', 'title': 'Skin', 'released': '18 Oct. 2005', 'imDbRating': '8.4'}, {'episodeNumber': '7', 'title': 'Hook Man', 'released': '25 Oct. 2005', 'imDbRating': '8.0'}, {'episodeNumber': '8', 'title': 'Bugs', 'released': '8 Nov. 2005', 'imDbRating': '7.0'}, {'episodeNumber': '9', 'title': 'Home', 'released': '15 Nov. 2005', 'imDbRating': '8.9'}, {'episodeNumber': '10', 'title': 'Asylum', 'released': '22 Nov. 2005', 'imDbRating': '8.5'}, {'episodeNumber': '11', 'title': 'Scarecrow', 'released': '10 Jan. 2006', 'imDbRating': '8.7'}, {'episodeNumber': '12', 'title': 'Faith', 'released': '17 Jan. 2006', 'imDbRating': '8.9'}, {'episodeNumber': '13', 'title': 'Route 666', 'released': '31 Jan. 2006', 'imDbRating': '7.4'}, {'episodeNumber': '14', 'title': 'Nightmare', 'released': '7 Feb. 2006', 'imDbRating': '8.3'}, {'episodeNumber': '15', 'title': 'The Benders', 'released': '14 Feb. 2006', 'imDbRating': '8.3'}, {'episodeNumber': '16', 'title': 'Shadow', 'released': '28 Feb. 2006', 'imDbRating': '8.6'}, {'episodeNumber': '17', 'title': 'Hell House', 'released': '30 Mar. 2006', 'imDbRating': '8.4'}, {'episodeNumber': '18', 'title': 'Something Wicked', 'released': '6 Apr. 2006', 'imDbRating': '8.6'}, {'episodeNumber': '19', 'title': 'Provenance', 'released': '13 Apr. 2006', 'imDbRating': '8.7'}, {'episodeNumber': '20', 'title': "Dead Man's Blood", 'released': '20 Apr. 2006', 'imDbRating': '8.5'}, {'episodeNumber': '21', 'title': 'Salvation', 'released': '27 Apr. 2006', 'imDbRating': '8.9'}, {'episodeNumber': '22', 'title': "Devil's Trap", 'released': '4 May 2006', 'imDbRating': '9.3'}], 'season 2': [{'episodeNumber': '1', 'title': 'In My Time of Dying', 'released': '28 Sep. 2006', 'imDbRating': '9.3'}, {'episodeNumber': '2', 'title': 'Everybody Loves a Clown', 'released': '5 Oct. 2006', 'imDbRating': '8.2'}, {'episodeNumber': '3', 'title': 'Bloodlust', 'released': '12 Oct. 2006', 'imDbRating': '8.3'}, {'episodeNumber': '4', 'title': "Children Shouldn't Play with Dead Things", 'released': '19 Oct. 2006', 'imDbRating': '8.0'}, {'episodeNumber': '5', 'title': 'Simon Said', 'released': '26 Oct. 2006', 'imDbRating': '8.6'}, {'episodeNumber': '6', 'title': 'No Exit', 'released': '2 Nov. 2006', 'imDbRating': '8.4'}, {'episodeNumber': '7', 'title': 'The Usual Suspects', 'released': '9 Nov. 2006', 'imDbRating': '8.7'}, {'episodeNumber': '8', 'title': 'Crossroad Blues', 'released': '16 Nov. 2006', 'imDbRating': '8.8'}, {'episodeNumber': '9', 'title': 'Croatoan', 'released': '7 Dec. 2006', 'imDbRating': '8.8'}, {'episodeNumber': '10', 'title': 'Hunted', 'released': '11 Jan. 2007', 'imDbRating': '8.5'}, {'episodeNumber': '11', 'title': 'Playthings', 'released': '18 Jan. 2007', 'imDbRating': '8.4'}, {'episodeNumber': '12', 'title': 'Nightshifter', 'released': '25 Jan. 2007', 'imDbRating': '9.0'}, {'episodeNumber': '13', 'title': 'Houses of the Holy', 'released': '1 Feb. 2007', 'imDbRating': '8.1'}, {'episodeNumber': '14', 'title': 'Born Under a Bad Sign', 'released': '8 Feb. 2007', 'imDbRating': '8.8'}, {'episodeNumber': '15', 'title': 'Tall Tales', 'released': '15 Feb. 2007', 'imDbRating': '9.2'}, {'episodeNumber': '16', 'title': 'Roadkill', 'released': '15 Mar. 2007', 'imDbRating': '8.9'}, {'episodeNumber': '17', 'title': 'Heart', 'released': '22 Mar. 2007', 'imDbRating': '8.8'}, {'episodeNumber': '18', 'title': 'Hollywood Babylon', 'released': '19 Apr. 2007', 'imDbRating': '8.5'}, {'episodeNumber': '19', 'title': 'Folsom Prison Blues', 'released': '26 Apr. 2007', 'imDbRating': '8.7'}, {'episodeNumber': '20', 'title': 'What Is and What Should Never Be', 'released': '3 May 2007', 'imDbRating': '9.4'}, {'episodeNumber': '21', 'title': 'All Hell Breaks Loose: Part 1', 'released': '10 May 2007', 'imDbRating': '9.2'}, {'episodeNumber': '22', 'title': 'All Hell Breaks Loose: Part 2', 'released': '17 May 2007', 'imDbRating': '9.5'}]}

# %% codecell
series_df = pd.read_csv('series_archive.csv')
total_seasons = series_df['Season'].nunique()
# %% codecell
fig = px.scatter(
  series_df,
  x='Number',
  y='Score',
  facet_col='Season',
  #with a large number of seasons the subplots were too thin
  facet_col_spacing = 0.005,
  #aplying total number of seasons in facet_col_wrap, facet_col_spacing works as intend
  facet_col_wrap = total_seasons,
  color='Season',
  color_continuous_scale=px.colors.sequential.Bluered,
  title = 'Supernatural episodes ratings by IMDb',
  hover_name = 'Episode name',
  hover_data = {
       'Score':True,
       'Episode name':False,
       'Season':False,
       'Number':False,
       'Release date': True,
       #a clever way i found to join to column values in one hover key without having to change from plotly express to plotly go
       'Episode': ['S{:02} EP{:02}'.format(season, number) for season, number in zip(series_df['Season'], series_df['Number'])]
  }
)

fig.update_xaxes(matches=None, showticklabels=False, showgrid=False, zeroline = False)
fig.update_yaxes(tick0 = 6.5, dtick=1.5)
fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', ' ')))
fig.update_layout(
  title = {'x': 0.5, 'y':0.9, 'xanchor': 'center', 'yanchor': 'top'},
  yaxis_title = 'Ratings',
  width = 100 * total_seasons
)
#hide the color legend
fig.update(layout_coloraxis_showscale=False)

#hide the xaxis label in each facet
for axis in fig.layout:
    if type(fig.layout[axis]) == go.layout.XAxis:
        fig.layout[axis].title.text = ''
# %% codecell
fig.show()
