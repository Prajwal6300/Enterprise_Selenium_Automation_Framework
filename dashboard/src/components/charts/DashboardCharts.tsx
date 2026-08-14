'use client';

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar, Doughnut, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface PassRateDoughnutProps {
  passed: number;
  failed: number;
  skipped: number;
}

export const PassRateDoughnut: React.FC<PassRateDoughnutProps> = ({
  passed,
  failed,
  skipped,
}) => {
  const total = passed + failed + skipped;
  const passRate = total > 0 ? ((passed / total) * 100).toFixed(1) : '100';

  const data = {
    labels: ['Passed', 'Failed', 'Skipped'],
    datasets: [
      {
        data: [passed, failed, skipped],
        backgroundColor: ['#10b981', '#ef4444', '#f59e0b'],
        borderWidth: 2,
        borderColor: '#ffffff',
        hoverOffset: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '75%',
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          boxWidth: 12,
          padding: 12,
          font: { size: 12, family: 'Inter' },
        },
      },
      tooltip: {
        callbacks: {
          label: (context: any) => ` ${context.label}: ${context.raw} tests`,
        },
      },
    },
  };

  return (
    <div style={{ position: 'relative', height: '220px', width: '100%' }}>
      <Doughnut data={data} options={options} />
      <div
        style={{
          position: 'absolute',
          top: '42%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          pointerEvents: 'none',
        }}
      >
        <div style={{ fontSize: '24px', fontWeight: '800', color: '#0f172a' }}>{passRate}%</div>
        <div style={{ fontSize: '11px', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>Pass Rate</div>
      </div>
    </div>
  );
};

interface PassRateTrendLineProps {
  labels: string[];
  rates: number[];
}

export const PassRateTrendLine: React.FC<PassRateTrendLineProps> = ({ labels, rates }) => {
  const data = {
    labels,
    datasets: [
      {
        label: 'Pass Rate (%)',
        data: rates,
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.08)',
        fill: true,
        tension: 0.35,
        pointBackgroundColor: '#2563eb',
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        min: 0,
        max: 100,
        ticks: { callback: (val: any) => `${val}%`, font: { size: 11, family: 'Inter' } },
        grid: { color: '#f1f5f9' },
      },
      x: {
        ticks: { font: { size: 11, family: 'Inter' } },
        grid: { display: false },
      },
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context: any) => ` Pass Rate: ${context.raw}%`,
        },
      },
    },
  };

  return (
    <div style={{ height: '240px', width: '100%' }}>
      <Line data={data} options={options} />
    </div>
  );
};

interface DurationTrendBarProps {
  labels: string[];
  durations: number[];
}

export const DurationTrendBar: React.FC<DurationTrendBarProps> = ({ labels, durations }) => {
  const data = {
    labels,
    datasets: [
      {
        label: 'Execution Duration (s)',
        data: durations,
        backgroundColor: '#3b82f6',
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: { callback: (val: any) => `${val}s`, font: { size: 11, family: 'Inter' } },
        grid: { color: '#f1f5f9' },
      },
      x: {
        ticks: { font: { size: 11, family: 'Inter' } },
        grid: { display: false },
      },
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context: any) => ` Total Duration: ${context.raw}s`,
        },
      },
    },
  };

  return (
    <div style={{ height: '240px', width: '100%' }}>
      <Bar data={data} options={options} />
    </div>
  );
};

interface FailureTrendLineProps {
  labels: string[];
  failures: number[];
}

export const FailureTrendLine: React.FC<FailureTrendLineProps> = ({ labels, failures }) => {
  const data = {
    labels,
    datasets: [
      {
        label: 'Failures',
        data: failures,
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        fill: true,
        tension: 0.35,
        pointBackgroundColor: '#ef4444',
        pointRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 1, font: { size: 11, family: 'Inter' } },
        grid: { color: '#f1f5f9' },
      },
      x: {
        ticks: { font: { size: 11, family: 'Inter' } },
        grid: { display: false },
      },
    },
    plugins: {
      legend: { display: false },
    },
  };

  return (
    <div style={{ height: '240px', width: '100%' }}>
      <Line data={data} options={options} />
    </div>
  );
};

interface ModuleDistributionBarProps {
  modules: { module: string; count: number }[];
}

export const ModuleDistributionBar: React.FC<ModuleDistributionBarProps> = ({ modules }) => {
  const data = {
    labels: modules.map((m) => m.module),
    datasets: [
      {
        label: 'Tests Count',
        data: modules.map((m) => m.count),
        backgroundColor: [
          '#2563eb',
          '#06b6d4',
          '#10b981',
          '#f59e0b',
          '#8b5cf6',
          '#ec4899',
          '#64748b',
        ],
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 1, font: { size: 11, family: 'Inter' } },
        grid: { color: '#f1f5f9' },
      },
      x: {
        ticks: { font: { size: 11, family: 'Inter' } },
        grid: { display: false },
      },
    },
    plugins: {
      legend: { display: false },
    },
  };

  return (
    <div style={{ height: '240px', width: '100%' }}>
      <Bar data={data} options={options} />
    </div>
  );
};

interface BrowserDistributionPieProps {
  browsers: { browser: string; count: number }[];
}

export const BrowserDistributionPie: React.FC<BrowserDistributionPieProps> = ({ browsers }) => {
  const data = {
    labels: browsers.map((b) => b.browser),
    datasets: [
      {
        data: browsers.map((b) => b.count),
        backgroundColor: ['#2563eb', '#f97316', '#0284c7', '#6366f1'],
        borderWidth: 2,
        borderColor: '#ffffff',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: { boxWidth: 12, padding: 12, font: { size: 12, family: 'Inter' } },
      },
    },
  };

  return (
    <div style={{ height: '220px', width: '100%' }}>
      <Pie data={data} options={options} />
    </div>
  );
};
