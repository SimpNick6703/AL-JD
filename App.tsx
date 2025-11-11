
import React, { useState, useCallback } from 'react';
import { Article, View } from './types';
import { generateRandomTips, generateArticleFromTopic } from './services/apiService';
import HomePage from './components/HomePage';
import ArticlesListPage from './components/ArticlesListPage';
import ArticleDetailPage from './components/ArticleDetailPage';
import LoadingSpinner from './components/LoadingSpinner';

const App: React.FC = () => {
  const [view, setView] = useState<View>(View.Home);
  const [articles, setArticles] = useState<Article[]>([]);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = useCallback(async (topic?: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const generatedArticles = topic
        ? await generateArticleFromTopic(topic)
        : await generateRandomTips();
      setArticles(generatedArticles);
      setView(View.List);
    } catch (err) {
      console.error("Generation failed:", err);
      setError("Sorry, something went wrong while generating content. Please try again.");
      // Stay on home page if error occurs
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleSelectArticle = (article: Article) => {
    setSelectedArticle(article);
    setView(View.Detail);
  };
  
  const handleUpdateArticle = (updatedArticle: Article) => {
    setSelectedArticle(updatedArticle);
    setArticles(prevArticles => prevArticles.map(a => a.id === updatedArticle.id ? updatedArticle : a));
  };

  const navigateBackToList = () => {
    setSelectedArticle(null);
    setView(View.List);
  };
  
  const navigateBackToHome = () => {
      setArticles([]);
      setView(View.Home);
  }

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="min-h-screen flex flex-col justify-center items-center">
          <LoadingSpinner />
          <p className="mt-4 text-lg text-gray-300">Generating content, please wait...</p>
        </div>
      );
    }
    
    if (error && view === View.Home) {
       return (
         <div className="min-h-screen flex flex-col justify-center items-center">
            <p className="text-red-400 mb-4">{error}</p>
            <HomePage onGenerate={handleGenerate} />
         </div>
       );
    }

    switch (view) {
      case View.List:
        return <ArticlesListPage articles={articles} onSelectArticle={handleSelectArticle} onBack={navigateBackToHome} />;
      case View.Detail:
        if (selectedArticle) {
          return <ArticleDetailPage article={selectedArticle} onUpdateArticle={handleUpdateArticle} onBack={navigateBackToList} />;
        }
        // Fallback if no article selected
        setView(View.List); 
        return null;
      case View.Home:
      default:
        return <HomePage onGenerate={handleGenerate} />;
    }
  };

  return (
    <div className="bg-gray-900 min-h-screen text-white font-sans">
      {renderContent()}
    </div>
  );
};

export default App;
