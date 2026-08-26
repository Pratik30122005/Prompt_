import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import { CRITERIA, CRITERIA_LABELS, MODEL_COLORS } from '../utils/constants';

export default function ScoreRadar({ results }) {
  if (!results || results.length === 0) return null;

  // Format data for Radar Chart
  const chartData = CRITERIA.map((criterion) => {
    const entry = { criterion: CRITERIA_LABELS[criterion] || criterion };
    results.forEach((r) => {
      const key = `${r.model} (${r.thinking === null ? 'Default' : r.thinking})`;
      entry[key] = r.avg_score?.[criterion] || 0;
    });
    return entry;
  });

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-4">
        7-Criteria Quality Comparison (Radar)
      </h3>
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
            <PolarGrid stroke="#334155" opacity={0.3} />
            <PolarAngleAxis
              dataKey="criterion"
              tick={{ fill: '#94a3b8', fontSize: 11 }}
            />
            <PolarRadiusAxis angle={30} domain={[0, 5]} tick={{ fill: '#64748b' }} />
            {results.map((r, idx) => {
              const key = `${r.model} (${r.thinking === null ? 'Default' : r.thinking})`;
              return (
                <Radar
                  key={key}
                  name={key}
                  dataKey={key}
                  stroke={MODEL_COLORS[idx % MODEL_COLORS.length]}
                  fill={MODEL_COLORS[idx % MODEL_COLORS.length]}
                  fillOpacity={0.2}
                />
              );
            })}
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                borderColor: '#1e293b',
                borderRadius: '0.75rem',
                color: '#fff',
                fontSize: '12px',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
