import React, { useState } from 'react';
import { CourseCard } from '../components/courses/CourseCard';
import { Search, Filter, BookOpen } from 'lucide-react';
import type { Course } from '../types/course';

interface CoursesPageProps {
  onSelectCourse?: (courseId: string) => void;
}

const ALL_COURSES: Course[] = [
  {
    course_id: 'crs_gnn_01',
    title: 'Graph Neural Networks for Recommendation Systems',
    description: 'Master LightGCN, PyTorch Geometric, and link prediction for collaborative filtering.',
    instructor_name: 'Dr. Elena Rostova',
    thumbnail_url: '',
    category: 'Artificial Intelligence',
    difficulty_level: 'Advanced',
    duration_hours: 6.5,
    rating: 4.9,
    enrolled_count: 1420,
    prerequisites: ['Python', 'PyTorch'],
    skills_taught: ['LightGCN', 'PyTorch Geometric', 'GNN'],
    lessons: [],
  },
  {
    course_id: 'crs_qdrant_02',
    title: 'Production Vector Search with Qdrant & Milvus',
    description: 'Build fast ANN retrieval engines scaling to millions of embeddings.',
    instructor_name: 'Marcus Vance',
    thumbnail_url: '',
    category: 'Data Engineering',
    difficulty_level: 'Intermediate',
    duration_hours: 4.0,
    rating: 4.8,
    enrolled_count: 2890,
    prerequisites: ['Python'],
    skills_taught: ['Qdrant', 'HNSW', 'ANN Search'],
    lessons: [],
  },
  {
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
    lessons: [],
  },
  {
    course_id: 'crs_py_04',
    title: 'Advanced Python AsyncIO & Performance Tuning',
    description: 'Master async/await, memory management, and high-concurrency server development.',
    instructor_name: 'Guido Van R',
    thumbnail_url: '',
    category: 'Software Engineering',
    difficulty_level: 'Advanced',
    duration_hours: 5.5,
    rating: 4.95,
    enrolled_count: 4200,
    prerequisites: ['Python'],
    skills_taught: ['Python', 'AsyncIO', 'Performance'],
    lessons: [],
  },
];

const CATEGORIES = ['All', 'Cybersecurity', 'Artificial Intelligence', 'Data Engineering', 'Software Engineering'];

export const CoursesPage: React.FC<CoursesPageProps> = ({ onSelectCourse }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const filteredCourses = ALL_COURSES.filter((course) => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      course.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || course.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-indigo-600" />
            Course Catalog
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Explore our curated, skill-indexed course library for technical mastery.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search courses..."
              className="pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:outline-none focus:border-indigo-500 w-56"
            />
          </div>

          <button className="px-3.5 py-2 border border-slate-200 rounded-lg text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 flex items-center gap-1.5">
            <Filter className="w-4 h-4 text-slate-500" /> Filter
          </button>
        </div>
      </div>

      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors shrink-0 ${
              selectedCategory === cat
                ? 'bg-indigo-600 text-white font-semibold'
                : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredCourses.map((course) => (
          <CourseCard key={course.course_id} course={course} onSelect={onSelectCourse} />
        ))}
      </div>
    </div>
  );
};
