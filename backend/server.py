from flask import Flask, jsonify, request
from flask_cors import CORS #comment this on deployment
import sqlite3
import pickle;
import numpy as np;

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
clf= pickle.load(open("decisiontree.pickle", 'rb'))
CORS(app) #comment this on deployment
con = sqlite3.connect("dsproject2023.db", check_same_thread=False)
cur = con.cursor()

def getResponse(rows,columns):
    sql = """SELECT Genre,count(*) 
             FROM game
             WHERE Genre = ?
             GROUP BY Genre
             ORDER BY count(*) DESC
             LIMIT 0,10"""
    
    #สร้าง BarChart Data
    labels = []
    data = []
    for row in rows :
        labels.append(row[0])
        data.append(row[1])

    result = dict()
    result["columns"] = columns
    result["rows"] = rows
    result["chart"] = dict()
    result["chart"]["labels"] = labels
    result["chart"]["data"] = data


    response = jsonify(result)
    
    return response

def getHistogram(listData,bins):
    hist, bin_edges = np.histogram(listData, bins=bins)
    rows = []
    for i in range(len(hist)):
        middle = (bin_edges[i] +  bin_edges[i+1])/2;
        row = (float(middle), int(hist[i]))
        rows.append(row)
    return rows


@app.route('/')
def index():
    return 'Python is fun'



@app.route('/api/ex02combobox/a')
def ex02comboboxA():
    sql = """SELECT Genre, count(*) 
             FROM game GROUP BY Genre 
             ORDER BY Count(*) DESC 
          """
    res = cur.execute(sql)
    rows = res.fetchall()
    columns =  ["Genre", "numberOfGenre"]

    response = getResponse(rows,columns)
    
    return response

@app.route('/api/UserInputEx02/<input1>')
def ex02UserInput(input1):
    sql = """SELECT Global_Sales
             FROM game WHERE Genre = ?"""
    param = [str(input1)]
    res = cur.execute(sql,param)
    rows = res.fetchall()
    listData = []
    for row in rows:
        listData.append(row[0])

    rows = getHistogram(listData,10)
    columns =  ["ยอดขายทั่วโลก", "จำนวนเกม"]
    response = getResponse(rows,columns)

    return response


#ตัวอย่าง Ex05 Data
@app.route('/abalone/data/')
def getAbaloneData():
    #columns = '"Sex","Length","Diameter","Height","Whole weight","Shucked weight","Viscera weight","Shell weight","Rings"'
    columns = '"YearsExperience","Age","Salary"'
    sql = "SELECT " + columns + "FROM Salary_Data"
                
    res = cur.execute(sql)
    rows = res.fetchall()
    

    result = dict()
    result["columns"] = ["YearsExperience","Age","Salary"]
    result["rows"] = rows


    response = jsonify(result)
    
    return response
#http://127.0.0.1:5000/api/dataex05
@app.route('/api/dataex05/')
def dataex05():
    #columns = '"Sex","Length","Diameter","Height","Whole weight","Shucked weight","Viscera weight","Shell weight","Rings"'
    columns = '"YearsExperience","Age","Salary"'
    sql = "SELECT " + columns + "FROM Salary_Data "
                
    res = cur.execute(sql)
    rows = res.fetchall()
    

    result = dict()
    result["columns"] = ["YearsExperience","Age","Salary"]
    result["rows"] = rows


    response = jsonify(result)
    
    return response

#ตัวอย่าง Ex05 Predict
@app.route('/abalone/predict/',methods = ['POST'])
def predictAbaloneRing():
    
    if request.method == 'POST':
      YearsExperience = request.form['YearsExperience']
      Age = request.form['Age']
      predict_input = np.array([[YearsExperience,Age]])
      predict_output = clf.predict(predict_input)
    
    
    return jsonify(predict_output[0])

@app.route('/api/predictex05/',methods = ['POST'])
def predictex05():
    
    if request.method == 'POST':
      YearsExperience = request.form['YearsExperience']
      Age = request.form['Age']
      predict_input = np.array([[YearsExperience,Age]])
      predict_output = clf.predict(predict_input)
    
    
    return jsonify(predict_output[0])

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=8000)