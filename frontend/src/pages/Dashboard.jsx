import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { listEvaluations, deleteEvaluation } from '../api/client';
import { formatTimestamp, truncate } from '../utils/formatters';

export default function Dashboard() {
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await listEvaluations();
      setEvaluations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e, id) => {
    e.preventDefault();
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this evaluation history?')) {
      try {
        await deleteEvaluation(id);
        setEvaluations(evaluations.filter((item) => item.id !== id));
      } catch (err) {
        alert(err.message);
      }
    }
  };

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-indigo-900 via-indigo-800 to-purple-900 text-white rounded-3xl p-8 shadow-xl relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <span className="inline-block px-3 py-1 bg-indigo-500/30 border border-indigo-400/30 rounded-full text-xs font-semibold uppercase tracking-wider mb-3">
            Prompt Evaluation Studio
          </span>
          <h1 className="text-3xl font-extrabold tracking-tight mb-2">
            Compare Gemini Models, Budgets & ROI
          </h1>
          <p className="text-indigo-200 text-sm leading-relaxed mb-6">
            Evaluate response quality, latency, token usage, and USD cost across Gemini models and thinking settings in real-time.
          </p>
          <Link
            to="/evaluate"
            className="inline-flex items-center gap-2 px-6 py-3 bg-white text-indigo-900 hover:bg-indigo-50 font-bold rounded-xl shadow-lg transition transform hover:-translate-y-0.5"
          >
            <span>⚡ Start New Evaluation</span>
          </Link>
        </div>
      </div>

      {/* Stats Quick Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Evaluations</span>
          <p className="text-3xl font-extrabold text-slate-900 dark:text-slate-100 mt-2">
            {evaluations.length}
          </p>
        </div>
        <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Supported Models</span>
          <p className="text-3xl font-extrabold text-indigo-600 dark:text-indigo-400 mt-2">
            3+
          </p>
        </div>
        <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Evaluation Engine</span>
          <p className="text-lg font-bold text-emerald-600 dark:text-emerald-400 mt-3 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
            eval.py Ready
          </p>
        </div>
      </div>

      {/* History List */}
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
            Recent Evaluations
          </h2>
          <button
            onClick={loadHistory}
            className="text-xs font-medium text-indigo-600 dark:text-indigo-400 hover:underline"
          >
            🔄 Refresh
          </button>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400">Loading history...</div>
        ) : error ? (
          <div className="p-6 bg-red-50 text-red-600 rounded-2xl text-sm">
            Failed to connect to backend: {error}. Make sure server.py is running!
          </div>
        ) : evaluations.length === 0 ? (
          <div className="bg-white dark:bg-slate-900 rounded-2xl p-12 text-center border border-slate-200 dark:border-slate-800">
            <p className="text-slate-400 text-sm mb-4">No prompt evaluations recorded yet.</p>
            <Link
              to="/evaluate"
              className="inline-block px-5 py-2.5 bg-indigo-600 text-white font-semibold text-xs rounded-xl shadow"
            >
              Run First Evaluation
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">
            {evaluations.map((item) => (
              <Link
                key={item.id}
                to={`/results/${item.id}`}
                className="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/50 shadow-sm hover:shadow-md transition flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 group"
              >
                <div className="space-y-1 max-w-xl">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-xs text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/50 px-2 py-0.5 rounded-md">
                      #{item.id}
                    </span>
                    <span className="text-xs text-slate-400">
                      {formatTimestamp(item.timestamp)}
                    </span>
                  </div>
                  <p className="font-medium text-slate-900 dark:text-slate-100 text-sm group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition">
                    "{truncate(item.prompt, 110)}"
                  </p>
                  <div className="flex flex-wrap gap-2 pt-1 text-xs text-slate-500">
                    <span>Models: {item.models.join(', ')}</span>
                    <span>•</span>
                    <span>Judge: {item.judge ? 'Enabled' : 'Disabled'}</span>
                  </div>
                </div>

                <div className="flex items-center gap-4 self-end sm:self-center">
                  {item.avg_score && (
                    <div className="text-right">
                      <span className="text-xs text-slate-400 block">Avg Score</span>
                      <span className="font-mono font-bold text-sm text-emerald-600 dark:text-emerald-400">
                        {item.avg_score}/5
                      </span>
                    </div>
                  )}
                  <button
                    onClick={(e) => handleDelete(e, item.id)}
                    className="p-2 text-slate-400 hover:text-red-500 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition"
                    title="Delete evaluation"
                  >
                    🗑️
                  </button>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
