import { Menu, Bot } from 'lucide-react';
import { useLayout } from '../../context/LayoutContext';

const MobileHeader = () => {
  const { toggleMobileMenu } = useLayout();
  
  return (
    <header className="mobile-header">
      <button className="hamburger-btn" onClick={toggleMobileMenu} aria-label="Open Menu">
        <Menu size={24} />
      </button>
      <div className="mobile-logo">
        <Bot size={20} className="mobile-bot-icon" />
        <span className="mobile-title">SQL Agent</span>
      </div>
      <div style={{ width: 24 }}></div> {/* Spacer for centering the logo */}
    </header>
  );
};

export default MobileHeader;
