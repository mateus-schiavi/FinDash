from flask import Flask, render_template
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Carregar dados de exemplo (substitua por seus próprios dados)
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=10),
        'Revenue': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
        'Expenses': [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
    }
    df = pd.DataFrame(data)

    # Criar visualização Plotly
    fig = px.line(df, x='Date', y=['Revenue', 'Expenses'], title='Finance Dashboard')

    # Converter a figura Plotly em HTML
    graph_html = fig.to_html(full_html=False)

    # Renderizar o template HTML com o gráfico
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
