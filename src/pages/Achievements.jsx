import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Trophy, 
  Star, 
  Target, 
  Award, 
  Users, 
  TrendingUp, 
  Calendar,
  CheckCircle,
  Lock,
  Crown,
  Medal,
  Zap,
  Clock
} from 'lucide-react'
import { AnimatePresence } from 'framer-motion'

const Achievements = () => {
  const [selectedTab, setSelectedTab] = useState('badges')

  const badges = [
    {
      id: 1,
      name: 'First Steps',
      description: 'Complete your first lesson',
      icon: '🎯',
      category: 'beginner',
      unlocked: true,
      date: '2024-01-15',
      rarity: 'common'
    },
    {
      id: 2,
      name: 'Vocabulary Master',
      description: 'Learn 100 new words',
      icon: '📚',
      category: 'vocabulary',
      unlocked: true,
      date: '2024-01-20',
      rarity: 'rare'
    },
    {
      id: 3,
      name: 'Grammar Guru',
      description: 'Complete 10 grammar lessons',
      icon: '📝',
      category: 'grammar',
      unlocked: false,
      progress: 7,
      total: 10,
      rarity: 'epic'
    },
    {
      id: 4,
      name: 'Game Champion',
      description: 'Win 50 games',
      icon: '🏆',
      category: 'games',
      unlocked: false,
      progress: 23,
      total: 50,
      rarity: 'legendary'
    },
    {
      id: 5,
      name: 'Perfect Score',
      description: 'Get 100% on any quiz',
      icon: '⭐',
      category: 'achievement',
      unlocked: true,
      date: '2024-01-18',
      rarity: 'rare'
    },
    {
      id: 6,
      name: 'Streak Master',
      description: 'Study for 7 days in a row',
      icon: '🔥',
      category: 'streak',
      unlocked: false,
      progress: 4,
      total: 7,
      rarity: 'epic'
    },
    {
      id: 7,
      name: 'Social Butterfly',
      description: 'Complete 5 lessons with friends',
      icon: '🦋',
      category: 'social',
      unlocked: false,
      progress: 2,
      total: 5,
      rarity: 'rare'
    },
    {
      id: 8,
      name: 'Speed Learner',
      description: 'Complete 3 lessons in one day',
      icon: '⚡',
      category: 'speed',
      unlocked: true,
      date: '2024-01-22',
      rarity: 'epic'
    }
  ]

  const stats = [
    { label: 'Total Badges', value: '3/8', icon: Trophy, color: 'text-yellow-500' },
    { label: 'Current Streak', value: '4 days', icon: TrendingUp, color: 'text-green-500' },
    { label: 'Lessons Completed', value: '15', icon: CheckCircle, color: 'text-blue-500' },
    { label: 'Games Won', value: '23', icon: Star, color: 'text-purple-500' },
    { label: 'Words Learned', value: '127', icon: Target, color: 'text-red-500' },
    { label: 'Study Time', value: '8.5h', icon: Clock, color: 'text-indigo-500' }
  ]

  const leaderboard = [
    { rank: 1, name: 'Alex Johnson', score: 2840, avatar: '👑', level: 'Master' },
    { rank: 2, name: 'Sarah Chen', score: 2650, avatar: '🥇', level: 'Expert' },
    { rank: 3, name: 'Mike Rodriguez', score: 2480, avatar: '🥈', level: 'Advanced' },
    { rank: 4, name: 'Emma Wilson', score: 2310, avatar: '🥉', level: 'Intermediate' },
    { rank: 5, name: 'David Kim', score: 2150, avatar: '⭐', level: 'Intermediate' },
    { rank: 6, name: 'Lisa Thompson', score: 1980, avatar: '⭐', level: 'Beginner' },
    { rank: 7, name: 'James Brown', score: 1820, avatar: '⭐', level: 'Beginner' },
    { rank: 8, name: 'Maria Garcia', score: 1650, avatar: '⭐', level: 'Beginner' },
    { rank: 9, name: 'Tom Anderson', score: 1490, avatar: '⭐', level: 'Beginner' },
    { rank: 10, name: 'Anna Lee', score: 1320, avatar: '⭐', level: 'Beginner' }
  ]

  const getRarityColor = (rarity) => {
    switch (rarity) {
      case 'common': return 'border-gray-300 bg-gray-50 dark:border-gray-600 dark:bg-gray-800'
      case 'rare': return 'border-blue-300 bg-blue-50 dark:border-blue-600 dark:bg-blue-900'
      case 'epic': return 'border-purple-300 bg-purple-50 dark:border-purple-600 dark:bg-purple-900'
      case 'legendary': return 'border-yellow-300 bg-yellow-50 dark:border-yellow-600 dark:bg-yellow-900'
      default: return 'border-gray-300 bg-gray-50 dark:border-gray-600 dark:bg-gray-800'
    }
  }

  const getRarityText = (rarity) => {
    switch (rarity) {
      case 'common': return 'text-gray-600 dark:text-gray-400'
      case 'rare': return 'text-blue-600 dark:text-blue-400'
      case 'epic': return 'text-purple-600 dark:text-purple-400'
      case 'legendary': return 'text-yellow-600 dark:text-yellow-400'
      default: return 'text-gray-600 dark:text-gray-400'
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
            Your Achievements
          </h1>
          <p className="modern-text text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Track your progress, unlock badges, and compete with other learners on the leaderboard!
          </p>
        </motion.div>

        {/* Stats Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-12"
        >
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card p-4 text-center"
              >
                <Icon className={`w-8 h-8 mx-auto mb-2 ${stat.color}`} />
                <div className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  {stat.label}
                </div>
              </motion.div>
            )
          })}
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="flex justify-center mb-8"
        >
          <div className="flex space-x-1 bg-gray-100 dark:bg-gray-800 rounded-xl p-1">
            {[
              { id: 'badges', label: 'Badges', icon: Trophy },
              { id: 'leaderboard', label: 'Leaderboard', icon: Crown }
            ].map((tab) => {
              const Icon = tab.icon
              return (
                <motion.button
                  key={tab.id}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                    selectedTab === tab.id
                      ? 'bg-white dark:bg-gray-700 text-primary-600 dark:text-primary-400 shadow-soft'
                      : 'text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400'
                  }`}
                >
                  <Icon size={18} />
                  <span>{tab.label}</span>
                </motion.button>
              )
            })}
          </div>
        </motion.div>

        {/* Content */}
        <AnimatePresence mode="wait">
          {selectedTab === 'badges' && (
            <motion.div
              key="badges"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
            >
              {badges.map((badge, index) => (
                <motion.div
                  key={badge.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                  className={`card p-6 border-2 ${getRarityColor(badge.rarity)} ${!badge.unlocked ? 'opacity-60' : ''}`}
                >
                  <div className="text-center space-y-4">
                    {/* Badge Icon */}
                    <div className="relative">
                      <div className="text-4xl mb-2">
                        {badge.unlocked ? badge.icon : '🔒'}
                      </div>
                      {badge.unlocked && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="absolute -top-1 -right-1"
                        >
                          <CheckCircle className="text-green-500" size={20} />
                        </motion.div>
                      )}
                    </div>

                    {/* Badge Info */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                        {badge.name}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                        {badge.description}
                      </p>
                      
                      {/* Progress Bar for locked badges */}
                      {!badge.unlocked && badge.progress !== undefined && (
                        <div className="mb-3">
                          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mb-1">
                            <span>Progress</span>
                            <span>{badge.progress}/{badge.total}</span>
                          </div>
                          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                            <motion.div
                              className="bg-primary-500 h-2 rounded-full"
                              initial={{ width: 0 }}
                              animate={{ width: `${(badge.progress / badge.total) * 100}%` }}
                              transition={{ duration: 1, delay: 0.5 }}
                            />
                          </div>
                        </div>
                      )}

                      {/* Unlock Date */}
                      {badge.unlocked && badge.date && (
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          Unlocked: {new Date(badge.date).toLocaleDateString()}
                        </div>
                      )}

                      {/* Rarity Badge */}
                      <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getRarityText(badge.rarity)} bg-white dark:bg-gray-800 border`}>
                        {badge.rarity.charAt(0).toUpperCase() + badge.rarity.slice(1)}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}

          {selectedTab === 'leaderboard' && (
            <motion.div
              key="leaderboard"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="max-w-4xl mx-auto"
            >
              <div className="card p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                    Global Leaderboard
                  </h2>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Updated daily
                  </div>
                </div>

                <div className="space-y-3">
                  {leaderboard.map((player, index) => (
                    <motion.div
                      key={player.rank}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                      className={`flex items-center justify-between p-4 rounded-xl transition-all duration-300 ${
                        index < 3 
                          ? 'bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900 dark:to-orange-900 border border-yellow-200 dark:border-yellow-700'
                          : 'bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700'
                      }`}
                    >
                      <div className="flex items-center space-x-4">
                        <div className="text-2xl">{player.avatar}</div>
                        <div>
                          <div className="font-semibold text-gray-900 dark:text-white">
                            {player.name}
                          </div>
                          <div className="text-sm text-gray-500 dark:text-gray-400">
                            {player.level}
                          </div>
                        </div>
                      </div>
                      
                      <div className="text-right">
                        <div className="font-bold text-gray-900 dark:text-white">
                          {player.score.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          points
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* Your Position */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.5 }}
                  className="mt-6 p-4 bg-primary-50 dark:bg-primary-900 rounded-xl border border-primary-200 dark:border-primary-700"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="text-2xl">👤</div>
                      <div>
                        <div className="font-semibold text-gray-900 dark:text-white">
                          Your Position
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          Keep learning to climb the ranks!
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-primary-600 dark:text-primary-400">
                        #15
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        1,240 points
                      </div>
                    </div>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default Achievements