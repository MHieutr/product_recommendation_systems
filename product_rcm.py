from dash import Dash, dcc, html, Input, Output
import pandas as pd
import ast

recommendations_df = pd.read_csv('Product_rcm_data.csv')

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={
        'width': '620px',
        'height': '400px',
        'padding': '10px',
        'font-family': 'cursive',
        'background-color': '#FFC7C7',
        'border-radius': '16px',
        'margin': '100px auto'
    },
    children=[
        html.H1("Product Recommendation System", style={'text-align': 'center', 'color': '#8785A2'}),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': product, 'value': product} for product in recommendations_df['product']],
            value='Turmeric Powder/Arisina Pudi',
            style={
                'background-color': '#FFE2E2',
                'color': '#8785A2',
                'border': '1px solid #8785A2',
                'font-size': '14px',
                'border-radius': '8px', 
            },
        ),
        html.Div(id='recommendations', style={'background-color': '#F6F6F6', 'border-radius': '8px', 'margin-top': '10px'})
    ]
)

@app.callback(
    Output('recommendations', 'children'),
    [Input('product-dropdown', 'value')]
)
def update_recommendations(selected_product):
    recommended_products = recommendations_df[recommendations_df['product'] == selected_product]['10_rcm_product'].values[0]
    recommended_products = ast.literal_eval(recommended_products)
    return html.Div(
        children=[html.Li(product, style={'color': '#8785A2', 'font-size': '14px', 'list-style':'none', 'margin': '5px 0px'})
                  for product in recommended_products], style={'padding-left': '10px'})

if __name__ == '__main__':
    app.run_server(debug=False)



