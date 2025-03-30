from flask import Flask, render_template, request
import pandas as pd
import joblib

# Initialize Flask App
app = Flask(__name__)

# Load Trained Model & Scaler
model = joblib.load('churn_model_optimized.pkl')
scaler = joblib.load('scaler.pkl')

# Define feature order as per model
feature_order = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 
    'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 
    'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 
    'MonthlyCharges', 'TotalCharges'
]

# Home Route → Form Page
@app.route('/')
def home():
    return render_template('index.html')

# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        data = {
            'gender': int(request.form['gender']),
            'SeniorCitizen': int(request.form['SeniorCitizen']),
            'Partner': int(request.form['Partner']),
            'Dependents': int(request.form['Dependents']),
            'tenure': float(request.form['tenure']),
            'PhoneService': int(request.form['PhoneService']),
            'MultipleLines': int(request.form['MultipleLines']),
            'InternetService': int(request.form['InternetService']),
            'OnlineSecurity': int(request.form['OnlineSecurity']),
            'OnlineBackup': int(request.form['OnlineBackup']),
            'DeviceProtection': int(request.form['DeviceProtection']),
            'TechSupport': int(request.form['TechSupport']),
            'StreamingTV': int(request.form['StreamingTV']),
            'StreamingMovies': int(request.form['StreamingMovies']),
            'Contract': int(request.form['Contract']),
            'PaperlessBilling': int(request.form['PaperlessBilling']),
            'PaymentMethod': int(request.form['PaymentMethod']),
            'MonthlyCharges': float(request.form['MonthlyCharges']),
            'TotalCharges': float(request.form['TotalCharges'])
        }

        # Convert to DataFrame
        features = pd.DataFrame([data], columns=feature_order)

        # Scale numeric features
        features[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.transform(features[['tenure', 'MonthlyCharges', 'TotalCharges']])

        # Predict
        prediction = model.predict(features)
        result = 'Churn' if prediction[0] == 1 else 'No Churn'

        return render_template('index.html', prediction_text=f'Prediction: {result}')

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
