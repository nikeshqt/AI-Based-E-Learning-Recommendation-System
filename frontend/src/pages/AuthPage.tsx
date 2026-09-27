import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Sparkles, Lock, Mail, User, Target, LogIn, UserPlus } from 'lucide-react';

export const AuthPage: React.FC = () => {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<'login' | 'register'>('login');

  // Form fields
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [careerGoal, setCareerGoal] = useState('Cybersecurity Analyst');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // Status & error handling
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side validations
    if (!email.trim() || !password.trim()) {
      setError('Please provide both email and password.');
      return;
    }

    if (mode === 'register') {
      if (!fullName.trim()) {
        setError('Full Name is required for registration.');
        return;
      }
      if (password !== confirmPassword) {
        setError('Passwords do not match. Please verify your password entry.');
        return;
      }
      if (password.length < 6) {
        setError('Password must be at least 6 characters long.');
        return;
      }
    }

    try {
      setLoading(true);
      if (mode === 'login') {
        await login(email.trim(), password);
      } else {
        await register(fullName.trim(), email.trim(), password, careerGoal);
      }
    } catch (err: any) {
      console.error('Auth submit error:', err);
      setError(err.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center p-4 font-sans text-[#0F172A]">
      <div className="w-full max-w-md bg-[#FFFFFF] border border-[#E2E8F0] rounded-xl p-8 shadow-sm space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center p-3 bg-indigo-50 border border-indigo-100 rounded-xl text-[#4F46E5] mb-1">
            <Sparkles className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold text-[#0F172A] tracking-tight">NeuralLearn AI</h1>
          <p className="text-xs text-[#64748B]">
            AI-Powered Personalized E-Learning Platform
          </p>
        </div>

        {/* Mode Toggle Tabs */}
        <div className="grid grid-cols-2 p-1 bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg text-xs font-semibold">
          <button
            type="button"
            onClick={() => {
              setMode('login');
              setError(null);
            }}
            className={`py-2 rounded-md transition-colors flex items-center justify-center space-x-1.5 ${
              mode === 'login'
                ? 'bg-[#FFFFFF] text-[#4F46E5] shadow-xs'
                : 'text-[#64748B] hover:text-[#0F172A]'
            }`}
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </button>
          <button
            type="button"
            onClick={() => {
              setMode('register');
              setError(null);
            }}
            className={`py-2 rounded-md transition-colors flex items-center justify-center space-x-1.5 ${
              mode === 'register'
                ? 'bg-[#FFFFFF] text-[#4F46E5] shadow-xs'
                : 'text-[#64748B] hover:text-[#0F172A]'
            }`}
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Register</span>
          </button>
        </div>

        {/* Error Alert Box */}
        {error && (
          <div className="p-3.5 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg font-medium">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {mode === 'register' && (
            <div>
              <label className="block text-[#475569] font-medium mb-1.5">Full Name *</label>
              <div className="relative">
                <User className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" />
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g. Nikeshwaran R"
                  className="w-full pl-9 pr-3 py-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg text-[#0F172A] focus:outline-none focus:border-[#4F46E5]"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-[#475569] font-medium mb-1.5">Email Address *</label>
            <div className="relative">
              <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@example.com"
                className="w-full pl-9 pr-3 py-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg text-[#0F172A] focus:outline-none focus:border-[#4F46E5]"
              />
            </div>
          </div>

          {mode === 'register' && (
            <div>
              <label className="block text-[#475569] font-medium mb-1.5">Target Career Goal</label>
              <div className="relative">
                <Target className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" />
                <select
                  value={careerGoal}
                  onChange={(e) => setCareerGoal(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg text-[#0F172A] focus:outline-none focus:border-[#4F46E5]"
                >
                  <option value="Cybersecurity Analyst">Cybersecurity Analyst</option>
                  <option value="Data Scientist & AI Specialist">Data Scientist & AI Specialist</option>
                  <option value="Full-Stack Web Developer">Full-Stack Web Developer</option>
                  <option value="Cloud Security Engineer">Cloud Security Engineer</option>
                </select>
              </div>
            </div>
          )}

          <div>
            <label className="block text-[#475569] font-medium mb-1.5">Password *</label>
            <div className="relative">
              <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg text-[#0F172A] focus:outline-none focus:border-[#4F46E5]"
              />
            </div>
          </div>

          {mode === 'register' && (
            <div>
              <label className="block text-[#475569] font-medium mb-1.5">Confirm Password *</label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" />
                <input
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-9 pr-3 py-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-lg text-[#0F172A] focus:outline-none focus:border-[#4F46E5]"
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-[#4F46E5] hover:bg-[#4338CA] text-white font-semibold rounded-lg transition-colors flex items-center justify-center space-x-2 text-xs shadow-sm mt-2"
          >
            {loading ? (
              <span>Processing...</span>
            ) : mode === 'login' ? (
              <span>Sign In to Dashboard</span>
            ) : (
              <span>Create Student Account</span>
            )}
          </button>
        </form>

        <div className="pt-2 text-center text-[11px] text-[#64748B] border-t border-[#E2E8F0]">
          <span>PostgreSQL RecSys v2.0 • Secured JWT Token Auth</span>
        </div>
      </div>
    </div>
  );
};
