# CS:GO Match Visualizer

A system for parsing and visualizing CS:GO tournament match statistics through:
1. Backend API for match logs parsing
2. Interactive dashboard for data visualization

## Quick Start
### Requirements: 
- Docker and Docker Compose

Run the project:

```bash
make up
```
*This will run both the Backend and the Frontend as Docker containers, using Docker Compose.*

## Slow Start
If you do not wish to run the project using Docker, you can instead manually start each service.

### Requirements:
- Python 3.12
- UV (Python Package Manager)
- npm 

### Backend
```bash
cd backend
make up
```

Running tests:

```bash
cd backend
make test
``` 

### Frontend
```bash
cd frontend
npm install
npm run dev
``` 
### URLs
Backend URL: `http://localhost:8000/docs` (Open API)
Frontend URL: `http://localhost:5173`
