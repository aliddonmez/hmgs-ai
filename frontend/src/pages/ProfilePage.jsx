import { useState } from 'react'
import { getProfile } from '../api'

export default function ProfilePage({ profile, onProfileChange }) {
  const [userId, setUserId] = useState(profile.userId || '')
  const [loading, setLoading] = useState(false)
  const [loggedIn, setLoggedIn] = useState(false)
  const [error, setError] = useState('')

  const login = async () => {
    const cleanUserId = userId.trim()

    if (!cleanUserId) {
      setError('Profil ID zorunlu.')
      setLoggedIn(false)
      return
    }

    setLoading(true)
    setError('')
    setLoggedIn(false)

    try {
      const foundProfile = await getProfile(cleanUserId)

      onProfileChange({
        userId: foundProfile.user_id,
        displayName: foundProfile.display_name,
      })
      setLoggedIn(true)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const clear = () => {
    setUserId('')
    onProfileChange({ userId: '', displayName: '' })
    setError('')
    setLoggedIn(false)
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Kullanıcı Profili</h1>
        <p>Kayıtlı profil ID ile giriş yapın. Quiz ve dashboard verileri bu profile göre çalışır.</p>
      </div>

      <div className="profile-layout">
        <div className="card fade-up">
          <div className="form-group">
            <label className="label" htmlFor="profile-user-id">Profil ID</label>
            <input
              id="profile-user-id"
              className="input"
              placeholder="örn. ali_balcı"
              value={userId}
              onChange={e => setUserId(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') login() }}
            />
          </div>

          {error && <div className="alert alert-error profile-alert">⚠️ {error}</div>}
          {loggedIn && <div className="alert alert-success profile-alert">✅ Giriş yapıldı.</div>}

          <div className="profile-actions">
            <button className="btn btn-primary" onClick={login} disabled={loading}>
              {loading ? <><div className="spinner" style={{ width: 18, height: 18 }} /> Giriş yapılıyor…</> : 'Giriş Yap'}
            </button>
            <button className="btn btn-ghost" onClick={clear}>Temizle</button>
          </div>
        </div>

        <div className="profile-summary card fade-up">
          <div className="profile-summary-avatar">
            {(profile.displayName || profile.userId || userId || '?').slice(0, 1).toUpperCase()}
          </div>
          <div>
            <div className="profile-summary-title">{profile.displayName || 'Giriş yapılmadı'}</div>
            <div className="profile-summary-id">{profile.userId || 'Profil ID girilmedi'}</div>
          </div>
        </div>
      </div>
    </div>
  )
}
