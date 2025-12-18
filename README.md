# Weather Check App

A full-stack weather application with AI-powered tool calling. Ask questions about weather in natural language and get real-time weather information powered by LangChain and OpenWeatherMap API.

## Features

- 🤖 AI-powered natural language weather queries
- 🌤️ Real-time weather data from OpenWeatherMap
- 🔧 LangChain tool calling with OpenRouter
- ⚡ Fast and responsive UI built with Next.js
- 🎨 Dark themed interface

## Live Demo

- **Deployed**: https://weather-check-wheat.vercel.app/

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- OpenRouter API key
- OpenWeatherMap API key

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd sanchai
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

Run the backend server:

```bash
python main.py
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup

Navigate to the root directory:

```bash
cd ..
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend will start on `http://localhost:3000`


## Usage

1. Open the application in your browser
2. Type a weather query in natural language (e.g., "What's the weather in Kolkata?")
3. Click Send or press Enter
4. The AI will process your request and fetch real-time weather data



## Technologies Used

### Frontend
- Next.js 14
- React
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- LangChain
- OpenAI (via OpenRouter)
- Python

### APIs
- OpenRouter (LLM)
- OpenWeatherMap (Weather data)

## Deployment

### Backend (Render)
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables in Render dashboard
4. Deploy

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Vercel will auto-detect Next.js
3. Deploy

## API Endpoints

### Backend

- `GET /` - Health check
- `POST /chat` - Send weather queries
  ```json
  {
    "message": "What's the weather in Kolkata?"
  }
  ```

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
