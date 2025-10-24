import reflex as rx
from app.state import State


def hero_section() -> rx.Component:
    """The hero section for the landing page."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    "✨ New: Introducing Team Bookings!",
                    class_name="inline-block px-3 py-1 text-xs font-medium text-emerald-700 bg-emerald-100 rounded-full",
                ),
                rx.el.h1(
                    "The simplest way to ",
                    rx.el.span("book appointments", class_name="text-emerald-500"),
                    ".",
                    class_name="mt-6 text-4xl md:text-6xl font-extrabold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Bookify offers a seamless, intuitive, and powerful booking experience. Save time, reduce no-shows, and delight your clients.",
                    class_name="mt-6 text-lg text-gray-600 max-w-2xl mx-auto",
                ),
                rx.el.div(
                    rx.el.a(
                        "Get Started for Free",
                        href="/book",
                        class_name="inline-flex items-center justify-center px-6 py-3 text-base font-semibold text-white bg-emerald-500 rounded-lg shadow-md hover:bg-emerald-600 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2",
                    ),
                    rx.el.a(
                        "Book a Demo",
                        rx.icon("arrow-right", class_name="ml-2 h-5 w-5"),
                        href="#",
                        class_name="ml-4 inline-flex items-center justify-center px-6 py-3 text-base font-semibold text-emerald-600 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2",
                    ),
                    class_name="mt-10 flex justify-center items-center",
                ),
            ),
            class_name="text-center",
        ),
        class_name="px-4 py-20 sm:py-32",
    )


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    """A card for displaying a feature."""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-white"),
            class_name="flex items-center justify-center h-12 w-12 rounded-xl bg-emerald-500",
        ),
        rx.el.h3(title, class_name="mt-5 text-lg font-semibold text-gray-900"),
        rx.el.p(description, class_name="mt-2 text-sm text-gray-600"),
        class_name="p-6 bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300",
    )


def features_section() -> rx.Component:
    """The features section."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Everything you need, and more.",
                    class_name="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl",
                ),
                rx.el.p(
                    "Manage your schedule, clients, and business with our powerful suite of tools.",
                    class_name="mt-4 text-lg text-gray-600",
                ),
            ),
            rx.el.div(
                feature_card(
                    "calendar-days",
                    "Smart Calendar",
                    "Sync your availability across multiple calendars automatically. Avoid double bookings forever.",
                ),
                feature_card(
                    "bell",
                    "Automated Reminders",
                    "Reduce no-shows with automated email and SMS reminders for your clients.",
                ),
                feature_card(
                    "credit-card",
                    "Online Payments",
                    "Securely accept payments and deposits upfront. Integrated with Stripe.",
                ),
                feature_card(
                    "line-chart",
                    "Insightful Analytics",
                    "Understand your business with detailed reports on bookings, revenue, and client retention.",
                ),
                feature_card(
                    "globe",
                    "Custom Booking Page",
                    "Create a professional, branded booking page that reflects your business.",
                ),
                feature_card(
                    "users-round",
                    "Client Management",
                    "Keep track of your client history, notes, and contact information all in one place.",
                ),
                class_name="mt-12 grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3",
            ),
        ),
        id="features",
        class_name="px-4 py-24 sm:px-6 lg:px-8 bg-gray-50",
    )


def service_card(service: dict) -> rx.Component:
    """A card for displaying a service/pricing tier."""
    return rx.el.div(
        rx.el.div(
            rx.icon(service["icon"], class_name="h-8 w-8 text-emerald-500 mb-4"),
            rx.el.h3(service["name"], class_name="text-xl font-bold text-gray-900"),
            rx.el.p(
                service["description"], class_name="mt-2 text-sm text-gray-600 h-10"
            ),
            rx.el.div(
                rx.el.span("$", class_name="text-2xl font-medium text-gray-500 mr-1"),
                rx.el.span(
                    service["price"], class_name="text-5xl font-extrabold text-gray-900"
                ),
                rx.el.span("/session", class_name="text-lg font-medium text-gray-500"),
                class_name="mt-6 flex items-baseline",
            ),
            rx.el.a(
                "Book This Plan",
                href="#",
                class_name="mt-8 block w-full text-center px-6 py-3 text-base font-semibold text-white bg-emerald-500 rounded-lg shadow-md hover:bg-emerald-600 transition-colors",
            ),
        ),
        rx.el.ul(
            rx.foreach(
                service["features"],
                lambda feature: rx.el.li(
                    rx.icon("check", class_name="h-5 w-5 text-emerald-500"),
                    rx.el.span(feature, class_name="ml-3 text-sm text-gray-600"),
                    class_name="flex items-center",
                ),
            ),
            class_name="mt-8 space-y-4",
        ),
        class_name="flex flex-col p-8 bg-white rounded-2xl border border-gray-200 shadow-lg",
    )


def pricing_section() -> rx.Component:
    """The pricing section."""
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Flexible pricing for businesses of all sizes",
                class_name="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl text-center",
            ),
            rx.el.p(
                "Choose the plan that's right for you. No hidden fees, ever.",
                class_name="mt-4 text-lg text-gray-600 text-center",
            ),
            rx.el.div(
                rx.foreach(State.services, service_card),
                class_name="mt-16 grid max-w-lg gap-8 mx-auto lg:max-w-none lg:grid-cols-3",
            ),
        ),
        id="pricing",
        class_name="px-4 py-24 sm:px-6 lg:px-8",
    )