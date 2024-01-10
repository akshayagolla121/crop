#backend of the app
from flask import Flask,render_template,jsonify,request
import pickle
import sqlite3
app = Flask(__name__)

@app.route('/') #for home url empty /
def home():
    return render_template('home.html')


@app.route('/prediction.html',methods =['GET','POST']) #to know we need to open the prediction.html page
def prediction():
    if request.method == 'POST':
        nitro = request.form.get("nitrogen")
        phos = request.form.get("phosphorus")
        pott = request.form.get("potassium")
        temp = request.form.get("temperature")
        hum = request.form.get("humidity")
        ph = request.form.get("ph")
        rain = request.form.get("rainfall")
        print(nitro,phos,pott,temp,hum,ph,rain)
        with open('model.pkl','rb') as model_file: # to use our machine learning model in the app 
            mlmodel = pickle.load(model_file)
        res = mlmodel.predict([[float(nitro),float(phos),float(pott),float(temp),float(hum),float(ph),float(rain)]])   
        print(res)
        conn = sqlite3.connect('cropdatabase.db')
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO CROPS VALUES({nitro},{phos},{pott},{temp},{hum},{ph},{rain},'{res[0]}')''')
        conn.commit()
        return  render_template("result.html",res=res[0])
    else:
        return render_template('prediction.html')
    
    
@app.route('/showdata.html',methods =['GET','POST'])    
def showdata():
    conn = sqlite3.connect('cropdatabase.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM CROPS;')
    x = cur.fetchall()
    #print(data)
    li  = []
    for i in x:
        p = {}
        p['Nitrogen'] = i[0]
        p['Phosphorus'] = i[1]
        p['Potassium'] = i[2]
        p['Temperature'] = i[3]
        p['Humidity'] = i[4]
        p['Ph'] = i[5]
        p['Rainfall'] = i[6]
        p['Result'] = i[7]
        li.append(p)
    return render_template('showdata.html',data = li)


#to run code in aloop
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 5050) #to make this project public
