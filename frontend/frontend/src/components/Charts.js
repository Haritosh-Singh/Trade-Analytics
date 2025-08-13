import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import './Charts.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// Profit Chart Component
export const ProfitChart = ({ data }) => {
  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Profit',
        data: [65, 59, 80, 81, 56, 55, 40, 60, 70, 85, 90, 95],
        fill: true,
        borderColor: '#0d7ff2',
        backgroundColor: 'rgba(13, 127, 242, 0.1)',
        tension: 0.4,
        pointBackgroundColor: '#0d7ff2',
        pointBorderColor: '#0d7ff2',
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#0d7ff2',
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        display: false,
        grid: {
          display: false,
        },
      },
      y: {
        display: false,
        grid: {
          display: false,
        },
      },
    },
    elements: {
      line: {
        borderWidth: 3,
      },
    },
  };

  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
};

// Cost Breakdown Chart Component
export const CostChart = ({ data }) => {
  const chartData = {
    labels: ['Product X', 'Product Y', 'Product Z'],
    datasets: [
      {
        label: 'Cost',
        data: [30, 70, 25],
        backgroundColor: ['#0d7ff2', '#0d7ff2', '#0d7ff2'],
        borderRadius: 4,
        borderWidth: 0,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#0d7ff2',
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: false,
        },
        ticks: {
          color: '#60758a',
          font: {
            size: 12,
          },
        },
      },
      y: {
        display: false,
        grid: {
          display: false,
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <Bar data={chartData} options={options} />
    </div>
  );
};

// Performance Chart Component
export const PerformanceChart = ({ dealers }) => {
  if (!dealers || dealers.length === 0) {
    return <div className="no-data">No performance data available</div>;
  }

  const chartData = {
    labels: dealers.slice(0, 5).map(dealer => dealer.name),
    datasets: [
      {
        label: 'Performance',
        data: dealers.slice(0, 5).map(dealer => dealer.performance_rating),
        backgroundColor: '#0d7ff2',
        borderRadius: 4,
        borderWidth: 0,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#0d7ff2',
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        display: false,
        grid: {
          display: false,
        },
      },
      y: {
        display: true,
        grid: {
          display: false,
        },
        ticks: {
          color: '#60758a',
          font: {
            size: 12,
          },
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <Bar data={chartData} options={options} />
    </div>
  );
};
