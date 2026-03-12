/**
 * Simulator Component
 * Interface for running manual deployment simulations
 */

import React, { useState } from 'react';
import {
  simulateManualDeployment,
  simulateBatchDeployments,
  getSimulationSummary,
} from '../../services/api';
import './Simulator.css';

const Simulator = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [summary, setSummary] = useState(null);
  const [batchCount, setBatchCount] = useState(10);
  const [spreadDays, setSpreadDays] = useState(30);

  const runSingleSimulation = async () => {
    setLoading(true);
    setResult(null);

    try {
      const data = await simulateManualDeployment();
      setResult({
        type: 'single',
        data: data.deployment,
        message: 'Manual deployment simulated successfully',
      });
      
      // Refresh summary
      loadSummary();
    } catch (error) {
      setResult({
        type: 'error',
        message: 'Failed to simulate deployment',
      });
    } finally {
      setLoading(false);
    }
  };

  const runBatchSimulation = async () => {
    setLoading(true);
    setResult(null);

    try {
      const data = await simulateBatchDeployments(batchCount, spreadDays);
      setResult({
        type: 'batch',
        data: data,
        message: `Simulated ${data.count} manual deployments`,
      });
      
      // Refresh summary
      loadSummary();
    } catch (error) {
      setResult({
        type: 'error',
        message: 'Failed to simulate batch deployments',
      });
    } finally {
      setLoading(false);
    }
  };

  const loadSummary = async () => {
    try {
      const data = await getSimulationSummary();
      setSummary(data);
    } catch (error) {
      console.error('Failed to load summary:', error);
    }
  };

  // Load summary on mount
  React.useEffect(() => {
    loadSummary();
  }, []);

  return (
    <div className="simulator">
      <div className="simulator-header">
        <h2>🔄 Manual Deployment Simulator</h2>
        <p className="simulator-subtitle">
          Generate realistic manual deployment data based on Week 4 baseline
        </p>
      </div>

      {/* Summary Stats */}
      {summary && summary.count > 0 && (
        <div className="simulation-summary">
          <h3>Simulation Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <div className="summary-label">Simulations Run</div>
              <div className="summary-value">{summary.count}</div>
            </div>
            <div className="summary-item">
              <div className="summary-label">Average Duration</div>
              <div className="summary-value">
                {summary.average_duration_hours?.toFixed(2)} hours
              </div>
            </div>
            <div className="summary-item">
              <div className="summary-label">Success Rate</div>
              <div className="summary-value">
                {summary.success_rate?.toFixed(1)}%
              </div>
            </div>
            <div className="summary-item">
              <div className="summary-label">Total Errors</div>
              <div className="summary-value">{summary.total_errors}</div>
            </div>
          </div>
        </div>
      )}

      {/* Simulator Controls */}
      <div className="simulator-controls">
        {/* Single Simulation */}
        <div className="control-card">
          <h3>Single Simulation</h3>
          <p>Run one manual deployment simulation</p>
          
          <button
            onClick={runSingleSimulation}
            disabled={loading}
            className="sim-button primary"
          >
            {loading ? 'Simulating...' : '▶️ Run Single Simulation'}
          </button>

          <div className="control-info">
            <strong>What this does:</strong>
            <ul>
              <li>Simulates one complete manual deployment</li>
              <li>Duration: ~12 hours (with realistic variance)</li>
              <li>Injects errors based on Week 4 error rates</li>
              <li>Stores result in database for analysis</li>
            </ul>
          </div>
        </div>

        {/* Batch Simulation */}
        <div className="control-card">
          <h3>Batch Simulation</h3>
          <p>Run multiple simulations spread over time</p>

          <div className="batch-inputs">
            <div className="input-group">
              <label htmlFor="batch-count">Number of Simulations:</label>
              <input
                id="batch-count"
                type="number"
                min="1"
                max="50"
                value={batchCount}
                onChange={(e) => setBatchCount(parseInt(e.target.value))}
              />
            </div>

            <div className="input-group">
              <label htmlFor="spread-days">Spread Over (days):</label>
              <input
                id="spread-days"
                type="number"
                min="1"
                max="90"
                value={spreadDays}
                onChange={(e) => setSpreadDays(parseInt(e.target.value))}
              />
            </div>
          </div>

          <button
            onClick={runBatchSimulation}
            disabled={loading}
            className="sim-button primary"
          >
            {loading ? 'Simulating...' : `▶️ Run ${batchCount} Simulations`}
          </button>

          <div className="control-info">
            <strong>What this does:</strong>
            <ul>
              <li>Simulates {batchCount} manual deployments</li>
              <li>Spreads them across {spreadDays} days</li>
              <li>Each has realistic variance and errors</li>
              <li>Creates complete dataset for statistical analysis</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className={`simulation-result ${result.type}`}>
          <h3>
            {result.type === 'error' ? '❌' : '✅'} 
            {' '}{result.message}
          </h3>

          {result.type === 'single' && result.data && (
            <div className="result-details">
              <div className="result-item">
                <span className="result-label">Duration:</span>
                <span className="result-value">{result.data.duration_formatted}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Status:</span>
                <span className="result-value">{result.data.status}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Errors:</span>
                <span className="result-value">{result.data.errors_count}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Timestamp:</span>
                <span className="result-value">
                  {new Date(result.data.timestamp).toLocaleString()}
                </span>
              </div>
            </div>
          )}

          {result.type === 'batch' && result.data && (
            <div className="result-details">
              <p>Created {result.data.count} simulated manual deployments</p>
              <p>View them in the Dashboard or Statistical Analysis views</p>
            </div>
          )}
        </div>
      )}

      {/* Explanation */}
      <div className="simulator-explanation">
        <h3>📚 How the Simulator Works</h3>
        
        <div className="explanation-section">
          <h4>Based on Real Data</h4>
          <p>
            The simulator uses a manual deployment I done as a baseline:
          </p>
          <ul>
            <li><strong>Average duration:</strong> 12 hours</li>
            <li><strong>Error rate:</strong> 15 errors across 20 steps</li>
            <li><strong>Success rate:</strong> 75% (3 out of 4 attempts)</li>
          </ul>
        </div>

        <div className="explanation-section">
          <h4>Realistic Variance</h4>
          <p>
            Each simulation adds realistic human variance:
          </p>
          <ul>
            <li>Duration varies by ±30 minutes (normal distribution)</li>
            <li>Errors occur probabilistically at each step</li>
            <li>Time lost per error: 5-30 minutes</li>
            <li>Occasional complete failures (matching 75% success rate)</li>
          </ul>
        </div>

      </div>
    </div>
  );
};

export default Simulator;