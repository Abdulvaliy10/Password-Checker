import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Mic, 
  Volume2, 
  Play, 
  Pause, 
  RotateCcw, 
  CheckCircle,
  X,
  Target,
  Clock,
  Star,
  Headphones,
  MessageCircle,
  Video,
  FileText
} from 'lucide-react'

const Practice = () => {
  const [selectedPractice, setSelectedPractice] = useState(null)
  const [isRecording, setIsRecording] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)

  const practiceTypes = [
    {
      id: 'speaking',
      title: 'Speaking Practice',
      description: 'Improve your pronunciation with interactive speaking exercises',
      icon: Mic,
      color: 'primary',
      status: 'coming-soon',
      features: [
        'Voice recognition technology',
        'Pronunciation feedback',
        'Conversation practice',
        'Accent training'
      ]
    },
    {
      id: 'listening',
      title: 'Listening Comprehension',
      description: 'Enhance your listening skills with audio exercises',
      icon: Headphones,
      color: 'secondary',
      status: 'coming-soon',
      features: [
        'Audio lessons',
        'Comprehension quizzes',
        'Speed control',
        'Transcript support'
      ]
    },
    {
      id: 'conversation',
      title: 'Conversation Practice',
      description: 'Practice real-world conversations with AI partners',
      icon: MessageCircle,
      color: 'accent',
      status: 'coming-soon',
      features: [
        'AI conversation partners',
        'Role-playing scenarios',
        'Real-time feedback',
        'Cultural context'
      ]
    },
    {
      id: 'video-lessons',
      title: 'Video Lessons',
      description: 'Learn through engaging video content',
      icon: Video,
      color: 'warning',
      status: 'coming-soon',
      features: [
        'Interactive videos',
        'Subtitles and captions',
        'Comprehension checks',
        'Progress tracking'
      ]
    }
  ]

  const currentExercises = [
    {
      id: 1,
      title: 'Basic Pronunciation',
      type: 'Speaking',
      difficulty: 'Beginner',
      duration: '10 min',
      description: 'Practice basic English sounds and pronunciation',
      completed: false,
      locked: false
    },
    {
      id: 2,
      title: 'Listening to Numbers',
      type: 'Listening',
      difficulty: 'Beginner',
      duration: '8 min',
      description: 'Listen and identify numbers from 1 to 100',
      completed: true,
      locked: false
    },
    {
      id: 3,
      title: 'Greeting Conversations',
      type: 'Conversation',
      difficulty: 'Beginner',
      duration: '15 min',
      description: 'Practice common greeting phrases and responses',
      completed: false,
      locked: false
    },
    {
      id: 4,
      title: 'Weather Vocabulary',
      type: 'Speaking',
      difficulty: 'Intermediate',
      duration: '12 min',
      description: 'Learn and practice weather-related vocabulary',
      completed: false,
      locked: true
    },
    {
      id: 5,
      title: 'Story Comprehension',
      type: 'Listening',
      difficulty: 'Intermediate',
      duration: '20 min',
      description: 'Listen to short stories and answer questions',
      completed: false,
      locked: true
    },
    {
      id: 6,
      title: 'Job Interview Practice',
      type: 'Conversation',
      difficulty: 'Advanced',
      duration: '25 min',
      description: 'Practice common job interview questions and answers',
      completed: false,
      locked: true
    }
  ]

  const startPractice = (practice) => {
    setSelectedPractice(practice)
  }

  const closePractice = () => {
    setSelectedPractice(null)
  }

  const toggleRecording = () => {
    setIsRecording(!isRecording)
  }

  const togglePlaying = () => {
    setIsPlaying(!isPlaying)
  }

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="fun-text text-gray-900 dark:text-white mb-4">
            Practice Your Skills
          </h1>
          <p className="modern-text text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Enhance your speaking, listening, and conversation skills with our interactive practice sessions. 
            More features coming soon!
          </p>
        </motion.div>

        {/* Coming Soon Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-16"
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8 text-center">
            Advanced Features Coming Soon
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {practiceTypes.map((practice, index) => {
              const Icon = practice.icon
              return (
                <motion.div
                  key={practice.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="card p-6 relative"
                >
                  <div className="absolute top-4 right-4">
                    <span className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-600 dark:text-yellow-400 text-xs font-medium rounded-full">
                      Coming Soon
                    </span>
                  </div>
                  
                  <div className="text-center space-y-4">
                    <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 ${
                      practice.color === 'primary' ? 'bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400' :
                      practice.color === 'secondary' ? 'bg-secondary-100 dark:bg-secondary-900 text-secondary-600 dark:text-secondary-400' :
                      practice.color === 'accent' ? 'bg-accent-100 dark:bg-accent-900 text-accent-600 dark:text-accent-400' :
                      'bg-warning-100 dark:bg-warning-900 text-warning-600 dark:text-warning-400'
                    }`}>
                      <Icon size={32} />
                    </div>
                    
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {practice.title}
                    </h3>
                    
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {practice.description}
                    </p>
                    
                    <div className="space-y-2">
                      {practice.features.map((feature, idx) => (
                        <div key={idx} className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
                          <CheckCircle size={12} className="text-green-500" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        {/* Current Practice Exercises */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-8 text-center">
            Available Practice Exercises
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {currentExercises.map((exercise, index) => (
              <motion.div
                key={exercise.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
                className={`card p-6 relative ${exercise.locked ? 'opacity-60' : ''}`}
              >
                {exercise.locked && (
                  <div className="absolute top-4 right-4">
                    <X className="text-gray-400" size={20} />
                  </div>
                )}
                
                {exercise.completed && (
                  <div className="absolute top-4 left-4">
                    <CheckCircle className="text-green-500" size={20} />
                  </div>
                )}

                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {exercise.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      {exercise.description}
                    </p>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                    <span className="flex items-center space-x-1">
                      <Target size={14} />
                      <span>{exercise.difficulty}</span>
                    </span>
                    <span className="flex items-center space-x-1">
                      <Clock size={14} />
                      <span>{exercise.duration}</span>
                    </span>
                  </div>

                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    disabled={exercise.locked}
                    onClick={() => startPractice(exercise)}
                    className={`w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-xl font-medium transition-all duration-300 ${
                      exercise.locked
                        ? 'bg-gray-200 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
                        : exercise.completed
                        ? 'bg-green-500 hover:bg-green-600 text-white'
                        : 'bg-primary-500 hover:bg-primary-600 text-white'
                    }`}
                  >
                    <Play size={16} />
                    <span>
                      {exercise.locked ? 'Locked' : exercise.completed ? 'Practice Again' : 'Start Practice'}
                    </span>
                  </motion.button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Practice Modal */}
        {selectedPractice && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            onClick={closePractice}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {selectedPractice.title}
                </h2>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={closePractice}
                  className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  <X size={24} />
                </motion.button>
              </div>

              <div className="space-y-6">
                <div className="text-center">
                  <div className="text-6xl mb-4">🎤</div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                    Practice Session
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    This is a placeholder for the actual practice session. 
                    Advanced features like voice recognition and AI conversation partners are coming soon!
                  </p>
                </div>

                <div className="flex justify-center space-x-4">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={toggleRecording}
                    className={`p-4 rounded-full ${
                      isRecording 
                        ? 'bg-red-500 text-white' 
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                    }`}
                  >
                    <Mic size={24} />
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={togglePlaying}
                    className={`p-4 rounded-full ${
                      isPlaying 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                    }`}
                  >
                    {isPlaying ? <Pause size={24} /> : <Play size={24} />}
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="p-4 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
                  >
                    <RotateCcw size={24} />
                  </motion.button>
                </div>

                <div className="text-center">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Duration: {selectedPractice.duration} • Difficulty: {selectedPractice.difficulty}
                  </p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default Practice