from flask import Flask, redirect, url_for, request, Response, render_template,jsonify
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
from io import BytesIO
import base64

plt.switch_backend('Agg')
app = Flask(_name_)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '23110350'
app.config['MYSQL_DB'] = 'electoral_bonds'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['query']
        results_purchase, results_redemption = search(search_query)
        return render_template('search_results.html', results_purchase=results_purchase, results_redemption=results_redemption)
def search(bond_number):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM eb_purchase_details WHERE Bond Number = %s OR Name of the Purchaser = %s OR Reference No (URN) = %s", (bond_number, bond_number, bond_number))
    results_purchase = cursor.fetchall()
    cursor.execute("SELECT * FROM eb_redemption_details WHERE Bond Number = %s OR Name of the Political Party = %s OR Pay Branch Code = %s", (bond_number, bond_number, bond_number))
    results_redemption = cursor.fetchall()
    cursor.close()
    return results_purchase , results_redemption

@app.route('/bar_chart_data', methods=['GET'])
def bar_chart_data():
    cursor = mysql.connection.cursor()  
    cursor.execute("SELECT Name of the Political Party,  SUM(CAST(REPLACE(Denominations, ',', '') AS DECIMAL(20, 2))) FROM eb_redemption_details GROUP BY Name of the Political Party")

    results = cursor.fetchall()  
    labels = [result[0] for result in results] 
    sizes = [result[1] for result in results]  
    data = {
        "labels": labels,
        "values": sizes
    }

    cursor.close() 
    return jsonify(data) 
if _name_ == '_main_':
    app.run(debug=True)