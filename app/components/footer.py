import reflex as rx


def footer() -> rx.Component:
    """The footer component."""
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.icon(
                            "calendar-check", class_name="h-8 w-8 text-emerald-500"
                        ),
                        href="/",
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.p("Bookify", class_name="text-lg font-bold text-gray-800"),
                ),
                rx.el.p(
                    "Seamless booking for modern businesses.",
                    class_name="mt-4 text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Product",
                        class_name="text-sm font-semibold text-gray-900 tracking-wider uppercase",
                    ),
                    rx.el.ul(
                        rx.el.li(
                            rx.el.a(
                                "Features",
                                href="#features",
                                class_name="hover:text-emerald-600 transition-colors",
                            )
                        ),
                        rx.el.li(
                            rx.el.a(
                                "Pricing",
                                href="#pricing",
                                class_name="hover:text-emerald-600 transition-colors",
                            )
                        ),
                        rx.el.li(
                            rx.el.a(
                                "Book a Demo",
                                href="#",
                                class_name="hover:text-emerald-600 transition-colors",
                            )
                        ),
                        class_name="mt-4 space-y-4 text-sm text-gray-500 font-medium",
                    ),
                ),
                rx.el.div(
                    rx.el.h3(
                        "Company",
                        class_name="text-sm font-semibold text-gray-900 tracking-wider uppercase",
                    ),
                    rx.el.ul(
                        rx.el.li(
                            rx.el.a(
                                "About Us",
                                href="#",
                                class_name="hover:text-emerald-600 transition-colors",
                            )
                        ),
                        rx.el.li(
                            rx.el.a(
                                "Careers",
                                href="#",
                                class_name="hover:text-emerald-600 transition-colors",
                            )
                        ),
                        rx.el.li(
                            rx.el.a(
                                "Contact",
                                href="#",
                                class_name="hover:text-emerald-600 transition-colors",
                            )
                        ),
                        class_name="mt-4 space-y-4 text-sm text-gray-500 font-medium",
                    ),
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
        ),
        rx.el.div(
            rx.el.p(
                "© 2024 Bookify Inc. All rights reserved.",
                class_name="text-sm text-gray-400",
            ),
            rx.el.div(
                rx.el.a(rx.icon("twitter", class_name="h-5 w-5"), href="#"),
                rx.el.a(rx.icon("github", class_name="h-5 w-5"), href="#"),
                rx.el.a(rx.icon("linkedin", class_name="h-5 w-5"), href="#"),
                class_name="flex items-center gap-6 text-gray-400",
            ),
            class_name="mt-12 pt-8 border-t border-gray-200 flex items-center justify-between",
        ),
        class_name="bg-white py-12 px-4 sm:px-6 lg:px-8",
    )