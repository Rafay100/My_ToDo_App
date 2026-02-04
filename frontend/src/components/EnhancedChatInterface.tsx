'use client';

/**
 * Enhanced ChatInterface component with modern UI design
 * Features AI-powered chat with visual indicators and smart interactions
 */
import { useState, useEffect, useRef } from 'react';
import { apiClient, ChatResponse } from '../services/apiClient';
import { CheckCircle2, Clock, RotateCcw, Zap, Bot, User, Sparkles, Loader2, CheckCheck, Flame, Repeat } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  status?: 'sent' | 'delivered' | 'read'; // For message status indicators
  toolsUsed?: string[]; // Track which AI tools were used
  actionStatus?: 'success' | 'pending' | 'error'; // For inline confirmations
}

interface ChatInterfaceProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [aiStatus, setAiStatus] = useState<'idle' | 'thinking' | 'typing'>('idle');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setAiStatus('thinking');

    try {
      // Simulate AI thinking delay for better UX
      await new Promise(resolve => setTimeout(resolve, 800));

      // Send message to backend
      const response: ChatResponse = await apiClient.sendChatMessage(
        userId,
        inputValue,
        conversationId || undefined
      );

      // Update conversation ID if this is the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Determine if AI performed any actions and set appropriate status
      let actionStatus: 'success' | 'pending' | 'error' | undefined;
      let toolsUsed: string[] = [];

      // Simple heuristic to detect actions from AI response
      if (response.response.toLowerCase().includes('created') || response.response.toLowerCase().includes('added')) {
        actionStatus = 'success';
        toolsUsed = ['add_task'];
      } else if (response.response.toLowerCase().includes('completed') || response.response.toLowerCase().includes('done')) {
        actionStatus = 'success';
        toolsUsed = ['complete_task'];
      } else if (response.response.toLowerCase().includes('reminder')) {
        actionStatus = 'success';
        toolsUsed = ['schedule_reminder'];
      }

      // Add AI response to messages
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        status: 'delivered',
        toolsUsed,
        actionStatus
      };

      setAiStatus('typing');
      // Simulate typing delay for more realistic interaction
      await new Promise(resolve => setTimeout(resolve, 500));
      setAiStatus('idle');

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to UI
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'system',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
        actionStatus: 'error'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setAiStatus('idle');
    }
  };

  // Render message status indicator
  const renderStatusIndicator = (status: Message['status']) => {
    switch (status) {
      case 'sent':
        return <Clock className="h-3 w-3 text-muted-foreground" />;
      case 'delivered':
        return <CheckCircle2 className="h-3 w-3 text-muted-foreground" />;
      case 'read':
        return <CheckCheck className="h-3 w-3 text-primary" />;
      default:
        return null;
    }
  };

  // Render AI tool usage badges
  const renderToolBadges = (tools: string[] = []) => {
    if (!tools || tools.length === 0) return null;

    return (
      <div className="flex flex-wrap gap-1 mt-2">
        {tools.map((tool, index) => (
          <Badge key={index} variant="secondary" className="text-xs">
            <Zap className="h-2.5 w-2.5 mr-1" />
            {tool.replace('_', ' ')}
          </Badge>
        ))}
      </div>
    );
  };

  // Render inline action status
  const renderActionStatus = (actionStatus: Message['actionStatus']) => {
    if (!actionStatus) return null;

    switch (actionStatus) {
      case 'success':
        return (
          <Badge variant="secondary" className="ml-2 text-xs">
            <CheckCircle2 className="h-2.5 w-2.5 mr-1 text-green-500" />
            Action completed
          </Badge>
        );
      case 'pending':
        return (
          <Badge variant="secondary" className="ml-2 text-xs">
            <Loader2 className="h-2.5 w-2.5 mr-1 text-yellow-500 animate-spin" />
            Processing...
          </Badge>
        );
      case 'error':
        return (
          <Badge variant="destructive" className="ml-2 text-xs">
            <span>Error</span>
          </Badge>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto bg-background rounded-xl shadow-lg overflow-hidden border">
      {/* Chat header with AI status */}
      <div className="bg-muted/50 px-4 py-3 border-b backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Bot className="h-6 w-6 text-primary" />
              {aiStatus !== 'idle' && (
                <div className="absolute -bottom-1 -right-1 h-3 w-3 rounded-full bg-green-500 border-2 border-background">
                  <div className="h-full w-full rounded-full bg-green-400 animate-ping opacity-75"></div>
                </div>
              )}
            </div>
            <div>
              <h2 className="text-lg font-semibold text-foreground">AI Task Assistant</h2>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                {aiStatus === 'thinking' && (
                  <>
                    <Loader2 className="h-3 w-3 animate-spin" />
                    <span>Processing your request...</span>
                  </>
                )}
                {aiStatus === 'typing' && (
                  <>
                    <Sparkles className="h-3 w-3" />
                    <span>Preparing response...</span>
                  </>
                )}
                {aiStatus === 'idle' && (
                  <span>Ready to help with your tasks</span>
                )}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {conversationId && (
              <Badge variant="outline" className="text-xs">
                {conversationId.substring(0, 8)}...
              </Badge>
            )}
            <Button variant="ghost" size="icon">
              <RotateCcw className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-background/30 min-h-[500px]">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center py-12">
            <div className="mb-6 p-3 rounded-full bg-primary/10">
              <Bot className="h-10 w-10 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2">Welcome to TaskFlow AI</h3>
            <p className="text-muted-foreground max-w-md mb-6">
              Your intelligent assistant for managing tasks with natural language
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-lg">
              <div className="bg-muted/50 p-4 rounded-lg border">
                <div className="flex items-center gap-2 mb-2">
                  <Flame className="h-4 w-4 text-orange-500" />
                  <span className="font-medium">Quick Actions</span>
                </div>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>"Add a task to buy groceries"</li>
                  <li>"Show me my tasks"</li>
                  <li>"Mark my meeting as complete"</li>
                </ul>
              </div>

              <div className="bg-muted/50 p-4 rounded-lg border">
                <div className="flex items-center gap-2 mb-2">
                  <Repeat className="h-4 w-4 text-blue-500" />
                  <span className="font-medium">Smart Features</span>
                </div>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>"Remind me to call John tomorrow"</li>
                  <li>"Schedule weekly team sync"</li>
                  <li>"Prioritize urgent tasks"</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl p-4 relative ${
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground rounded-br-none'
                    : message.role === 'assistant'
                    ? 'bg-muted text-foreground rounded-bl-none'
                    : 'bg-destructive/10 text-destructive-foreground'
                }`}
              >
                {/* Message header */}
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {message.role === 'user' ? (
                      <User className="h-4 w-4 opacity-80" />
                    ) : message.role === 'assistant' ? (
                      <Bot className="h-4 w-4 opacity-80" />
                    ) : (
                      <span className="text-xs font-medium">SYSTEM</span>
                    )}
                    <span className="text-xs font-medium opacity-90">
                      {message.role === 'user'
                        ? 'You'
                        : message.role === 'assistant'
                        ? 'AI Assistant'
                        : 'System'}
                    </span>
                  </div>

                  <div className="flex items-center gap-1">
                    {renderStatusIndicator(message.status)}
                    {renderActionStatus(message.actionStatus)}
                    <span className="text-xs opacity-70 ml-1">
                      {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>

                {/* Message content */}
                <div className="text-sm leading-relaxed">{message.content}</div>

                {/* Tool usage badges */}
                {message.toolsUsed && renderToolBadges(message.toolsUsed)}
              </div>
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[85%] bg-muted text-foreground rounded-2xl p-4 rounded-bl-none">
              <div className="flex items-center gap-2 mb-2">
                <Bot className="h-4 w-4 opacity-80" />
                <span className="text-xs font-medium opacity-90">AI Assistant</span>
              </div>
              <div className="flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-sm">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="border-t bg-background p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask me to manage your tasks..."
            disabled={isLoading}
            className="flex-1 border border-input rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/20 bg-background placeholder:text-muted-foreground"
          />
          <Button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="px-6 py-3 rounded-xl gap-2 bg-primary hover:bg-primary/90 transition-all"
          >
            <span>Send</span>
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-3">
          <Badge variant="secondary" className="text-xs cursor-pointer hover:bg-accent">
            Add task
          </Badge>
          <Badge variant="secondary" className="text-xs cursor-pointer hover:bg-accent">
            Show tasks
          </Badge>
          <Badge variant="secondary" className="text-xs cursor-pointer hover:bg-accent">
            Complete task
          </Badge>
          <Badge variant="secondary" className="text-xs cursor-pointer hover:bg-accent">
            Set reminder
          </Badge>
        </div>
      </form>
    </div>
  );
}