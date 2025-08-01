# Thoughtful AI Customer Support Agent

A Python-based customer support AI agent built with Streamlit that helps users learn about Thoughtful AI's healthcare automation services.

## Features

- **Interactive Chat Interface**: Clean, modern web-based chat UI
- **Intelligent Question Matching**: Uses text similarity algorithms to find relevant answers
- **Predefined Knowledge Base**: Answers questions about EVA, CAM, PHIL, and other Thoughtful AI services
- **Fallback Responses**: Graceful handling of questions outside the knowledge base
- **Error Handling**: Robust input validation and error management
- **Real-time Statistics**: Message count and system status display
- **Sample Questions**: Quick access to common queries
- **Chat History**: Persistent conversation history with timestamps

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

## Usage

1. **Ask Questions**: Type your questions about Thoughtful AI's services in the input field
2. **Get Instant Answers**: The agent will provide relevant responses based on the predefined knowledge base
3. **Use Sample Questions**: Click on the sample questions in the sidebar for quick access
4. **Clear Chat**: Use the "Clear Chat" button to start a new conversation

## Supported Topics

- **EVA (Eligibility Verification Agent)**: Patient eligibility and benefits verification
- **CAM (Claims Processing Agent)**: Claims submission and management
- **PHIL (Payment Posting Agent)**: Automated payment posting and reconciliation
- **General Thoughtful AI Services**: Overview of automation agents and benefits

## Technical Implementation

### Core Components

1. **ChatService**: Handles question matching and response generation
   - Text preprocessing and similarity calculation
   - Enhanced matching with key term boosting
   - Error handling and input validation

2. **Streamlit App**: Web interface and user interaction
   - Real-time chat display with message bubbles
   - Input handling and response processing
   - Statistics and navigation features

### Algorithm Details

- **Text Similarity**: Uses word overlap and Jaccard similarity
- **Key Term Boosting**: Enhances matching for domain-specific terms
- **Fallback System**: Provides helpful responses for unmatched queries
- **Input Validation**: Handles edge cases and invalid inputs

## Customization

To add new questions and answers, modify the `PREDEFINED_DATA` list in `chat_service.py`:

```python
{
    "question": "Your new question here?",
    "answer": "Your detailed answer here."
}
```

To customize fallback responses, update the `FALLBACK_RESPONSES` list in the same file.

## Error Handling

The system includes comprehensive error handling for:
- Empty or invalid inputs
- Overly long questions (500+ characters)
- Processing errors and exceptions
- Network or system issues

## Performance

- **Response Time**: ~0.5-1.5 seconds including simulated thinking time
- **Accuracy**: High precision for predefined topics with intelligent fallback
- **Scalability**: Easily extensible knowledge base and response system