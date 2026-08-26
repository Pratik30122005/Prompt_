import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Evaluate from './pages/Evaluate'
import Results from './pages/Results'
import Compare from './pages/Compare'
import Settings from './pages/Settings'

export default function App() {
  return (
    <div className="flex min-h-screen">
      <Navbar />
      <main className="flex-1 ml-0 md:ml-64 min-h-screen">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/evaluate" element={<Evaluate />} />
            <Route path="/results/:id" element={<Results />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}
