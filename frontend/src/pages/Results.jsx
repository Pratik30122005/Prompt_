import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getEvaluation } from '../api/client';
import ResultTable from '../components/ResultTable';
import ScoreRadar from '../components/ScoreRadar';
import CostBar from '../components/CostBar';
import ResponseViewer from '../components/ResponseViewer';
import { formatTimestamp } from '../utils/formatters';

export default function Results() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [id]);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await getEvaluation(id);
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-12 text-center text-slate-400">Loading evaluation results...</div>;
  if (error) return <div className="p-6 bg-red-50 text-red-600 rounded-2xl text-sm">Error: {error}</div>;
  if (!data) return null;

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-mono font-bold text-xs text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/50 px-2 py-0.5 rounded-md">
              Evaluation #{data.id}
            </span>
            <span className="text-xs text-slate-400">{formatTimestamp(data.timestamp)}</span>
          </div>
          <h1 className="text-xl font-extrabold text-slate-900 dark:text-slate-100">
            Evaluation Report
          </h1>
        </div>

        <div className="flex gap-2">
          <Link
            to="/evaluate"
            className="px-4 py-2 bg-indigo-600 text-white font-semibold text-xs rounded-xl hover:bg-indigo-700 transition"
          >
            ⚡ New Evaluation
          </Link>
        </div>
      </div>

      {/* Prompt Card */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-md border border-slate-800 space-y-2">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block">Evaluated Prompt</span>
        <div className="p-3 bg-slate-950 rounded-xl font-mono text-xs leading-relaxed text-slate-200 border border-slate-800 whitespace-pre-wrap max-h-48 overflow-y-auto">
          {data.prompt}
        </div>
        {data.config?.reference && (
          <div className="pt-2 text-xs">
            <span className="text-slate-400 block font-bold">Reference Ground Truth:</span>
            <p className="text-slate-300 font-mono italic">"{data.config.reference}"</p>
          </div>
        )}
      </div>

      {/* Table Summary */}
      <ResultTable results={data.results} />

      {/* Visual Charts */}
      {data.config?.judge && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ScoreRadar results={data.results} />
          <CostBar results={data.results} />
        </div>
      )}

      {/* Text Outputs & Verdicts */}
      <ResponseViewer results={data.results} />
    </div>
  );
}
