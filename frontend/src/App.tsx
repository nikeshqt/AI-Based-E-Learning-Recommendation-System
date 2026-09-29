import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
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

// Admin imports
import { AdminHeader } from './components/admin/AdminHeader';
import { AdminSidebar, type AdminTab } from './components/admin/AdminSidebar';
import { AccessDenied } from './components/admin/AccessDenied';
import { AdminDashboardPage } from './pages/admin/AdminDashboardPage';
import { AdminStudentsPage } from './pages/admin/AdminStudentsPage';
import { AdminStudentDetailPage } from './pages/admin/AdminStudentDetailPage';
import { AdminCoursesPage } from './pages/admin/AdminCoursesPage';
import { AdminProgressPage } from './pages/admin/AdminProgressPage';
import { AdminAnalyticsPage } from './pages/admin/AdminAnalyticsPage';
import { AdminActivityPage } from './pages/admin/AdminActivityPage';
import { ShieldCheck } from 'lucide-react';

function AppContent() {
  const { user, isAuthenticated, loading } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  // Student active tab state
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [activeCourseId] = useState<string>('crs_sec_04');

  // Automatic redirect after admin login
  useEffect(() => {
    if (
      user &&
      user.role === 'admin' &&
      location.pathname === '/' &&
      !location.search.includes('preview=true')
    ) {
      navigate('/admin', { replace: true });
    }
  }, [user, location.pathname, location.search, navigate]);

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

  // Check if current route is an Admin route
  const isAdminRoute = location.pathname.startsWith('/admin');

  // If a student tries to navigate to /admin, show Access Denied
  if (isAdminRoute && user?.role !== 'admin') {
    return (
      <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col p-4 md:p-6 max-w-[1600px] mx-auto font-sans">
        <Header activeTab="dashboard" />
        <AccessDenied onReturnToDashboard={() => navigate('/')} />
        <Footer />
      </div>
    );
  }

  // If user is Admin and is on an admin route
  if (isAdminRoute && user?.role === 'admin') {
    // Determine active admin tab and subroute
    let currentAdminTab: AdminTab = 'dashboard';
    let selectedStudentId: string | null = null;

    if (location.pathname === '/admin' || location.pathname === '/admin/dashboard') {
      currentAdminTab = 'dashboard';
    } else if (location.pathname.startsWith('/admin/students/')) {
      currentAdminTab = 'students';
      selectedStudentId = location.pathname.replace('/admin/students/', '');
    } else if (location.pathname === '/admin/students') {
      currentAdminTab = 'students';
    } else if (location.pathname === '/admin/courses') {
      currentAdminTab = 'courses';
    } else if (location.pathname === '/admin/progress') {
      currentAdminTab = 'progress';
    } else if (location.pathname === '/admin/analytics') {
      currentAdminTab = 'analytics';
    } else if (location.pathname === '/admin/activity') {
      currentAdminTab = 'activity';
    } else if (location.pathname === '/admin/settings') {
      currentAdminTab = 'settings';
    }

    const renderAdminContent = () => {
      if (selectedStudentId) {
        return (
          <AdminStudentDetailPage
            studentId={selectedStudentId}
            onBack={() => navigate('/admin/students')}
          />
        );
      }

      switch (currentAdminTab) {
        case 'dashboard':
          return (
            <AdminDashboardPage
              onNavigateToTab={(tab) => navigate(`/admin/${tab}`)}
            />
          );
        case 'students':
          return (
            <AdminStudentsPage
              onSelectStudent={(id) => navigate(`/admin/students/${id}`)}
            />
          );
        case 'courses':
          return <AdminCoursesPage />;
        case 'progress':
          return <AdminProgressPage />;
        case 'analytics':
          return <AdminAnalyticsPage />;
        case 'activity':
          return <AdminActivityPage />;
        case 'settings':
          return <SettingsPage />;
        default:
          return (
            <AdminDashboardPage
              onNavigateToTab={(tab) => navigate(`/admin/${tab}`)}
            />
          );
      }
    };

    return (
      <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col p-4 md:p-6 max-w-[1600px] mx-auto font-sans">
        <AdminHeader onSwitchToStudentView={() => navigate('/?preview=true')} />
        <div className="flex-1 flex gap-6">
          <AdminSidebar
            activeTab={currentAdminTab}
            setActiveTab={(tab) => {
              if (tab === 'dashboard') navigate('/admin');
              else navigate(`/admin/${tab}`);
            }}
            onSelectStudentId={(id) => {
              if (id) navigate(`/admin/students/${id}`);
              else navigate('/admin/students');
            }}
          />
          <main className="flex-1 overflow-y-auto min-w-0">
            {renderAdminContent()}
          </main>
        </div>
        <Footer />
      </div>
    );
  }

  // Existing Student Views
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
      {/* If admin is previewing student view, show banner to return to admin console */}
      {user?.role === 'admin' && (
        <div className="mb-4 bg-indigo-900 text-white px-4 py-2.5 rounded-xl text-xs flex items-center justify-between shadow-xs">
          <span className="font-medium flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-indigo-300" />
            You are currently previewing the Student Interface as an Administrator.
          </span>
          <button
            onClick={() => navigate('/admin')}
            className="px-3 py-1 bg-white text-indigo-900 font-semibold rounded-lg hover:bg-indigo-50 transition-colors cursor-pointer"
          >
            Return to Admin Console
          </button>
        </div>
      )}

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
