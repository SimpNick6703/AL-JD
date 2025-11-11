
import React from 'react';

interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  const renderLine = (line: string, index: number) => {
    if (line.startsWith('### ')) {
      return <h3 key={index} className="text-xl font-semibold mt-4 mb-2">{line.substring(4)}</h3>;
    }
    if (line.startsWith('## ')) {
      return <h2 key={index} className="text-2xl font-bold mt-6 mb-3 border-b border-gray-600 pb-2">{line.substring(3)}</h2>;
    }
    if (line.startsWith('# ')) {
      return <h1 key={index} className="text-3xl font-extrabold mt-8 mb-4 border-b-2 border-indigo-500 pb-2">{line.substring(2)}</h1>;
    }
    if (line.startsWith('* ') || line.startsWith('- ')) {
      return <li key={index} className="ml-6 list-disc">{line.substring(2)}</li>;
    }
    if (line.trim() === '') {
        return <br key={index} />;
    }

    // Basic inline formatting
    const parts = line.split(/(\*\*.*?\*\*|`.*?`)/g).filter(Boolean);
    return <p key={index} className="my-2 leading-relaxed">
        {parts.map((part, i) => {
            if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={i}>{part.slice(2, -2)}</strong>;
            }
            if (part.startsWith('`') && part.endsWith('`')) {
                return <code key={i} className="bg-gray-800 text-indigo-300 px-2 py-1 rounded-md text-sm">{part.slice(1, -1)}</code>;
            }
            return part;
        })}
    </p>;
  };
  
  const renderContent = () => {
    const blocks = content.split(/(\`\`\`[\s\S]*?\`\`\`)/g).filter(Boolean);

    return blocks.map((block, index) => {
      if (block.startsWith('```')) {
        const lines = block.split('\n');
        const lang = lines[0].substring(3);
        const code = lines.slice(1, -1).join('\n');
        return (
          <pre key={index} className="bg-gray-800 p-4 rounded-lg my-4 overflow-x-auto">
            <code className={`language-${lang}`}>{code}</code>
          </pre>
        );
      } else {
        return <div key={index}>{block.split('\n').map(renderLine)}</div>;
      }
    });
  };

  return <div className="prose prose-invert max-w-none">{renderContent()}</div>;
};

export default MarkdownRenderer;
