from celery import Celery
from datetime import timedelta, datetime, time

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

from app import app
from mail import send_email_with_lots, send_html_email
from models import User, ParkingLot, Reservation

from celery.schedules import crontab
from flask import render_template_string

@celery.task()
def send_daily_reminder():
    with app.app_context():
        subject = "Daily Parking Lots Update"
        body = "Hello,\n\nHere is the daily update of available parking lots:"

        lots = ParkingLot.query.all()
        users = User.query.filter(~User.roles.any(name='admin')).all()

        for user in users:
            send_email_with_lots(user.email, subject, body, lots)

    print("Daily reminder emails sent!")
    return "Daily reminder emails sent!"


from datetime import datetime, date
from calendar import monthrange

def get_current_month_date_range():
    today = date.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(today.year, today.month)[1])
    return first_day, last_day


def build_html_report(user, reservations, start_date, end_date):
    html_template = """
    <h2>Monthly Activity Report for {{ user.email }}</h2>
    <p>Period: {{ start_date }} to {{ end_date }}</p>
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
        <thead>
            <tr>
                <th>Reservation ID</th>
                <th>Lot ID</th>
                <th>Spot ID</th>
                <th>Vehicle Number</th>
                <th>Entry Time</th>
                <th>Exit Time</th>
                <th>Total Cost (₹)</th>
            </tr>
        </thead>
        <tbody>
            {% for r in reservations %}
                <tr>
                    <td>{{ r.id }}</td>
                    <td>{{ r.lot_id }}</td>
                    <td>{{ r.spot_id }}</td>
                    <td>{{ r.vehicle_number }}</td>
                    <td>{{ r.entry_time.strftime('%Y-%m-%d %H:%M') }}</td>
                    <td>{{ r.exit_time.strftime('%Y-%m-%d %H:%M') if r.exit_time else 'N/A' }}</td>
                    <td>{{ "%.2f"|format(r.total_cost or 0) }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    """
    return render_template_string(html_template, user=user, reservations=reservations,
                                  start_date=start_date, end_date=end_date)



@celery.task
def send_monthly_activity_report():
    with app.app_context():
        start_date, end_date = get_current_month_date_range()
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        users = User.query.filter(~User.roles.any(name='admin')).all()
        sent_count = 0

        for user in users:
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.entry_time >= start_datetime,
                Reservation.entry_time <= end_datetime
            ).order_by(Reservation.entry_time).all()

            if not reservations:
                print(f"No reservations for user {user.email} in period {start_date} to {end_date}")
                continue

            report_html = build_html_report(user, reservations, start_date, end_date)
            subject = f"ParkEase Monthly Activity Report - {start_date.strftime('%B %Y')}"

            try:
                send_html_email(user.email, subject, report_html)
                print(f"Monthly report sent to {user.email}")
                sent_count += 1
            except Exception as e:
                print(f"Failed to send to {user.email}: {e}")

        print(f"Monthly activity reports sent to {sent_count} users.")
        return "Monthly activity reports sent!"


celery.conf.beat_schedule = {
    'send-daily-reminder': {
        'task': 'celery_app.send_daily_reminder',
        # Uncomment and set for production:
        # 'schedule': crontab(hour=20, minute=0),
        'schedule': timedelta(seconds=15),  # For testing: every 15 seconds
    },
    'send-monthly-activity-report': {
        'task': 'celery_app.send_monthly_activity_report',
        # Uncomment and set for production:
        # 'schedule': crontab(day_of_month=1, hour=0, minute=0),
        'schedule': timedelta(seconds=30),  # For testing every 30 seconds
    },
}
