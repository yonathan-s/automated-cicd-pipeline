import React, { useState, useEffect } from 'react';
import { getFullAnalysis, getDeployments } from '../../services/api';
import ComparisonChart from '../Charts/ComparisonChart';
import TimelineChart from './TimelineChart';
import './StatisticalAnalysis.css';

// Stored so I can re-use them often in the UI
const STAT_EXPLANATIONS = {
  t_statistic: "How large the difference is relative to the variation in the data. The higher this number, the more confident we are a real difference exists.",
  p_value_t: "The probability that this result happened by chance.",
  degrees_of_freedom: "Reflects the number of data points used. Higher means more reliable results.",
  cohens_d: "Measures how big the difference actually is in practical terms.",
  chi_square: "Measures how different the success rates are between the two methods. A low value means the difference is small.",
  p_value_chi: "The probability that this result happened by chance.",
  success_rates: "Automated deployments succeeded more often than manual ones, but smaller sample size has to be considered."
};

const StatisticalAnalysis = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [deployments, setDeployments] = useState([]);

  useEffect(() => {
    loadAnalysis();
  }, []);

  const loadAnalysis = async () => {
    setLoading(true);
    setError(null);
    // ai added this try block (claude)
    // Promise.all to fetch deployments and analysis together, both are needed to render charts
    try {
      const [analysisData, deploymentsData] = await Promise.all([
        getFullAnalysis(),
        getDeployments(null, 50),
      ]);

      setAnalysis(analysisData);
      setDeployments(deploymentsData.deployments || []);

    } catch (err) {
      console.error('Error loading analysis:', err);
      setError('Failed to load statistical analysis');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="statistics-loading">
        <div className="loading-spinner"></div>
        <p>Running statistical analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="statistics-error">
        <h3>❌ Error</h3>
        <p>{error}</p>
        <button onClick={loadAnalysis} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  //Destructure the analysis results for easier access in the UI
  const { descriptive_statistics, inferential_statistics, improvement_metrics } = analysis;

  return (
    <div className="statistical-analysis">
      <div className="analysis-header">
        <h2>📊 Statistical Analysis</h2>
        <button onClick={loadAnalysis} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      <div className="charts-section">
        <ComparisonChart statistics={descriptive_statistics} />
        <TimelineChart deployments={deployments} />
      </div>

      <div className="statistics-section">
        <h3>📋 Descriptive Statistics</h3>
        
        <div className="statistics-grid">
          <div className="stat-card">
            <h4>Manual Deployments</h4>
            {descriptive_statistics?.manual ? (
              <div className="stat-details">
                <div className="stat-row">
                  <span className="stat-label">Count:</span>
                  <span className="stat-value">{descriptive_statistics.manual.count}</span>
                </div>
                {/* converted the following to hours and minutes for readability */}
                <div className="stat-row">
                  <span className="stat-label">Mean Duration:</span>
                  <span className="stat-value">
                    {(descriptive_statistics.manual.mean_duration / 3600).toFixed(2)} hours
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">Std Deviation:</span>
                  <span className="stat-value">
                    {(descriptive_statistics.manual.std_duration / 60).toFixed(2)} minutes
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">Success Rate:</span>
                  <span className="stat-value">
                    {descriptive_statistics.manual.success_rate.toFixed(1)}%
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">Avg Errors:</span>
                  <span className="stat-value">
                    {descriptive_statistics.manual.mean_errors.toFixed(2)}
                  </span>
                </div>
              </div>
            ) : (
              <p className="no-data">No manual deployment data</p>
            )}
          </div>

          <div className="stat-card">
            <h4>Automated Deployments</h4>
            {descriptive_statistics?.automated ? (
              <div className="stat-details">
                <div className="stat-row">
                  <span className="stat-label">Count:</span>
                  <span className="stat-value">{descriptive_statistics.automated.count}</span>
                </div>
                {/* converted the following to hours and minutes for readability */}
                <div className="stat-row">
                  <span className="stat-label">Mean Duration:</span>
                  <span className="stat-value">
                    {(descriptive_statistics.automated.mean_duration / 60).toFixed(2)} minutes
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">Std Deviation:</span>
                  <span className="stat-value">
                    {(descriptive_statistics.automated.std_duration).toFixed(2)} seconds
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">Success Rate:</span>
                  <span className="stat-value">
                    {descriptive_statistics.automated.success_rate.toFixed(1)}%
                  </span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">Avg Errors:</span>
                  <span className="stat-value">
                    {descriptive_statistics.automated.mean_errors.toFixed(2)}
                  </span>
                </div>
              </div>
            ) : (
              <p className="no-data">No automated deployment data</p>
            )}
          </div>
        </div>
      </div>

      {inferential_statistics && (
        <div className="statistics-section">
          <h3>📊 Inferential Statistics</h3>
          
          {inferential_statistics.t_test && (
            <div className="test-result">
              <h4>Independent Samples T-Test (Deployment Duration)</h4>
              <div className="test-details">
                <div className="test-row">
                  <span className="test-label">t-statistic: {STAT_EXPLANATIONS.t_statistic}</span>
                  <span className="test-value">
                    {inferential_statistics.t_test.t_statistic.toFixed(4)}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">p-value: {STAT_EXPLANATIONS.p_value_t}</span>
                  <span className={`test-value ${inferential_statistics.t_test.significant ? 'significant' : ''}`}>
                    {inferential_statistics.t_test.p_value.toExponential(4)}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">Degrees of Freedom: {STAT_EXPLANATIONS.degrees_of_freedom}</span>
                  <span className="test-value">
                    {inferential_statistics.t_test.degrees_of_freedom}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">Cohen's d: {STAT_EXPLANATIONS.cohens_d}</span>
                  <span className="test-value">
                    {inferential_statistics.t_test.cohens_d.toFixed(4)} 
                    <span className="effect-size"> ({inferential_statistics.t_test.effect_size} effect)</span>
                  </span>
                </div>
                <div className="test-interpretation">
                  <strong>Interpretation:</strong> {inferential_statistics.t_test.interpretation}
                </div>
              </div>
            </div>
          )}

          {inferential_statistics.chi_square && (
            <div className="test-result">
              <h4>Chi-Square Test (Success Rates)</h4>
              <div className="test-details">
                <div className="test-row">
                  <span className="test-label">x^2 statistic: {STAT_EXPLANATIONS.chi_square}</span>
                  <span className="test-value">
                    {/* error handling added as a precaution through, (vscode co-pilot done it)*/}
                    {typeof inferential_statistics.chi_square.chi_square === 'number'
                      ? inferential_statistics.chi_square.chi_square.toFixed(4)
                      : inferential_statistics.chi_square.chi_square}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">p-value: {STAT_EXPLANATIONS.p_value_chi}</span>
                  <span className={`test-value ${inferential_statistics.chi_square.significant ? 'significant' : ''}`}>
                    {typeof inferential_statistics.chi_square.p_value === 'number'
                      ? inferential_statistics.chi_square.p_value.toFixed(4)
                      : inferential_statistics.chi_square.p_value}
                  </span>
                </div>

                <div className="test-row">
                  <span className="test-label">Manual Success Rate: {STAT_EXPLANATIONS.success_rates}</span>
                  <span className="test-value">
                    {typeof inferential_statistics.chi_square.manual_success_rate === 'number'
                      ? `${inferential_statistics.chi_square.manual_success_rate.toFixed(1)}%`
                      : inferential_statistics.chi_square.manual_success_rate}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">Automated Success Rate: {STAT_EXPLANATIONS.success_rates}</span>
                  <span className="test-value">
                    {typeof inferential_statistics.chi_square.automated_success_rate === 'number'
                      ? `${inferential_statistics.chi_square.automated_success_rate.toFixed(1)}%`
                      : inferential_statistics.chi_square.automated_success_rate}
                  </span>
                </div>
                <div className="test-interpretation">
                  <strong>Interpretation:</strong> {inferential_statistics.chi_square.interpretation}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {improvement_metrics && (
        <div className="statistics-section">
          <h3>Improvement Metrics</h3>
          <div className="improvement-grid">
            <div className="improvement-card">
              <div className="improvement-icon">⚡</div>
              <div className="improvement-label">Time Reduction</div>
              <div className="improvement-value">
                {improvement_metrics.time_reduction_percent.toFixed(1)}%
              </div>
              <div className="improvement-subtitle">
                {(improvement_metrics.time_reduction_seconds / 3600).toFixed(2)} hours saved
              </div>
            </div>

            <div className="improvement-card">
              <div className="improvement-icon">++</div>
              <div className="improvement-label">Error Reduction</div>
              <div className="improvement-value">
                {improvement_metrics.error_reduction_percent.toFixed(1)}%
              </div>
              <div className="improvement-subtitle">
                Fewer configuration errors
              </div>
            </div>

            <div className="improvement-card">
              <div className="improvement-icon">✅</div>
              <div className="improvement-label">Success Rate Gain</div>
              <div className="improvement-value">
                +{improvement_metrics.success_rate_improvement.toFixed(1)}%
              </div>
              <div className="improvement-subtitle">
                More reliable deployments
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="academic-note">
        <h4>📚 Statistical Significance Note</h4>
        <p>
          <strong>p-value &lt; 0.05:</strong> The difference is statistically significant (less than 5% chance this difference occurred by random chance).
        </p>
        <p>
          <strong>Cohen's d:</strong> Measures effect size. Values &gt; 0.8 indicate a large practical difference between groups.
        </p>
        <p>
          These statistical tests provide empirical evidence that automation significantly improves deployment performance.
        </p>
      </div>
    </div>
  );
};

export default StatisticalAnalysis;