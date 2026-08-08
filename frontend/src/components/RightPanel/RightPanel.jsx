import { X } from 'lucide-react';
import { useLayout } from '../../context/LayoutContext';
import SchemaViewer from './SchemaViewer';
import './RightPanel.css';

const RightPanel = () => {
  const { isRightSidebarOpen, closeRightSidebar } = useLayout();

  return (
    <aside className={`right-panel ${!isRightSidebarOpen ? 'closed' : ''}`}>
      <div className="right-panel-header">
        <h2 className="right-panel-title">Database Explorer</h2>
        <button className="close-btn" onClick={closeRightSidebar} title="Close Panel">
          <X size={20} />
        </button>
      </div>

      <div className="panel-card">
        <h3 className="panel-title">Connection Info</h3>
        <p className="placeholder-text">Status: 🟢 Connected</p>
        <p className="placeholder-text">Type: SQLite</p>
      </div>

      <div className="panel-card">
        <h3 className="panel-title">Database Schema</h3>
        <SchemaViewer />
      </div>
      
      <div className="panel-card">
        <h3 className="panel-title">Quick Actions</h3>
        <p className="placeholder-text">Action buttons (Export, Run, Chart) will appear here...</p>
      </div>
    </aside>
  );
};

export default RightPanel;
