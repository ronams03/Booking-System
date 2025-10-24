import reflex as rx
from typing import TypedDict


class Service(TypedDict):
    icon: str
    name: str
    description: str
    price: str
    features: list[str]


class State(rx.State):
    """The base state for the app."""

    services: list[Service] = [
        {
            "icon": "user",
            "name": "Personal Consultation",
            "description": "One-on-one session with our top experts.",
            "price": "49",
            "features": [
                "30-Minute Session",
                "Expert Advice",
                "Actionable Plan",
                "Follow-up Email",
            ],
        },
        {
            "icon": "users",
            "name": "Team Workshop",
            "description": "A collaborative workshop for your entire team.",
            "price": "199",
            "features": [
                "2-Hour Workshop",
                "Up to 10 members",
                "Interactive Activities",
                "Digital Whiteboard Access",
            ],
        },
        {
            "icon": "briefcase",
            "name": "Corporate Package",
            "description": "Comprehensive solutions for your business needs.",
            "price": "499",
            "features": [
                "Full Day On-site",
                "Unlimited Members",
                "Customized Agenda",
                "Dedicated Support",
            ],
        },
    ]