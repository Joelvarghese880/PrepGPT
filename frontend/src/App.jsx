import { useChat } from './hooks/useChat'
import ChatWindow from './components/ChatWindow'
import InputBox from './components/InputBox'

export default function App() {
  const { messages, isLoading, error, ask } = useChat()

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-mark" aria-hidden="true" />
        <div>
          <h1 className="app-title">PrepGPT</h1>
          <p className="app-subtitle">RAG-grounded interview prep · DSA · OOP · SQL · DBMS · OS · CN</p>
        </div>
      </header>

      <main className="app-main">
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}
          onPickTopic={(prompt) => ask(prompt)}
        />
      </main>

      <footer className="app-footer">
        <InputBox onSend={ask} disabled={isLoading} />
      </footer>
    </div>
  )
}