# -*- coding: utf-8 -*-
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go

def make_graph(series_name):
    disk_engine = create_engine('sqlite:///series_info.db')

    episodes = pd.read_sql_query("SELECT * FROM episodes",disk_engine)
    desired_eps = episodes.loc[episodes['series_name'] == name]
    n_seasons = desired_eps.season.nunique()

    fig = px.scatter(
      desired_eps,
      x='ep_number',
      y='rating',
      facet_col='season',
      #with a large number of seasons the subplots were too thin
      facet_col_spacing = 0.005,
      #aplying total number of seasons in facet_col_wrap, facet_col_spacing works as intend
      facet_col_wrap = n_seasons,
      color='season',
      color_continuous_scale=px.colors.sequential.Bluered,
      title = name + ' episodes ratings by IMDb',
      hover_name = 'ep_name',
      hover_data = {
           'rating':':.1f',
           'ep_name':False,
           'season':False,
           'ep_number':False,
           'release_date': True,
           #a clever way i found to join to column values in one hover key without having to change from plotly express to plotly go
           'Episode': ['S{:02} EP{:02}'.format(season, number) for season, number in zip(desired_eps['season'], desired_eps['ep_number'])]
      }
    )

    fig.update_xaxes(matches=None, showticklabels=False, showgrid=False, zeroline = False)
    fig.update_yaxes(tick0 = 6.5, dtick=1.5)
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', ' ')))
    fig.update_layout(
      title = {'x': 0.5, 'y':0.9, 'xanchor': 'center', 'yanchor': 'top'},
      yaxis_title = 'Ratings',
      width = 100 * n_seasons
    )
    #hide the color legend
    fig.update(layout_coloraxis_showscale=False)

    #hide the xaxis label in each facet
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''

    return fig

def main():
    fig = make_graph('Supernatural')
    fig.show()
    return

if __name__ == '__main__':
    main()
