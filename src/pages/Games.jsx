import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Gamepad2, 
  Play, 
  Star, 
  Trophy, 
  Clock, 
  Target, 
  CheckCircle,
  X,
  RotateCcw,
  Volume2
} from 'lucide-react'

const Games = () => {
  const [selectedGame, setSelectedGame] = useState(null)
  const [gameState, setGameState] = useState('menu') // menu, playing, completed
  const [score, setScore] = useState(0)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)

  const games = [
    {
      id: 'vocabulary-quiz',
      title: 'Vocabulary Quiz',
      description: 'Test your knowledge of English vocabulary with fun multiple-choice questions.',
      difficulty: 'Beginner',
      duration: '5 min',
      icon: '🎯',
      color: 'primary',
      questions: [
        {
          question: 'What color is the sky on a sunny day?',
          options: ['Red', 'Blue', 'Green', 'Yellow'],
          correct: 1
        },
        {
          question: 'Which animal says "meow"?',
          options: ['Dog', 'Cat', 'Bird', 'Fish'],
          correct: 1
        },
        {
          question: 'What do you use to write on paper?',
          options: ['Fork', 'Pen', 'Shoe', 'Book'],
          correct: 1
        },
        {
          question: 'Which fruit is yellow and grows on trees?',
          options: ['Apple', 'Banana', 'Orange', 'Grape'],
          correct: 1
        },
        {
          question: 'What do you wear on your feet?',
          options: ['Hat', 'Shoes', 'Gloves', 'Scarf'],
          correct: 1
        }
      ]
    },
    {
      id: 'word-matching',
      title: 'Word Matching',
      description: 'Match English words with their correct meanings or pictures.',
      difficulty: 'Intermediate',
      duration: '8 min',
      icon: '🔗',
      color: 'secondary',
      pairs: [
        { word: 'Happy', meaning: 'Feeling joy or pleasure' },
        { word: 'Big', meaning: 'Large in size' },
        { word: 'Fast', meaning: 'Moving quickly' },
        { word: 'Hot', meaning: 'High temperature' },
        { word: 'New', meaning: 'Recently made or created' }
      ]
    },
    {
      id: 'flashcards',
      title: 'Flashcards',
      description: 'Learn new words with interactive flashcards and pronunciation.',
      difficulty: 'Beginner',
      duration: '10 min',
      icon: '📚',
      color: 'accent',
      cards: [
        { word: 'Apple', definition: 'A round fruit with red, yellow, or green skin', pronunciation: '/ˈæp.əl/' },
        { word: 'House', definition: 'A building where people live', pronunciation: '/haʊs/' },
        { word: 'School', definition: 'A place where children learn', pronunciation: '/skuːl/' },
        { word: 'Friend', definition: 'Someone you like and trust', pronunciation: '/frend/' },
        { word: 'Family', definition: 'A group of people related by blood or marriage', pronunciation: '/ˈfæm.əl.i/' }
      ]
    },
    {
      id: 'grammar-challenge',
      title: 'Grammar Challenge',
      description: 'Practice English grammar with sentence completion exercises.',
      difficulty: 'Intermediate',
      duration: '12 min',
      icon: '📝',
      color: 'warning',
      questions: [
        {
          question: 'Complete the sentence: "I ___ to school every day."',
          options: ['go', 'goes', 'going', 'went'],
          correct: 0
        },
        {
          question: 'Which word is correct? "She ___ a beautiful dress."',
          options: ['wear', 'wears', 'wearing', 'wore'],
          correct: 1
        },
        {
          question: 'Choose the right form: "They ___ playing in the park."',
          options: ['is', 'are', 'am', 'be'],
          correct: 1
        },
        {
          question: 'Fill in the blank: "Yesterday, I ___ to the store."',
          options: ['go', 'goes', 'went', 'going'],
          correct: 2
        },
        {
          question: 'Which is correct? "The sun ___ in the east."',
          options: ['rise', 'rises', 'rising', 'rose'],
          correct: 1
        }
      ]
    }
  ]

  const startGame = (game) => {
    setSelectedGame(game)
    setGameState('playing')
    setScore(0)
    setCurrentQuestion(0)
    setShowAnswer(false)
  }

  const endGame = () => {
    setGameState('completed')
  }

  const resetGame = () => {
    setGameState('menu')
    setSelectedGame(null)
    setScore(0)
    setCurrentQuestion(0)
    setShowAnswer(false)
  }

  const handleAnswer = (selectedOption) => {
    if (selectedGame.id === 'vocabulary-quiz' || selectedGame.id === 'grammar-challenge') {
      const isCorrect = selectedOption === selectedGame.questions[currentQuestion].correct
      if (isCorrect) {
        setScore(score + 1)
      }
      
      if (currentQuestion + 1 < selectedGame.questions.length) {
        setCurrentQuestion(currentQuestion + 1)
      } else {
        endGame()
      }
    }
  }

  const renderGameContent = () => {
    if (!selectedGame) return null

    switch (selectedGame.id) {
      case 'vocabulary-quiz':
      case 'grammar-challenge':
        if (gameState === 'playing') {
          const question = selectedGame.questions[currentQuestion]
          return (
            <motion.div
              key={currentQuestion}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              className="space-y-6"
            >
              <div className="text-center">
                <div className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                  Question {currentQuestion + 1} of {selectedGame.questions.length}
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
                  <motion.div
                    className="bg-primary-500 h-2 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${((currentQuestion + 1) / selectedGame.questions.length) * 100}%` }}
                  />
                </div>
              </div>

              <div className="card p-8">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
                  {question.question}
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {question.options.map((option, index) => (
                    <motion.button
                      key={index}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleAnswer(index)}
                      className="p-4 border-2 border-gray-200 dark:border-gray-600 rounded-xl text-left hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900 transition-all duration-300"
                    >
                      <span className="font-medium text-gray-900 dark:text-white">
                        {String.fromCharCode(65 + index)}. {option}
                      </span>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          )
        }
        break

      case 'flashcards':
        return (
          <div className="space-y-6">
            <div className="text-center">
              <div className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                Card {currentQuestion + 1} of {selectedGame.cards.length}
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
                <motion.div
                  className="bg-accent-500 h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${((currentQuestion + 1) / selectedGame.cards.length) * 100}%` }}
                />
              </div>
            </div>

            <motion.div
              key={currentQuestion}
              initial={{ opacity: 0, rotateY: 180 }}
              animate={{ opacity: 1, rotateY: 0 }}
              className="card p-8 text-center"
            >
              <div className="space-y-6">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
                  {selectedGame.cards[currentQuestion].word}
                </h2>
                
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="p-3 bg-accent-100 dark:bg-accent-900 rounded-full text-accent-600 dark:text-accent-400"
                >
                  <Volume2 size={24} />
                </motion.button>
                
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  {selectedGame.cards[currentQuestion].pronunciation}
                </div>
                
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="text-gray-600 dark:text-gray-300"
                >
                  {selectedGame.cards[currentQuestion].definition}
                </motion.div>
              </div>
            </motion.div>

            <div className="flex justify-center space-x-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
                disabled={currentQuestion === 0}
                className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  if (currentQuestion + 1 < selectedGame.cards.length) {
                    setCurrentQuestion(currentQuestion + 1)
                  } else {
                    endGame()
                  }
                }}
                className="btn-primary"
              >
                {currentQuestion + 1 < selectedGame.cards.length ? 'Next' : 'Finish'}
              </motion.button>
            </div>
          </div>
        )

      case 'word-matching':
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Match the words with their meanings
              </h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {selectedGame.pairs.map((pair, index) => (
                <motion.div
                  key={index}
                  whileHover={{ scale: 1.02 }}
                  className="card p-6 cursor-pointer"
                >
                  <div className="text-center space-y-4">
                    <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                      {pair.word}
                    </div>
                    <div className="text-gray-600 dark:text-gray-300">
                      {pair.meaning}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
            
            <div className="text-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={endGame}
                className="btn-primary"
              >
                Complete Matching
              </motion.button>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  const renderGameResult = () => {
    if (!selectedGame || gameState !== 'completed') return null

    const totalQuestions = selectedGame.questions?.length || 0
    const percentage = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0
    const isPerfect = percentage === 100
    const isGood = percentage >= 80
    const isPassing = percentage >= 60

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center space-y-6"
      >
        <div className="card p-8">
          <div className="text-6xl mb-4">
            {isPerfect ? '🏆' : isGood ? '🎉' : isPassing ? '👍' : '📚'}
          </div>
          
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {isPerfect ? 'Perfect Score!' : isGood ? 'Great Job!' : isPassing ? 'Well Done!' : 'Keep Practicing!'}
          </h2>
          
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            You scored {score} out of {totalQuestions} ({percentage}%)
          </p>
          
          <div className="flex justify-center space-x-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={resetGame}
              className="btn-primary"
            >
              Play Again
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={resetGame}
              className="btn-secondary"
            >
              Back to Games
            </motion.button>
          </div>
        </div>
      </motion.div>
    )
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
            Fun Learning Games
          </h1>
          <p className="modern-text text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Practice your English skills with our collection of interactive games. 
            Have fun while learning vocabulary, grammar, and more!
          </p>
        </motion.div>

        <AnimatePresence mode="wait">
          {gameState === 'menu' && (
            <motion.div
              key="menu"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            >
              {games.map((game, index) => (
                <motion.div
                  key={game.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                  className="card p-6 cursor-pointer"
                  onClick={() => startGame(game)}
                >
                  <div className="text-center space-y-4">
                    <div className="text-4xl">{game.icon}</div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                      {game.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {game.description}
                    </p>
                    <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                      <span className="flex items-center space-x-1">
                        <Target size={14} />
                        <span>{game.difficulty}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <Clock size={14} />
                        <span>{game.duration}</span>
                      </span>
                    </div>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="btn-primary w-full"
                    >
                      <Play size={16} className="mr-2" />
                      Play Now
                    </motion.button>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}

          {gameState === 'playing' && (
            <motion.div
              key="playing"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="max-w-4xl mx-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {selectedGame.title}
                </h2>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={resetGame}
                  className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  <X size={24} />
                </motion.button>
              </div>
              {renderGameContent()}
            </motion.div>
          )}

          {gameState === 'completed' && (
            <motion.div
              key="completed"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="max-w-2xl mx-auto"
            >
              {renderGameResult()}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default Games