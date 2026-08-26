import React from 'react';
import { FAILURE_COLORS } from '../utils/constants';

export default function CriticalFailureBadge({ failures }) {
  if (!failures || failures.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-1.5">
      {failures.map((fail) => (
        <span
          key={fail}
          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider ${
            FAILURE_COLORS[fail] || 'bg-red-100 text-red-800'
          }`}
        >
          ⚠️ {fail.replace('_', ' ')}
        </span>
      ))}
    </div>
  );
}
