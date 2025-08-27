import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Gamepad2, 
  Trophy, 
  Mic, 
  Star, 
  Users, 
  Target, 
  Sparkles 
} from 'lucide-react'

const Home = () => {
  const features = [
    {
      icon: BookOpen,
      title: 'Interactive Lessons',
      description: 'Learn vocabulary, grammar, and phrases through engaging lessons designed for young learners.',
      color: 'primary',
      path: '/lessons'
    },
    {
      icon: Gamepad2,
      title: 'Fun Games',
      description: 'Practice your English skills with exciting games like quizzes, flashcards, and word matching.',
      color: 'secondary',
      path: '/games'
    },
    {
      icon: Trophy,
      title: 'Achievements',
      description: 'Earn badges, stars, and rewards as you progress through your learning journey.',
      color: 'warning',
      path: '/achievements'
    },
    {
      icon: Mic,
      title: 'Speaking Practice',
      description: 'Improve your pronunciation and speaking skills with our interactive practice sessions.',
      color: 'accent',
      path: '/practice'
    }
  ]

  const stats = [
    { number: '10,000+', label: 'Happy Students', icon: Users },
    { number: '500+', label: 'Lessons Available', icon: BookOpen },
    { number: '50+', label: 'Fun Games', icon: Gamepad2 },
    { number: '100+', label: 'Achievements', icon: Trophy }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Hero Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <div className="space-y-4">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2, duration: 0.6 }}
                  className="inline-flex items-center space-x-2 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 px-4 py-2 rounded-full text-sm font-medium"
                >
                  <Sparkles size={16} />
                  <span>Learn English the Fun Way!</span>
                </motion.div>
                
                <h1 className="fun-text text-gray-900 dark:text-white leading-tight">
                  Master English with{' '}
                  <span className="bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">
                    Fun & Games
                  </span>
                </h1>
                
                <p className="modern-text text-gray-600 dark:text-gray-300 max-w-lg">
                  Join thousands of young learners worldwide in an exciting journey to master English. 
                  Our interactive platform makes learning fun, engaging, and effective!
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/lessons">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-primary w-full sm:w-auto"
                  >
                    Start Learning
                  </motion.button>
                </Link>
                <Link to="/games">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-secondary w-full sm:w-auto"
                  >
                    Play Games
                  </motion.button>
                </Link>
              </div>
            </motion.div>

            {/* Hero Visual */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="relative"
            >
              <div className="relative z-10">
                <div className="grid grid-cols-2 gap-4">
                  <motion.div
                    animate={{ y: [0, -10, 0] }}
                    transition={{ duration: 3, repeat: Infinity }}
                    className="card p-6 text-center"
                  >
                    <BookOpen className="w-12 h-12 text-primary-500 mx-auto mb-4" />
                    <h3 className="font-semibold text-gray-900 dark:text-white">Lessons</h3>
                  </motion.div>
                  <motion.div
                    animate={{ y: [0, 10, 0] }}
                    transition={{ duration: 3, repeat: Infinity, delay: 1 }}
                    className="card p-6 text-center"
                  >
                    <Gamepad2 className="w-12 h-12 text-secondary-500 mx-auto mb-4" />
                    <h3 className="font-semibold text-gray-900 dark:text-white">Games</h3>
                  </motion.div>
                  <motion.div
                    animate={{ y: [0, 10, 0] }}
                    transition={{ duration: 3, repeat: Infinity, delay: 2 }}
                    className="card p-6 text-center"
                  >
                    <Trophy className="w-12 h-12 text-warning-500 mx-auto mb-4" />
                    <h3 className="font-semibold text-gray-900 dark:text-white">Achievements</h3>
                  </motion.div>
                  <motion.div
                    animate={{ y: [0, -10, 0] }}
                    transition={{ duration: 3, repeat: Infinity, delay: 1.5 }}
                    className="card p-6 text-center"
                  >
                    <Mic className="w-12 h-12 text-accent-500 mx-auto mb-4" />
                    <h3 className="font-semibold text-gray-900 dark:text-white">Practice</h3>
                  </motion.div>
                </div>
              </div>
              
              {/* Background decoration */}
              <div className="absolute inset-0 -z-10">
                <div className="absolute top-0 right-0 w-72 h-72 bg-primary-200 dark:bg-primary-800 rounded-full opacity-20 blur-3xl"></div>
                <div className="absolute bottom-0 left-0 w-72 h-72 bg-accent-200 dark:bg-accent-800 rounded-full opacity-20 blur-3xl"></div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="text-center"
                >
                  <Icon className="w-8 h-8 text-primary-500 mx-auto mb-3" />
                  <div className="fun-text text-gray-900 dark:text-white">{stat.number}</div>
                  <div className="text-gray-600 dark:text-gray-400 font-medium">{stat.label}</div>
                </motion.div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="fun-text text-gray-900 dark:text-white mb-4">
              Why Choose Fun English?
            </h2>
            <p className="modern-text text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Our platform combines cutting-edge technology with proven learning methods to create 
              an engaging and effective English learning experience.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              const colorClasses = {
                primary: 'text-primary-500 bg-primary-100 dark:bg-primary-900',
                secondary: 'text-secondary-500 bg-secondary-100 dark:bg-secondary-900',
                accent: 'text-accent-500 bg-accent-100 dark:bg-accent-900',
                warning: 'text-warning-500 bg-warning-100 dark:bg-warning-900'
              }
              
              return (
                <Link key={index} to={feature.path}>
                  <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    whileHover={{ y: -5 }}
                    className="card p-6 text-center group cursor-pointer"
                  >
                    <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300 ${colorClasses[feature.color]}`}>
                      <Icon size={32} />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      {feature.description}
                    </p>
                  </motion.div>
                </Link>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-500 to-accent-500">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <h2 className="fun-text text-white">
              Ready to Start Your English Journey?
            </h2>
            <p className="modern-text text-white/90 max-w-2xl mx-auto">
              Join thousands of learners who are already improving their English skills with our fun and interactive platform.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/lessons">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-white text-primary-600 font-semibold py-3 px-8 rounded-xl hover:bg-gray-100 transition-colors duration-300"
                >
                  Get Started Free
                </motion.button>
              </Link>
              <Link to="/games">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="border-2 border-white text-white font-semibold py-3 px-8 rounded-xl hover:bg-white hover:text-primary-600 transition-colors duration-300"
                >
                  Try Our Games
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home