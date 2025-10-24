import reflex as rx
from app.components.header import header
from app.components.footer import footer
from app.components.landing import hero_section, features_section, pricing_section
from app.pages.booking import booking_page, booking_confirmation_page
from app.pages.admin import (
    dashboard_page,
    customers_page,
    availability_page,
    analytics_page,
)
from app.pages.admin_bookings import bookings_page
from app.pages.login import login_page
from app.states.booking_state import BookingState
from app.states.auth_state import AuthState


def index() -> rx.Component:
    """The main landing page."""
    return rx.el.main(
        header(),
        hero_section(),
        features_section(),
        pricing_section(),
        footer(),
        class_name="font-['Poppins'] bg-white",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
app.add_page(login_page, route="/login")
app.add_page(booking_page, route="/book", on_load=BookingState.on_load_booking_page)
app.add_page(booking_confirmation_page, route="/booking-confirmation/[booking_id]")
app.add_page(dashboard_page, route="/admin", on_load=AuthState.check_auth)
app.add_page(bookings_page, route="/admin/bookings", on_load=AuthState.check_auth)
app.add_page(customers_page, route="/admin/customers", on_load=AuthState.check_auth)
app.add_page(
    availability_page, route="/admin/availability", on_load=AuthState.check_auth
)
app.add_page(analytics_page, route="/admin/analytics", on_load=AuthState.check_auth)