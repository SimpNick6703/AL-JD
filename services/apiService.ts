
import { Article, EditAction } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const generateRandomTips = async (): Promise<Article[]> => {
  const res = await fetch(`${API_BASE_URL}/api/articles/generate-tips`, {
    method: 'POST'
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Failed to generate tips');
  }
  return res.json();
};

export const generateArticleFromTopic = async (topic: string): Promise<Article[]> => {
  const res = await fetch(`${API_BASE_URL}/api/articles/from-topic`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic })
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Failed to generate article');
  }
  return res.json();
};

export const editArticleContent = async (content: string, action: EditAction): Promise<string> => {
  const res = await fetch(`${API_BASE_URL}/api/articles/edit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, action })
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || 'Failed to edit article');
  }
  const data = await res.json();
  return data.content;
};
