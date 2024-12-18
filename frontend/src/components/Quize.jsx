import React, { useState, useEffect } from 'react';
import quizData from '../quiz.json'; // Import the JSON file
import { useNavigate } from 'react-router-dom';

const Quiz = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [showResult, setShowResult] = useState(false);

  useEffect(() => {
    // Shuffle and select 10 random questions from the JSON file
    const shuffledQuestions = [...quizData.questions]
      .sort(() => Math.random() - 0.5)
      .slice(0, 10);
    setQuestions(shuffledQuestions);
  }, []);

  const handleOptionClick = (option) => {
    setSelectedOption(option);
  };

  const handleNextQuestion = () => {
    // Check the answer and update the score
    if (selectedOption === questions[currentQuestionIndex].answer) {
      setScore(score + 1);
    }

    setSelectedOption(null);

    // Move to the next question or show the result
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      setShowResult(true);
    }
  };

  const handleRestart = () => {
    // Restart the quiz
    const shuffledQuestions = [...quizData.questions]
      .sort(() => Math.random() - 0.5)
      .slice(0, 10);
    setQuestions(shuffledQuestions);
    setCurrentQuestionIndex(0);
    setScore(0);
    setSelectedOption(null);
    setShowResult(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h4 className="font-bold text-gray-800 mb-8">
        Periodic Table Quiz: Test Your Knowledge of the First 20 Elements
      </h4>
      {showResult ? (
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800">Quiz Completed!</h2>
          <p className="mt-4 text-lg text-gray-600">
            Your score: <span className="text-blue-500">{score}</span> out of{" "}
            <span className="text-blue-500">{questions.length}</span>
          </p>
          {score < 5 && (
            <div className="mt-4 text-red-500">
              <p>Your score is below 5. Don't worry, keep practicing!</p>
              <p>Try again to improve your knowledge and score!</p>
            </div>
          )}
          <button
            className="mt-6 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 mb-3"
            onClick={handleRestart}
          >
            Restart Quiz
          </button>
          <br />
        </div>
      ) : (
        questions.length > 0 && (
          <div className="w-full max-w-3xl bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">
              Question {currentQuestionIndex + 1} of {questions.length}
            </h2>
            <p className="text-gray-700 mb-6">
              {questions[currentQuestionIndex].question}
            </p>
            <div className="grid gap-4">
              {questions[currentQuestionIndex].options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleOptionClick(option)}
                  className={`px-4 py-2 rounded-md text-left w-full ${
                    selectedOption === option
                      ? "bg-blue-500 text-white"
                      : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>
            <button
              onClick={handleNextQuestion}
              disabled={selectedOption === null}
              className="mt-6 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300"
            >
              {currentQuestionIndex === questions.length - 1
                ? "Finish Quiz"
                : "Next Question"}
            </button>
          </div>
        )
      )}
    </div>
  );
};

export default Quiz;
