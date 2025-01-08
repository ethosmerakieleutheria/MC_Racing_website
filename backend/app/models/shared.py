from pydantic import BaseModel, validator
from datetime import datetime

class TimeSlotRequest(BaseModel):
    date: str  # Format: MM/DD/YYYY
    start_time: str  # Format: HH:MM PM/AM
    end_time: str  # Format: HH:MM PM/AM
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%m/%d/%Y')
            return v
        except ValueError:
            raise ValueError('Date must be in MM/DD/YYYY format')
    
    @validator('start_time', 'end_time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%I:%M %p')
            return v
        except ValueError:
            raise ValueError('Time must be in HH:MM PM/AM format (e.g., 02:30 PM)')

def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Convert date and time strings to datetime object"""
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    time_obj = datetime.strptime(time_str, '%I:%M %p').time()
    return datetime.combine(date_obj, time_obj)