import os

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from routers import reminder

app = FastAPI()
app.include_router(reminder.router, prefix="/reminders", tags=["reminders"])


@app.get("/")
async def base_page():
    return RedirectResponse(url=app.url_path_for('home'))


@app.get("/healthcheck", tags=["healthcheck"])
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "5000"))
    log_level = os.getenv("LOG_LEVEL", "info")

    uvicorn.run("main:app", host=host, port=port, log_level="info")
