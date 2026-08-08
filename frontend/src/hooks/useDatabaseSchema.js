import { useState, useEffect, useCallback } from 'react';
import databaseService from '../services/databaseService';

/**
 * Custom hook to fetch and manage the database schema state.
 */
export const useDatabaseSchema = () => {
  const [schemaData, setSchemaData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSchema = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await databaseService.getSchema();
      if (response && response.success) {
        setSchemaData(response.data);
      } else {
        throw new Error("Failed to load schema data.");
      }
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch schema once on mount
  useEffect(() => {
    fetchSchema();
  }, [fetchSchema]);

  return {
    schemaData,
    isLoading,
    error,
    refetch: fetchSchema
  };
};
