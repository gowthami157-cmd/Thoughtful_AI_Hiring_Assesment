import React from 'react';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isFromAgent: boolean;
  timestamp: Date;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, isFromAgent, timestamp }) => {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`flex items-start space-x-3 mb-4 ${isFromAgent ? '' : 'flex-row-reverse space-x-reverse'}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isFromAgent 
          ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' 
          : 'bg-gradient-to-br from-gray-500 to-gray-600 text-white'
      }`}>
        {isFromAgent ? <Bot size={16} /> : <User size={16} />}
      </div>
      
      <div className={`flex-grow max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl ${isFromAgent ? '' : 'text-right'}`}>
        <div className={`inline-block px-4 py-3 rounded-2xl shadow-sm ${
          isFromAgent 
            ? 'bg-white text-gray-800 rounded-bl-md' 
            : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-br-md'
        }`}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
        </div>
        <p className={`text-xs text-gray-500 mt-1 ${isFromAgent ? 'text-left' : 'text-right'}`}>
          {formatTime(timestamp)}
        </p>
      </div>
    </div>
  );
};