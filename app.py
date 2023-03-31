from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    df=pd.read_csv('Sales Data.csv')

    # Get the user input from the form
    selected_year = int(request.form['year'])

    # Group data by 'Year' and 'Account', and calculate total sales
    sales_by_year_account = df.groupby(['Year', 'Account'])['Qty'].sum().reset_index()

    # Filter the results based on the sales threshold and the selected year
    low_sales_accounts = sales_by_year_account[(sales_by_year_account['Qty'] < 10) & (sales_by_year_account['Year'] == selected_year)]

    # Plot the data using seaborn
    plt.figure(figsize=(15, 8))
    sns.barplot(x='Year', y='Qty', hue='Account', data=low_sales_accounts, ci=None)
    plt.ylabel('Total Sales')
    plt.xlabel('Year')
    plt.title(f'Accounts with Sales Less Than 10 in {selected_year}')

    # Remove the legend
    plt.legend().remove()

    # Save the plot as a base64-encoded image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('plot.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
