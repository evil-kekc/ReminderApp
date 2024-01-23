from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from starlette.templating import Jinja2Templates

from bson import ObjectId

from database.db import ReminderManager

router = APIRouter()
templates = Jinja2Templates(directory='templates')
reminders = []


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with ReminderManager() as reminder_manager:
        upcoming_reminders = reminder_manager.get_all_reminders()

    return templates.TemplateResponse(
        'home.html',
        {'request': request, 'upcoming_reminders': upcoming_reminders}
    )


@router.post("/", response_class=HTMLResponse)
async def create_reminder(request: Request):
    from main import app

    form = await request.form()
    reminder_text = form['reminder']
    reminder_date = form['date']
    reminder_time = form['time']

    date_str = f'{reminder_date} {reminder_time}'
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M')

    with ReminderManager() as reminder_manager:
        reminder_manager.save_reminder(
            reminder_text=reminder_text,
            reminder_time=date_obj
        )

    return RedirectResponse(
        url=app.url_path_for('home'),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/delete/{index}", response_class=HTMLResponse)
async def remove_reminder(index: str):
    from main import app

    try:
        with ReminderManager() as reminder_manager:
            reminder_manager.delete_reminder(
                reminder_id=ObjectId(index)
            )
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    return RedirectResponse(
        url=app.url_path_for("home"),
        status_code=status.HTTP_303_SEE_OTHER
    )
