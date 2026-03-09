/**
 * StatsCard Component
 * Displays a single statistic with icon and trend
 */

import React from 'react';
import './StatsCard.css';

const StatsCard = ({ title, value, subtitle, icon, trend, color = 'blue' }) => {
  return (
    <div className={`stats-card stats-card-${color}`}>
      <div className="stats-card-icon">
        <span className="icon">{icon}</span>
      </div>
      
      <div className="stats-card-content">
        <h3 className="stats-card-title">{title}</h3>
        <div className="stats-card-value">{value}</div>
        
        {subtitle && (
          <div className="stats-card-subtitle">{subtitle}</div>
        )}
        
        {trend && (
          <div className={`stats-card-trend ${trend.type}`}>
            <span className="trend-icon">
              {trend.type === 'up' ? '↑' : trend.type === 'down' ? '↓' : '→'}
            </span>
            <span className="trend-text">{trend.text}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatsCard;