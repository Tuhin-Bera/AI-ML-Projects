from flask import Flask, render_template, request
import  pandas as pd
import  pickle


app = Flask(__name__)

car = pd.read_csv("cleaned_car.csv")
model = pickle.load(open("Liner_regressionmodel.pkl", "rb"))



@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models_dict = car.groupby('company')['name'].apply(list).to_dict()
    years = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()

    return render_template(
        "index.html",
        companies=companies,
        car_models_dict=car_models_dict,   # <-- add this!
        years=years,
        fuel_type=fuel_type
    )

@app.route('/predict', methods=['POST'])
def predict():
    company = request.form.get('company')
    car_model = request.form.get('model')
    year = int(request.form.get('year'))
    fuel_type = request.form.get('fuel_type')
    kms_driven = int(request.form.get('kms_driven'))
    print(company, car_model, year, fuel_type, kms_driven)
    input_data = pd.DataFrame(
        [[car_model, company, year, kms_driven, fuel_type]],
        columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']
    )
    prediction = model.predict(input_data)
    # print(prediction[0])
    return  str(prediction[0])




if __name__ == '__main__':
    app.run(debug=True)