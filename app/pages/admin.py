import reflex as rx
from app.states.admin_state import AdminState
from app.states.auth_state import AuthState
from app.state import State


def admin_sidebar() -> rx.Component:
    """The sidebar for the admin dashboard."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("calendar-check", class_name="h-8 w-8 text-emerald-500"),
                    rx.el.span("Bookify Admin", class_name="ml-2 text-xl font-bold"),
                    href="/admin",
                    class_name="flex items-center px-4 h-16 border-b",
                ),
                rx.el.nav(
                    rx.foreach(
                        AdminState.nav_items,
                        lambda item: rx.el.a(
                            rx.icon(item["icon"], class_name="h-5 w-5"),
                            rx.el.span(item["label"]),
                            href=item["href"],
                            class_name=rx.cond(
                                rx.State.router.page.path == item["href"],
                                "flex items-center gap-3 rounded-lg px-3 py-2 bg-emerald-100 text-emerald-800 transition-all font-semibold",
                                "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
                            ),
                        ),
                    ),
                    class_name="flex-1 flex flex-col gap-2 p-4",
                ),
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("log-out", class_name="h-5 w-5"),
                    rx.el.span("Logout"),
                    on_click=AuthState.logout,
                    class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 w-full text-left",
                ),
                class_name="mt-auto p-4 border-t",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden border-r bg-gray-100/40 md:block w-64 flex-shrink-0",
    )


def admin_layout(main_content: rx.Component) -> rx.Component:
    """A general layout for all admin pages."""
    return rx.el.div(
        admin_sidebar(),
        rx.el.main(main_content, class_name="flex-1 overflow-auto"),
        class_name="flex min-h-screen w-full font-['Poppins'] bg-gray-50/50",
    )


def metric_card(metric: dict) -> rx.Component:
    """A card for displaying a metric."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3(metric["name"], class_name="text-sm font-medium text-gray-500"),
            rx.match(
                metric["name"],
                (
                    "Total Revenue",
                    rx.icon("dollar-sign", class_name="h-4 w-4 text-gray-500"),
                ),
                (
                    "Total Bookings",
                    rx.icon("book-marked", class_name="h-4 w-4 text-gray-500"),
                ),
                (
                    "Upcoming",
                    rx.icon("calendar-clock", class_name="h-4 w-4 text-gray-500"),
                ),
                (
                    "Cancellation Rate",
                    rx.icon("ban", class_name="h-4 w-4 text-gray-500"),
                ),
                rx.icon("bar-chart", class_name="h-4 w-4 text-gray-500"),
            ),
            class_name="flex flex-row items-center justify-between pb-2",
        ),
        rx.el.div(
            rx.el.div(metric["value"], class_name="text-2xl font-bold"),
            rx.cond(
                metric["change"],
                rx.el.p(
                    f"{metric['change']} from last month",
                    class_name=rx.cond(
                        metric["change_type"] == "increase",
                        "text-xs text-green-500",
                        rx.cond(
                            metric["change_type"] == "decrease",
                            "text-xs text-red-500",
                            "text-xs text-gray-500",
                        ),
                    ),
                ),
                None,
            ),
        ),
        class_name="p-4 bg-white rounded-lg border border-gray-200 shadow-sm",
    )


def dashboard_page() -> rx.Component:
    """The main dashboard page."""
    return admin_layout(
        rx.el.div(
            rx.el.h1("Dashboard", class_name="text-2xl font-bold"),
            rx.el.div(
                rx.foreach(AdminState.metrics, metric_card),
                class_name="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-4",
            ),
            class_name="p-6",
        )
    )


def bookings_page() -> rx.Component:
    return admin_layout(
        rx.el.div("Bookings Management - Coming Soon", class_name="p-6")
    )


def customers_page() -> rx.Component:
    return admin_layout(
        rx.el.div("Customer Management - Coming Soon", class_name="p-6")
    )


def availability_page() -> rx.Component:
    return admin_layout(
        rx.el.div("Availability Settings - Coming Soon", class_name="p-6")
    )


def analytics_page() -> rx.Component:
    return admin_layout(
        rx.el.div("Analytics Dashboard - Coming Soon", class_name="p-6")
    )