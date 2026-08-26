import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/evaluate', label: 'New Evaluation', icon: '⚡' },
    { path: '/compare', label: 'Compare Evals', icon: '⚖️' },
    { path: '/settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col fixed inset-y-0 left-0 z-50 shadow-xl border-r border-slate-800 hidden md:flex">
      <div className="p-6 border-b border-slate-800 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-lg text-white shadow-md">
          P_
        </div>
        <div>
          <h1 className="font-bold text-lg tracking-tight leading-none text-slate-100">Prompt_</h1>
          <span className="text-xs text-slate-400 font-medium">Gemini Eval Studio</span>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-150 ${
                isActive
                  ? 'bg-indigo-600/90 text-white shadow-md shadow-indigo-600/20 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`
            }
          >
            <span className="text-base">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800/80">
        <div className="p-3.5 bg-slate-800/50 rounded-xl border border-slate-700/50 flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></div>
          <div className="text-xs">
            <p className="font-medium text-slate-300">FastAPI Engine</p>
            <p className="text-slate-500">eval.py connected</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
