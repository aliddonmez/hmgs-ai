import { useEffect, useRef, useState } from 'react'
import { chatAsk } from '../api'

const EXAMPLE_QUESTIONS = [
  'Hırsızlık suçunda ceza miktarı nedir?',
  'Yağma suçu nedir ?',
  'Kasten yaralama ile taksirle yaralama farkı nedir ? ',
  'Velayet hakkı nasıl değiştirilir?',
]

function TypingDots() {
  return (
    <div className="bubble bubble-bot" style={{ padding: '12px 16px' }}>
      <div className="typing-dots">
        <span /><span /><span />
      </div>
    </div>
  )
}

function Bubble({ role, content }) {
  return (
    <div className={`bubble-row ${role}`}>
      <div className={`avatar avatar-${role === 'user' ? 'user' : 'bot'}`}>
        {role === 'user' ? '👤' : '⚖️'}
      </div>
      <div className={`bubble bubble-${role === 'user' ? 'user' : 'bot'}`}>
        {content}
      </div>
    </div>
  )
}

export default function ChatPage() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const send = async (question) => {
    const q = (question || input).trim()
    if (!q || loading) return

    setMessages(prev => [...prev, { role: 'user', content: q }])
    setInput('')
    setLoading(true)

    try {
      const data = await chatAsk(q)
      const answer =
        data.type === 'no_answer'
          ? data.text
          : data.text || 'Yanıt alınamadı.'
      setMessages(prev => [...prev, { role: 'assistant', content: answer }])
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: '⚠️ Sunucuya bağlanılamadı. Backend çalışıyor mu?' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <div className="page" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="page-header">
        <h1>Hukuki Asistan</h1>
        <p>Hukuki sorularınızı sorun, belgelerden destekli cevaplar alın.</p>
      </div>

      <div className="chat-wrap" style={{ flex: 1, minHeight: 0 }}>
        <div className="chat-messages">
          {messages.length === 0 && !loading && (
            <div className="chat-empty fade-up">
              <div className="empty-icon">⚖️</div>
              <h2>HMGS Hukuki Asistan</h2>
              <p>Hukuki metinlere dayalı sorularınızı yanıtlıyorum. Bir konudan başlayın:</p>
              <div className="chat-chips">
                {EXAMPLE_QUESTIONS.map(q => (
                  <button key={q} className="chip" onClick={() => send(q)}>{q}</button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <Bubble key={i} role={m.role} content={m.content} />
          ))}

          {loading && (
            <div className="bubble-row">
              <div className="avatar avatar-bot">⚖️</div>
              <TypingDots />
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="chat-input-bar">
          <textarea
            ref={textareaRef}
            id="chat-input"
            rows={1}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Hukuki sorunuzu yazın… (Enter: gönder, Shift+Enter: yeni satır)"
            disabled={loading}
          />
          <button
            id="chat-send-btn"
            className="send-btn"
            onClick={() => send()}
            disabled={!input.trim() || loading}
            title="Gönder"
          >
            {loading ? <div className="spinner" style={{ width: 20, height: 20 }} /> : '➤'}
          </button>
        </div>
      </div>
    </div>
  )
}
