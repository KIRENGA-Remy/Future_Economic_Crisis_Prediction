Economic Forecast Dashboard
The Economic Forecast Dashboard is a full-stack application that predicts economic indicators such as inflation rate, GDP growth rate, unemployment rate, interest rate, and stock index value for a given country over a specified number of months. The backend uses FastAPI and machine learning models trained on historical economic data, while the frontend is built using React and visualizes predictions using interactive charts.

Table of Contents
Features
Technologies Used
Folder Structure
Setup Instructions
Backend
Frontend
How to Run the Application
API Documentation
Contributing
License
Features
Predictive Analytics : Predict economic indicators for any country in the dataset.
Interactive Charts : Visualize predictions using line charts powered by Chart.js.
Dynamic Input : Users can specify the country and the number of months to predict.
Error Handling : Graceful error handling for invalid inputs or missing data.
CORS Support : Secure communication between frontend and backend.
Technologies Used
Backend
FastAPI : High-performance web framework for building APIs.
Scikit-learn : Machine learning library for training Random Forest models.
Pandas/Numpy : Data manipulation and preprocessing.
Pickle : Serialization of machine learning models.
CORS Middleware : Enables cross-origin requests from the frontend.
Frontend
React : JavaScript library for building user interfaces.
Chart.js : Library for creating interactive charts.
Axios : HTTP client for making API requests.
CSS : Styling for the dashboard.
Folder Structure
Backend

backend/
│   ├── main.py               # Main FastAPI application
│   ├── model.pkl             # Pre-trained machine learning model (if applicable)
│   └── requirements.txt      # List of dependencies to install
Frontend

frontend/
│   ├── public/               # Public assets (e.g., favicon, index.html)
│   ├── src/                  # React source code
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styles for the dashboard
│   │   ├── index.js          # Entry point for the React app
│   │   └── ...               # Other React components and assets
│   ├── package.json          # Dependencies and scripts
│   ├── README.md             # Frontend-specific documentation
│   └── ...                   # Other configuration files
Setup Instructions
Backend Setup
Install Dependencies
Navigate to the backend/ folder and install the required packages:

pip install -r requirements.txt
Prepare the Dataset
Ensure the dataset economic_indicators_dataset_2010_2023.csv is placed in the backend/ folder. This dataset should contain columns like Date, Country, Inflation Rate (%), GDP Growth Rate (%), etc.
Train the Model (Optional)
If no pre-trained model (model.pkl) exists, the backend will automatically train a new model when the server starts. Alternatively, you can manually train the model by running the following command in Python:

python main.py
Run the Backend Server
Start the FastAPI server using Uvicorn:

uvicorn main:app --reload
The backend will be available at http://127.0.0.1:8000.
Frontend Setup
Navigate to the Frontend Folder
Move to the frontend/ folder:

cd frontend
Install Dependencies
Install the required Node.js packages:

npm install
Run the Development Server
Start the React development server:

npm start
The frontend will be available at http://localhost:3000.
How to Run the Application
Start the Backend
Ensure the backend server is running at http://127.0.0.1:8000.
Start the Frontend
Open another terminal, navigate to the frontend/ folder, and run:

npm start
Access the Dashboard
Open your browser and go to http://localhost:3000. You should see the Economic Forecast Dashboard.
Make Predictions
Enter the name of a country and the number of months to predict, then click "Get Forecast" to view the results.
API Documentation
The backend exposes a single endpoint for making predictions:

POST /predict
Request Body :

⌄
{
  "country": "USA",
  "prediction_months": 3
}
Response :

{
  "predictions": [
    {
      "Date": "2023-10-31",
      "Country": "USA",
      "Inflation Rate (%)": 3.5,
      "GDP Growth Rate (%)": 2.1,
      "Unemployment Rate (%)": 3.9,
      "Interest Rate (%)": 5.5,
      "Stock Index Value": 3400.0
    },
    ...
  ]
}
You can access the interactive API documentation at:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.