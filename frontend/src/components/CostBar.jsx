import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { formatCost } from '../utils/formatters';

export default function CostBar({ results }) {
  if (!results || results.length === 0) return null;

  const data = results.map((r) => ({
    name: `${r.model.replace('gemini-', '')} (${r.thinking === null ? 'def' : r.thinking})`,
    cost: r.cost || 0,
    latency: r.secs || 0,
  }));

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Cost vs Latency Trade-off
      </h3>
      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
            <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} />
            <YAxis
              yAxisId="left"
              orientation="left"
              stroke="#6366f1"
              tickFormatter={(v) => `$${v}`}
              tick={{ fontSize: 11 }}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#10b981"
              tickFormatter={(v) => `${v}s`}
              tick={{ fontSize: 11 }}
            />
            <Tooltip
              formatter={(value, name) =>
                name === 'cost' ? [formatCost(value), 'Cost (USD)'] : [`${value}s`, 'Latency (Sec)']
              }
              contentStyle={{
                backgroundColor: '#0f172a',
                borderColor: '#1e293b',
                borderRadius: '0.75rem',
                color: '#fff',
                fontSize: '12px',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px' }} />
            <Bar yAxisId="left" dataKey="cost" name="Cost (USD)" fill="#6366f1" radius={[4, 4, 0, 0]} />
            <Bar yAxisId="right" dataKey="latency" name="Latency (Sec)" fill="#10b981" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
