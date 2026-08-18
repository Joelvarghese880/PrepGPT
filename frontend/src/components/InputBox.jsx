import { useState, useRef } from 'react'

export default function InputBox({ onSend, disabled }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)

  function handleSubmit(e) {
    e.preventDefault()
    if (!value.trim() || disabled) return
    onSend(value)
    setValue('')
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  function handleChange(e) {
    setValue(e.target.value)
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = `${Math.min(el.scrollHeight, 160)}px`
    }
  }

  return (
    <form className="input-bar" onSubmit={handleSubmit}>
      <textarea
        ref={textareaRef}
        className="input-textarea"
        placeholder="Ask about DSA, OOP, SQL, DBMS, OS, or networking..."
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        rows={1}
        disabled={disabled}
      />
      <button
        type="submit"
        className="send-button"
        disabled={disabled || !value.trim()}
        aria-label="Send message"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M4 12L20 4L14 20L11 13L4 12Z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
        </svg>
      </button>
    </form>
  )
}