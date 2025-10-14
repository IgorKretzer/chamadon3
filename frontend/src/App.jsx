import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import HomePage from './pages/HomePage'
import DashboardPage from './pages/DashboardPage'
import { BarChart3, Home, Moon, Sun } from 'lucide-react'

function App() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'dark'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  return (
    <Router>
      <div className="app">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <h1 className="header-title">IA Chamados Sponte</h1>
            <nav className="header-nav">
              <Link to="/" className="nav-link">
                <Home size={20} />
                Análise
              </Link>
              <Link to="/dashboard" className="nav-link">
                <BarChart3 size={20} />
                Dashboard
              </Link>
              <button onClick={toggleTheme} className="theme-toggle" title={`Mudar para modo ${theme === 'dark' ? 'claro' : 'escuro'}`}>
                {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
              </button>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>IA Chamados Sponte - v1.0.0 | Desenvolvido para N3 Suporte</p>
        </footer>
      </div>
    </Router>
  )
}

export default App

