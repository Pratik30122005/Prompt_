import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PromptInput from '../components/PromptInput';
import ModelSelector from '../components/ModelSelector';
import RunProgress from '../components/RunProgress';
import ApiKeyInput from '../components/ApiKeyInput';
import { evaluatePrompt, hasApiKey } from '../api/client';
import { DEFAULT_MODELS } from '../utils/constants';

export default function Evaluate() {
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState('');
  const [reference, setReference] = useState('');
  const [selectedModels, setSelectedModels] = useState([DEFAULT_MODELS[1], DEFAULT_MODELS[2]]);
  const [thinkingBudgets, setThinkingBudgets] = useState([null]);
  const [nRuns, setNRuns] = useState(1);
  const [judge, setJudge] = useState(true);
  const [judgeModel, setJudgeModel] = useState(DEFAULT_MODELS[1]);

  const [isEvaluating, setIsEvaluating] = useState(false);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);

  const handleRun = async (isDemo = false) => {
    if (!prompt.trim()) {
      alert('Please enter a prompt to evaluate.');
      return;
    }

    if (!hasApiKey() && !isDemo) {
      // Set 'demo' key in localStorage for instant testing
      localStorage.setItem('gemini_api_key', 'demo');
    }

    setIsEvaluating(true);
    setError(null);
    setProgress(null);

    try {
      const config = {
        prompt: prompt.trim(),
        models: selectedModels,
        thinking_budgets: thinkingBudgets,
        n: nRuns,
        judge,
        judge_model: judgeModel,
        reference: reference.trim() || null,
      };

      await evaluatePrompt(config, (event) => {
        if (event.type === 'progress') {
          setProgress(event);
        } else if (event.type === 'complete') {
          navigate(`/results/${event.id}`);
        } else if (event.type === 'error') {
          setError(event.message);
          setIsEvaluating(false);
        }
      });
    } catch (err) {
      setError(err.message);
      setIsEvaluating(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
          New Prompt Evaluation
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Configure prompt inputs, models, extended thinking budgets, and judge criteria.
        </p>
      </div>

      {!hasApiKey() && (
        <div className="mb-4">
          <ApiKeyInput />
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 rounded-2xl text-red-600 dark:text-red-400 text-sm font-mono">
          ⚠️ Error: {error}
        </div>
      )}

      {isEvaluating && <RunProgress progress={progress} />}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <PromptInput
            prompt={prompt}
            setPrompt={setPrompt}
            reference={reference}
            setReference={setReference}
          />
        </div>
        <div>
          <ModelSelector
            selectedModels={selectedModels}
            setSelectedModels={setSelectedModels}
            thinkingBudgets={thinkingBudgets}
            setThinkingBudgets={setThinkingBudgets}
            nRuns={nRuns}
            setNRuns={setNRuns}
            judge={judge}
            setJudge={setJudge}
            judgeModel={judgeModel}
            setJudgeModel={setJudgeModel}
          />

          <button
            type="button"
            onClick={handleRun}
            disabled={isEvaluating || !prompt.trim()}
            className="w-full mt-6 py-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-400 text-white font-bold rounded-2xl shadow-lg hover:shadow-xl transition transform active:scale-98 flex items-center justify-center gap-2 text-base"
          >
            {isEvaluating ? (
              <>
                <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>Evaluating...</span>
              </>
            ) : (
              <>
                <span>🚀 Run Evaluation</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
