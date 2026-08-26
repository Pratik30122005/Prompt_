import React, { useState, useEffect } from 'react';
import { listEvaluations, getEvaluation } from '../api/client';
import ResultTable from '../components/ResultTable';
import ScoreRadar from '../components/ScoreRadar';
import CostBar from '../components/CostBar';
import { formatTimestamp, truncate } from '../utils/formatters';

export default function Compare() {
  const [evaluations, setEvaluations] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [comparedData, setComparedData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    listEvaluations().then(setEvaluations).catch(console.error);
  }, []);

  const toggleSelect = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter((item) => item !== id));
    } else {
      if (selectedIds.length < 3) {
        setSelectedIds([...selectedIds, id]);
      } else {
        alert('You can compare up to 3 evaluations at once.');
      }
    }
  };

  const handleCompare = async () => {
    if (selectedIds.length === 0) return;
    setLoading(true);
    try {
      const fullResults = await Promise.all(selectedIds.map((id) => getEvaluation(id)));
      setComparedData(fullResults);
    } catch (err) {
      alert('Failed to load comparison: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const combinedResults = comparedData.flatMap((evalItem) =>
    (evalItem.results || []).map((r) => ({
      ...r,
      model: `${r.model} [${evalItem.id}]`,
    }))
  );

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
          Compare Evaluations Side-by-Side
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Select up to 3 past evaluation runs to compare model quality, trade-offs, and cost metrics.
        </p>
      </div>

      {/* Select List */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
          Select Runs to Compare ({selectedIds.length}/3)
        </h3>

        {evaluations.length === 0 ? (
          <p className="text-sm text-slate-400">No evaluations found in history.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {evaluations.map((item) => {
              const active = selectedIds.includes(item.id);
              return (
                <div
                  key={item.id}
                  onClick={() => toggleSelect(item.id)}
                  className={`p-4 rounded-xl border cursor-pointer transition flex flex-col justify-between space-y-2 ${
                    active
                      ? 'border-indigo-600 bg-indigo-50/50 dark:bg-indigo-950/30'
                      : 'border-slate-200 dark:border-slate-800 hover:border-slate-300'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-xs font-bold text-indigo-600">#{item.id}</span>
                    <span className="text-xs text-slate-400">{formatTimestamp(item.timestamp)}</span>
                  </div>
                  <p className="text-xs font-medium text-slate-900 dark:text-slate-100">
                    "{truncate(item.prompt, 60)}"
                  </p>
                  <div className="text-xs text-slate-500 font-mono">
                    Models: {item.models.join(', ')}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        <button
          onClick={handleCompare}
          disabled={selectedIds.length === 0 || loading}
          className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-400 text-white font-bold rounded-xl text-xs transition shadow"
        >
          {loading ? 'Loading...' : `Compare ${selectedIds.length} Evaluation(s)`}
        </button>
      </div>

      {/* Comparison Visuals */}
      {combinedResults.length > 0 && (
        <div className="space-y-8">
          <ResultTable results={combinedResults} />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ScoreRadar results={combinedResults} />
            <CostBar results={combinedResults} />
          </div>
        </div>
      )}
    </div>
  );
}
