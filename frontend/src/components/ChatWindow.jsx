import { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'
import TopicChips from './TopicChips'

export default function ChatWindow({ messages, isLoading, error, onPickTopic }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const isEmpty = messages.length === 0

  return (
    <div className="chat-window">
      {isEmpty ? (
        <div className="empty-state">
          <p className="empty-state-eyebrow">Open notebook</p>
          <h2 className="empty-state-title">What's on the syllabus tonight?</h2>
          <p className="empty-state-sub">
            Ask about DSA patterns, OOP concepts, SQL, DBMS, OS, or networking —
            or pull a flashcard below to start.
          </p>
          <TopicChips onPick={onPickTopic} disabled={isLoading} />
        </div>
      ) : (
        <div className="message-list">
          {messages.map((m, i) => (
            <MessageBubble key={i} role={m.role} content={m.content} sources={m.sources} />
          ))}

          {isLoading && (
            <div className="message-row">
              <div className="message-bubble message-bubble-bot message-bubble-loading">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            </div>
          )}

          {error && (
            <div className="error-banner">
              {error}
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      )}
    </div>
  )
}