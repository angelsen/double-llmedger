# Double LLMedger Backend Architecture

## Directory Structure
```
backend/
├── __init__.py
├── alembic/                # Database migrations
├── api/                    # API endpoints
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── dashboard.py        # Dashboard data
│   ├── transactions.py     # Transaction management
│   └── dependencies.py     # Shared API dependencies
├── core/                   # Core application components
│   ├── __init__.py
│   ├── config.py           # App configuration
│   ├── security.py         # Authentication & authorization
│   └── exceptions.py       # Custom exceptions
├── db/                     # Database models & setup
│   ├── __init__.py
│   ├── database.py         # SQLAlchemy session
│   └── models/             # Database models
│       ├── __init__.py
│       ├── user.py         # User and session models
│       ├── transaction.py  # Financial transactions
│       └── account.py      # Chart of accounts
├── schemas/                # Pydantic models
│   ├── __init__.py
│   ├── user.py             # User schemas
│   └── transaction.py      # Transaction schemas
├── services/               # Business logic
│   ├── __init__.py
│   ├── auth.py             # Authentication service
│   └── dashboard.py        # Dashboard data service
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── helpers.py
└── main.py                 # Application entry point
```

## Key Components

### Database (SQLAlchemy ORM)
- Replace direct SQLite access with SQLAlchemy models
- Map to existing tables created by Lucia auth
- Add migration support with Alembic

### API (FastAPI)
- Organize routes into separate modules
- Use dependency injection for auth
- Maintain compatibility with frontend

### Authentication
- Implement session validation compatible with Lucia cookies
- Use Pydantic for request/response validation
- Improve error handling

## Future Expansion
This structure easily accommodates planned features:
- Invoice processing (LayoutLM)
- Double-entry accounting
- Payment planning
- Messaging queue

## Implementation Priority
1. Set up basic SQLAlchemy models for users/sessions
2. Implement authentication service
3. Migrate existing dashboard endpoint
4. Add test coverage