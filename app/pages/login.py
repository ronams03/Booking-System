import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    """The login page for the admin dashboard."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("calendar-check", class_name="h-8 w-8 text-emerald-500"),
                    href="/",
                    class_name="flex items-center justify-center",
                ),
                rx.el.h2(
                    "Sign in to your admin account",
                    class_name="mt-6 text-center text-2xl font-bold tracking-tight text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Email address",
                                htmlFor="email",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="email",
                                    id="email",
                                    name="email",
                                    auto_complete="email",
                                    required=True,
                                    class_name="mt-1 block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-emerald-500 focus:outline-none focus:ring-emerald-500 sm:text-sm",
                                ),
                                class_name="mt-1",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Password",
                                htmlFor="password",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="password",
                                    id="password",
                                    name="password",
                                    auto_complete="current-password",
                                    required=True,
                                    class_name="mt-1 block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-emerald-500 focus:outline-none focus:ring-emerald-500 sm:text-sm",
                                ),
                                class_name="mt-1",
                            ),
                            class_name="mt-4",
                        ),
                        rx.cond(
                            AuthState.login_error,
                            rx.el.div(
                                rx.el.p(
                                    AuthState.login_error,
                                    class_name="text-sm text-red-600",
                                ),
                                class_name="mt-4",
                            ),
                            None,
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.cond(
                                    AuthState.is_loading,
                                    rx.spinner(class_name="mr-2"),
                                    None,
                                ),
                                rx.cond(
                                    AuthState.is_loading, "Signing in...", "Sign in"
                                ),
                                type="submit",
                                disabled=AuthState.is_loading,
                                class_name="mt-6 flex w-full justify-center rounded-md border border-transparent bg-emerald-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50",
                            ),
                            class_name="pt-2",
                        ),
                    ),
                    on_submit=AuthState.login,
                ),
                class_name="mt-8",
            ),
            class_name="mx-auto w-full max-w-sm",
        ),
        class_name="flex min-h-screen flex-col justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 font-['Poppins']",
    )