import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import QuizPage from './pages/QuizPage'
import DashboardPage from './pages/DashboardPage'
import ScenarioPage from './pages/ScenarioPage'

const NAV = [
  { path: '/', icon: '💬', label: 'Chat' },
  { path: '/quiz', icon: '🧠', label: 'Quiz' },
  { path: '/scenarios', icon: '📖', label: 'Senaryolar' },
  { path: '/dashboard', icon: '📊', label: 'Dashboard' },
]

export default function App() {
  return (
    <BrowserRouter>
      <div className="layout">
        {/* ── Sidebar ── */}
        <aside className="sidebar">
          <div className="sidebar-logo">
            <span className="logo-icon">⚖️</span>
            <div>
              <div className="logo-text">HMGS</div>
              <div className="logo-sub">Hukuki Asistan</div>
            </div>
          </div>

          <nav className="sidebar-nav">
            {NAV.map(n => (
              <NavLink
                key={n.path}
                to={n.path}
                end={n.path === '/'}
                className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
              >
                <span className="nav-icon">{n.icon}</span>
                <span>{n.label}</span>
              </NavLink>
            ))}
          </nav>

          <div className="sidebar-footer">
            HMGS v1.0 · AI Destekli
          </div>
        </aside>

        {/* ── Content ── */}
        <main className="main">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/quiz" element={<QuizPage />} />
            <Route path="/scenarios" element={<ScenarioPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
