import reflex as rx
import json
import uuid
import logging
from datetime import datetime
from typing import TypedDict, Optional
from app.state import State as BaseState


class Booking(TypedDict):
    id: str
    service_name: str
    date: str
    time: str
    name: str
    email: str
    phone: Optional[str]
    notes: Optional[str]
    status: str


class BookingState(rx.State):
    bookings_json: str = rx.LocalStorage("[]", name="bookings")
    form_errors: dict[str, str] = {}
    form_submitting: bool = False
    available_times: list[str] = [
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
    ]

    def _validate_form(self, form_data: dict) -> bool:
        errors = {}
        if not form_data.get("service"):
            errors["service"] = "Please select a service."
        if not form_data.get("date"):
            errors["date"] = "Please select a date."
        if not form_data.get("time"):
            errors["time"] = "Please select a time."
        if not form_data.get("name"):
            errors["name"] = "Name is required."
        if not form_data.get("email"):
            errors["email"] = "Email is required."
        self.form_errors = errors
        return not errors

    @rx.event
    async def create_booking(self, form_data: dict):
        self.form_submitting = True
        yield
        if not self._validate_form(form_data):
            self.form_submitting = False
            return
        new_booking = Booking(
            id=str(uuid.uuid4()),
            service_name=form_data["service"],
            date=form_data["date"],
            time=form_data["time"],
            name=form_data["name"],
            email=form_data["email"],
            phone=form_data.get("phone"),
            notes=form_data.get("notes"),
            status="pending",
        )
        try:
            current_bookings = json.loads(self.bookings_json)
        except json.JSONDecodeError as e:
            logging.exception(f"Error decoding bookings JSON: {e}")
            current_bookings = []
        current_bookings.append(new_booking)
        self.bookings_json = json.dumps(current_bookings)
        self.form_submitting = False
        yield rx.redirect(f"/booking-confirmation/{new_booking['id']}")
        return

    @rx.var
    def bookings(self) -> list[Booking]:
        try:
            return json.loads(self.bookings_json)
        except json.JSONDecodeError as e:
            logging.exception(f"Error decoding bookings JSON: {e}")
            return []

    @rx.var
    def current_booking(self) -> Optional[Booking]:
        booking_id = self.router.page.params.get("booking_id")
        if not booking_id:
            return None
        for booking in self.bookings:
            if booking["id"] == booking_id:
                return booking
        return None

    @rx.var
    def min_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    @rx.event
    def on_load_booking_page(self):
        self.form_errors = {}
        self.form_submitting = False

    @rx.event
    def update_booking_status_in_storage(self, booking_id: str, status: str):
        try:
            current_bookings = json.loads(self.bookings_json)
        except json.JSONDecodeError as e:
            logging.exception(f"Error decoding bookings JSON for update: {e}")
            return
        for i, booking in enumerate(current_bookings):
            if booking["id"] == booking_id:
                current_bookings[i]["status"] = status
                self.bookings_json = json.dumps(current_bookings)
                return