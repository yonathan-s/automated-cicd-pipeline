/**
 * ComparisonChart Component
 * Bar chart comparing manual vs automated deployment durations
 */

import React from 'react';
import { Bar } from 'react-chartjs-2';
import ChartDataLabels from 'chartjs-plugin-datalabels';
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

  const manualMean = manual.mean_duration || 0;
  const manualMin = manual.min_duration || 0;
  const manualMax = manual.max_duration || 0;

  const automatedMean = automated.mean_duration || 0;
  const automatedMin = automated.min_duration || 0;
  const automatedMax = automated.max_duration || 0;

  const manualMeanErrors = manual.mean_errors || 0;
  const automatedMeanErrors = automated.mean_errors || 0;

  const timeImprovement =
    manualMean > 0
      ? ((manualMean - automatedMean) / manualMean) * 100
      : 0;

  const errorReduction =
    manualMeanErrors > 0
      ? ((manualMeanErrors - automatedMeanErrors) / manualMeanErrors) * 100
      : 0;

  const data = {
    labels: ['Average Duration', 'Min Duration', 'Max Duration'],
    datasets: [
      {
        label: 'Manual',
        data: [
          manualMean / 60,
          manualMin / 60,
          manualMax / 60,
        ],
        backgroundColor: colors.manual.background,
        borderColor: colors.manual.border,
        borderWidth: 2,
      },
      {
        label: 'Automated',
        data: [
          automatedMean / 60,
          automatedMin / 60,
          automatedMax / 60,
        ],
        backgroundColor: colors.automated.background,
        borderColor: colors.automated.border,
        borderWidth: 2,
        minBarLength: 6,
      },
    ],
  };

  const options = {
    ...defaultOptions,
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Time (minutes)',
        },
      },
    },
    plugins: {
      ...defaultOptions.plugins,
      legend: {
        display: true,
      },
      tooltip: {
        ...defaultOptions.plugins.tooltip,
        callbacks: {
          label: function (context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            label += formatDuration(context.parsed.y * 60);
            return label;
          },
        },
      },
      datalabels: {
        anchor: 'end',
        align: 'end',
        formatter: function (value) {
          return value.toFixed(1) + ' min';
        },
        font: {
          weight: 'bold',
          size: 10,
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <h3 className="chart-title">📊 Manual vs Automated Comparison</h3>
      <div className="chart-wrapper" style={{ height: '420px' }}>
        <Bar data={data} options={options} plugins={[ChartDataLabels]} />
      </div>

      <div className="chart-insights">
        <div className="insight-item">
          <span className="insight-label">Time Improvement:</span>
          <span className="insight-value">
            {timeImprovement.toFixed(1)}%
          </span>
        </div>
        <div className="insight-item">
          <span className="insight-label">Error Reduction:</span>
          <span className="insight-value">
            {errorReduction.toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default ComparisonChart;