interface Question {
  question: string;
  answer: string;
}

interface ChatResponse {
  message: string;
  isFromAgent: boolean;
  timestamp: Date;
}

const PREDEFINED_DATA: Question[] = [
  {
    question: "What does the eligibility verification agent (EVA) do?",
    answer: "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
  },
  {
    question: "What does the claims processing agent (CAM) do?",
    answer: "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
  },
  {
    question: "How does the payment posting agent (PHIL) work?",
    answer: "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
  },
  {
    question: "Tell me about Thoughtful AI's Agents.",
    answer: "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
  },
  {
    question: "What are the benefits of using Thoughtful AI's agents?",
    answer: "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
  }
];

const FALLBACK_RESPONSES = [
  "I'm here to help you learn about Thoughtful AI's automation agents. Could you ask me about EVA, CAM, PHIL, or our general services?",
  "I specialize in questions about Thoughtful AI's healthcare automation solutions. What would you like to know about our agents?",
  "I'm designed to help with questions about Thoughtful AI's services. Feel free to ask about our eligibility verification, claims processing, or payment posting agents!",
  "That's an interesting question! I'm focused on helping with Thoughtful AI-related inquiries. How can I assist you with our automation agents?"
];

// Simple text similarity function using word overlap
function calculateSimilarity(text1: string, text2: string): number {
  const words1 = text1.toLowerCase().split(/\s+/).filter(word => word.length > 2);
  const words2 = text2.toLowerCase().split(/\s+/).filter(word => word.length > 2);
  
  const intersection = words1.filter(word => words2.includes(word));
  const union = [...new Set([...words1, ...words2])];
  
  return intersection.length / union.length;
}

// Enhanced similarity that also checks for key terms
function enhancedSimilarity(userInput: string, question: string): number {
  const baseSimilarity = calculateSimilarity(userInput, question);
  
  // Boost score for key terms
  const keyTerms = ['eva', 'cam', 'phil', 'agent', 'eligibility', 'claims', 'payment', 'benefits'];
  const userLower = userInput.toLowerCase();
  const questionLower = question.toLowerCase();
  
  let boost = 0;
  keyTerms.forEach(term => {
    if (userLower.includes(term) && questionLower.includes(term)) {
      boost += 0.2;
    }
  });
  
  return Math.min(baseSimilarity + boost, 1.0);
}

export class ChatService {
  private static readonly SIMILARITY_THRESHOLD = 0.1;

  static async processUserInput(userInput: string): Promise<ChatResponse> {
    try {
      // Validate input
      if (!userInput || userInput.trim().length === 0) {
        throw new Error("Please enter a valid question.");
      }

      if (userInput.trim().length > 500) {
        throw new Error("Please keep your question under 500 characters.");
      }

      const trimmedInput = userInput.trim();
      
      // Find the best matching question
      let bestMatch: Question | null = null;
      let bestScore = 0;

      for (const item of PREDEFINED_DATA) {
        const score = enhancedSimilarity(trimmedInput, item.question);
        if (score > bestScore) {
          bestScore = score;
          bestMatch = item;
        }
      }

      // Simulate thinking delay for more natural interaction
      await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));

      let responseMessage: string;

      if (bestMatch && bestScore > this.SIMILARITY_THRESHOLD) {
        responseMessage = bestMatch.answer;
      } else {
        // Use random fallback response
        const randomIndex = Math.floor(Math.random() * FALLBACK_RESPONSES.length);
        responseMessage = FALLBACK_RESPONSES[randomIndex];
      }

      return {
        message: responseMessage,
        isFromAgent: true,
        timestamp: new Date()
      };

    } catch (error) {
      return {
        message: error instanceof Error ? error.message : "I encountered an error processing your request. Please try again.",
        isFromAgent: true,
        timestamp: new Date()
      };
    }
  }

  static createUserMessage(userInput: string): ChatResponse {
    return {
      message: userInput,
      isFromAgent: false,
      timestamp: new Date()
    };
  }
}