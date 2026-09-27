import { useState } from 'react';
import { Header } from './components/common/Header';
import { Sidebar } from './components/common/Sidebar';
import { Footer } from './components/common/Footer';
import { DashboardPage } from './pages/DashboardPage';
import { SkillAssessmentPage } from './pages/SkillAssessmentPage';
import { SkillGapPage } from './pages/SkillGapPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { LearningPathPage } from './pages/LearningPathPage';
import { CoursesPage } from './pages/CoursesPage';
import { CourseLearningPage } from './pages/CourseLearningPage';
import { ProgressPage } from './pages/ProgressPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';
import { AuthPage } from './pages/AuthPage';
import { AITutorChat } from './components/ai-tutor/AITutorChat';
import { CourseDetailModal } from './components/courses/CourseDetailModal';
import { AuthProvider, useAuth } from './context/AuthContext';
import type { Course } from './types/course';

function AppContent() {
  const { isAuthenticated, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [activeCourseId] = useState<string>('crs_sec_04');

  const sampleModalCourse: Course = {
    course_id: 'crs_sec_03',
    title: 'Cybersecurity Fundamentals: Network Defense & Wireshark',
    description: 'Learn packet inspection, intrusion detection systems, and network vulnerability analysis.',
    instructor_name: 'Sarah Connor',
    thumbnail_url: '',
    category: 'Cybersecurity',
    difficulty_level: 'Intermediate',
    duration_hours: 8.0,
    rating: 4.9,
    enrolled_count: 3100,
    prerequisites: ['Networking', 'Linux'],
    skills_taught: ['Networking', 'Cybersecurity', 'Wireshark'],
    lessons: [
      { lesson_id: 'lsn_1', title: 'Introduction to OSI & TCP/IP Layer Security', duration_minutes: 25, is_completed: true },
      { lesson_id: 'lsn_2', title: 'Packet Capture & Inspection with Wireshark', duration_minutes: 45, is_completed: false },
      { lesson_id: 'lsn_3', title: 'Firewall Rule Configuration & Network ACLs', duration_minutes: 35, is_completed: false },
    ],
  };

  const handleSelectCourse = () => {
    setSelectedCourse(sampleModalCourse);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center p-6 font-sans">
        <div className="flex items-center space-x-3 text-[#64748B]">
          <div className="w-5 h-5 border-2 border-[#4F46E5] border-t-transparent rounded-full animate-spin"></div>
          <span className="font-medium text-sm">Authenticating session...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthPage />;
  }

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <DashboardPage
            onSelectCourse={handleSelectCourse}
            onNavigateToSkillGaps={() => setActiveTab('skill-gaps')}
            onNavigateToLearningPath={() => setActiveTab('learning-path')}
          />
        );
      case 'assessment':
        return <SkillAssessmentPage onNavigateToRecommendations={() => setActiveTab('recommendations')} />;
      case 'skill-gaps':
        return <SkillGapPage onNavigateToRecommendations={() => setActiveTab('recommendations')} />;
      case 'recommendations':
        return <RecommendationsPage onSelectCourse={handleSelectCourse} />;
      case 'learning-path':
        return <LearningPathPage />;
      case 'courses':
        return <CoursesPage onSelectCourse={handleSelectCourse} />;
      case 'learn':
        return (
          <CourseLearningPage
            courseId={activeCourseId}
            onBack={() => setActiveTab('dashboard')}
          />
        );
      case 'progress':
        return <ProgressPage />;
      case 'analytics':
        return <AnalyticsPage />;
      case 'ai-tutor':
        return (
          <div className="max-w-2xl mx-auto">
            <AITutorChat />
          </div>
        );
      case 'settings':
        return <SettingsPage />;
      default:
        return (
          <DashboardPage
            onSelectCourse={handleSelectCourse}
            onNavigateToSkillGaps={() => setActiveTab('skill-gaps')}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col p-4 md:p-6 max-w-[1600px] mx-auto font-sans">
      <Header activeTab={activeTab} />
      <div className="flex-1 flex gap-6">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="flex-1 overflow-y-auto">
          {renderActiveTab()}
        </main>
      </div>
      <Footer />
      <CourseDetailModal course={selectedCourse} onClose={() => setSelectedCourse(null)} />
    </div>
  );
}

export function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
