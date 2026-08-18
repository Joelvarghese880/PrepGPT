import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function formatSourceName(path) {
  // "interview_prep_docs\\dsa_patterns.md" -> "DSA Patterns"
  const filename = path.split(/[\\/]/).pop().replace('.md', '')
  return filename
    .split('_')
    .map((w) => w.toUpperCase() === w ? w : w[0].toUpperCase() + w.slice(1))
    .join(' ')
}

export default function MessageBubble({ role, content, sources }) {
  const isUser = role === 'user'

  return (
    <div className={`message-row ${isUser ? 'message-row-user' : ''}`}>
      <div className={`message-bubble ${isUser ? 'message-bubble-user' : 'message-bubble-bot'}`}>
        {isUser ? (
          <p className="message-text">{content}</p>
        ) : (
          <div className="markdown-content">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          </div>
        )}

        {!isUser && sources && sources.length > 0 && (
          <div className="source-panel">
            <span className="source-panel-label">Grounded in</span>
            <div className="source-chips">
              {sources.map((s, i) => (
                <span key={i} className="source-chip" title={s.preview}>
                  {formatSourceName(s.source)}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}