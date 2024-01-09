#backend of the app
from flask import Flask,render_template,jsonify,request
import pickle
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
        return  render_template("result.html",res=res)
    else:
        return render_template('prediction.html')


#to run code in aloop
if __name__ == '__main__':
    app.run()