import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

export const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 15,
        font: {
          size: 12,
        },
      },
    },
    tooltip: {
      // Used claude AI for colour hex values
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      titleFont: {
        size: 14,
      },
      bodyFont: {
        size: 13,
      },
    },
  },
};

//Used claude AI for colour hex values
export const colors = {
  manual: {
    background: 'rgba(59, 130, 246, 0.5)',
    border: 'rgb(59, 130, 246)',
  },
  automated: {
    background: 'rgba(16, 185, 129, 0.5)',
    border: 'rgb(16, 185, 129)',
  },
  success: {
    background: 'rgba(16, 185, 129, 0.5)',
    border: 'rgb(16, 185, 129)',
  },
  failed: {
    background: 'rgba(239, 68, 68, 0.5)',
    border: 'rgb(239, 68, 68)',
  },
};


export const formatDuration = (seconds) => {

  if (seconds < 60) {
    return `${seconds}s`;

  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs}s`;

  } else {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  }
};