import calendar
from datetime import datetime

def get_calendar_html():
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    first_day_of_month = datetime(current_year, current_month, 1)
    first_weekday = first_day_of_month.weekday()
    first_weekday = (first_weekday + 1) % 7
    days_in_month = (datetime(current_year, current_month + 1, 1) - first_day_of_month).days

    markup = f"<b>       {calendar.month_name[current_month]} {current_year}</b>\n\n"
    markup += "<span foreground='wheat'>" + " ".join(weekdays) + "</span>\n"

    day_counter = 1
    for i in range(6):
        week = []
        for j in range(7):
            if i == 0 and j < first_weekday:
                week.append("   ")
            elif day_counter <= days_in_month:
                if day_counter == current_day:
                    week.append(f"<span foreground='wheat'>{day_counter:2}</span> ")

                else:
                    week.append(f"{day_counter:2} ")
                day_counter += 1
            else:
                week.append("   ")
        
        markup += " ".join(week) + "\n"

    return markup

