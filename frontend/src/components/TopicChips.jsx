const TOPICS = [
  { label: 'DSA', prompt: 'Explain a common DSA pattern I should know.' },
  { label: 'OOP', prompt: 'Explain polymorphism with an example.' },
  { label: 'SQL', prompt: 'What is the difference between primary key and foreign key?' },
  { label: 'DBMS', prompt: 'What is database normalization?' },
  { label: 'OS', prompt: 'Explain the difference between process and thread.' },
  { label: 'CN', prompt: 'Explain the TCP three-way handshake.' },
]

export default function TopicChips({ onPick, disabled }) {
  return (
    <div className="topic-chips">
      {TOPICS.map((t) => (
        <button
          key={t.label}
          className="topic-chip"
          onClick={() => onPick(t.prompt)}
          disabled={disabled}
        >
          <span className="topic-chip-fold" aria-hidden="true" />
          {t.label}
        </button>
      ))}
    </div>
  )
}