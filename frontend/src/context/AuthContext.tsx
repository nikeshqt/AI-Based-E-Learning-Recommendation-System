import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { UserProfile } from '../types/user';
import { apiClient } from '../services/api';

interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (fullName: string, email: string, password: string, learningGoal?: string) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [loading, setLoading] = useState<boolean>(true);

  const fetchCurrentUser = async (authToken?: string) => {
    const activeToken = authToken || localStorage.getItem('token');
    if (!activeToken) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const response = await apiClient.get<UserProfile>('/auth/me', {
        headers: { Authorization: `Bearer ${activeToken}` },
      });
      setUser(response.data);
      setToken(activeToken);
    } catch (err) {
      console.error('Failed to fetch authenticated student profile:', err);
      localStorage.removeItem('token');
      setToken(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const res = await apiClient.post<{ access_token: string; user_id: string }>('/auth/login', {
        email,
        password,
      });
      const newToken = res.data.access_token;
      localStorage.setItem('token', newToken);
      setToken(newToken);
      await fetchCurrentUser(newToken);
    } catch (err: any) {
      setLoading(false);
      const msg = err?.response?.data?.detail || 'Invalid email or password.';
      throw new Error(msg);
    }
  };

  const register = async (
    fullName: string,
    email: string,
    password: string,
    learningGoal = 'Cybersecurity Analyst'
  ) => {
    setLoading(true);
    try {
      await apiClient.post('/auth/register', {
        full_name: fullName,
        email,
        password,
        learning_goal: learningGoal,
      });
      // Automatically login after registration
      await login(email, password);
    } catch (err: any) {
      setLoading(false);
      const msg = err?.response?.data?.detail || 'Registration failed. Email may already be registered.';
      throw new Error(msg);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const refreshProfile = async () => {
    await fetchCurrentUser();
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!user && !!token,
        login,
        register,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
