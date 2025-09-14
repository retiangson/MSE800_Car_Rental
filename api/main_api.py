from fastapi import FastAPI
from api import cars_api, users_api, rentals_api
from Business.Services.Installer import ServiceInstaller

app = FastAPI(
    title="Car Rental API",
    description="API backend for Car Rental System",
    version="1.0.0"
)

# Setup DI (dependency injection)
installer = ServiceInstaller()

# Inject services into routers
cars_api.car_service = installer.car_service
users_api.user_service = installer.user_service
rentals_api.rental_service = installer.rental_service

# Register routers
app.include_router(cars_api.router)
app.include_router(users_api.router)
app.include_router(rentals_api.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Car Rental API 🚗"}
