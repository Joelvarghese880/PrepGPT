import { useState, useRef } from 'react'
import { sendMessage } from '../api/chatApi'

// One session ID per browser tab load — keeps this conversation's memory
// separate from any other session on the backend.
function makeSessionId() {
  return crypto.randomUUID()
}

export function useChat() {
  const sessionId = useRef(makeSessionId())
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  async function ask(question) {
    if (!question.trim() || isLoading) return

    const userMsg = { role: 'user', content: question }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)
    setError(null)

    try {
      const result = await sendMessage(question, sessionId.current)
      const botMsg = {
        role: 'assistant',
        content: result.answer,
        sources: result.sources || [],
      }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      setError(err.message || 'Something went wrong. Is the backend running?')
    } finally {
      setIsLoading(false)
    }
  }

  return { messages, isLoading, error, ask }
}