import reflex as rx
from app.state import State
from app.states.booking_state import BookingState
from app.components.header import header
from app.components.footer import footer


def booking_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Service", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.select(
                    rx.el.option("Select a service", value="", disabled=True),
                    rx.foreach(
                        State.services,
                        lambda service: rx.el.option(
                            service["name"], value=service["name"]
                        ),
                    ),
                    name="service",
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm rounded-md",
                    default_value="",
                ),
                rx.cond(
                    BookingState.form_errors.contains("service"),
                    rx.el.p(
                        BookingState.form_errors["service"],
                        class_name="mt-1 text-sm text-red-600",
                    ),
                    None,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Date", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="date",
                        name="date",
                        min=BookingState.min_date,
                        class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm",
                    ),
                    rx.cond(
                        BookingState.form_errors.contains("date"),
                        rx.el.p(
                            BookingState.form_errors["date"],
                            class_name="mt-1 text-sm text-red-600",
                        ),
                        None,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Time", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.select(
                        rx.el.option("Select a time", value="", disabled=True),
                        rx.foreach(
                            BookingState.available_times,
                            lambda time: rx.el.option(time, value=time),
                        ),
                        name="time",
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm rounded-md",
                        default_value="",
                    ),
                    rx.cond(
                        BookingState.form_errors.contains("time"),
                        rx.el.p(
                            BookingState.form_errors["time"],
                            class_name="mt-1 text-sm text-red-600",
                        ),
                        None,
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Full Name", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.input(
                    name="name",
                    placeholder="John Doe",
                    class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm",
                ),
                rx.cond(
                    BookingState.form_errors.contains("name"),
                    rx.el.p(
                        BookingState.form_errors["name"],
                        class_name="mt-1 text-sm text-red-600",
                    ),
                    None,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    type="email",
                    name="email",
                    placeholder="you@example.com",
                    class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm",
                ),
                rx.cond(
                    BookingState.form_errors.contains("email"),
                    rx.el.p(
                        BookingState.form_errors["email"],
                        class_name="mt-1 text-sm text-red-600",
                    ),
                    None,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Phone Number (Optional)",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    type="tel",
                    name="phone",
                    class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Notes (Optional)",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.textarea(
                    name="notes",
                    rows=4,
                    class_name="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                rx.cond(
                    BookingState.form_submitting, rx.spinner(class_name="mr-2"), None
                ),
                rx.cond(
                    BookingState.form_submitting, "Processing...", "Confirm Booking"
                ),
                type="submit",
                disabled=BookingState.form_submitting,
                class_name="w-full inline-flex justify-center py-3 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50",
            ),
        ),
        on_submit=BookingState.create_booking,
        reset_on_submit=True,
        class_name="max-w-2xl mx-auto p-8 bg-white rounded-lg shadow-md",
    )


def booking_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.h1(
                "Book an Appointment",
                class_name="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl text-center",
            ),
            rx.el.p(
                "Fill out the form below to schedule your appointment.",
                class_name="mt-4 text-lg text-gray-600 text-center",
            ),
            rx.el.div(booking_form(), class_name="mt-12"),
            class_name="px-4 py-16 sm:px-6 lg:px-8",
        ),
        footer(),
        class_name="font-['Poppins'] bg-gray-50",
    )


def booking_confirmation_page() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.cond(
                BookingState.current_booking,
                rx.el.div(
                    rx.el.div(
                        rx.icon("square_check", class_name="h-12 w-12 text-green-500"),
                        class_name="mx-auto flex items-center justify-center",
                    ),
                    rx.el.h2(
                        "Booking Confirmed!",
                        class_name="mt-6 text-2xl font-bold text-center text-gray-900",
                    ),
                    rx.el.p(
                        "Thank you, {BookingState.current_booking['name']}. Your appointment has been scheduled.",
                        class_name="mt-2 text-sm text-center text-gray-600",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Booking Details",
                                class_name="text-lg font-medium text-gray-900",
                            ),
                            rx.el.dl(
                                rx.el.div(
                                    rx.el.dt("Service"),
                                    rx.el.dd(
                                        BookingState.current_booking["service_name"]
                                    ),
                                    class_name="py-3 flex justify-between text-sm font-medium",
                                ),
                                rx.el.div(
                                    rx.el.dt("Date"),
                                    rx.el.dd(BookingState.current_booking["date"]),
                                    class_name="py-3 flex justify-between text-sm font-medium border-t border-gray-200",
                                ),
                                rx.el.div(
                                    rx.el.dt("Time"),
                                    rx.el.dd(BookingState.current_booking["time"]),
                                    class_name="py-3 flex justify-between text-sm font-medium border-t border-gray-200",
                                ),
                                rx.el.div(
                                    rx.el.dt("Email"),
                                    rx.el.dd(BookingState.current_booking["email"]),
                                    class_name="py-3 flex justify-between text-sm font-medium border-t border-gray-200",
                                ),
                                class_name="mt-4",
                            ),
                        ),
                        class_name="mt-8 p-6 bg-gray-50 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "A confirmation email has been sent. If you have any questions, please contact us.",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="mt-8 text-center",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Back to Home",
                            href="/",
                            class_name="mt-8 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700",
                        ),
                        class_name="mt-6 flex justify-center",
                    ),
                ),
                rx.el.div(
                    rx.el.h2(
                        "Booking not found.",
                        class_name="text-2xl font-bold text-center",
                    ),
                    rx.el.p(
                        "The booking you are looking for could not be found.",
                        class_name="mt-2 text-sm text-center",
                    ),
                    rx.el.a(
                        "Go to Booking Page",
                        href="/book",
                        class_name="mt-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-emerald-600 hover:bg-emerald-700",
                    ),
                ),
            ),
            class_name="max-w-md mx-auto py-16 px-4 sm:px-6 lg:px-8",
        ),
        footer(),
        class_name="font-['Poppins'] bg-white",
    )