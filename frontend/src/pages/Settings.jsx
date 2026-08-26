import React, { useState, useEffect } from 'react';
import ApiKeyInput from '../components/ApiKeyInput';
import { getModels } from '../api/client';
import { CRITERIA, CRITERIA_DESCRIPTIONS } from '../utils/constants';

export default function Settings() {
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    getModels().then(setModelInfo).catch(console.error);
  }, []);

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
          Settings & Model Info
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Manage API keys, inspect pricing models, and review the evaluation criteria.
        </p>
      </div>

      {/* API Key Management */}
      <ApiKeyInput />

      {/* Pricing Reference */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
          Gemini Model Pricing Reference (eval.py rates)
        </h3>
        <p className="text-xs text-slate-500 dark:text-slate-400">
          Rates per 1 million tokens in USD (Input / Output). Extended thinking tokens are billed as output.
        </p>

        {modelInfo?.prices ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono border-collapse">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-400 uppercase">
                  <th className="py-2 px-3">Model</th>
                  <th className="py-2 px-3">Input Cost / 1M</th>
                  <th className="py-2 px-3">Output / Think Cost / 1M</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {Object.entries(modelInfo.prices).map(([m, p]) => (
                  <tr key={m}>
                    <td className="py-2.5 px-3 font-bold text-slate-900 dark:text-slate-100">{m}</td>
                    <td className="py-2.5 px-3 text-indigo-600 dark:text-indigo-400">${p.input.toFixed(2)}</td>
                    <td className="py-2.5 px-3 text-purple-600 dark:text-purple-400">${p.output.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-xs text-slate-400">Loading model list...</p>
        )}
      </div>

      {/* 7 Criteria Definitions */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
          LLM Judge 7 Criteria Definitions
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {CRITERIA.map((c) => (
            <div key={c} className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200/60 dark:border-slate-800">
              <span className="text-xs font-bold capitalize text-indigo-600 dark:text-indigo-400 block mb-1">
                {c.replace('_', ' ')}
              </span>
              <p className="text-xs text-slate-600 dark:text-slate-300">
                {CRITERIA_DESCRIPTIONS[c]}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
