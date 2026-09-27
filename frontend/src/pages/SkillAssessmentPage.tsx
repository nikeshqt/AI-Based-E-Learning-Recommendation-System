import React, { useState, useEffect } from 'react';
import {
  Code,
  Globe,
  Terminal,
  Shield,
  Brain,
  Database,
  Layout,
  Cloud,
  ArrowRight,
  CheckCircle,
  BarChart2,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import {
  fetchAvailableAssessments,
  fetchAssessmentQuestions,
  submitAssessmentAnswers,
  type QuestionPublic,
  type AssessmentResultData,
} from '../services/assessmentService';

interface Domain {
  id: string;
  name: string;
  description: string;
  questionsCount: number;
  estimatedTime: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  icon: React.ElementType;
}

const DOMAINS: Domain[] = [
  {
    id: 'python',
    name: 'Python',
    description: 'Data structures, OOP, async syntax, list comprehensions, and standard libraries.',
    questionsCount: 5,
    estimatedTime: '10 mins',
    difficulty: 'Intermediate',
    icon: Code,
  },
  {
    id: 'networking',
    name: 'Networking',
    description: 'TCP/IP model, DNS resolution, HTTP/S protocols, subnets, and packet routing.',
    questionsCount: 5,
    estimatedTime: '10 mins',
    difficulty: 'Intermediate',
    icon: Globe,
  },
  {
    id: 'linux',
    name: 'Linux',
    description: 'Bash commands, file permissions, process management, shell scripting, and systemd.',
    questionsCount: 5,
    estimatedTime: '10 mins',
    difficulty: 'Beginner',
    icon: Terminal,
  },
  {
    id: 'cybersecurity',
    name: 'Cybersecurity',
    description: 'OWASP Top 10, cryptography, IAM authentication, vulnerability scanning, and SIEM.',
    questionsCount: 5,
    estimatedTime: '10 mins',
    difficulty: 'Intermediate',
    icon: Shield,
  },
  {
    id: 'ai_ml',
    name: 'AI / Machine Learning',
    description: 'TF-IDF, vector embeddings, loss functions, PyTorch models, and evaluation metrics.',
    questionsCount: 5,
    estimatedTime: '15 mins',
    difficulty: 'Advanced',
    icon: Brain,
  },
  {
    id: 'sql',
    name: 'SQL',
    description: 'Relational queries, JOINs, indexing, window functions, and schema normalization.',
    questionsCount: 5,
    estimatedTime: '10 mins',
    difficulty: 'Intermediate',
    icon: Database,
  },
  {
    id: 'web_dev',
    name: 'Web Development',
    description: 'React, TypeScript, DOM APIs, CSS Grid/Flexbox, and RESTful API architecture.',
    questionsCount: 5,
    estimatedTime: '10 mins',
    difficulty: 'Intermediate',
    icon: Layout,
  },
  {
    id: 'cloud',
    name: 'Cloud Computing',
    description: 'Docker containers, Kubernetes pod deployment, IAM policies, and serverless logic.',
    questionsCount: 5,
    estimatedTime: '10 mins',
    difficulty: 'Intermediate',
    icon: Cloud,
  },
];

interface SkillAssessmentPageProps {
  onNavigateToRecommendations?: () => void;
}

export const SkillAssessmentPage: React.FC<SkillAssessmentPageProps> = ({
  onNavigateToRecommendations,
}) => {
  const [viewState, setViewState] = useState<'landing' | 'quiz' | 'results'>('landing');
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null);
  const [questions, setQuestions] = useState<QuestionPublic[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [resultData, setResultData] = useState<AssessmentResultData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchAvailableAssessments().catch((err) => console.log('Assessments load error:', err));
  }, []);

  const handleStartDomain = async (domain: Domain) => {
    setSelectedDomain(domain);
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token') || undefined;
      const allQuestions = await fetchAssessmentQuestions('asm_tech_eval_01', token);
      // Filter questions for the selected domain if available, or use full set
      const domainQuestions = allQuestions.filter(
        (q) => q.domain.toLowerCase() === domain.name.toLowerCase()
      );
      const activeSet = domainQuestions.length > 0 ? domainQuestions : allQuestions;

      setQuestions(activeSet);
      setCurrentQuestionIndex(0);
      setSelectedAnswers({});
      setViewState('quiz');
    } catch (err) {
      console.error('Error fetching questions:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectOption = (optionText: string) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [currentQuestionIndex]: optionText,
    }));
  };

  const handleNextQuestion = async () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      // Submit assessment payload to backend
      setIsLoading(true);
      try {
        const token = localStorage.getItem('token') || undefined;
        const answerPayloads = questions.map((q, idx) => ({
          question_id: q.question_id,
          selected_option: selectedAnswers[idx] || '',
        }));

        const result = await submitAssessmentAnswers('asm_tech_eval_01', answerPayloads, token);
        setResultData(result);
        setViewState('results');
      } catch (err) {
        console.error('Error submitting assessment:', err);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  const currentQ = questions[currentQuestionIndex];
  const progressPercent = questions.length > 0
    ? Math.round(((currentQuestionIndex + 1) / questions.length) * 100)
    : 0;

  return (
    <div className="space-y-6">
      {viewState === 'landing' && (
        <>
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
            <h2 className="text-2xl font-bold text-slate-900">Skill Assessment</h2>
            <p className="text-sm text-slate-600 mt-1">
              Evaluate your technical skills across domains to receive persistent skill mastery indexing.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {DOMAINS.map((domain) => {
              const Icon = domain.icon;
              return (
                <div
                  key={domain.id}
                  className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:border-slate-300 shadow-xs transition-all"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className="p-2 bg-indigo-50 border border-indigo-100 rounded-lg text-indigo-600">
                        <Icon className="w-5 h-5" />
                      </div>
                      <span
                        className={`text-xs font-medium px-2.5 py-0.5 rounded-full border ${
                          domain.difficulty === 'Beginner'
                            ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                            : domain.difficulty === 'Intermediate'
                            ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                            : 'bg-amber-50 text-amber-700 border-amber-200'
                        }`}
                      >
                        {domain.difficulty}
                      </span>
                    </div>

                    <h3 className="text-base font-semibold text-slate-900">{domain.name}</h3>
                    <p className="text-xs text-slate-600 mt-1 line-clamp-2">{domain.description}</p>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100 space-y-3">
                    <div className="flex items-center justify-between text-xs text-slate-500">
                      <span>{domain.questionsCount} Questions</span>
                      <span>Est. {domain.estimatedTime}</span>
                    </div>

                    <button
                      onClick={() => handleStartDomain(domain)}
                      disabled={isLoading}
                      className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-medium rounded-lg transition-colors flex items-center justify-center gap-1.5 disabled:opacity-50"
                    >
                      {isLoading ? 'Loading...' : 'Start Assessment'} <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </>
      )}

      {viewState === 'quiz' && currentQ && (
        <div className="max-w-3xl mx-auto space-y-6">
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
              <div>
                <span className="text-xs font-semibold text-indigo-600 uppercase tracking-wider">
                  Skill Assessment
                </span>
                <div className="flex items-center gap-2 mt-0.5">
                  <h2 className="text-xl font-bold text-slate-900">{selectedDomain?.name || currentQ.domain}</h2>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 border border-slate-200 text-slate-700 font-medium">
                    {currentQ.difficulty}
                  </span>
                </div>
              </div>

              <div className="text-right">
                <span className="text-xs text-slate-500 font-medium">Question {currentQuestionIndex + 1} of {questions.length}</span>
                <div className="w-32 bg-slate-100 h-2 rounded-full overflow-hidden mt-1.5">
                  <div
                    className="bg-indigo-600 h-full transition-all duration-300"
                    style={{ width: `${progressPercent}%` }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-base font-semibold text-slate-900">{currentQ.prompt}</h3>

              {currentQ.code_snippet && (
                <pre className="p-4 bg-slate-900 text-slate-100 rounded-lg text-xs font-mono overflow-x-auto border border-slate-800">
                  <code>{currentQ.code_snippet}</code>
                </pre>
              )}

              <div className="space-y-2.5 pt-2">
                {currentQ.options.map((opt, idx) => {
                  const isSelected = selectedAnswers[currentQuestionIndex] === opt;
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSelectOption(opt)}
                      className={`w-full text-left p-4 rounded-xl border text-sm transition-all ${
                        isSelected
                          ? 'bg-indigo-50/80 border-indigo-600 text-indigo-900 font-semibold'
                          : 'bg-white border-slate-200 text-slate-800 hover:bg-slate-50'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-5 h-5 rounded-full border flex items-center justify-center text-xs shrink-0 ${
                            isSelected
                              ? 'border-indigo-600 bg-indigo-600 text-white'
                              : 'border-slate-300 bg-white'
                          }`}
                        >
                          {isSelected && <CheckCircle className="w-3.5 h-3.5" />}
                        </div>
                        <span>{opt}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="flex items-center justify-between pt-6 mt-6 border-t border-slate-100">
              <button
                onClick={handlePrevQuestion}
                disabled={currentQuestionIndex === 0 || isLoading}
                className="px-4 py-2 border border-slate-200 rounded-lg text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-40 disabled:hover:bg-white flex items-center gap-1.5"
              >
                <ChevronLeft className="w-4 h-4" /> Previous
              </button>

              <button
                onClick={handleNextQuestion}
                disabled={selectedAnswers[currentQuestionIndex] === undefined || isLoading}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 text-white text-xs font-medium rounded-lg transition-colors flex items-center gap-1.5"
              >
                {isLoading ? 'Submitting...' : currentQuestionIndex === questions.length - 1 ? 'Submit Assessment' : 'Next'}
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {viewState === 'results' && resultData && (
        <div className="max-w-4xl mx-auto space-y-6">
          <div className="bg-white border border-slate-200 rounded-xl p-6 text-center shadow-xs">
            <div className="inline-flex p-3 bg-emerald-50 border border-emerald-200 text-emerald-600 rounded-full mb-3">
              <BarChart2 className="w-6 h-6" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900">Assessment Complete</h2>
            <p className="text-xs text-slate-500 mt-1">
              Your technical evaluation has been calculated and persisted in PostgreSQL.
            </p>

            <div className="my-6 inline-block bg-slate-50 border border-slate-200 rounded-2xl px-8 py-5">
              <span className="text-xs font-medium text-slate-500 block uppercase tracking-wider">Overall Score</span>
              <span className="text-4xl font-extrabold text-slate-900 mt-1 block">{resultData.overall_score}%</span>
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-5">
            <h3 className="text-lg font-bold text-slate-900">Topic Performance</h3>
            <div className="space-y-4">
              {Object.entries(resultData.topic_scores).map(([topic, score]) => (
                <div key={topic} className="space-y-1.5">
                  <div className="flex justify-between text-xs font-semibold text-slate-800">
                    <span>{topic}</span>
                    <span>{score}%</span>
                  </div>
                  <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${
                        score >= 70 ? 'bg-indigo-600' : score >= 40 ? 'bg-amber-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${score}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
            <h3 className="text-lg font-bold text-slate-900">Skill Analysis & Proficiency</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(resultData.skill_proficiency).map(([skill, label]) => (
                <div key={skill} className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
                  <span className="text-xs font-semibold text-slate-600 block mb-1">{skill}</span>
                  <div className="text-xs font-bold text-indigo-700 bg-white p-2.5 rounded-lg border border-slate-200">
                    {label}
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-4 text-center">
              <button
                onClick={() => {
                  if (onNavigateToRecommendations) onNavigateToRecommendations();
                  else setViewState('landing');
                }}
                className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl transition-colors inline-flex items-center gap-2 shadow-xs"
              >
                View My AI Recommendations <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
