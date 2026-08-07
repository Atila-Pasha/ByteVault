from datetime import datetime
import random


def get_greeting(firstname: str, snippets_count: int):
    hour = datetime.now().hour

    if 5 <= hour < 12:
        titles = [
            f"Good Morning, {firstname}.",
            f"Morning, {firstname}.",
            f"Welcome back, {firstname}.",
            f"Ready for a productive day, {firstname}?",
        ]

    elif 12 <= hour < 17:
        titles = [
            f"Good Afternoon, {firstname}.",
            f"Welcome back, {firstname}.",
            f"Hope your day is going well, {firstname}.",
            f"Let's build something today.",
        ]

    elif 17 <= hour < 22:
        titles = [
            f"Good Evening, {firstname}.",
            f"Welcome back, {firstname}.",
            f"Time for another coding session.",
            f"Let's finish today strong.",
        ]

    else:
        titles = [
            f"Working late, {firstname}?",
            f"Night session started.",
            f"Still coding?",
            f"The night is yours.",
        ]

    title = random.choice(titles)

    subtitles = []

    if snippets_count == 0:
        subtitles.extend([
            "Your vault is empty. Create your first snippet.",
            "Start building your personal code library.",
            "Every great collection starts with one snippet.",
        ])

    else:
        subtitles.extend([
            f"You have {snippets_count} snippets in your vault.",
            f"{snippets_count} snippets ready whenever you need them.",
            f"Your code library contains {snippets_count} snippets.",
        ])

    if snippets_count >= 25:
        subtitles.append(
            "Your collection keeps growing."
        )

    if snippets_count >= 100:
        subtitles.append(
            "A solid knowledge base is taking shape."
        )

    if snippets_count >= 250:
        subtitles.append(
            "You've built an impressive snippet library."
        )

    tips = [
        "Tip: Keep your snippets well documented.",
        "Tip: Small reusable snippets save hours.",
        "Tip: Clear names make snippets easier to find.",
        "Tip: Delete outdated snippets regularly.",
        "Tip: Reusable code is productive code.",
        "Tip: Simplicity beats complexity.",
    ]


    if random.random() < 0.15:
        subtitle = random.choice(tips)
    else:
        subtitle = random.choice(subtitles)

    return title, subtitle