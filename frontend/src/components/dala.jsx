import React from 'react';
import { Link } from 'react-router-dom';
import { LABEL, HEADING_2XS } from './tokens';

export function Rule() {
  return <hr className="border-0 border-t border-hairline" />;
}

/** Uppercase micro-label. Iris by default, saffron for the things worth flagging. */
export function Label({ children, tone = 'iris' }) {
  return (
    <span style={LABEL} className={`uppercase ${tone === 'saffron' ? 'text-saffron' : 'text-iris'}`}>
      {children}
    </span>
  );
}

// The spec's dark palette, applied by overriding the semantic tokens on one element - every
// bg-paper / text-ink / text-ash below it follows. Iris is the same violet in both themes.
const DARK = {
  '--color-paper': '#000000',
  '--color-ink': '#ffffff',
  '--color-ash': '#9a9a9a',
  '--color-mist': '#bdbdbd',
  '--color-saffron': '#ffb829',
  '--color-hairline': '#1a1a1a',
  '--color-well': '#0d0d0d',
};

/**
 * Full-bleed canvas with the 1280px measure.
 *
 * `fading` dims the page on the way out and, on a dark page, warms the canvas to white as it
 * goes - otherwise leaving the black landing for the light router page is a hard flash.
 */
export function Shell({ children, theme = 'light', fading = false, fadeMs = 550 }) {
  return (
    <div
      style={{
        ...(theme === 'dark' ? DARK : null),
        transitionDuration: `${fadeMs}ms`,
        ...(fading && theme === 'dark' ? { backgroundColor: '#ffffff' } : null),
      }}
      className="min-h-screen bg-paper text-ink font-display transition-colors ease-out selection:bg-iris selection:text-paper"
    >
      <div
        style={{ transitionDuration: `${fadeMs}ms` }}
        className={`mx-auto w-full max-w-[1280px] px-6 sm:px-10 transition-opacity ease-out ${
          fading ? 'opacity-0' : 'opacity-100'
        }`}
      >
        {children}
      </div>
    </div>
  );
}

/** Transparent nav: wordmark left, one element right. */
export function Nav({ children }) {
  return (
    <nav className="flex items-center justify-between gap-6 py-6">
      <Link
        to="/"
        style={HEADING_2XS}
        className="text-iris whitespace-nowrap"
      >
        Prompt Evaluation
      </Link>
      {children}
    </nav>
  );
}
