from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from typing import List
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class EconomicData(BaseModel):
    country: str
    prediction_months: int = 1

def load_and_prepare_data():
    df = pd.read_csv('economic_indicators_dataset_2010_2023.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    return df

def train_model(df):
    features = ['Month', 'Year', 'Inflation Rate (%)', 'GDP Growth Rate (%)', 
                'Unemployment Rate (%)', 'Interest Rate (%)']
    targets = ['Inflation Rate (%)', 'GDP Growth Rate (%)', 
               'Unemployment Rate (%)', 'Interest Rate (%)', 'Stock Index Value']
    models = {}
    for country in df['Country'].unique():
        country_df = df[df['Country'] == country]
        X = country_df[features]
        models[country] = {}
        for target in targets:
            y = country_df[target]
            rf = RandomForestRegressor(n_estimators=100, random_state=42)
            rf.fit(X, y)
            models[country][target] = rf
    with open('models.pkl', 'wb') as f:
        pickle.dump(models, f)
    return models

if os.path.exists('models.pkl'):
    with open('models.pkl', 'rb') as f:
        models = pickle.load(f)
else:
    df = load_and_prepare_data()
    models = train_model(df)

def analyze_predictions(predictions):
    analysis = {"recommendations": [], "status": "Good"}
    last_pred = predictions[-1]  # Analyze the last predicted month
    
    # Inflation Rate Analysis
    if last_pred["Inflation Rate (%)"] > 5:
        analysis["recommendations"].append(
            "High Inflation Detected: Consider tightening monetary policy, increasing interest rates, or reducing government spending to control price levels."
        )
        analysis["status"] = "Warning"
    elif last_pred["Inflation Rate (%)"] < 1:
        analysis["recommendations"].append(
            "Low Inflation Detected: Stimulate the economy with lower interest rates or increased government spending to avoid deflation."
        )

    # GDP Growth Rate Analysis
    if last_pred["GDP Growth Rate (%)"] < 2:
        analysis["recommendations"].append(
            "Low GDP Growth: Implement fiscal stimulus, tax cuts, or infrastructure investments to boost economic activity."
        )
        analysis["status"] = "Warning"
    elif last_pred["GDP Growth Rate (%)"] > 5:
        analysis["recommendations"].append(
            "High GDP Growth: Monitor for overheating; consider gradual policy adjustments to ensure sustainable growth."
        )

    # Unemployment Rate Analysis
    if last_pred["Unemployment Rate (%)"] > 6:
        analysis["recommendations"].append(
            "High Unemployment: Create job programs, incentivize hiring through tax breaks, or invest in workforce training."
        )
        analysis["status"] = "Warning"
    elif last_pred["Unemployment Rate (%)"] < 3:
        analysis["recommendations"].append(
            "Low Unemployment: Watch for wage inflation; ensure labor market flexibility to maintain balance."
        )

    # Interest Rate Analysis
    if last_pred["Interest Rate (%)"] > 5:
        analysis["recommendations"].append(
            "High Interest Rates: Assess borrowing costs; consider easing rates if growth slows."
        )
    elif last_pred["Interest Rate (%)"] < 1:
        analysis["recommendations"].append(
            "Low Interest Rates: Encourage investment but monitor for asset bubbles."
        )

    # If no issues, provide positive feedback
    if not analysis["recommendations"]:
        analysis["recommendations"].append(
            "Economy appears stable: Maintain current policies and monitor trends for sustained growth."
        )

    return analysis

@app.post("/predict")
async def predict_economic_data(data: EconomicData):
    try:
        df = load_and_prepare_data()
        country = data.country
        if country not in models:
            return {"error": f"No data available for {country}"}
        country_df = df[df['Country'] == country].sort_values('Date')
        last_date = country_df['Date'].iloc[-1]
        last_data = country_df.iloc[-1]
        predictions = []
        current_date = last_date
        for _ in range(data.prediction_months):
            current_date = current_date + pd.offsets.MonthEnd(1)
            input_data = pd.DataFrame({
                'Month': [current_date.month],
                'Year': [current_date.year],
                'Inflation Rate (%)': [last_data['Inflation Rate (%)']],
                'GDP Growth Rate (%)': [last_data['GDP Growth Rate (%)']],
                'Unemployment Rate (%)': [last_data['Unemployment Rate (%)']],
                'Interest Rate (%)': [last_data['Interest Rate (%)']]
            })
            pred = {'Date': current_date.strftime('%Y-%m-%d'), 'Country': country}
            for target in models[country]:
                prediction = models[country][target].predict(input_data)[0]
                pred[target] = float(prediction)
                if target != 'Stock Index Value':
                    last_data[target] = prediction
            predictions.append(pred)
        
        # Add analysis
        analysis = analyze_predictions(predictions)
        return {"predictions": predictions, "analysis": analysis}
    except Exception as e:
        return {"error": str(e)}