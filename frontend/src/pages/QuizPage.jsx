import { useState } from 'react'
import { quizStart, quizAnswer } from '../api'

const MODES = [
  { value: 'random',     label: '🎲 Rastgele',    desc: 'Karışık soru seçimi' },
  { value: 'balanced',   label: '⚖️ Dengeli',     desc: 'Konulara göre dengeli dağılım' },
  { value: 'weak_focus', label: '🎯 Zayıf Odak',  desc: 'Zayıf olduğun konulardan seç' },
]

const LETTERS = ['A', 'B', 'C', 'D', 'E']

// ── Setup ekranı ─────────────────────────────────────────────────────────────
function SetupForm({ onStart, profile }) {
  const [mode, setMode]           = useState('random')
  const [n, setN]                 = useState(20)
  const [weakTopic, setWeakTopic] = useState('')
  const [loading, setLoading]     = useState(false)
  const [error, setError]         = useState('')

  const start = async () => {
    const activeUserId = profile?.userId?.trim()
    if (!activeUserId) { setError('Önce Profil sayfasından profil ID ile giriş yapın.'); return }
    setError('')
    setLoading(true)
    try {
      const data = await quizStart({
        user_id: activeUserId,
        mode,
        n_questions: n,
        weak_topic: weakTopic.trim() || null,
      })
      onStart(data, activeUserId)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Quiz Modu</h1>
        <p>Hukuki bilginizi test edin. Parametrelerinizi ayarlayın ve başlayın.</p>
      </div>

      <div className="quiz-setup">
        <div className="card fade-up">
          <div className="form-group">
            <label className="label">Quiz Modu</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {MODES.map(m => (
                <button
                  key={m.value}
                  id={`mode-${m.value}`}
                  onClick={() => setMode(m.value)}
                  style={{
                    padding: '12px 16px',
                    borderRadius: 'var(--radius-sm)',
                    border: `1.5px solid ${mode === m.value ? 'var(--teal)' : 'var(--border)'}`,
                    background: mode === m.value ? 'var(--teal-glow)' : 'var(--surface)',
                    color: mode === m.value ? 'var(--teal)' : 'var(--text-dim)',
                    cursor: 'pointer',
                    textAlign: 'left',
                    fontFamily: 'inherit',
                    transition: 'all var(--transition)',
                    boxShadow: '0 1px 3px rgba(27,42,71,0.05)',
                  }}
                >
                  <div style={{ fontWeight: 600, fontSize: 14 }}>{m.label}</div>
                  <div style={{ fontSize: 12, opacity: 0.7, marginTop: 2 }}>{m.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {mode === 'weak_focus' && (
            <div className="form-group">
              <label className="label" htmlFor="quiz-weak-topic">Zayıf Konu (isteğe bağlı)</label>
              <input
                id="quiz-weak-topic"
                className="input"
                placeholder="örn. Ceza Hukuku"
                value={weakTopic}
                onChange={e => setWeakTopic(e.target.value)}
              />
            </div>
          )}

          <div className="form-group">
            <label className="label" htmlFor="quiz-n-questions">
              Soru Sayısı: <strong style={{ color: 'var(--teal)' }}>{n}</strong>
            </label>
            <input
              id="quiz-n-questions"
              type="range"
              min={5} max={50} step={5}
              value={n}
              onChange={e => setN(Number(e.target.value))}
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
              <span>5</span><span>50</span>
            </div>
          </div>

          {error && <div className="alert alert-error" style={{ marginBottom: 16 }}>⚠️ {error}</div>}

          <button
            id="quiz-start-btn"
            className="btn btn-primary"
            onClick={start}
            disabled={loading}
            style={{ width: '100%', justifyContent: 'center' }}
          >
            {loading ? <><div className="spinner" style={{ width: 18, height: 18 }} /> Yükleniyor…</> : '🚀 Quiz\'i Başlat'}
          </button>
        </div>
      </div>
    </div>
  )
}


// ── Soru ekranı ──────────────────────────────────────────────────────────────
function QuestionScreen({ session, onFinish }) {
  const [current, setCurrent]     = useState(session)
  const [selected, setSelected]   = useState(null)
  const [feedback, setFeedback]   = useState(null)   // { dogru_mu, correct_index, aciklama }
  const [loading, setLoading]     = useState(false)
  const [error, setError]         = useState('')

  const total    = current.total
  const idx      = current.current_index
  const progress = ((idx) / total) * 100
  const q        = current.question

  const submit = async () => {
    if (selected === null) return
    setLoading(true)
    setError('')
    try {
      const data = await quizAnswer(current.session_id, selected)
      setFeedback(data.result)
      if (data.finished) {
        setTimeout(() => onFinish(data.score), 1400)
      } else {
        setTimeout(() => {
          setCurrent(prev => ({ ...prev, ...data, current_index: data.current_index }))
          setSelected(null)
          setFeedback(null)
        }, 1400)
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const getOptionClass = (i) => {
    if (!feedback) return selected === i ? 'option-btn selected' : 'option-btn'
    if (i === feedback.correct_index) return 'option-btn correct'
    if (i === selected && !feedback.dogru_mu) return 'option-btn wrong'
    return 'option-btn'
  }

  return (
    <div className="page">
      <div className="quiz-progress">
        <div className="quiz-progress-bar" style={{ width: `${progress}%` }} />
      </div>

      <div className="quiz-question-card card">
        <div className="question-meta">
          <span className="badge badge-gold">Soru {idx + 1} / {total}</span>
          {q.ders  && <span className="badge" style={{ background: 'var(--surface-2)', color: 'var(--text-dim)', border: '1px solid var(--border)' }}>{q.ders}</span>}
          {q.konu  && <span className="badge" style={{ background: 'var(--surface-2)', color: 'var(--text-dim)', border: '1px solid var(--border)' }}>{q.konu}</span>}
        </div>

        <p className="question-text">{q.question}</p>

        <div className="options-list">
          {(q.options || []).map((opt, i) => (
            <button
              key={i}
              id={`option-${i}`}
              className={getOptionClass(i)}
              onClick={() => !feedback && setSelected(i)}
              disabled={!!feedback || loading}
            >
              <span className="option-letter">{LETTERS[i]}</span>
              {opt}
            </button>
          ))}
        </div>

        {feedback && (
          <div className={`alert ${feedback.dogru_mu ? 'alert-success' : 'alert-error'} fade-up`} style={{ marginBottom: 16 }}>
            {feedback.dogru_mu ? '✅ Doğru!' : '❌ Yanlış!'}{' '}
            {feedback.aciklama && <span style={{ opacity: 0.85 }}>{feedback.aciklama}</span>}
          </div>
        )}

        {error && <div className="alert alert-error" style={{ marginBottom: 12 }}>⚠️ {error}</div>}

        <button
          id="quiz-submit-btn"
          className="btn btn-primary"
          onClick={submit}
          disabled={selected === null || !!feedback || loading}
        >
          {loading ? <><div className="spinner" style={{ width: 18, height: 18 }} /> Kontrol ediliyor…</> : 'Cevabı Gönder →'}
        </button>
      </div>
    </div>
  )
}


// ── Skor ekranı ───────────────────────────────────────────────────────────────
function ScoreScreen({ score, onRestart }) {
  const pct = score.total > 0 ? Math.round((score.score / score.total) * 100) : 0
  const color = pct >= 70 ? '#1a8a4a' : pct >= 40 ? '#d68910' : '#c0392b'

  return (
    <div className="page" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
      <div className="quiz-score-card card fade-up">
        <div style={{ fontSize: 48, marginBottom: 16 }}>🏆</div>
        <h2 style={{ fontSize: 22, fontWeight: 800, marginBottom: 8 }}>Quiz Tamamlandı!</h2>
        <p style={{ color: 'var(--text-dim)', fontSize: 14, marginBottom: 28 }}>Sonuçlarınız kaydedildi.</p>

        <div className="score-ring" style={{ borderColor: color }}>
          <div className="score-number" style={{ color }}>{score.score}</div>
          <div className="score-label">/ {score.total}</div>
        </div>

        <div style={{ fontSize: 32, fontWeight: 800, color, marginBottom: 8 }}>%{pct}</div>
        <p style={{ color: 'var(--text-dim)', fontSize: 14, marginBottom: 28 }}>
          {pct >= 70 ? '🎉 Harika bir performans!' : pct >= 40 ? '📚 Çalışmaya devam edin.' : '💪 Daha fazla pratik gerekli.'}
        </p>

        <button
          id="quiz-restart-btn"
          className="btn btn-primary"
          onClick={onRestart}
          style={{ width: '100%', justifyContent: 'center' }}
        >
          🔄 Yeni Quiz Başlat
        </button>
      </div>
    </div>
  )
}


// ── Ana bileşen ───────────────────────────────────────────────────────────────
export default function QuizPage({ profile }) {
  const [phase, setPhase]     = useState('setup')   // setup | question | score
  const [session, setSession] = useState(null)
  const [score, setScore]     = useState(null)

  const handleStart = (data) => {
    setSession(data)
    setPhase('question')
  }

  const handleFinish = (s) => {
    setScore(s)
    setPhase('score')
  }

  const handleRestart = () => {
    setSession(null)
    setScore(null)
    setPhase('setup')
  }

  if (phase === 'setup')    return <SetupForm onStart={handleStart} profile={profile} />
  if (phase === 'question') return <QuestionScreen session={session} onFinish={handleFinish} />
  if (phase === 'score')    return <ScoreScreen score={score} onRestart={handleRestart} />
}
