import reflex as rx
from app.states.admin_state import AdminState
from app.state import State
from app.pages.admin import admin_layout


def status_badge(status: str) -> rx.Component:
    """A badge to display the booking status."""
    return rx.el.div(
        status.capitalize(),
        class_name=rx.cond(
            status == "confirmed",
            "px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full w-fit",
            rx.cond(
                status == "cancelled",
                "px-2 py-1 text-xs font-medium text-red-800 bg-red-100 rounded-full w-fit",
                "px-2 py-1 text-xs font-medium text-yellow-800 bg-yellow-100 rounded-full w-fit",
            ),
        ),
    )


def booking_detail_modal() -> rx.Component:
    """Modal to show booking details and actions."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.content(
            rx.cond(
                AdminState.selected_booking,
                rx.el.div(
                    rx.el.h3(
                        f"Booking #{AdminState.selected_booking['id'][:8]}",
                        class_name="text-lg font-semibold",
                    ),
                    rx.el.dl(
                        rx.el.dt("Customer:", class_name="font-medium"),
                        rx.el.dd(AdminState.selected_booking["name"]),
                        rx.el.dt("Email:", class_name="font-medium mt-2"),
                        rx.el.dd(AdminState.selected_booking["email"]),
                        rx.el.dt("Service:", class_name="font-medium mt-2"),
                        rx.el.dd(AdminState.selected_booking["service_name"]),
                        rx.el.dt("Date & Time:", class_name="font-medium mt-2"),
                        rx.el.dd(
                            f"{AdminState.selected_booking['date']} at {AdminState.selected_booking['time']}"
                        ),
                        rx.el.dt("Status:", class_name="font-medium mt-2"),
                        rx.el.dd(status_badge(AdminState.selected_booking["status"])),
                        class_name="grid grid-cols-2 gap-y-1 text-sm mt-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Close",
                            on_click=AdminState.close_booking_modal,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
                        ),
                        rx.el.button(
                            "Cancel Booking",
                            on_click=lambda: AdminState.update_booking_status(
                                AdminState.selected_booking["id"], "cancelled"
                            ),
                            class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700",
                        ),
                        rx.el.button(
                            "Confirm Booking",
                            on_click=lambda: AdminState.update_booking_status(
                                AdminState.selected_booking["id"], "confirmed"
                            ),
                            class_name="px-4 py-2 text-sm font-medium text-white bg-emerald-600 border border-transparent rounded-md hover:bg-emerald-700",
                        ),
                        class_name="flex justify-end gap-3 mt-6",
                    ),
                ),
                rx.el.div("No booking selected."),
            ),
            class_name="max-w-md p-6 bg-white rounded-lg shadow-xl",
        ),
        open=AdminState.is_modal_open,
        on_open_change=AdminState.handle_modal_open_change,
    )


def bookings_table() -> rx.Component:
    """Table to display all bookings."""
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Customer"),
                    rx.el.th("Service"),
                    rx.el.th("Date & Time"),
                    rx.el.th("Status"),
                    rx.el.th("Actions"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AdminState.filtered_bookings,
                    lambda booking: rx.el.tr(
                        rx.el.td(booking["name"]),
                        rx.el.td(booking["service_name"]),
                        rx.el.td(f"{booking['date']} @ {booking['time']}"),
                        rx.el.td(status_badge(booking["status"])),
                        rx.el.td(
                            rx.el.button(
                                "View",
                                on_click=lambda: AdminState.open_booking_modal(
                                    booking["id"]
                                ),
                                class_name="text-emerald-600 hover:underline text-sm font-medium",
                            )
                        ),
                    ),
                )
            ),
            class_name="w-full text-sm text-left text-gray-500",
        ),
        class_name="overflow-hidden rounded-lg border border-gray-200 bg-white mt-4 shadow-sm",
    )


def bookings_page() -> rx.Component:
    """The bookings management page."""
    return admin_layout(
        rx.el.div(
            rx.el.div(rx.el.h1("Bookings", class_name="text-2xl font-bold")),
            bookings_table(),
            booking_detail_modal(),
            class_name="p-6",
        )
    )