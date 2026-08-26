import React, { useState } from 'react';
import { DEFAULT_MODELS } from '../utils/constants';

export default function ModelSelector({
  selectedModels,
  setSelectedModels,
  thinkingBudgets,
  setThinkingBudgets,
  nRuns,
  setNRuns,
  judge,
  setJudge,
  judgeModel,
  setJudgeModel,
}) {
  const [customModel, setCustomModel] = useState('');
  const [customThinking, setCustomThinking] = useState('');

  const toggleModel = (m) => {
    if (selectedModels.includes(m)) {
      if (selectedModels.length > 1) {
        setSelectedModels(selectedModels.filter((item) => item !== m));
      }
    } else {
      setSelectedModels([...selectedModels, m]);
    }
  };

  const addCustomModel = () => {
    if (customModel.trim() && !selectedModels.includes(customModel.trim())) {
      setSelectedModels([...selectedModels, customModel.trim()]);
      setCustomModel('');
    }
  };

  const toggleThinking = (budget) => {
    if (thinkingBudgets.includes(budget)) {
      if (thinkingBudgets.length > 1) {
        setThinkingBudgets(thinkingBudgets.filter((b) => b !== budget));
      }
    } else {
      setThinkingBudgets([...thinkingBudgets, budget]);
    }
  };

  const addCustomThinking = () => {
    const val = parseInt(customThinking.trim(), 10);
    if (!isNaN(val) && !thinkingBudgets.includes(val)) {
      setThinkingBudgets([...thinkingBudgets, val]);
      setCustomThinking('');
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-6">
      <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100 border-b border-slate-100 dark:border-slate-800 pb-3">
        Evaluation Settings
      </h3>

      {/* Model Selection */}
      <div>
        <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">
          Models to Compare
        </label>
        <div className="flex flex-wrap gap-2 mb-3">
          {DEFAULT_MODELS.map((m) => {
            const active = selectedModels.includes(m);
            return (
              <button
                key={m}
                type="button"
                onClick={() => toggleModel(m)}
                className={`px-3.5 py-2 rounded-xl text-xs font-medium transition flex items-center gap-1.5 ${
                  active
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                }`}
              >
                <span>{active ? '✓' : '+'}</span>
                <span>{m}</span>
              </button>
            );
          })}
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Custom model ID..."
            value={customModel}
            onChange={(e) => setCustomModel(e.target.value)}
            className="px-3 py-1.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 flex-1"
          />
          <button
            type="button"
            onClick={addCustomModel}
            className="px-3 py-1.5 bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-medium rounded-xl transition"
          >
            Add
          </button>
        </div>
      </div>

      {/* Thinking Budgets */}
      <div>
        <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">
          Thinking Budgets
        </label>
        <div className="flex flex-wrap gap-2 mb-2">
          {[
            { label: 'Default', val: null },
            { label: 'Off (0)', val: 0 },
            { label: '4,096 tokens', val: 4096 },
            { label: 'Dynamic (-1)', val: -1 },
          ].map(({ label, val }) => {
            const active = thinkingBudgets.includes(val);
            return (
              <button
                key={String(val)}
                type="button"
                onClick={() => toggleThinking(val)}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium transition ${
                  active
                    ? 'bg-purple-600 text-white shadow-sm'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
                }`}
              >
                {label}
              </button>
            );
          })}
        </div>
      </div>

      {/* N Runs & Judge */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-slate-100 dark:border-slate-800 pt-4">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">
            Runs per config (-n)
          </label>
          <p className="text-xs text-slate-400 mb-2">Higher N tests output consistency</p>
          <input
            type="number"
            min={1}
            max={10}
            value={nRuns}
            onChange={(e) => setNRuns(Math.max(1, parseInt(e.target.value) || 1))}
            className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-semibold text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-1">
            <label className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              LLM Judge Scoring
            </label>
            <input
              type="checkbox"
              checked={judge}
              onChange={(e) => setJudge(e.target.checked)}
              className="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500"
            />
          </div>
          <p className="text-xs text-slate-400 mb-2">Score 1-5 across 7 criteria</p>
          {judge && (
            <select
              value={judgeModel}
              onChange={(e) => setJudgeModel(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-medium text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              {DEFAULT_MODELS.map((m) => (
                <option key={m} value={m}>
                  Judge: {m}
                </option>
              ))}
            </select>
          )}
        </div>
      </div>
    </div>
  );
}
