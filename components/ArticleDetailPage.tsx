
import React, { useState, useEffect, useCallback } from 'react';
import { Article, EditAction } from '../types';
import MarkdownRenderer from './MarkdownRenderer';
import { editArticleContent } from '../services/apiService';
import LoadingSpinner from './LoadingSpinner';
import { ArrowLeftIcon, SparklesIcon, SaveIcon, CopyIcon } from './icons';

interface ArticleDetailPageProps {
  article: Article;
  onUpdateArticle: (updatedArticle: Article) => void;
  onBack: () => void;
}

const ArticleDetailPage: React.FC<ArticleDetailPageProps> = ({ article, onUpdateArticle, onBack }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [copyButtonText, setCopyButtonText] = useState('Copy');

  const handleEdit = useCallback(async (action: EditAction) => {
    setIsEditing(true);
    try {
      const newContent = await editArticleContent(article.content, action);
      onUpdateArticle({ ...article, content: newContent });
    } catch (error) {
      console.error("Failed to edit article:", error);
      // Here you could set an error state and display a message to the user
    } finally {
      setIsEditing(false);
    }
  }, [article, onUpdateArticle]);

  const handleSave = () => {
    const blob = new Blob([article.content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${article.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(article.content).then(() => {
      setCopyButtonText('Copied!');
      setTimeout(() => setCopyButtonText('Copy'), 2000);
    });
  };

  const editActions = [
    { label: 'Summarize', action: EditAction.Summarize },
    { label: 'Expand', action: EditAction.Expand },
    { label: 'Rephrase', action: EditAction.Rephrase },
    { label: 'Fix Grammar', action: EditAction.FixGrammar },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center mb-6">
        <button onClick={onBack} className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors p-2 -ml-2">
            <ArrowLeftIcon className="w-5 h-5" /> Back to List
        </button>
      </div>

      <div className="lg:grid lg:grid-cols-3 lg:gap-8">
        <main className="lg:col-span-2 bg-gray-800/50 p-6 sm:p-8 rounded-lg border border-gray-700 relative">
          {isEditing && (
            <div className="absolute inset-0 bg-gray-900/80 flex flex-col justify-center items-center z-10 rounded-lg">
                <LoadingSpinner />
                <p className="mt-4 text-lg text-gray-300">AI is thinking...</p>
            </div>
          )}
          <h1 className="text-3xl md:text-4xl font-extrabold text-white mb-2">{article.title}</h1>
          <p className="text-gray-400 mb-6 italic">{article.description}</p>
          <div className="h-px bg-gray-700 mb-6"></div>
          <MarkdownRenderer content={article.content} />
        </main>

        <aside className="lg:col-span-1 mt-8 lg:mt-0">
          <div className="sticky top-8">
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <SparklesIcon className="w-6 h-6 text-indigo-400"/>
                    AI Editing Tools
                </h3>
                <div className="grid grid-cols-2 gap-3 mb-6">
                    {editActions.map(({label, action}) => (
                         <button 
                            key={action}
                            onClick={() => handleEdit(action)}
                            disabled={isEditing}
                            className="bg-gray-700 text-sm text-white px-4 py-2 rounded-md hover:bg-gray-600 disabled:opacity-50 disabled:cursor-wait transition-colors"
                         >
                             {label}
                         </button>
                    ))}
                </div>
                
                <h3 className="text-lg font-semibold text-white mb-4">Actions</h3>
                <div className="flex flex-col gap-3">
                    <button 
                        onClick={handleSave}
                        className="w-full flex items-center justify-center gap-2 bg-indigo-600 text-white font-semibold px-4 py-2 rounded-md hover:bg-indigo-500 transition-colors"
                    >
                        <SaveIcon />
                        Save as Markdown
                    </button>
                    <button 
                        onClick={handleCopy}
                        className="w-full flex items-center justify-center gap-2 bg-gray-700 text-white font-semibold px-4 py-2 rounded-md hover:bg-gray-600 transition-colors"
                    >
                        <CopyIcon />
                        {copyButtonText}
                    </button>
                </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default ArticleDetailPage;
