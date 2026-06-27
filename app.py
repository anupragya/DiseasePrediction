from flask import Flask, render_template, url_for, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load your pre-trained model (Ensure this file is in your project directory)
# model = joblib.load('your_model_filename.pkl') 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/project', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        try:
            # 1. Extract the health metrics sent from your project.html form
            age = float(request.form.get('age', 0))
            gender = int(request.form.get('gender', 0))
            bmi = float(request.form.get('bmi', 0))
            blood_pressure = float(request.form.get('blood_pressure', 0))
            glucose_level = float(request.form.get('glucose_level', 0))
            cholesterol = float(request.form.get('cholesterol', 0))
            heart_rate = float(request.form.get('heart_rate', 0))
            smoking = int(request.form.get('smoking', 0))
            alcohol = int(request.form.get('alcohol', 0))
            physical_activity = int(request.form.get('physical_activity', 0))
            family_history = int(request.form.get('family_history', 0))
            
            # 2. Arrange features to match the exact order of your CleanedData.csv columns
            features = np.array([[age, gender, bmi, blood_pressure, glucose_level, 
                                  cholesterol, heart_rate, smoking, alcohol, 
                                  physical_activity, family_history]])
            
            # 3. Predict using your loaded model
            # prediction = model.predict(features)[0]
            # probability = model.predict_proba(features)[0][1] # If your model supports it
            
            # Placeholder result logic until you uncomment the model loading above:
            prediction = 0 
            
            return render_template('project.html', prediction=prediction, calculated=True)
            
        except Exception as e:
            return f"An error occurred during prediction: {str(e)}", 400

    # If it's a standard GET request, just display the empty form page
    return render_template('project.html', calculated=False)

# Essential missing block to run the development server
if __name__ == '__main__':
    app.run(debug=True)