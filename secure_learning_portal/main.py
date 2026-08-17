from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.request_middleware import RequestMiddleware
from database.database import Base, engine
from routers import auth_router, user_router, resource_router, admin_router, health_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure Learning Portal API",
    version="1.0.0",
    description="API quản lý tài nguyên học tập với JWT và phân quyền Admin/User"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestMiddleware)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(resource_router.router)
app.include_router(admin_router.router)
app.include_router(health_router.router)
