import calendar
from datetime import datetime

def get_calendar_html():
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    # List of weekday names
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    # Get the first day of the month and the number of days in the month
    first_day_of_month = datetime(current_year, current_month, 1)
    first_weekday = first_day_of_month.weekday()  # Monday = 0, Sunday = 6
    first_weekday = (first_weekday + 1) % 7  # Adjust so Sunday is 0, not 6
    days_in_month = (datetime(current_year, current_month + 1, 1) - first_day_of_month).days

    # Start the HTML-like markup for the header (Month Year)
    markup = f"<b>       {calendar.month_name[current_month]} {current_year}</b>\n\n"
    markup += "<span foreground='wheat'>" + " ".join(weekdays) + "</span>\n"

    # Add the days of the month
    day_counter = 1
    for i in range(6):  # 6 rows maximum in a month
        week = []
        for j in range(7):  # 7 days in a week
            if i == 0 and j < first_weekday:
                week.append("   ")  # Empty space for the days before the first day
            elif day_counter <= days_in_month:
                if day_counter == current_day:
                    week.append(f"<span foreground='wheat'>{day_counter:2}</span> ")  # Highlight current day
                else:
                    week.append(f"{day_counter:2} ")
                day_counter += 1
            else:
                week.append("   ")  # Empty space after the last day of the month
        
        markup += " ".join(week) + "\n"

    return markup

# Call the function and print the result
# print(get_calendar_html())
