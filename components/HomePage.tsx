
import React, { useState } from 'react';
import { SparklesIcon, ArrowRightIcon } from './icons';

interface HomePageProps {
  onGenerate: (topic?: string) => void;
}

const HomePage: React.FC<HomePageProps> = ({ onGenerate }) => {
  const [topic, setTopic] = useState('');

  const handleProceed = () => {
    if (topic.trim()) {
      onGenerate(topic);
    }
  };

  const handleRandom = () => {
    onGenerate();
  };
  
  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleProceed();
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-900">
      <div className="w-full max-w-2xl text-center">
        <div className="inline-block bg-indigo-500 p-4 rounded-full mb-6">
          <SparklesIcon className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
          AI Blog Generator
        </h1>
        <p className="text-lg md:text-xl text-gray-400 mb-8 max-w-xl mx-auto">
          Your personal AI assistant for creating high-quality programming content. Start with a topic or let us surprise you.
        </p>
        
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 shadow-2xl">
          <div className="flex flex-col sm:flex-row gap-4">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="e.g., 'React Hooks Best Practices'"
              className="flex-grow bg-gray-700 text-white placeholder-gray-500 border border-gray-600 rounded-md px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
            />
            <button
              onClick={handleProceed}
              disabled={!topic.trim()}
              className="flex items-center justify-center gap-2 bg-indigo-600 text-white font-semibold px-6 py-3 rounded-md hover:bg-indigo-500 disabled:bg-gray-600 disabled:cursor-not-allowed transition duration-200"
            >
              Proceed <ArrowRightIcon className="w-5 h-5" />
            </button>
          </div>
          <div className="relative flex items-center my-6">
            <div className="flex-grow border-t border-gray-600"></div>
            <span className="flex-shrink mx-4 text-gray-500">OR</span>
            <div className="flex-grow border-t border-gray-600"></div>
          </div>
          <button
            onClick={handleRandom}
            className="w-full flex items-center justify-center gap-2 bg-gray-700 text-white font-semibold px-6 py-3 rounded-md hover:bg-gray-600 transition duration-200"
          >
            <SparklesIcon className="w-5 h-5" />
            Generate 10 Random Tips
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
