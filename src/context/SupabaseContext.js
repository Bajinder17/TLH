import React, { createContext, useContext } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

const supabase = createClient(supabaseUrl, supabaseAnonKey);

const SupabaseContext = createContext();

export function SupabaseProvider({ children }) {
  const saveReport = async (scanType, data) => {
    try {
      const { data: report, error } = await supabase
        .from('reports')
        .insert([{ 
          scan_type: scanType, 
          scan_data: data, 
          created_at: new Date().toISOString() 
        }]);
        
      if (error) throw error;
      return report;
    } catch (error) {
      console.error('Error saving report:', error);
      throw error;
    }
  };

  const getReports = async () => {
    try {
      const { data, error } = await supabase
        .from('reports')
        .select('*')
        .order('created_at', { ascending: false });
        
      if (error) throw error;
      return data;
    } catch (error) {
      console.error('Error fetching reports:', error);
      throw error;
    }
  };

  const value = {
    supabase,
    saveReport,
    getReports
  };

  return (
    <SupabaseContext.Provider value={value}>
      {children}
    </SupabaseContext.Provider>
  );
}

export function useSupabase() {
  const context = useContext(SupabaseContext);
  if (context === undefined) {
    throw new Error('useSupabase must be used within a SupabaseProvider');
  }
  return context;
}
