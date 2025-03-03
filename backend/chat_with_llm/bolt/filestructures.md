backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── news.py
│   │   │   │   ├── analysis.py
│   │   │   │   ├── assets.py
│   │   │   │   └── dashboard.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── news.py
│   │   ├── analysis.py
│   │   └── asset.py
│   └── schemas/
│       ├── __init__.py
│       ├── user.py
│       ├── news.py
│       ├── analysis.py
│       └── asset.py
└── requirements.txt