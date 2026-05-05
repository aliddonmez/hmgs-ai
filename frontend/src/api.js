const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function chatAsk(question) {
  const res = await fetch(`${API}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  if (!res.ok) throw new Error('Chat isteği başarısız.')
  return res.json()
}

export async function quizStart(payload) {
  const res = await fetch(`${API}/api/quiz/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Quiz başlatılamadı.')
  }
  return res.json()
}

export async function quizAnswer(session_id, selected_index) {
  const res = await fetch(`${API}/api/quiz/answer`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id, selected_index }),
  })
  if (!res.ok) throw new Error('Cevap gönderilemedi.')
  return res.json()
}

export async function getDashboard(user_id) {
  const res = await fetch(`${API}/api/dashboard/${encodeURIComponent(user_id)}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Rapor alınamadı.')
  }
  return res.json()
}

export async function saveProfile(payload) {
  const res = await fetch(`${API}/api/profiles`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Profil kaydedilemedi.')
  }
  return res.json()
}

export async function getProfile(user_id) {
  const res = await fetch(`${API}/api/profiles/${encodeURIComponent(user_id)}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Profil alınamadı.')
  }
  return res.json()
}
