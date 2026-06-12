# apps/public_api/routers/api_v1_routers.py

from fastapi import APIRouter

# Import routers from different feature packages (without any business logic)
# Example: from features.auth import auth_router
# Example: from features.pomodoro import pomodoro_router

# Create the main application router for API V1 (Master Router)
api_v1_router = APIRouter(prefix="/api/v1")

# Include feature routers in the main router with dedicated prefixes and Swagger tags
# api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# api_v1_router.include_router(pomodoro_router, prefix="/pomodoro", tags=["Pomodoro"])
