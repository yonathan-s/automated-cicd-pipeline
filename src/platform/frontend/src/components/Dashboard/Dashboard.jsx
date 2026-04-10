import React, { useState, useEffect } from 'react';
import StatsCard from './StatsCard';
import DeploymentList from './DeploymentList';
import { getDeployments, getSummary, getStatistics } from '../../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [summary, setSummary] = useState(null);
  const [deployments, setDeployments] = useState([]);
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);

    try {

      const [summaryData, deploymentsData, statsData] = await Promise.all([
        getSummary(),
        getDeployments(null, 20),
        getStatistics(),
      ]);

      setSummary(summaryData);
      setDeployments(deploymentsData.deployments || []);
      setStatistics(statsData);
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError('Failed to load dashboard data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <h3>Error Loading Dashboard</h3>
        <p>{error}</p>
        <button onClick={loadDashboardData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  
  const getImprovementPercent = () => {
    if (statistics?.comparison?.time_improvement_percent) {
      return statistics.comparison.time_improvement_percent.toFixed(1);
    }
    return '0';
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard Overview</h2>
        <button onClick={loadDashboardData} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      
      <div className="stats-grid">
        <StatsCard
          icon="D"
          title="Total Deployments"
          value={summary?.total_deployments || 0}
          subtitle={`${summary?.manual_deployments || 0} manual, ${summary?.automated_deployments || 0} automated`}
          color="blue"
        />

        <StatsCard
          icon="!"
          title="Success Rate"
          value={`${(summary?.overall_success_rate || 0).toFixed(1)}%`}
          subtitle="Overall deployment success"
          color="green"
          trend={{
            type: 'up',
            text: 'Reliable deployments'
          }}
        />

        <StatsCard
          icon="⚡"
          title="Time Improvement"
          value={`${getImprovementPercent()}%`}
          subtitle="Manual vs Automated"
          color="purple"
          trend={{
            type: 'down',
            text: 'Faster deployments'
          }}
        />

        <StatsCard
          icon="x"
          title="Latest Status"
          value={summary?.latest_deployment?.status === 'success' ? 'Success' : 'Failed'}
          subtitle={summary?.latest_deployment ? 
            `${summary.latest_deployment.duration_formatted} ago` : 
            'No deployments yet'}
          color={summary?.latest_deployment?.status === 'success' ? 'green' : 'orange'}
        />
      </div>


      {statistics?.comparison && (
        <div className="comparison-summary">
          <h3>📈 Quick Comparison</h3>
          <div className="comparison-grid">
            <div className="comparison-item">
              <div className="comparison-label">Time Saved</div>
              <div className="comparison-value">
                {(statistics.comparison.time_improvement_absolute / 3600).toFixed(1)} hours
              </div>
            </div>
            <div className="comparison-item">
              <div className="comparison-label">Error Reduction</div>
              <div className="comparison-value">
                {statistics.comparison.error_reduction_percent.toFixed(1)}%
              </div>
            </div>
            <div className="comparison-item">
              <div className="comparison-label">Success Rate Improvement</div>
              <div className="comparison-value">
                +{statistics.comparison.success_rate_improvement.toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      )}


      <div className="dashboard-section">
        <DeploymentList
          deployments={deployments}
          title="Recent Deployments"
          limit={10}
        />
      </div>
    </div>
  );
};

export default Dashboard;