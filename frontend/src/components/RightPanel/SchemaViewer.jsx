import { useState } from 'react';
import { Database, Table, Key, Type, ChevronRight, ChevronDown, Loader, AlertCircle } from 'lucide-react';
import { useDatabaseSchema } from '../../hooks/useDatabaseSchema';
import './SchemaViewer.css';

const SchemaViewer = () => {
  const { schemaData, isLoading, error } = useDatabaseSchema();
  const [expandedTables, setExpandedTables] = useState({});

  const toggleTable = (tableName) => {
    setExpandedTables(prev => ({
      ...prev,
      [tableName]: !prev[tableName]
    }));
  };

  if (isLoading) {
    return (
      <div className="schema-state-container">
        <Loader className="schema-spinner" size={24} />
        <p>Loading schema...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="schema-state-container error">
        <AlertCircle size={24} />
        <p>{error}</p>
      </div>
    );
  }

  if (!schemaData || schemaData.length === 0) {
    return (
      <div className="schema-state-container">
        <Database size={24} />
        <p>No tables found.</p>
      </div>
    );
  }

  return (
    <div className="schema-viewer">
      <div className="schema-summary">
        <Database size={16} />
        <span>{schemaData.length} Tables</span>
      </div>
      
      <div className="schema-tables-list">
        {schemaData.map((table) => (
          <div key={table.table_name} className="schema-table-item">
            <div 
              className={`schema-table-header ${expandedTables[table.table_name] ? 'expanded' : ''}`}
              onClick={() => toggleTable(table.table_name)}
            >
              <div className="schema-table-header-left">
                {expandedTables[table.table_name] ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                <Table size={16} className="table-icon" />
                <span className="table-name">{table.table_name}</span>
              </div>
              <span className="column-count">{table.columns.length} cols</span>
            </div>
            
            {expandedTables[table.table_name] && (
              <div className="schema-columns-list">
                {table.columns.map((col) => (
                  <div key={col.name} className="schema-column-item">
                    <div className="schema-column-left">
                      {col.is_primary_key ? (
                        <Key size={14} className="icon-pk" title="Primary Key" />
                      ) : (
                        <Type size={14} className="icon-type" />
                      )}
                      <span className={`column-name ${col.is_primary_key ? 'pk-text' : ''}`}>
                        {col.name}
                      </span>
                    </div>
                    <span className="column-type">{col.type}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SchemaViewer;
