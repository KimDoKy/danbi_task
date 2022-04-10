def change_days_string(days:list) -> str:
    return " ".join(x for x in days)

def get_today_start_end(today:str) -> tuple:
    return (f"{today} 00:00:00", f"{today} 23:59:59")
