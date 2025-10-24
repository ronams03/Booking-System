import reflex as rx
from typing import TypedDict, Optional
from app.states.booking_state import BookingState, Booking
import datetime
import json
import logging
from collections import Counter


class Metric(TypedDict):
    name: str
    value: str
    change: str
    change_type: str


class BusinessHours(TypedDict):
    enabled: bool
    start: str
    end: str


class BlockedDate(TypedDict):
    date: str
    reason: str


class AdminState(rx.State):
    """The state for the admin dashboard UI and logic."""

    date_filter: str = "all"
    service_filter: str = "all"
    status_filter: str = "all"
    search_query: str = ""
    selected_booking_id: Optional[str] = None
    is_modal_open: bool = False
    business_hours: dict[str, BusinessHours] = {
        day: {"enabled": True, "start": "09:00", "end": "17:00"}
        for day in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
    }
    blocked_dates: list[BlockedDate] = []
    booking_trends_data: list[dict] = []
    popular_services_data: list[dict] = []
    time_slot_analytics: list[dict] = []
    nav_items: list[dict[str, str]] = [
        {"label": "Dashboard", "icon": "layout-dashboard", "href": "/admin"},
        {"label": "Bookings", "icon": "calendar", "href": "/admin/bookings"},
        {"label": "Customers", "icon": "users", "href": "/admin/customers"},
        {"label": "Availability", "icon": "clock", "href": "/admin/availability"},
        {"label": "Analytics", "icon": "bar-chart-2", "href": "/admin/analytics"},
    ]

    @rx.event
    def get_metrics(self, all_bookings: list[Booking]) -> list[Metric]:
        total_revenue = sum(
            (
                49
                if b["service_name"] == "Personal Consultation"
                else 199
                if b["service_name"] == "Team Workshop"
                else 499
                for b in all_bookings
                if b["status"] == "confirmed"
            )
        )
        total_bookings = len(all_bookings)
        today = datetime.date.today()
        upcoming_bookings = len(
            [
                b
                for b in all_bookings
                if datetime.datetime.strptime(b["date"], "%Y-%m-%d").date() >= today
                and b["status"] == "confirmed"
            ]
        )
        cancelled_count = len([b for b in all_bookings if b["status"] == "cancelled"])
        cancellation_rate = (
            cancelled_count / total_bookings * 100 if total_bookings > 0 else 0
        )
        return [
            {
                "name": "Total Revenue",
                "value": f"${total_revenue:,}",
                "change": "",
                "change_type": "neutral",
            },
            {
                "name": "Total Bookings",
                "value": str(total_bookings),
                "change": "",
                "change_type": "neutral",
            },
            {
                "name": "Upcoming",
                "value": str(upcoming_bookings),
                "change": "",
                "change_type": "neutral",
            },
            {
                "name": "Cancellation Rate",
                "value": f"{cancellation_rate:.1f}%",
                "change": "",
                "change_type": "neutral",
            },
        ]

    @rx.var
    async def filtered_bookings(self) -> list[Booking]:
        booking_state = await self.get_state(BookingState)
        all_bookings = booking_state.bookings
        if self.date_filter != "all":
            today = datetime.date.today()
            if self.date_filter == "today":
                all_bookings = [
                    b
                    for b in all_bookings
                    if datetime.datetime.strptime(b["date"], "%Y-%m-%d").date() == today
                ]
            elif self.date_filter == "this_week":
                start_of_week = today - datetime.timedelta(days=today.weekday())
                end_of_week = start_of_week + datetime.timedelta(days=6)
                all_bookings = [
                    b
                    for b in all_bookings
                    if start_of_week
                    <= datetime.datetime.strptime(b["date"], "%Y-%m-%d").date()
                    <= end_of_week
                ]
            elif self.date_filter == "this_month":
                all_bookings = [
                    b
                    for b in all_bookings
                    if datetime.datetime.strptime(b["date"], "%Y-%m-%d").date().month
                    == today.month
                ]
        if self.service_filter != "all":
            all_bookings = [
                b for b in all_bookings if b["service_name"] == self.service_filter
            ]
        if self.status_filter != "all":
            all_bookings = [
                b for b in all_bookings if b["status"] == self.status_filter
            ]
        return sorted(all_bookings, key=lambda b: (b["date"], b["time"]), reverse=True)

    @rx.var
    async def metrics(self) -> list[Metric]:
        booking_state = await self.get_state(BookingState)
        return self.get_metrics(booking_state.bookings)

    @rx.var
    async def selected_booking(self) -> Optional[Booking]:
        if self.selected_booking_id is None:
            return None
        booking_state = await self.get_state(BookingState)
        return next(
            (b for b in booking_state.bookings if b["id"] == self.selected_booking_id),
            None,
        )

    @rx.event
    def open_booking_modal(self, booking_id: str):
        self.selected_booking_id = booking_id
        self.is_modal_open = True

    @rx.event
    def close_booking_modal(self):
        self.is_modal_open = False
        self.selected_booking_id = None

    @rx.event
    def handle_modal_open_change(self, open: bool):
        self.is_modal_open = open
        if not open:
            self.selected_booking_id = None

    @rx.event
    def update_booking_status(self, booking_id: str, status: str):
        yield BookingState.update_booking_status_in_storage(booking_id, status)
        self.close_booking_modal()

    @rx.event
    def toggle_day_availability(self, day: str):
        self.business_hours[day]["enabled"] = not self.business_hours[day]["enabled"]

    @rx.event
    def update_business_hours(self, day: str, field: str, value: str):
        self.business_hours[day][field] = value

    @rx.event
    def add_blocked_date(self, form_data: dict):
        date = form_data.get("date")
        reason = form_data.get("reason", "Blocked")
        if date and (not any((d["date"] == date for d in self.blocked_dates))):
            self.blocked_dates.append(BlockedDate(date=date, reason=reason))
            self.blocked_dates = sorted(self.blocked_dates, key=lambda x: x["date"])

    @rx.event
    def remove_blocked_date(self, date: str):
        self.blocked_dates = [d for d in self.blocked_dates if d["date"] != date]

    @rx.event
    async def load_analytics(self):
        booking_state = await self.get_state(BookingState)
        all_bookings = booking_state.bookings
        trends = Counter((b["date"] for b in all_bookings))
        self.booking_trends_data = sorted(
            [{"date": d, "bookings": c} for d, c in trends.items()],
            key=lambda x: x["date"],
        )
        services = Counter((b["service_name"] for b in all_bookings))
        self.popular_services_data = [
            {"name": n, "count": c} for n, c in services.items()
        ]
        slots = Counter((b["time"] for b in all_bookings))
        self.time_slot_analytics = sorted(
            [{"time": t, "count": c} for t, c in slots.items()], key=lambda x: x["time"]
        )