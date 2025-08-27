import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Play, 
  Clock, 
  Star, 
  Users, 
  Target, 
  CheckCircle,
  Lock
} from 'lucide-react'

const Lessons = () => {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const categories = [
    { id: 'all', name: 'All Lessons', color: 'primary' },
    { id: 'vocabulary', name: 'Vocabulary', color: 'secondary' },
    { id: 'grammar', name: 'Grammar', color: 'accent' },
    { id: 'phrases', name: 'Phrases', color: 'warning' },
    { id: 'pronunciation', name: 'Pronunciation', color: 'primary' }
  ]

  const lessons = [
    {
      id: 1,
      title: 'Basic Greetings',
      category: 'phrases',
      difficulty: 'Beginner',
      duration: '15 min',
      students: 1250,
      rating: 4.8,
      completed: true,
      locked: false,
      description: 'Learn essential greetings and introductions in English.',
      topics: ['Hello', 'Goodbye', 'How are you?', 'Nice to meet you']
    },
    {
      id: 2,
      title: 'Colors and Numbers',
      category: 'vocabulary',
      difficulty: 'Beginner',
      duration: '20 min',
      students: 980,
      rating: 4.9,
      completed: false,
      locked: false,
      description: 'Master basic colors and numbers from 1 to 20.',
      topics: ['Red, Blue, Green', 'Numbers 1-20', 'Counting objects']
    },
    {
      id: 3,
      title: 'Present Simple Tense',
      category: 'grammar',
      difficulty: 'Intermediate',
      duration: '25 min',
      students: 750,
      rating: 4.7,
      completed: false,
      locked: false,
      description: 'Learn how to use the present simple tense correctly.',
      topics: ['I am', 'You are', 'He/She is', 'Daily routines']
    },
    {
      id: 4,
      title: 'Animal Names',
      category: 'vocabulary',
      difficulty: 'Beginner',
      duration: '18 min',
      students: 1100,
      rating: 4.6,
      completed: false,
      locked: false,
      description: 'Discover names of common animals in English.',
      topics: ['Pets', 'Farm animals', 'Wild animals', 'Animal sounds']
    },
    {
      id: 5,
      title: 'Question Words',
      category: 'grammar',
      difficulty: 'Intermediate',
      duration: '22 min',
      students: 650,
      rating: 4.5,
      completed: false,
      locked: true,
      description: 'Learn to ask questions using what, where, when, why, and how.',
      topics: ['What', 'Where', 'When', 'Why', 'How']
    },
    {
      id: 6,
      title: 'Food and Drinks',
      category: 'vocabulary',
      difficulty: 'Beginner',
      duration: '20 min',
      students: 890,
      rating: 4.8,
      completed: false,
      locked: false,
      description: 'Learn vocabulary for common foods and beverages.',
      topics: ['Fruits', 'Vegetables', 'Drinks', 'Meals']
    },
    {
      id: 7,
      title: 'Past Simple Tense',
      category: 'grammar',
      difficulty: 'Intermediate',
      duration: '30 min',
      students: 520,
      rating: 4.4,
      completed: false,
      locked: true,
      description: 'Master the past simple tense for talking about the past.',
      topics: ['Regular verbs', 'Irregular verbs', 'Yesterday', 'Last week']
    },
    {
      id: 8,
      title: 'Weather Expressions',
      category: 'phrases',
      difficulty: 'Beginner',
      duration: '16 min',
      students: 720,
      rating: 4.7,
      completed: false,
      locked: false,
      description: 'Learn how to talk about weather in English.',
      topics: ['Sunny', 'Rainy', 'Cold', 'Hot', 'Seasons']
    }
  ]

  const filteredLessons = lessons.filter(lesson => {
    const matchesCategory = selectedCategory === 'all' || lesson.category === selectedCategory
    const matchesSearch = lesson.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lesson.description.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Beginner': return 'text-green-600 bg-green-100 dark:bg-green-900'
      case 'Intermediate': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900'
      case 'Advanced': return 'text-red-600 bg-red-100 dark:bg-red-900'
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-900'
    }
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
            Interactive Lessons
          </h1>
          <p className="modern-text text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Choose from our collection of engaging lessons designed to make learning English fun and effective. 
            Track your progress and earn rewards as you complete each lesson!
          </p>
        </motion.div>

        {/* Search and Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-8 space-y-6"
        >
          {/* Search Bar */}
          <div className="relative max-w-md mx-auto">
            <input
              type="text"
              placeholder="Search lessons..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
            />
            <BookOpen className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          </div>

          {/* Category Filters */}
          <div className="flex flex-wrap justify-center gap-3">
            {categories.map((category) => (
              <motion.button
                key={category.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-full font-medium transition-all duration-300 ${
                  selectedCategory === category.id
                    ? 'bg-primary-500 text-white shadow-glow'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-primary-100 dark:hover:bg-primary-900 hover:text-primary-600 dark:hover:text-primary-400'
                }`}
              >
                {category.name}
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Lessons Grid */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
        >
          {filteredLessons.map((lesson, index) => (
            <motion.div
              key={lesson.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -5 }}
              className={`card p-6 relative ${lesson.locked ? 'opacity-60' : ''}`}
            >
              {/* Lock Icon for locked lessons */}
              {lesson.locked && (
                <div className="absolute top-4 right-4">
                  <Lock className="text-gray-400" size={20} />
                </div>
              )}

              {/* Completed Badge */}
              {lesson.completed && (
                <div className="absolute top-4 left-4">
                  <CheckCircle className="text-green-500" size={20} />
                </div>
              )}

              {/* Lesson Header */}
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {lesson.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {lesson.description}
                </p>
                
                {/* Difficulty Badge */}
                <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(lesson.difficulty)}`}>
                  {lesson.difficulty}
                </span>
              </div>

              {/* Lesson Stats */}
              <div className="flex items-center justify-between mb-4 text-sm text-gray-500 dark:text-gray-400">
                <div className="flex items-center space-x-1">
                  <Clock size={16} />
                  <span>{lesson.duration}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Users size={16} />
                  <span>{lesson.students}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Star size={16} className="text-yellow-500" />
                  <span>{lesson.rating}</span>
                </div>
              </div>

              {/* Topics */}
              <div className="mb-4">
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Topics covered:</h4>
                <div className="flex flex-wrap gap-1">
                  {lesson.topics.slice(0, 3).map((topic, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs rounded-full"
                    >
                      {topic}
                    </span>
                  ))}
                  {lesson.topics.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs rounded-full">
                      +{lesson.topics.length - 3} more
                    </span>
                  )}
                </div>
              </div>

              {/* Action Button */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                disabled={lesson.locked}
                className={`w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-xl font-medium transition-all duration-300 ${
                  lesson.locked
                    ? 'bg-gray-200 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
                    : lesson.completed
                    ? 'bg-green-500 hover:bg-green-600 text-white'
                    : 'bg-primary-500 hover:bg-primary-600 text-white'
                }`}
              >
                <Play size={16} />
                <span>
                  {lesson.locked ? 'Locked' : lesson.completed ? 'Review' : 'Start Lesson'}
                </span>
              </motion.button>
            </motion.div>
          ))}
        </motion.div>

        {/* Empty State */}
        {filteredLessons.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              No lessons found
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Try adjusting your search or filter criteria.
            </p>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default Lessons