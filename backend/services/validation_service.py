from fastapi import HTTPException

def validate_date_range(
    start_date,
    end_date
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )