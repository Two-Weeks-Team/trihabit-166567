from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

from models import SessionLocal, User, Habit, HabitCheck, CoachingSuggestion
from ai_service import generate_coaching_suggestion, generate_weekly_insights

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock authentication – in a real app this would be JWT based
def get_current_user(db=Depends(get_db)) -> User:
    # For demo purposes, return the first user or create one
    user = db.query(User).first()
    if not user:
        user = User(email="demo@example.com", password_hash="notahash")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

class HabitOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    goal: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

class CheckInIn(BaseModel):
    date: date = Field(..., description="Date of the check‑in (YYYY‑MM‑DD)")
    notes: Optional[str] = Field(None, description="Optional notes for the check‑in")

@router.get("/habits", response_model=dict)
def list_habits(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()
    return {"habits": [HabitOut.from_orm(h) for h in habits]}

@router.post("/habits/{habit_id}/check-in", response_model=dict)
def check_in_habit(habit_id: str, payload: CheckInIn, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    check = db.query(HabitCheck).filter(
        HabitCheck.user_id == current_user.id,
        HabitCheck.habit_id == habit.id,
        HabitCheck.date == payload.date
    ).first()
    if not check:
        check = HabitCheck(
            user_id=current_user.id,
            habit_id=habit.id,
            date=payload.date,
            checked_in=True,
            notes=payload.notes,
        )
        db.add(check)
    else:
        check.checked_in = True
        check.notes = payload.notes
    db.commit()
    return {"message": "Check‑in recorded successfully"}

@router.get("/habits/{habit_id}/coaching", response_model=dict)
async def get_coaching(habit_id: str, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    # Gather recent check‑in data (last 7 days)
    recent_checks = db.query(HabitCheck).filter(
        HabitCheck.habit_id == habit.id,
        HabitCheck.user_id == current_user.id
    ).order_by(HabitCheck.date.desc()).limit(7).all()
    check_data = [{"date": str(c.date), "checked_in": c.checked_in, "notes": c.notes} for c in recent_checks]
    suggestion = await generate_coaching_suggestion(habit.name, check_data)
    # Persist suggestion
    cs = CoachingSuggestion(
        user_id=current_user.id,
        habit_id=habit.id,
        suggestion=suggestion.get("suggestion", ""),
        reason=suggestion.get("reason"),
        confidence_score=suggestion.get("confidence_score")
    )
    db.add(cs)
    db.commit()
    return {"suggestion": cs.suggestion, "reason": cs.reason}

@router.get("/insights", response_model=dict)
async def weekly_insights(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    # Simple aggregation: count of checked‑in days per habit in last 7 days
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()
    summary = []
    for h in habits:
        count = db.query(HabitCheck).filter(
            HabitCheck.habit_id == h.id,
            HabitCheck.user_id == current_user.id,
            HabitCheck.date >= week_ago,
            HabitCheck.checked_in == True
        ).count()
        summary.append({"habit": h.name, "checked_in_days": count})
    insight = await generate_weekly_insights(summary)
    return {"insights": insight}
