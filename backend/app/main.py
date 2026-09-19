import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .database import Base, engine, SessionLocal
from .routes import leads, stats, export
from .seed.demo_data import seed


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title='Caprae Lead Intelligence', version='1.0.0', lifespan=lifespan,
              description='Synthetic interview demo. Format validation is not external verification.')
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',') if x.strip()], allow_methods=['GET'], allow_headers=['Accept', 'Content-Type'])
# Static export path must be registered before /leads/{lead_id}.
app.include_router(export.router)
app.include_router(leads.router)
app.include_router(stats.router)

FRONTEND_DIR = None
if os.getenv('SERVE_FRONTEND', '').lower() == 'true':
    FRONTEND_DIR = Path(__file__).resolve().parents[2] / 'frontend' / 'dist'
    if not (FRONTEND_DIR / 'index.html').is_file():
        raise RuntimeError('Frontend build missing. Run npm ci and npm run build inside frontend first.')
    app.mount('/assets', StaticFiles(directory=FRONTEND_DIR / 'assets'), name='frontend-assets')


@app.get('/')
def root():
    if FRONTEND_DIR:
        return FileResponse(FRONTEND_DIR / 'index.html', headers={'Cache-Control': 'no-cache'})
    return {'name': 'Caprae Lead Intelligence', 'dataset': 'Demo / Synthetic Data', 'docs': '/docs'}


@app.get('/health')
def health():
    return {'status': 'ok'}
