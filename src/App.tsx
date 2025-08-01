import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { TypingIndicator } from './components/TypingIndicator';
import { ChatService } from './services/chatService';
import { Bot, Sparkles } from 'lucide-react';

interface Message {
  id: string;
  message: string;
  isFromAgent: boolean;
  timestamp: Date;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages, isLoading]);

  useEffect(() => {
    // Add welcome message on component mount
    const welcomeMessage: Message = {
      id: Date.now().toString(),
      message: "Hello! I'm your Thoughtful AI support assistant. I can help you learn about our automation agents like EVA (Eligibility Verification), CAM (Claims Processing), and PHIL (Payment Posting). What would you like to know?",
      isFromAgent: true,
      timestamp: new Date()
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleSendMessage = async (userInput: string) => {
    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      ...ChatService.createUserMessage(userInput)
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Process the user input and get agent response
      const agentResponse = await ChatService.processUserInput(userInput);
      
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        ...agentResponse
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      // Handle any unexpected errors
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        message: "I apologize, but I encountered an unexpected error. Please try asking your question again.",
        isFromAgent: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    const welcomeMessage: Message = {
      id: Date.now().toString(),
      message: "Chat cleared! I'm here to help you learn about Thoughtful AI's automation agents. What would you like to know?",
      isFromAgent: true,
      timestamp: new Date()
    };
    setMessages([welcomeMessage]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center">
                <Bot className="text-white" size={24} />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Thoughtful AI Support</h1>
                <p className="text-sm text-gray-600">Healthcare Automation Assistant</p>
              </div>
            </div>
            <button
              onClick={clearChat}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors duration-200"
            >
              Clear Chat
            </button>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto h-[calc(100vh-80px)] flex flex-col">
        {/* Messages Area */}
        <div className="flex-grow overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-blue-700 rounded-full flex items-center justify-center mb-4">
                <Sparkles className="text-white" size={32} />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Welcome to Thoughtful AI Support</h2>
              <p className="text-gray-600 max-w-md">
                I'm here to help you learn about our healthcare automation agents. 
                Ask me about EVA, CAM, PHIL, or any of our services!
              </p>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message.message}
                  isFromAgent={message.isFromAgent}
                  timestamp={message.timestamp}
                />
              ))}
              {isLoading && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default App;