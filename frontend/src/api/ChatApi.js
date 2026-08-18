const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function sendMessage(question, sessionId) {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, session_id: sessionId }),
  })

  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`Request failed (${res.status}): ${detail}`)
  }

  return res.json() // { answer, sources: [{ source, preview }] }
}