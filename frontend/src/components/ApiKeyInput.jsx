import React, { useState, useEffect } from 'react';

export default function ApiKeyInput({ onSave }) {
  const [key, setKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const existing = localStorage.getItem('gemini_api_key') || '';
    setKey(existing);
  }, []);

  const handleSave = (e) => {
    e.preventDefault();
    localStorage.setItem('gemini_api_key', key.trim());
    setSaved(true);
    if (onSave) onSave(key.trim());
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
      <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100 mb-1">
        Gemini API Key
      </h3>
      <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
        Your API key is stored locally in browser storage and sent directly to your local FastAPI server.
      </p>

      <form onSubmit={handleSave} className="flex gap-3 items-center">
        <div className="relative flex-1">
          <input
            type={showKey ? 'text' : 'password'}
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="AIzaSy..."
            className="w-full px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-mono text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-10"
          />
          <button
            type="button"
            onClick={() => setShowKey(!showKey)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-xs"
          >
            {showKey ? 'Hide' : 'Show'}
          </button>
        </div>
        <button
          type="submit"
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm rounded-xl transition shadow-sm hover:shadow active:scale-95"
        >
          {saved ? 'Saved ✓' : 'Save Key'}
        </button>
      </form>
    </div>
  );
}
