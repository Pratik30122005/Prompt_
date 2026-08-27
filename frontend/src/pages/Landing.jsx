import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ParticleBrain, { DISPERSE_MS } from '../components/ParticleBrain';
import { Shell, Nav } from '../components/dala';
import { BODY, DISPLAY, PILL } from '../components/tokens';

export default function Landing() {
  const navigate = useNavigate();
  const [leaving, setLeaving] = useState(false);
  const went = useRef(false);

  const go = () => {
    if (went.current) return;
    // The triangles spread across the page and the route swaps when they are gone. Reduced
    // motion gets there directly.
    if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) {
      went.current = true;
      navigate('/route');
      return;
    }
    setLeaving(true);
    // rAF stops in a backgrounded tab, so onDone might never fire - do not strand the click
    setTimeout(() => arrive(), DISPERSE_MS + 400);
  };

  const arrive = () => {
    if (went.current) return;
    went.current = true;
    navigate('/route');
  };

  return (
    <Shell theme="dark" fading={leaving} fadeMs={DISPERSE_MS * 0.8}>
      <Nav>
        <button
          type="button"
          onClick={go}
          style={PILL}
          className="uppercase bg-iris text-paper px-7 hover:opacity-90 transition-opacity"
        >
          Route a task
        </button>
      </Nav>

      <section className="grid lg:grid-cols-[1.05fr_0.95fr] items-center gap-12 pt-16 pb-24 lg:pt-24 lg:pb-32">
        <div>
          <h1 style={DISPLAY}>
            Every task has a right tool. Ask which one.
          </h1>
          <p style={BODY} className="text-mist mt-9 max-w-xl">
            Describe the job. Get the tool, the intelligence tier it needs, and one sentence
            saying why — before you spend anything on it.
          </p>
        </div>
        <div className="h-[340px] sm:h-[460px] lg:h-[560px]">
          <ParticleBrain dispersing={leaving} onDone={arrive} />
        </div>
      </section>
    </Shell>
  );
}
