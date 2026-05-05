import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import QuizPage from './pages/QuizPage'
import DashboardPage from './pages/DashboardPage'
import ScenarioPage from './pages/ScenarioPage'
import ProfilePage from './pages/ProfilePage'

const PROFILE_STORAGE_KEY = 'hmgs.activeProfile'

const NAV = [
  { path: '/', icon: '💬', label: 'Chat' },
  { path: '/quiz', icon: '🧠', label: 'Quiz' },
  { path: '/scenarios', icon: '📖', label: 'Senaryolar' },
  { path: '/dashboard', icon: '📊', label: 'Dashboard' },
  { path: '/profile', icon: '👤', label: 'Profil' },
]

export default function App() {
  const [profile, setProfile] = useState(() => {
    try {
      const saved = localStorage.getItem(PROFILE_STORAGE_KEY)
      return saved ? JSON.parse(saved) : { userId: '', displayName: '' }
    } catch {
      return { userId: '', displayName: '' }
    }
  })

  useEffect(() => {
    localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profile))
  }, [profile])

  const profileLabel = profile.displayName || profile.userId || 'Profil yok'

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

          <div className="active-profile">
            <div className="profile-avatar">{profileLabel.slice(0, 1).toUpperCase()}</div>
            <div>
              <div className="profile-name">{profileLabel}</div>
              <div className="profile-id">{profile.userId || 'Kullanıcı ID seçilmedi'}</div>
            </div>
          </div>

          <div className="sidebar-footer">
            HMGS v1.0 · AI Destekli
          </div>
        </aside>

        {/* ── Content ── */}
        <main className="main">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/quiz" element={<QuizPage profile={profile} />} />
            <Route path="/scenarios" element={<ScenarioPage />} />
            <Route path="/dashboard" element={<DashboardPage profile={profile} />} />
            <Route path="/profile" element={<ProfilePage profile={profile} onProfileChange={setProfile} />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
