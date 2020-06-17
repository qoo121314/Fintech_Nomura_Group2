import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Nomura Project'
df = pd.read_excel('index.xlsx')
subset = df[['time', 'author', 'type', 'title', 'score', 'filename']]
subset.sort_index(ascending=False, inplace=True)

app.layout = html.Div([
    html.H1(children='PTT 資料分析'),

    dcc.RangeSlider(
        id='my-range-slider',
        min=2012,
        max=2020,
        step=1,
        value=[2012, 2020],
    ),
    html.Div(id='output-container-range-slider'),


    dcc.Tabs([
        dcc.Tab(label='Category', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': subset.groupby("type").count().sort_values("time",ascending=False).index[:8], 'y': subset.groupby("type").count().sort_values("time", ascending=False)["time"][:8],
                            'type': 'bar', 'name': 'Category'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='文章列表', children=[
            dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in subset.columns],
            data=subset.to_dict('records'),
            style_table={'height': '500px', 'overflowY': 'auto'},
            style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
            ],
            style_header={
                    'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'
                },
            filter_action="native",
            sort_action="native",
            sort_mode="single",
            column_selectable="single"
            # sort_action="native"
        )
        ]),
        dcc.Tab(label='Tab three', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Theme Model', children=[
            html.Iframe(src=app.get_asset_url('lda.html'),
                style=dict(position="absolute", left="0", top="20", width="98%", height="85%"))
        ]),
    ])
])

@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected {} to {}'.format(value[0],value[1])






if __name__ == '__main__':
    app.run_server(debug=True)