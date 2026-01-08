# Todo App - Local Development Guide

This guide will help you run the Todo application on your localhost.

## Prerequisites

- **Node.js** (v20 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.11 or higher) - [Download](https://www.python.org/)
- **PostgreSQL** (v14 or higher) OR use Neon Cloud Database - [Neon Setup](https://neon.tech/)
- **Docker & Docker Compose** (optional, for containerized setup) - [Download](https://www.docker.com/)
- **npm** or **yarn** (comes with Node.js)

## Option 1: Local Development (Recommended for Development)

### Step 1: Clone and Setup

```bash
cd todo_app
```

### Step 2: Set Up Environment Variables

Copy the environment files and add your secrets:

```bash
# Already created, but verify they exist
ls .env
ls backend/.env
ls frontend/.env.local
```

You should see:
- `/backend/.env` - Has DATABASE_URL and BETTER_AUTH_SECRET
- `/frontend/.env.local` - Has BETTER_AUTH_SECRET

**Verify both files have the same BETTER_AUTH_SECRET:**

```bash
# Check backend secret
grep BETTER_AUTH_SECRET backend/.env

# Check frontend secret
grep BETTER_AUTH_SECRET frontend/.env.local
```

Both should be identical.

### Step 3: Setup Backend

```bash
# Navigate to backend
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (create database tables)
# The database will be created automatically on first startup

# Start backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### Step 4: Setup Frontend (in a new terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# or with yarn
yarn install

# Start development server
npm run dev

# or with yarn
yarn dev
```

Frontend will be available at: **http://localhost:3000**

### Step 5: Open the App

1. Open your browser
2. Go to **http://localhost:3000**
3. Click "Sign Up" to create an account
4. Start creating tasks!

---

## Option 2: Docker Compose (Recommended for Testing)

### Step 1: Verify Docker is Installed

```bash
docker --version
docker-compose --version
```

### Step 2: Start Services

```bash
cd todo_app

# Start all services (PostgreSQL, Backend, Frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# To stop services
docker-compose down
```

Services will be available at:
- Frontend: **http://localhost:3000**
- Backend: **http://localhost:8000**
- PostgreSQL: **localhost:5432**

---

## Database Setup

### Option A: Neon Cloud Database (Recommended)

1. Go to [neon.tech](https://neon.tech/)
2. Create a free account
3. Create a new project
4. Copy the connection string
5. Update `DATABASE_URL` in `/backend/.env`:
   ```
   DATABASE_URL=postgresql://user:password@host/database?sslmode=require
   ```

### Option B: Local PostgreSQL

```bash
# macOS (with Homebrew)
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql
sudo systemctl start postgresql

# Windows
# Download and install from postgresql.org

# Create database
createdb todo_db

# Update DATABASE_URL in /backend/.env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
```

---

## Troubleshooting

### 1. Port Already in Use

If port 3000 or 8000 is already in use:

```bash
# Kill process on port 3000 (macOS/Linux)
lsof -ti:3000 | xargs kill -9

# Kill process on port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9

# Windows - use Task Manager or:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### 2. Database Connection Error

```
Error: could not connect to server
```

**Solution:**
- Verify DATABASE_URL is correct
- Check if PostgreSQL is running
- If using Neon, verify internet connection
- Check credentials in DATABASE_URL

### 3. "Module not found" Errors

```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 4. Port 5432 Already in Use

PostgreSQL is using the default port. Either:
- Stop the other PostgreSQL instance
- Change the port in DATABASE_URL

### 5. CORS Errors

Make sure `CORS_ORIGINS` in `/backend/.env` includes your frontend URL:

```
CORS_ORIGINS=http://localhost:3000
```

---

## Common Commands

### Backend Commands

```bash
# Start development server with auto-reload
uvicorn src.main:app --reload

# Run with specific host/port
uvicorn src.main:app --host 0.0.0.0 --port 8000

# View API documentation
# Open http://localhost:8000/docs in browser
```

### Frontend Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

### Database Commands

```bash
# Create database
createdb todo_db

# Connect to database
psql -U postgres -d todo_db

# Drop database
dropdb todo_db
```

---

## File Structure

```
todo_app/
├── backend/
│   ├── src/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings
│   │   ├── db/                  # Database
│   │   ├── models/              # SQLModel models
│   │   ├── routes/              # API endpoints
│   │   ├── schemas/             # Pydantic schemas
│   │   └── auth.py              # JWT authentication
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   ├── components/          # React components
│   │   ├── lib/                 # Utilities
│   │   └── types/               # TypeScript types
│   ├── package.json             # Node dependencies
│   ├── .env.local               # Environment variables
│   └── Dockerfile
├── docker-compose.yml           # Docker configuration
├── .env                         # Root environment
└── QUICKSTART.md                # This file
```

---

## API Endpoints

### Authentication

- `POST /api/auth/register` - Sign up
- `POST /api/auth/login` - Sign in
- `POST /api/auth/logout` - Sign out
- `GET /api/auth/me` - Current user

### Tasks

- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle completion

---

## Next Steps

1. **Create an account** at http://localhost:3000/signup
2. **Sign in** at http://localhost:3000/login
3. **Create tasks** on the dashboard
4. **Edit/Delete tasks** using the buttons
5. **Filter tasks** by status using the filter tabs

---

## Help & Support

- **API Docs**: http://localhost:8000/docs
- **Frontend Errors**: Check browser console (F12)
- **Backend Errors**: Check terminal where backend is running

---

## Production Deployment

To deploy to production:

1. Use Docker Compose with environment variables
2. Set up Neon PostgreSQL
3. Deploy frontend to Vercel/Netlify
4. Deploy backend to Railway/Render/Heroku

See `DEPLOYMENT.md` for detailed instructions.
