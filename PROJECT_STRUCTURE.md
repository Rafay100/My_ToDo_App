# TaskFlow AI - Project Structure

## Root Directory

```
My_ToDo/
├── README.md                           # Project overview and quick start
├── CLAUDE.md                           # Claude Code Rules
├── PROJECT_STRUCTURE.md                # This file
├── cookies.txt                         # Temporary file (if needed)
├── nul                                 # Placeholder file
├── package.json                        # Frontend package manifest
├── package-lock.json                   # Frontend lock file
├── IMPLEMENTATION_NOTES.md            # Implementation details
├── MODERN_UI_FEATURES.md              # UI feature documentation
├── PHASE_IV_COMPLETION_REPORT.md      # Phase completion documentation
├── STARTUP_GUIDE.md                   # Startup guide
├── temp_feature_desc.txt              # Temporary feature description
├── specs/                             # Feature specifications
│   └── todo-app/                      # Todo application feature
│       ├── spec.md                    # Feature requirements
│       ├── plan.md                    # Architecture & implementation plan
│       ├── tasks.md                   # Implementation tasks
│       └── intelligence/              # Requirements & research
│           └── market_research.md     # Market research and intelligence
├── history/                           # Development artifacts
│   ├── specs/                         # Historical specs
│   ├── plans/                         # Historical plans
│   ├── tasks/                         # Historical tasks
│   ├── adrs/                          # Architectural decision records
│   └── prompts/                       # AI interaction history
├── frontend/                          # Frontend application
│   ├── package.json
│   ├── next.config.mjs
│   ├── tsconfig.json
│   ├── src/
│   │   ├── app/                       # Next.js app router
│   │   │   ├── page.tsx               # Home page
│   │   │   ├── layout.tsx             # Root layout
│   │   │   ├── home-page.tsx          # Homepage component
│   │   │   ├── dashboard/             # Dashboard page
│   │   │   ├── new-auth/              # New authentication pages
│   │   │   │   ├── signin/
│   │   │   │   └── signup/
│   │   │   ├── chat/                  # Chat page
│   │   │   ├── calendar/              # Calendar page
│   │   │   └── tags/                  # Tags page
│   │   ├── components/                # Reusable components
│   │   │   ├── ui/                    # UI components
│   │   │   ├── AppLayout.tsx          # Main layout component
│   │   │   ├── auth-provider.tsx      # Authentication context
│   │   │   ├── theme-provider.tsx     # Theme context
│   │   │   └── TaskCard.tsx           # Task card component
│   │   ├── services/                  # API services
│   │   │   ├── todo_api.ts            # Todo API service
│   │   │   ├── auth_client.ts         # Auth API service
│   │   │   └── apiClient.ts           # General API client
│   │   └── types/                     # Type definitions
│   ├── public/                        # Static assets
│   └── .env.local                     # Environment variables
└── backend/                           # Backend API
    ├── requirements.txt               # Python dependencies
    ├── pyproject.toml                 # Project configuration
    ├── src/
    │   ├── main.py                    # Main application entry point
    │   ├── db.py                      # Database configuration
    │   ├── models/
    │   │   └── models.py              # Data models
    │   └── api/
    │       ├── auth.py                # Authentication endpoints
    │       ├── todos.py               # Todo endpoints
    │       ├── auth_middleware.py     # Authentication middleware
    │       └── chat_endpoint.py       # Chat endpoints
    ├── init_db.py                     # Database initialization
    ├── Dockerfile                     # Container configuration
    ├── tests/                         # Test files
    └── venv/                          # Virtual environment
```

## Key Directories Explained

### specs/todo-app/
Contains the specification documents for the todo application following the Spec-Kit methodology:
- **spec.md**: Defines feature requirements and user stories
- **plan.md**: Outlines architecture and implementation approach
- **tasks.md**: Lists implementation tasks with acceptance criteria
- **intelligence/**: Contains market research and technical intelligence

### history/
Stores historical development artifacts for traceability:
- **specs/**: Previous versions of specifications
- **plans/**: Historical implementation plans
- **tasks/**: Completed task records
- **adrs/**: Architectural decision records
- **prompts/**: AI interaction history for learning

### frontend/
Modern Next.js application with:
- App Router structure for optimal performance
- Component-based architecture
- Service layer for API communication
- Authentication context management
- Responsive UI components

### backend/
FastAPI-based API server with:
- Authentication and authorization
- Todo management endpoints
- Database models and ORM
- Chat and AI integration endpoints