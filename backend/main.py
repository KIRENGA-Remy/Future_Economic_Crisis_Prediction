from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from typing import List
import pickle
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
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
        return {"predictions": predictions}
    except Exception as e:
        return {"error": str(e)}