import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df2 = pd.read_csv('BigBasket.csv')  
df2 = df2.drop_duplicates(subset=['product']).reset_index(drop = True)
df2 = df2.drop(['index','sale_price', 'market_price', 'rating', 'description'], axis = 1)
df2 = df2.dropna().reset_index(drop = True)

def process_and_combine(row):
    combined = ' '.join(row.drop('product')).lower()
    return f"{combined}"

df2['soup'] = df2.apply(process_and_combine, axis=1)
df2['soup'] = df2['soup'].str.replace(r'[&,]', ' ', regex=True)
df2['soup'] = df2['soup'].str.split().str.join(' ')

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df2['soup'])
cos_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df2['product'])

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div( style= {
        'width': '600px',
        'height': '400px',
        'padding': '10px',
        'font-family': 'cursive',
        'background-color': '#FFC7C7',
        'border-radius': '16px',
        'display': 'flex',
        'flex-direction': 'column',
        'gap': '10px'
    }, 
    children = [
        html.H1("Product Recommendation Systems", style= {'text-align': 'center', 'color': '#8785A2'}),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': product, 'value': product} for product in df2['product']],
            value='Turmeric Powder/Arisina Pudi',
            style={
                    'background-color': '#FFE2E2',
                    'color': '#8785A2',
                    'border': '1px solid #8785A2',
                    'font-size': '14px',
                    'border-radius': '8px'
                    },
        ),
        html.Div(id='recommendations', style={'background-color': 'white', 'border-radius': '8px'})
])

@app.callback(
    Output('recommendations', 'children'),
    [Input('product-dropdown', 'value')]
)
def update_recommendations(selected_product):
    recommended_products = recommendations(selected_product, cos_sim)
    return html.Div(
                  children=[html.P(product, style={'color': '#8785A2', 'font-size': '14px', 'line-height': '10px'}) 
                            for product in recommended_products], style= {'padding-left': '10px'})

def recommendations(title, cosine_sim=cos_sim):
    index = indices[indices == title].index[0]
    similarity_scores = pd.Series(cosine_sim[index]).sort_values(ascending=False)
    top_10_products = list(similarity_scores.iloc[1:11].index)
    return [list(df2['product'])[i] for i in top_10_products]

if __name__ == '__main__':
    app.run_server(debug=True)
