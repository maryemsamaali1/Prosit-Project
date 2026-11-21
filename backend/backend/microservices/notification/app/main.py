
"""Notification microservice - entry point.

Run: python -m uvicorn app.main:app --port 8084
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers import notification
import py_eureka_client.eureka_client as eureka_client

# Port depuis la variable d'environnement
PORT = int(os.getenv("PORT", "8084"))


# Enregistrement et arrêt du client Eureka
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage : enregistrer NOTIFICATION dans Eureka
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="NOTIFICATION",
        instance_port=PORT,
        instance_host="127.0.0.1",
        instance_id=f"notification:127.0.0.1:{PORT}"
    )

    print(f"NOTIFICATION enregistré dans Eureka sur le port {PORT}")
    try:
            yield
    finally:
            # Arrêt : désenregistrer NOTIFICATION
            await eureka_client.stop_async()
            print("NOTIFICATION arrêté dans Eureka")


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification "
        "logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Conserver les routes existantes
app.include_router(notification.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )
