import './App.css';
import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [country, setCountry] = useState('');
  const [months, setMonths] = useState(1);
  const [predictions, setPredictions] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!country || months < 1) {
      setError('Please enter a valid country and number of months');
      return;
    }
    
    setLoading(true);
    setError(null);
    setPredictions(null);
    setAnalysis(null);
    
    try {
      console.log('Sending request to backend:', { country, prediction_months: parseInt(months) });
      const response = await axios.post('https://economic-crisis-prediction.onrender.com/predict', {
        // const response = await axios.post('http://127.0.0.1:8000/predict', {
        country,
        prediction_months: parseInt(months)
      });
      console.log('Response received:', response.data);
      setPredictions(response.data.predictions);
      setAnalysis(response.data.analysis);
    } catch (err) {
      console.error('Error details:', err);
      setError(err.response?.data?.error || 'An error occurred while fetching predictions');
    } finally {
      setLoading(false);
    }
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Economic Indicators Forecast' }
    }
  };

  const getChartData = (key, label, color) => ({
    labels: predictions ? predictions.map(p => p.Date) : [],
    datasets: [{
      label,
      data: predictions ? predictions.map(p => p[key]) : [],
      borderColor: color,
      backgroundColor: `${color}33`,
      tension: 0.1
    }]
  });

  return (
    <div className="container">
      <header>
        <h1>Economic Forecast Dashboard</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
  <label htmlFor="country">Country:</label>
  <select
    id="country"
    value={country}
    onChange={(e) => setCountry(e.target.value)}
  >
    <option value="" disabled>Select a country</option>
    <option value="Brazil">Brazil</option>
    <option value="France">France</option>
    <option value="USA">USA</option>
    <option value="Canada">Canada</option>
    <option value="Japan">Japan</option>
    <option value="Germany">Germany</option>
    <option value="China">China</option>
    <option value="UK">UK</option>
    <option value="India">India</option>
    <option value="Australia">Australia</option>
  </select>
</div>
          <div className="form-group">
            <label htmlFor="months">Months to Predict:</label>
            <input
              id="months"
              type="number"
              value={months}
              onChange={(e) => setMonths(e.target.value)}
              min="1"
              placeholder="Number of months"
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Predicting...' : 'Get Forecast'}
          </button>
        </form>
        {error && <div className="error">{error}</div>}
        {predictions && (
          <section className="charts">
            <div className="chart-container">
              <Line 
                options={{ ...chartOptions, title: { ...chartOptions.title, text: 'Inflation Rate' }}}
                data={getChartData('Inflation Rate (%)', 'Inflation (%)', '#FF6384')}
              />
            </div>
            <div className="chart-container">
              <Line 
                options={{ ...chartOptions, title: { ...chartOptions.title, text: 'GDP Growth Rate' }}}
                data={getChartData('GDP Growth Rate (%)', 'GDP Growth (%)', '#36A2EB')}
              />
            </div>
            <div className="chart-container">
              <Line 
                options={{ ...chartOptions, title: { ...chartOptions.title, text: 'Unemployment Rate' }}}
                data={getChartData('Unemployment Rate (%)', 'Unemployment (%)', '#FFCE56')}
              />
            </div>
            <div className="chart-container">
              <Line 
                options={{ ...chartOptions, title: { ...chartOptions.title, text: 'Interest Rate' }}}
                data={getChartData('Interest Rate (%)', 'Interest (%)', '#4BC0C0')}
              />
            </div>
            <div className="chart-container">
              <Line 
                options={{ ...chartOptions, title: { ...chartOptions.title, text: 'Stock Index Value' }}}
                data={getChartData('Stock Index Value', 'Stock Index', '#9966FF')}
              />
            </div>
          </section>
        )}
      </main>
      {analysis && (
        <section className="analysis-section">
          <h2>Economic Situation Analysis</h2>
          <div className={`analysis-card ${analysis.status.toLowerCase()}`}>
            <h3>Status: {analysis.status}</h3>
            <ul>
              {analysis.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </section>
      )}
      <footer>
        <p>Created by @GITOLI Remy Claudien</p>
      </footer>
    </div>
  );
}

export default App;