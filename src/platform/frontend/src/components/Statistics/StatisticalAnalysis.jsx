/**
 * StatisticalAnalysis Component
 * Displays statistical test results and analysis
 */

import React, { useState, useEffect } from 'react';
import { getFullAnalysis, getDeployments } from '../../services/api';
import ComparisonChart from '../Charts/ComparisonChart';
import TimelineChart from './TimelineChart';
import './StatisticalAnalysis.css';

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
        <h3>⚠️ Error</h3>
        <p>{error}</p>
        <button onClick={loadAnalysis} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  const { descriptive_statistics, inferential_statistics, improvement_metrics } = analysis;

  return (
    <div className="statistical-analysis">
      <div className="analysis-header">
        <h2>📊 Statistical Analysis</h2>
        <button onClick={loadAnalysis} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      {/* Charts */}
      <div className="charts-section">
        <ComparisonChart statistics={descriptive_statistics} />
        <TimelineChart deployments={deployments} />
      </div>

      {/* Descriptive Statistics */}
      <div className="statistics-section">
        <h3>📋 Descriptive Statistics</h3>
        
        <div className="statistics-grid">
          {/* Manual Statistics */}
          <div className="stat-card">
            <h4>Manual Deployments</h4>
            {descriptive_statistics?.manual ? (
              <div className="stat-details">
                <div className="stat-row">
                  <span className="stat-label">Count:</span>
                  <span className="stat-value">{descriptive_statistics.manual.count}</span>
                </div>
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

          {/* Automated Statistics */}
          <div className="stat-card">
            <h4>Automated Deployments</h4>
            {descriptive_statistics?.automated ? (
              <div className="stat-details">
                <div className="stat-row">
                  <span className="stat-label">Count:</span>
                  <span className="stat-value">{descriptive_statistics.automated.count}</span>
                </div>
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

      {/* Inferential Statistics */}
      {inferential_statistics && (
        <div className="statistics-section">
          <h3>📈 Inferential Statistics</h3>
          
          {/* T-Test Results */}
          {inferential_statistics.t_test && (
            <div className="test-result">
              <h4>Independent Samples T-Test (Deployment Duration)</h4>
              <div className="test-details">
                <div className="test-row">
                  <span className="test-label">t-statistic:</span>
                  <span className="test-value">
                    {inferential_statistics.t_test.t_statistic.toFixed(4)}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">p-value:</span>
                  <span className={`test-value ${inferential_statistics.t_test.significant ? 'significant' : ''}`}>
                    {inferential_statistics.t_test.p_value.toExponential(4)}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">Degrees of Freedom:</span>
                  <span className="test-value">
                    {inferential_statistics.t_test.degrees_of_freedom}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">Cohen's d:</span>
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

          {/* Chi-Square Results */}
          {inferential_statistics.chi_square && (
            <div className="test-result">
              <h4>Chi-Square Test (Success Rates)</h4>
              <div className="test-details">
                <div className="test-row">
                  <span className="test-label">χ² statistic:</span>
                  <span className="test-value">
                    {inferential_statistics.chi_square.chi_square.toFixed(4)}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">p-value:</span>
                  <span className={`test-value ${inferential_statistics.chi_square.significant ? 'significant' : ''}`}>
                    {inferential_statistics.chi_square.p_value.toFixed(4)}
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">Manual Success Rate:</span>
                  <span className="test-value">
                    {inferential_statistics.chi_square.manual_success_rate.toFixed(1)}%
                  </span>
                </div>
                <div className="test-row">
                  <span className="test-label">Automated Success Rate:</span>
                  <span className="test-value">
                    {inferential_statistics.chi_square.automated_success_rate.toFixed(1)}%
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

      {/* Improvement Metrics */}
      {improvement_metrics && (
        <div className="statistics-section">
          <h3>🎯 Improvement Metrics</h3>
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
              <div className="improvement-icon">🐛</div>
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

      {/* Academic Note */}
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