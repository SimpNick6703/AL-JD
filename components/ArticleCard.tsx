
import React from 'react';
import { Article } from '../types';
import { ArrowRightIcon } from './icons';

interface ArticleCardProps {
  article: Article;
  onReadMore: (article: Article) => void;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, onReadMore }) => {
  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 flex flex-col h-full transform hover:-translate-y-1 transition-transform duration-300 shadow-lg hover:shadow-indigo-500/30">
      <h3 className="text-xl font-bold text-white mb-3 flex-grow">{article.title}</h3>
      <p className="text-gray-400 mb-4 text-sm">{article.description}</p>
      <button
        onClick={() => onReadMore(article)}
        className="mt-auto self-start inline-flex items-center gap-2 text-indigo-400 font-semibold hover:text-indigo-300 transition-colors"
      >
        Read More
        <ArrowRightIcon className="w-4 h-4" />
      </button>
    </div>
  );
};

export default ArticleCard;
