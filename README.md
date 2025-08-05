# 🎨 AI Image Generator - Monorepo

An AI-powered interior design platform with real product recommendations, built as a proper monorepo.

## 🏗️ Project Structure

```
ai-image-generator-openai/
├── frontend/          # React + TypeScript + Vite + shadcn/ui
├── backend/           # FastAPI + Python + OpenAI API
├── quick-start.sh     # One-click startup script
├── package.json       # Workspace configuration
├── requirements.txt   # Python dependencies
├── api_server.py     # Main backend server
└── README.md         # This file
```

## 🚀 Quick Start

**One command to start everything:**

```bash
./quick-start.sh
```

Or use npm scripts:
```bash
npm run dev          # Start both servers
npm run frontend:dev # Start frontend only
npm run backend:dev  # Start backend only
```

## 📦 Installation

```bash
npm run install:all
```

This will install:
- ✅ Node.js dependencies for frontend
- ✅ Python dependencies for backend
- ✅ All required packages and tools

## 🌐 Access URLs

Once running:
- **Frontend**: http://localhost:8080/ (or detected port)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Development

### Frontend (React + TypeScript)
```bash
cd frontend
npm run dev
```

### Backend (FastAPI + Python)
```bash
cd backend
python3 api_server.py
```

## 📋 Features

- 🖼️ **AI Image Analysis**: Upload images for detailed design analysis
- 🎨 **Design Recommendations**: Get specific transformation suggestions
- 🛍️ **Real Product Integration**: SerpAPI-powered product recommendations
- 🎯 **Multiple Styles**: Support for various design styles
- ⚡ **Fast Development**: Hot reload for both frontend and backend

## 🔑 API Keys

The quick-start script automatically sets:
- **OpenAI API Key**: For AI image generation
- **SerpAPI Key**: For product recommendations

## 🛠️ Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- shadcn/ui (components)
- Tailwind CSS (styling)
- React Router (navigation)
- TanStack Query (data fetching)

**Backend:**
- FastAPI (API server)
- Python 3.7+
- OpenAI API (AI generation)
- SerpAPI (product search)
- Uvicorn (ASGI server)

## 📝 License

MIT License - see LICENSE file for details. 