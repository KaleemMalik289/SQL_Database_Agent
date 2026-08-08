import { NavLink, useNavigate } from 'react-router-dom';
import { 
  MessageSquare, 
  History, 
  Database, 
  BarChart2, 
  Settings, 
  Moon, 
  Sun,
  Bot,
  PanelLeftClose,
  PanelLeftOpen
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useLayout } from '../../context/LayoutContext';
import './Sidebar.css';

const Sidebar = () => {
  const { theme, toggleTheme } = useTheme();
  const { 
    isLeftSidebarOpen, 
    toggleLeftSidebar, 
    openRightSidebar,
    isMobileMenuOpen,
    closeMobileMenu
  } = useLayout();
  const navigate = useNavigate();

  const navItems = [
    { id: 'chat', label: 'New Chat', icon: MessageSquare, path: '/' },
    { id: 'history', label: 'History', icon: History, path: '/history' },
    { id: 'analytics', label: 'Analytics', icon: BarChart2, path: '/analytics' },
    { id: 'settings', label: 'Settings', icon: Settings, path: '/settings' },
  ];

  const handleDatabaseClick = () => {
    openRightSidebar();
    navigate('/databases');
    closeMobileMenu(); // Auto close sidebar on mobile when navigating
  };

  const handleNavClick = () => {
    closeMobileMenu(); // Auto close sidebar on mobile when navigating
  };

  // Compute classes for desktop collapse and mobile slide-in
  const sidebarClasses = [
    'sidebar',
    !isLeftSidebarOpen ? 'collapsed' : '',
    isMobileMenuOpen ? 'mobile-open' : ''
  ].filter(Boolean).join(' ');

  return (
    <aside className={sidebarClasses}>
      <div className="sidebar-header">
        <div className="logo-section">
          <div className="logo-container">
            <Bot size={20} />
          </div>
          {(isLeftSidebarOpen || isMobileMenuOpen) && <div className="app-title">AI SQL Agent</div>}
        </div>
        
        {/* Toggle button hidden on mobile, since mobile uses overlay */}
        <button className="toggle-btn desktop-only" onClick={toggleLeftSidebar} title={isLeftSidebarOpen ? "Close Sidebar" : "Open Sidebar"}>
          {isLeftSidebarOpen ? <PanelLeftClose size={20} /> : <PanelLeftOpen size={20} />}
        </button>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink 
            key={item.id} 
            to={item.path}
            onClick={handleNavClick}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            title={(!isLeftSidebarOpen && !isMobileMenuOpen) ? item.label : ""}
          >
            <item.icon className="nav-icon" />
            {(isLeftSidebarOpen || isMobileMenuOpen) && <span>{item.label}</span>}
          </NavLink>
        ))}
        
        <button 
          className="nav-item" 
          onClick={handleDatabaseClick}
          title={(!isLeftSidebarOpen && !isMobileMenuOpen) ? "Databases" : ""}
        >
          <Database className="nav-icon" />
          {(isLeftSidebarOpen || isMobileMenuOpen) && <span>Databases</span>}
        </button>
      </nav>

      <div className="sidebar-footer">
        <button className="theme-toggle" onClick={toggleTheme} title={(!isLeftSidebarOpen && !isMobileMenuOpen) ? "Toggle Theme" : ""}>
          {theme === 'dark' ? <Sun className="nav-icon" /> : <Moon className="nav-icon" />}
          {(isLeftSidebarOpen || isMobileMenuOpen) && <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>}
        </button>

        <div className="profile-card" title={(!isLeftSidebarOpen && !isMobileMenuOpen) ? "Profile" : ""}>
          <div className="avatar">KM</div>
          {(isLeftSidebarOpen || isMobileMenuOpen) && (
            <div className="profile-info">
              <span className="profile-name">Kaleem Malik</span>
              <span className="profile-role">AI Engineer</span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
