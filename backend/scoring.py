import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import List, Dict, Tuple

MODEL_PATH = "credit_model.pkl"
SCALER_PATH = "scaler.pkl"

def create_training_data():
    """
    Generate realistic training data for credit scoring.
    In production, this would come from historical data.
    """
    np.random.seed(42)
    n_samples = 1000
    
    # Generate features
    ages = np.random.normal(35, 12, n_samples)
    ages = np.clip(ages, 18, 80)
    
    incomes = np.random.lognormal(9, 0.8, n_samples)  # Log-normal distribution for income
    expenses = incomes * np.random.uniform(0.3, 0.9, n_samples)  # Expenses as % of income
    
    debt_percentages = np.random.beta(2, 5, n_samples) * 100  # Beta distribution for debt %
    previous_loans = np.random.poisson(2, n_samples)  # Poisson for loan count
    late_payments = np.random.poisson(1, n_samples)  # Poisson for late payments
    
    # Binary features
    marital_encoded = np.random.binomial(1, 0.6, n_samples)  # 60% married
    active_debts = np.random.binomial(1, 0.4, n_samples)  # 40% have active debts
    active_cards = np.random.binomial(1, 0.7, n_samples)  # 70% have credit cards
    
    payment_delays = np.random.exponential(5, n_samples)  # Exponential for delays
    balances = np.random.lognormal(7, 1, n_samples)  # Log-normal for balances
    
    # Create feature matrix
    X = np.column_stack([
        ages,
        incomes,
        expenses,
        debt_percentages,
        previous_loans,
        late_payments,
        marital_encoded,
        active_debts,
        active_cards,
        payment_delays,
        balances
    ])
    
    # Create realistic target variable (0 = good credit, 1 = bad credit)
    # Higher risk factors increase probability of bad credit
    risk_score = (
        (debt_percentages > 50) * 0.3 +
        (late_payments > 2) * 0.4 +
        (expenses / incomes > 0.8) * 0.2 +
        (previous_loans > 3) * 0.1 +
        (payment_delays > 10) * 0.2 +
        np.random.normal(0, 0.1, n_samples)  # Add some noise
    )
    
    y = (risk_score > 0.5).astype(int)
    
    return X, y

def train_model():
    """Train the credit scoring model"""
    print("Training credit scoring model...")
    
    X, y = create_training_data()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_scaled, y)
    
    # Save model and scaler
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    
    print(f"Model trained with accuracy: {model.score(X_scaled, y):.3f}")
    return model, scaler

def load_model():
    """Load the trained model and scaler"""
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    else:
        model, scaler = train_model()
    return model, scaler

def preprocess_features(data: dict) -> List[float]:
    """Convert input data to feature vector"""
    # Encode marital status
    marital_encoded = 1 if data['marital_status'].lower() in ['casado', 'married'] else 0
    
    # Convert boolean to int
    active_debts = 1 if data['active_debts'] else 0
    active_cards = 1 if data['active_credit_cards'] else 0
    
    features = [
        float(data['age']),
        float(data['monthly_income']),
        float(data['monthly_expense']),
        float(data['debt_percentage']),
        float(data['previous_loans']),
        float(data['late_payments']),
        float(marital_encoded),
        float(active_debts),
        float(active_cards),
        float(data.get('payment_delay', 0)),
        float(data.get('average_balance', 0))
    ]
    
    return features

def predict_credit_score(data: dict) -> Tuple[int, str, Dict]:
    """
    Predict credit score and return detailed analysis
    """
    model, scaler = load_model()
    
    # Preprocess input
    features = preprocess_features(data)
    features_scaled = scaler.transform([features])
    
    # Get prediction probability
    proba = model.predict_proba(features_scaled)[0]
    good_credit_prob = proba[0]  # Probability of good credit (class 0)
    
    # Convert to score (0-100)
    score = int(good_credit_prob * 100)
    
    # Determine risk level
    if score <= 40:
        risk_level = "riesgo alto"
    elif score <= 70:
        risk_level = "riesgo medio"
    else:
        risk_level = "bajo riesgo"
    
    # Feature importance analysis
    feature_names = [
        'edad', 'ingresos_mensuales', 'gastos_mensuales', 'porcentaje_deuda',
        'prestamos_anteriores', 'pagos_tardios', 'estado_civil', 'deudas_activas',
        'tarjetas_credito', 'retraso_pagos', 'saldo_promedio'
    ]
    
    # Get feature importances
    importances = model.feature_importances_
    feature_impact = dict(zip(feature_names, importances))
    
    # Analyze key factors affecting the score
    factors = analyze_risk_factors(data, features, feature_impact)
    
    return score, risk_level, factors

def analyze_risk_factors(data: dict, features: List[float], importance: Dict) -> Dict:
    """Analyze which factors most impact the credit score"""
    factors = {
        'positive': [],
        'negative': [],
        'neutral': []
    }
    
    # Income vs expenses ratio
    income_expense_ratio = data['monthly_income'] / data['monthly_expense']
    if income_expense_ratio > 1.5:
        factors['positive'].append("Relación ingresos/gastos saludable")
    elif income_expense_ratio < 1.2:
        factors['negative'].append("Gastos muy altos en relación a ingresos")
    
    # Debt percentage
    if data['debt_percentage'] < 30:
        factors['positive'].append("Bajo nivel de endeudamiento")
    elif data['debt_percentage'] > 60:
        factors['negative'].append("Alto nivel de endeudamiento")
    
    # Payment history
    if data['late_payments'] == 0:
        factors['positive'].append("Historial de pagos perfecto")
    elif data['late_payments'] > 2:
        factors['negative'].append("Múltiples retrasos en pagos")
    
    # Age factor
    if 25 <= data['age'] <= 55:
        factors['positive'].append("Edad en rango óptimo para crédito")
    elif data['age'] < 25:
        factors['neutral'].append("Edad joven - historial crediticio limitado")
    
    # Previous loans
    if data['previous_loans'] > 5:
        factors['negative'].append("Demasiados préstamos anteriores")
    elif 1 <= data['previous_loans'] <= 3:
        factors['positive'].append("Experiencia crediticia moderada")
    
    return factors

def get_risk_level(score: int) -> str:
    """Convert score to risk level"""
    if score <= 40:
        return "riesgo alto"
    elif score <= 70:
        return "riesgo medio"
    else:
        return "bajo riesgo"
