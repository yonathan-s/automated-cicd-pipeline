/**
 * ComparisonChart Component
 * Bar chart comparing manual vs automated deployments
 */

import React from 'react';
import { Bar } from 'react-chartjs-2';
import { defaultOptions, colors, formatDuration } from '../Charts/ChartConfig';
import './ComparisonChart.css';

const ComparisonChart = ({ statistics }) => {
  if (!statistics?.manual || !statistics?.automated) {
    return (
      <div className="chart-container">
        <p className="chart-no-data">
          Not enough data for comparison. Need both manual and automated deployments.
        </p>
      </div>
    );
  }

  const manual = statistics.manual;
  const automated = statistics.automated;

  const data = {
    labels: ['Average Duration', 'Min Duration', 'Max Duration', 'Average Errors'],
    datasets: [
      {
        label: 'Manual',
        data: [
          manual.avg_duration / 60, // Convert to minutes
          manual.min_duration / 60,
          manual.max_duration / 60,
          manual.avg_errors,
        ],
        backgroundColor: colors.manual.background,
        borderColor: colors.manual.border,
        borderWidth: 2,
      },
      {
        label: 'Automated',
        data: [
          automated.avg_duration / 60,
          automated.min_duration / 60,
          automated.max_duration / 60,
          automated.avg_errors,
        ],
        backgroundColor: colors.automated.background,
        borderColor: colors.automated.border,
        borderWidth: 2,
      },
    ],
  };

  const options = {
    ...defaultOptions,
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Time (minutes) / Count',
        },
      },
    },
    plugins: {
      ...defaultOptions.plugins,
      tooltip: {
        ...defaultOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.dataIndex === 3) {
              // Errors count
              label += context.parsed.y.toFixed(1) + ' errors';
            } else {
              // Duration
              label += formatDuration(context.parsed.y * 60);
            }
            return label;
          },
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <h3 className="chart-title">📊 Manual vs Automated Comparison</h3>
      <div className="chart-wrapper">
        <Bar data={data} options={options} />
      </div>
      
      <div className="chart-insights">
        <div className="insight-item">
          <span className="insight-label">Time Improvement:</span>
          <span className="insight-value">
            {((manual.avg_duration - automated.avg_duration) / manual.avg_duration * 100).toFixed(1)}%
          </span>
        </div>
        <div className="insight-item">
          <span className="insight-label">Error Reduction:</span>
          <span className="insight-value">
            {manual.avg_errors > 0 ? 
              ((manual.avg_errors - automated.avg_errors) / manual.avg_errors * 100).toFixed(1) : 
              '0'}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default ComparisonChart;