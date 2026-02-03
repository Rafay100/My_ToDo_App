/**
 * API Client service for connecting frontend to backend API
 */

interface ChatRequest {
  message: string;
  conversation_id?: string;
  metadata?: Record<string, any>;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  timestamp: string;
  status: 'success' | 'error';
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  /**
   * Send a chat message to the backend API
   */
  async sendChatMessage(userId: string, message: string, conversationId?: string): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  }

  /**
   * Get conversation history
   */
  async getConversationHistory(userId: string, conversationId: string) {
    try {
      const response = await fetch(`${this.baseUrl}/api/${userId}/conversations/${conversationId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error getting conversation history:', error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();

export type { ChatRequest, ChatResponse };