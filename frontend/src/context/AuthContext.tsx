import React, { createContext, useContext, useState, type ReactNode } from 'react';
import type { UserProfile } from '../types/user';

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  login: (email: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>({
    user_id: 'usr_98741',
    full_name: 'Alex Morgan',
    email: 'alex.morgan@ai-learning.io',
    learning_goal: 'Data Science & AI Engineering',
    preferred_learning_style: 'visual',
    skill_level: 'intermediate',
    weekly_goal_hours: 5,
    completed_hours: 4.2,
    streak_days: 12,
    skills: [],
  });

  const login = (email: string) => {
    setUser({
      user_id: 'usr_' + Date.now(),
      full_name: 'Learner User',
      email,
      learning_goal: 'AI & RecSys Architect',
      preferred_learning_style: 'visual',
      skill_level: 'beginner',
      weekly_goal_hours: 5,
      completed_hours: 0,
      streak_days: 1,
      skills: [],
    });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, logout }}>
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
