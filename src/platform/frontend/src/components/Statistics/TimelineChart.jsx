import React from 'react';
import { Line } from 'react-chartjs-2';
import { format } from 'date-fns';
import { defaultOptions, colors } from '../Charts/ChartConfig';
import '../Charts/ComparisonChart.css';

const TimelineChart = ({ deployments }) => {
  if (!deployments || deployments.length === 0) {
    return (
      <div className="chart-container">
        <p className="chart-no-data">No deployment data available</p>
      </div>
    );
  }

  const sorted = [...deployments].sort((a, b) => 
    new Date(a.timestamp) - new Date(b.timestamp)
  );


  const manualDeployments = sorted.filter(d => d.deployment_type === 'manual');
  const automatedDeployments = sorted.filter(d => d.deployment_type === 'automated');

  // AI (Claude) assisted with the chart data structure and dataset configuration
  const data = {
    labels: sorted.map(d => format(new Date(d.timestamp), 'MMM d, HH:mm')),
    datasets: [
      {
        label: 'Manual Deployments',
        // added null to keep the point off the chart without breaking the line for the other dataset
        data: sorted.map(d => 
          d.deployment_type === 'manual' ? d.duration_seconds / 60 : null
        ),
        borderColor: colors.manual.border,
        backgroundColor: colors.manual.background,
        tension: 0.1,
        spanGaps: true,
      },
      {
        label: 'Automated Deployments',
        data: sorted.map(d => 
          d.deployment_type === 'automated' ? d.duration_seconds / 60 : null
        ),
        borderColor: colors.automated.border,
        backgroundColor: colors.automated.background,
        tension: 0.1,
        spanGaps: true,
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
          text: 'Duration (minutes)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Timestamp',
        },
        ticks: {
          maxRotation: 45,
          minRotation: 45,
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <h3 className="chart-title">📈 Deployment Duration Timeline</h3>
      <div className="chart-wrapper">
        <Line data={data} options={options} />
      </div>
      
      <div className="chart-insights">
        <div className="insight-item">
          <span className="insight-label">Total Deployments:</span>
          <span className="insight-value" style={{color: '#3b82f6'}}>
            {deployments.length}
          </span>
        </div>
        <div className="insight-item">
          <span className="insight-label">Manual:</span>
          <span className="insight-value" style={{color: colors.manual.border}}>
            {manualDeployments.length}
          </span>
        </div>
        <div className="insight-item">
          <span className="insight-label">Automated:</span>
          <span className="insight-value" style={{color: colors.automated.border}}>
            {automatedDeployments.length}
          </span>
        </div>
      </div>
    </div>
  );
};

export default TimelineChart;