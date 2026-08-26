import React from 'react';

export default function RunProgress({ progress }) {
  if (!progress) return null;

  const { model, thinking, run, total_runs, config, total_configs, secs } = progress;
  const percent = Math.min(
    100,
    Math.round((((config - 1) * total_runs + run) / (total_configs * total_runs)) * 100)
  );

  return (
    <div className="bg-slate-900 border border-slate-800 text-white rounded-2xl p-6 shadow-xl space-y-4">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 rounded-full bg-indigo-500 animate-ping"></div>
          <span className="font-semibold text-sm">Evaluating Prompt...</span>
        </div>
        <span className="text-xs font-mono text-slate-400">{percent}% Complete</span>
      </div>

      <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
        <div
          className="bg-indigo-500 h-2 rounded-full transition-all duration-300"
          style={{ width: `${percent}%` }}
        ></div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2 text-xs">
        <div>
          <span className="text-slate-400 block">Current Model</span>
          <span className="font-mono font-medium text-slate-200">{model || '-'}</span>
        </div>
        <div>
          <span className="text-slate-400 block">Thinking Budget</span>
          <span className="font-mono font-medium text-slate-200">
            {thinking === null ? 'Default' : thinking}
          </span>
        </div>
        <div>
          <span className="text-slate-400 block">Run Iteration</span>
          <span className="font-mono font-medium text-slate-200">
            {run} of {total_runs}
          </span>
        </div>
        <div>
          <span className="text-slate-400 block">Last Run Latency</span>
          <span className="font-mono font-medium text-emerald-400">
            {secs ? `${secs}s` : 'In progress...'}
          </span>
        </div>
      </div>
    </div>
  );
}
