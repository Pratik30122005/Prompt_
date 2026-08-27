import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { recommendTool, getTools, hasApiKey } from '../api/client';
import { Shell, Nav, Rule, Label } from '../components/dala';
import { BODY, CAPTION, HEADING_2XS, HEADING_LG, HEADING_SM, HEADING_XS, LABEL, PILL } from '../components/tokens';

const EXAMPLES = [
  'Build a 10-slide investor deck from these Q3 revenue numbers',
  'Reconcile two 200k-row CSV exports and explain every variance',
  'What are our three competitors charging for this in 2026?',
  'Refactor the auth middleware across the repo and keep the tests green',
];

export default function Recommend() {
  const [task, setTask] = useState('');
  const [rec, setRec] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  // ponytail: inline key row rather than reusing ApiKeyInput - that component is a white
  // bordered card and Settings still needs it exactly as it is. Same localStorage key.
  const [keyed, setKeyed] = useState(hasApiKey);
  const [keyDraft, setKeyDraft] = useState('');
  const [serverKeyed, setServerKeyed] = useState(null);  // null = still asking

  useEffect(() => {
    getTools().then((t) => setServerKeyed(!!t.has_key)).catch(() => setServerKeyed(false));
  }, []);

  const saveKey = (e) => {
    e.preventDefault();
    if (!keyDraft.trim()) return;
    localStorage.setItem('gemini_api_key', keyDraft.trim());
    setKeyed(true);
  };

  const handleRecommend = async (text) => {
    const value = (text ?? task).trim();
    if (!value) return;
    // Sending no key is fine when the server has one; it refuses outright when neither does.
    setLoading(true);
    setError(null);
    setRec(null);
    try {
      setRec(await recommendTool(value));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Nothing runs without a real key - no demo, no fabricated recommendation.
  const canRun = keyed || serverKeyed !== false;

  const primary = rec?.primary;
  const isMax = primary?.intelligence === 'max';

  return (
    <Shell>
      <Nav>
        <Link to="/" style={LABEL} className="uppercase text-ash hover:text-ink transition-colors">
          Home
        </Link>
      </Nav>

      <section className="pt-14 pb-20 lg:pt-20 lg:pb-28">
        <h1 style={HEADING_LG} className="max-w-3xl">
          What do you want to do?
        </h1>

        <textarea
          rows={3}
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Turn last quarter's sales numbers into a board presentation"
          style={{ ...BODY, borderRadius: 24 }}
          className="mt-10 w-full bg-well text-ink placeholder:text-ash/60 px-7 py-6 resize-none focus:outline-none focus:ring-1 focus:ring-iris"
        />

        <div className="flex flex-wrap gap-3 mt-6">
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              type="button"
              onClick={() => { setTask(ex); handleRecommend(ex); }}
              style={{ fontSize: 14, fontWeight: 400 }}
              className="rounded-full px-5 py-2 bg-well text-ash hover:text-ink transition-colors"
            >
              {ex.length > 44 ? `${ex.slice(0, 44)}…` : ex}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap items-center gap-x-8 gap-y-5 mt-10">
          <button
            type="button"
            onClick={() => handleRecommend()}
            disabled={loading || !task.trim() || !canRun}
            style={PILL}
            className="uppercase bg-iris text-paper px-9 disabled:opacity-35 hover:opacity-90 transition-opacity"
          >
            {loading ? 'Routing…' : 'Recommend a tool'}
          </button>
          {!keyed && serverKeyed === false && (
            <form onSubmit={saveKey} className="flex items-center gap-4 flex-1 min-w-[280px]">
              <input
                type="password"
                value={keyDraft}
                onChange={(e) => setKeyDraft(e.target.value)}
                placeholder="Paste your Gemini API key"
                style={{ fontWeight: 200, fontSize: 15, borderRadius: 24 }}
                className="flex-1 bg-well text-ink placeholder:text-ash/60 px-6 h-[45px] focus:outline-none focus:ring-1 focus:ring-iris"
              />
              <button type="submit" style={LABEL} className="uppercase text-ash hover:text-ink transition-colors">
                Save
              </button>
            </form>
          )}
        </div>

        {!canRun && (
          <p style={BODY} className="text-saffron mt-8 max-w-3xl">
            No Gemini API key configured. Put <span className="font-mono">GEMINI_API_KEY</span>{' '}
            in <span className="font-mono">.env</span> next to <span className="font-mono">server.py</span>{' '}
            and restart it, or paste a key above. Routing is disabled until then.
          </p>
        )}

        {error && <p style={BODY} className="text-saffron mt-8">{error}</p>}
      </section>

      {primary && (
        <>
          <Rule />
          <section className="py-20 lg:py-28">
            <Label tone={isMax ? 'saffron' : 'iris'}>
              {primary.intelligence} intelligence · {primary.thinking} thinking
            </Label>
            <h2 style={HEADING_LG} className="mt-6">
              {primary.display}
            </h2>
            {primary.tier && (
              <p style={HEADING_2XS} className="text-ash mt-4">
                {primary.tier}
              </p>
            )}
            <p style={BODY} className="text-mist mt-9 max-w-3xl">{primary.why}</p>

            <div className="flex flex-wrap gap-x-14 gap-y-4 mt-12" style={CAPTION}>
              <span className="text-ash">
                Task <span className="text-ink">{rec.task_type?.replace('_', ' ')}</span>
              </span>
              <span className="text-ash">
                Complexity <span className="text-ink">{rec.complexity}</span>
              </span>
              {primary.cost && (
                <span className="text-ash">Cost <span className="text-ink">{primary.cost}</span></span>
              )}
              {rec.deliverable && (
                <span className="text-ash">
                  Deliverable <span className="text-ink">{rec.deliverable}</span>
                </span>
              )}
            </div>

            {primary.unknown_tool && (
              <p style={BODY} className="text-saffron mt-10">
                This tool is not in the catalog — its tier and cost could not be verified.
              </p>
            )}
          </section>
        </>
      )}

      {rec?.alternatives?.length > 0 && (
        <>
          <Rule />
          <section className="py-20 lg:py-24">
            <Label>Also works</Label>
            <div className="mt-10 space-y-14">
              {rec.alternatives.map((a) => (
                <div key={a.tool} className="max-w-3xl">
                  <h3 style={HEADING_SM}>
                    {a.display}
                    {a.tier && <span className="text-ash"> · {a.tier}</span>}
                  </h3>
                  <p style={BODY} className="text-mist mt-5">{a.why}</p>
                  <p style={CAPTION} className="text-ash mt-3">
                    Pick it instead if: {a.tradeoff}
                  </p>
                </div>
              ))}
            </div>
          </section>
        </>
      )}

      {rec?.avoid?.length > 0 && (
        <>
          <Rule />
          <section className="py-20 lg:py-24">
            <Label tone="saffron">Don&apos;t use</Label>
            <div className="mt-10 space-y-10">
              {rec.avoid.map((a) => (
                <div key={a.tool} className="max-w-3xl">
                  <h3 style={HEADING_XS} className="text-ash">
                    {a.display}
                  </h3>
                  <p style={BODY} className="text-mist mt-4">{a.why}</p>
                </div>
              ))}
            </div>
          </section>
        </>
      )}

    </Shell>
  );
}
