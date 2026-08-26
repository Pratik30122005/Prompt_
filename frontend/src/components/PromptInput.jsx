import React, { useRef } from 'react';

export default function PromptInput({ prompt, setPrompt, reference, setReference }) {
  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => setPrompt(event.target.result);
      reader.readAsText(file);
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="flex justify-between items-center mb-2">
          <label className="text-sm font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            Prompt to Evaluate <span className="text-red-500">*</span>
          </label>
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline font-medium flex items-center gap-1"
          >
            📁 Load from File
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept=".txt,.md,.json,.py,.js"
            className="hidden"
          />
        </div>
        <textarea
          rows={6}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter prompt text here..."
          className="w-full p-4 bg-slate-50 dark:bg-slate-800/80 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-mono text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 leading-relaxed"
        />
        <div className="flex justify-between items-center mt-2 text-xs text-slate-400">
          <span>{prompt.length} characters</span>
          <span>Supports plain text, system instructions, formatted templates</span>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <label className="block text-sm font-semibold text-slate-900 dark:text-slate-100 mb-1">
          Reference Answer (Optional Ground Truth)
        </label>
        <p className="text-xs text-slate-500 dark:text-slate-400 mb-2">
          If provided, the LLM Judge will score responses against this standard of accuracy.
        </p>
        <textarea
          rows={3}
          value={reference}
          onChange={(e) => setReference(e.target.value)}
          placeholder="Expected ideal answer or ground truth fact..."
          className="w-full p-3.5 bg-slate-50 dark:bg-slate-800/80 border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-mono text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 leading-relaxed"
        />
      </div>
    </div>
  );
}
