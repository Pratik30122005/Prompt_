import React, { useState } from 'react';
import CriticalFailureBadge from './CriticalFailureBadge';
import { scoreColorClass } from '../utils/formatters';

export default function ResponseViewer({ results }) {
  const [activeTab, setActiveTab] = useState(0);
  const [activeRunIndex, setActiveRunIndex] = useState(0);

  if (!results || results.length === 0) return null;

  const currentResult = results[activeTab] || results[0];
  const currentRun = currentResult?.runs?.[activeRunIndex] || currentResult?.runs?.[0];

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden space-y-4 p-6">
      <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
        Generated Responses & LLM Verdicts
      </h3>

      {/* Tabs for Configurations */}
      <div className="flex gap-2 border-b border-slate-200 dark:border-slate-800 overflow-x-auto pb-2">
        {results.map((r, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => {
              setActiveTab(idx);
              setActiveRunIndex(0);
            }}
            className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition ${
              activeTab === idx
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            {r.model} (thinking: {r.thinking === null ? 'Default' : r.thinking})
          </button>
        ))}
      </div>

      {/* Multiple Runs Selector */}
      {currentResult?.runs?.length > 1 && (
        <div className="flex items-center gap-2 text-xs">
          <span className="text-slate-400 font-medium">Select Run Iteration:</span>
          {currentResult.runs.map((_, rIdx) => (
            <button
              key={rIdx}
              type="button"
              onClick={() => setActiveRunIndex(rIdx)}
              className={`px-3 py-1 rounded-lg font-mono font-bold transition ${
                activeRunIndex === rIdx
                  ? 'bg-purple-600 text-white'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-500'
              }`}
            >
              Run #{rIdx + 1}
            </button>
          ))}
        </div>
      )}

      {/* Response Box & Judge Verdict */}
      {currentRun && (
        <div className="space-y-4 pt-2">
          {currentRun.verdict && (
            <div className="p-4 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800/60 rounded-xl">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-400">
                  ⚖️ Judge Verdict
                </span>
                <CriticalFailureBadge failures={currentRun.critical_failures} />
              </div>
              <p className="text-sm font-medium text-indigo-950 dark:text-indigo-200">
                "{currentRun.verdict}"
              </p>

              {/* Criterion Scores */}
              {currentRun.scores && Object.keys(currentRun.scores).length > 0 && (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-3 pt-3 border-t border-indigo-200/50 dark:border-indigo-800/50 text-xs">
                  {Object.entries(currentRun.scores).map(([crit, val]) => (
                    <div key={crit} className="flex justify-between px-2 py-1 bg-white/60 dark:bg-slate-900/60 rounded-lg">
                      <span className="text-slate-500 capitalize">{crit.replace('_', ' ')}</span>
                      <span className={`font-bold ${scoreColorClass(val)}`}>{val}/5</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          <div>
            <div className="flex justify-between items-center mb-2 text-xs text-slate-400 font-mono">
              <span>OUTPUT TEXT ({currentRun.text?.length || 0} chars)</span>
              <span>{currentRun.secs}s latency</span>
            </div>
            <div className="p-4 bg-slate-950 text-slate-100 rounded-xl font-mono text-sm leading-relaxed overflow-x-auto whitespace-pre-wrap border border-slate-800">
              {currentRun.text}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
