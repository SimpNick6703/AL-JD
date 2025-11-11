
import React from 'react';
import { Article } from '../types';
import ArticleCard from './ArticleCard';
import { ArrowLeftIcon } from './icons';

interface ArticlesListPageProps {
  articles: Article[];
  onSelectArticle: (article: Article) => void;
  onBack: () => void;
}

const ArticlesListPage: React.FC<ArticlesListPageProps> = ({ articles, onSelectArticle, onBack }) => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center mb-8">
        <button onClick={onBack} className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors p-2 -ml-2">
            <ArrowLeftIcon className="w-5 h-5" /> Back
        </button>
      </div>
      <h2 className="text-3xl font-bold text-center mb-2">Generated Articles</h2>
      <p className="text-gray-400 text-center mb-8">Here's what the AI generated for you. Click "Read More" to dive in.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {articles.map(article => (
          <ArticleCard key={article.id} article={article} onReadMore={onSelectArticle} />
        ))}
      </div>
    </div>
  );
};

export default ArticlesListPage;
