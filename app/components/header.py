import reflex as rx
from app.states.auth_state import AuthState


def nav_item(text: str, url: str) -> rx.Component:
    """A navigation item."""
    return rx.el.a(
        text,
        href=url,
        class_name="text-sm font-medium text-gray-500 hover:text-emerald-600 transition-colors",
    )


def header() -> rx.Component:
    """The header component."""
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("calendar-check", class_name="h-7 w-7 text-emerald-500"),
                    href="/",
                    class_name="flex items-center",
                ),
                rx.el.p("Bookify", class_name="ml-2 text-xl font-bold text-gray-800"),
            ),
            rx.el.nav(
                nav_item("Features", "#features"),
                nav_item("Pricing", "#pricing"),
                nav_item("About", "#"),
                nav_item("Contact", "#"),
                class_name="hidden md:flex items-center gap-8",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.a(
                        "Go to Dashboard",
                        href="/admin",
                        class_name="text-sm font-semibold text-gray-600 hover:text-emerald-700 transition-colors",
                    ),
                    rx.el.a(
                        "Sign In",
                        href="/login",
                        class_name="text-sm font-semibold text-gray-600 hover:text-emerald-700 transition-colors",
                    ),
                ),
                rx.el.a(
                    "Book Now",
                    href="/book",
                    class_name="ml-6 inline-flex items-center justify-center px-4 py-2 text-sm font-semibold text-white bg-emerald-500 rounded-lg shadow-sm hover:bg-emerald-600 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2",
                ),
                class_name="flex items-center",
            ),
        ),
        class_name="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-gray-200",
    )