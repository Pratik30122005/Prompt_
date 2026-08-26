import React from 'react';
import {
  formatCost,
  formatSeconds,
  formatScore,
  formatTokens,
  scoreColorClass,
  scoreBgClass,
} from '../utils/formatters';
import { CRITERIA, CRITERIA_SHORT } from '../utils/constants';
import CriticalFailureBadge from './CriticalFailureBadge';

export default function ResultTable({ results }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
      <div className="p-6 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center">
        <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
          Evaluation Summary Table
        </h3>
        <span className="text-xs text-slate-400 font-mono">{results.length} configurations evaluated</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="py-3 px-4">Model</th>
              <th className="py-3 px-4">Thinking</th>
              <th className="py-3 px-4">Sec</th>
              <th className="py-3 px-4">Cost$</th>
              <th className="py-3 px-4">Tokens</th>
              <th className="py-3 px-4">Score</th>
              <th className="py-3 px-4">Variance</th>
              {CRITERIA.map((c) => (
                <th key={c} className="py-3 px-3 text-center" title={c}>
                  {CRITERIA_SHORT[c]}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm font-mono">
            {results.map((r, idx) => {
              const overallScore = r.avg_score
                ? Object.values(r.avg_score).reduce((a, b) => a + b, 0) /
                  Object.values(r.avg_score).length
                : null;

              const allFailures = [
                ...new Set(r.runs?.flatMap((run) => run.critical_failures || []) || []),
              ];

              return (
                <tr
                  key={idx}
                  className="hover:bg-slate-50/80 dark:hover:bg-slate-800/30 transition-colors"
                >
                  <td className="py-3.5 px-4 font-semibold text-slate-900 dark:text-slate-100">
                    <div>{r.model}</div>
                    {allFailures.length > 0 && (
                      <div className="mt-1">
                        <CriticalFailureBadge failures={allFailures} />
                      </div>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 dark:text-slate-400">
                    {r.thinking === null ? '-' : r.thinking}
                  </td>
                  <td className="py-3.5 px-4 text-slate-700 dark:text-slate-300">
                    {formatSeconds(r.secs)}
                  </td>
                  <td className="py-3.5 px-4 text-indigo-600 dark:text-indigo-400 font-semibold">
                    {formatCost(r.cost)}
                  </td>
                  <td className="py-3.5 px-4 text-slate-600 dark:text-slate-400">
                    {formatTokens(r.tokens)}
                  </td>
                  <td className="py-3.5 px-4">
                    {overallScore ? (
                      <span
                        className={`inline-block px-2.5 py-1 rounded-lg text-xs font-bold ${scoreBgClass(
                          overallScore
                        )} ${scoreColorClass(overallScore)}`}
                      >
                        {formatScore(overallScore)}
                      </span>
                    ) : (
                      '-'
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-slate-500">
                    {r.variance !== undefined ? r.variance.toFixed(2) : '-'}
                  </td>
                  {CRITERIA.map((c) => {
                    const score = r.avg_score?.[c];
                    return (
                      <td key={c} className="py-3.5 px-3 text-center text-xs font-bold">
                        {score ? (
                          <span className={scoreColorClass(score)}>{score.toFixed(1)}</span>
                        ) : (
                          '-'
                        )}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
