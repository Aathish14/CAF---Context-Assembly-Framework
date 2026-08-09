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

fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer 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',
    'HTTP-Referer': '<YOUR_SITE_URL>',
    'X-Title': '<YOUR_SITE_NAME>',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-4o',
    messages: [
      {
        role: 'user',
        content: 'What is the meaning of life?',
      },
    ],
  }),
});