from datetime import time

def is_valid_slot(dt):
    return dt.minute in [0,30]

def is_within_working_hours(dt):
    return time(10, 0) <= dt.time() <= time(18, 30)
