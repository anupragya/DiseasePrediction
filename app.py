from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load your actual trained machine learning model
try:
    model = joblib.load(r'C:\Users\anupr\OneDrive\Desktop\medical_disease\models\RandomForest.lb')
except FileNotFoundError:
    print("Warning: 'RandomForest.lb' not found. Please run train_model.py first.")
    model = None

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
        if model is None:
            return jsonify({'success': False, 'error': 'Model file not loaded on server.'}), 500
            
        try:
            # Extract clinical metrics sent from your project form
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
            
            # Combine into a feature vector matching your CleanedData.csv columns exactly
            features = np.array([[age, gender, bmi, blood_pressure, glucose_level, 
                                  cholesterol, heart_rate, smoking, alcohol, 
                                  physical_activity, family_history]])
            
            # Live Model Execution
            prediction = int(model.predict(features)[0])
            
            # Get probability percentage for Class 1 (Disease presence)
            probabilities = model.predict_proba(features)[0]
            risk_probability = float(probabilities[1] * 100)
            
            return jsonify({
                'success': True,
                'prediction': prediction,
                'probability': round(risk_probability, 1)
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    return render_template('project.html')

if __name__ == '__main__':
    app.run(debug=True)

