import React from 'react';
import { format } from 'date-fns';
import './DeploymentList.css';

const DeploymentList = ({ deployments, title = 'Recent Deployments', limit = 10 }) => {
  const displayDeployments = deployments.slice(0, limit);

  const getStatusIcon = (status) => {
    return status === 'success' ? '✓' : '✗';
  };

  const getTypeLabel = (type) => {
    return type === 'manual' ? 'Manual' : 'Automated';
  };

  const getTypeBadge = (type) => {
    return type === 'manual' ? 'manual' : 'automated';
  };

  return (
    <div className="deployment-list">
      <h3 className="deployment-list-title">{title}</h3>
      
      {displayDeployments.length === 0 ? (
        <div className="no-deployments">
          <p>No deployments found</p>
          <p className="help-text">
            Use the Simulator to generate manual deployments or wait for automated deployments from CI/CD
          </p>
        </div>
      ) : (
        <div className="deployment-items">
          {displayDeployments.map((deployment) => (
            <div
              key={deployment.id}
              className={`deployment-item deployment-${deployment.status}`}
            >
              <div className="deployment-status">
                <span className={`status-icon status-${deployment.status}`}>
                  {getStatusIcon(deployment.status)}
                </span>
              </div>

              <div className="deployment-info">
                <div className="deployment-header">
                  <span className={`deployment-type badge-${getTypeBadge(deployment.deployment_type)}`}>
                    {getTypeLabel(deployment.deployment_type)}
                  </span>
                  {deployment.commit_sha && (
                    <span className="deployment-commit">
                      {deployment.commit_sha.substring(0, 7)}
                    </span>
                  )}
                </div>

                <div className="deployment-meta">
                  <span className="deployment-duration">
                    ⏱ {deployment.duration_seconds} seconds ({Math.floor(deployment.duration_seconds / 3600)}h {Math.floor((deployment.duration_seconds % 3600) / 60)}m)
                  </span>
                  <span className="deployment-time">
                    {format(new Date(deployment.timestamp), 'MMM d, HH:mm')}
                  </span>
                  {deployment.triggered_by && (
                    <span className="deployment-trigger">
                      by {deployment.triggered_by}
                    </span>
                  )}
                </div>

                {deployment.errors_count > 0 && (
                  <div className="deployment-errors">
                    <span className="error-badge">
                      {deployment.errors_count} error{deployment.errors_count > 1 ? 's' : ''}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DeploymentList;