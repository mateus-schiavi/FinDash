from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# DataFrame para armazenar os dados
data = {
    'Date': pd.date_range(start='2024-01-01', periods=10),
    'Revenue': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
    'Expenses': [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
}
df = pd.DataFrame(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obter os valores de despesas e receitas do formulário
        revenue = float(request.form['revenue'])
        expenses = float(request.form['expenses'])
        
        # Atualizar os dados do DataFrame
        new_data = {'Date': pd.Timestamp.now(), 'Revenue': revenue, 'Expenses': expenses}
        df.loc[len(df)] = new_data
        
    # Criar visualização Plotly
    fig = px.line(df, x='Date', y=['Revenue', 'Expenses'], title='Finance Dashboard')

    # Converter a figura Plotly em HTML
    graph_html = fig.to_html(full_html=False)

    # Renderizar o template HTML com o gráfico
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
