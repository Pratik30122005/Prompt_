import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Landing from './pages/Landing'
import Recommend from './pages/Recommend'
import Dashboard from './pages/Dashboard'
import Evaluate from './pages/Evaluate'
import Results from './pages/Results'
import Compare from './pages/Compare'
import Settings from './pages/Settings'

// The landing page paints its own full-bleed black; the eval studio keeps the sidebar shell.
function StudioShell({ children }) {
  return (
    <div className="flex min-h-screen">
      <Navbar />
      <main className="flex-1 ml-0 md:ml-64 min-h-screen">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">{children}</div>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/route" element={<Recommend />} />
      <Route path="/dashboard" element={<StudioShell><Dashboard /></StudioShell>} />
      <Route path="/evaluate" element={<StudioShell><Evaluate /></StudioShell>} />
      <Route path="/results/:id" element={<StudioShell><Results /></StudioShell>} />
      <Route path="/compare" element={<StudioShell><Compare /></StudioShell>} />
      <Route path="/settings" element={<StudioShell><Settings /></StudioShell>} />
    </Routes>
  )
}
