import { Routes, Route } from 'react-router-dom'
import { useTheme } from './context/ThemeContext'
import { useLayout } from './context/LayoutContext'
import Sidebar from './components/Sidebar/Sidebar'
import RightPanel from './components/RightPanel/RightPanel'
import MobileHeader from './components/Navbar/MobileHeader'
import Chat from './pages/Chat'
import './styles/layout.css'

// Future pages
const Settings = () => <div style={{ padding: '2rem' }}><h1>Settings</h1><p>Settings interface will be built here...</p></div>

function App() {
  const { theme } = useTheme();
  const { isMobileMenuOpen, closeMobileMenu } = useLayout();

  return (
    <div className={`app-layout ${theme}`}>
      {/* Mobile Overlay backdrop */}
      {isMobileMenuOpen && (
        <div className="mobile-overlay" onClick={closeMobileMenu}></div>
      )}

      <Sidebar />
      
      <main className="main-workspace">
        <MobileHeader />
        <Routes>
          <Route path="/" element={<Chat />} />
          <Route path="/settings" element={<Settings />} />
          {/* Catch-all for undefined routes during development */}
          <Route path="*" element={<Chat />} />
        </Routes>
      </main>

      <RightPanel />
    </div>
  )
}

export default App
