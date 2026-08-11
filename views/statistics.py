import flet as ft
import flet_charts as fch

from database.db import SessionLocal

from repositories.statistics import (
    get_total_snippets,
    get_language_statistics,
    get_total_views,
    get_total_favorites,
    get_most_viewed_snippets,
)


BG = "#0A0F1F"
SURFACE = "#0F172A"
CARD = "#111827"
TEXT_SECONDARY = "#94A3B8"
PURPLE = "#8B5CF6"


def statistics_view(page: ft.Page) -> ft.Control:


    db = SessionLocal()

    try:
        total_snippets = get_total_snippets(db)
        language_stats = get_language_statistics(db)
        total_views = get_total_views(db)
        total_favorites = get_total_favorites(db)

        most_viewed = get_most_viewed_snippets(
            db,
            limit=5,
        )

    finally:
        db.close()

    total_languages = len(language_stats)

    most_used_language = (
        language_stats[0][0]
        if language_stats
        else "None"
    )


    chart_colors = [
        "#8B5CF6",
        "#3B82F6",
        "#06B6D4",
        "#10B981",
        "#F59E0B",
        "#EF4444",
        "#EC4899",
        "#6366F1",
    ]


    def stat_card(
        title: str,
        value: str,
        icon,
    ):
        return ft.Container(
            expand=True,
            bgcolor=SURFACE,
            border_radius=12,
            padding=18,
            content=ft.Row(
                spacing=15,
                controls=[
                    ft.Container(
                        width=45,
                        height=45,
                        border_radius=12,
                        bgcolor="#1D2148",
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(
                            icon,
                            color=PURPLE,
                            size=22,
                        ),
                    ),

                    ft.Column(
                        spacing=3,
                        controls=[
                            ft.Text(
                                title,
                                size=13,
                                color=TEXT_SECONDARY,
                            ),

                            ft.Text(
                                value,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ],
            ),
        )

    pie_sections = []

    total_language_count = sum(
        count
        for _, count in language_stats
    )

    for index, (language, count) in enumerate(language_stats):

        percentage = (
            count / total_language_count * 100
            if total_language_count
            else 0
        )

        pie_sections.append(
            fch.PieChartSection(
                value=count,
                title=f"{percentage:.0f}%",
                color=chart_colors[
                    index % len(chart_colors)
                ],
                radius=85,
                title_style=ft.TextStyle(
                    size=12,
                    color="white",
                    weight=ft.FontWeight.BOLD,
                ),
            )
        )

    language_pie_chart = fch.PieChart(
        expand=True,
        sections=pie_sections,
        sections_space=2,
        center_space_radius=45,
        center_space_color=SURFACE,
    )



    language_legend = []

    for index, (language, count) in enumerate(language_stats):

        percentage = (
            count / total_language_count * 100
            if total_language_count
            else 0
        )

        language_legend.append(
            ft.Row(
                spacing=10,
                controls=[
                    ft.Container(
                        width=10,
                        height=10,
                        border_radius=5,
                        bgcolor=chart_colors[
                            index % len(chart_colors)
                        ],
                    ),

                    ft.Text(
                        language,
                        size=13,
                        expand=True,
                    ),

                    ft.Text(
                        f"{percentage:.1f}%",
                        size=13,
                        color=TEXT_SECONDARY,
                    ),
                ],
            )
        )

    if not language_legend:

        language_legend.append(
            ft.Text(
                "No language data available.",
                color=TEXT_SECONDARY,
            )
        )



    bar_groups = []

    for index, (language, count) in enumerate(language_stats):

        bar_color = (
            PURPLE
            if index == 0
            else "#475569"
        )

        bar_groups.append(
            fch.BarChartGroup(
                x=index,
                rods=[
                    fch.BarChartRod(
                        from_y=0,
                        to_y=count,
                        width=30,
                        color=bar_color,
                        border_radius=6,
                        tooltip=fch.BarChartRodTooltip(
                            f"{language}: {count}"
                        ),
                    ),
                ],
            )
        )

    bottom_labels = []

    for index, (language, _) in enumerate(language_stats):

        bottom_labels.append(
            fch.ChartAxisLabel(
                value=index,
                label=ft.Text(
                    language,
                    size=11,
                    color=TEXT_SECONDARY,
                ),
            )
        )

    max_language_count = max(
        [count for _, count in language_stats],
        default=10,
    )

    language_bar_chart = fch.BarChart(
        expand=True,
        interactive=True,

        max_y=max_language_count + 5,

        groups=bar_groups,

        bottom_axis=fch.ChartAxis(
            labels=bottom_labels,
            label_size=35,
        ),

        left_axis=fch.ChartAxis(
            label_size=35,
        ),

        right_axis=fch.ChartAxis(
            show_labels=False,
        ),

        horizontal_grid_lines=fch.ChartGridLines(
            color="#1E293B",
            width=1,
            dash_pattern=[3, 3],
        ),
    )


    viewed_controls = []

    for index, snippet in enumerate(
        most_viewed,
        start=1,
    ):

        viewed_controls.append(
            ft.Container(
                bgcolor=SURFACE,
                border_radius=10,
                padding=12,

                content=ft.Row(
                    spacing=15,
                    controls=[
                        ft.Text(
                            f"{index:02d}",
                            size=14,
                            color=PURPLE,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Column(
                            expand=True,
                            spacing=3,
                            controls=[
                                ft.Text(
                                    snippet.title,
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),

                                ft.Text(
                                    snippet.language,
                                    size=12,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),

                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.Icon(
                                    ft.Icons.VISIBILITY,
                                    size=16,
                                    color=TEXT_SECONDARY,
                                ),

                                ft.Text(
                                    str(
                                        snippet.view_count
                                    ),
                                    size=13,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    if not viewed_controls:

        viewed_controls.append(
            ft.Container(
                bgcolor=SURFACE,
                border_radius=10,
                padding=20,
                alignment=ft.Alignment(0, 0),

                content=ft.Text(
                    "No snippets viewed yet.",
                    color=TEXT_SECONDARY,
                ),
            )
        )



    return ft.Column(
        spacing=15,
        scroll=ft.ScrollMode.AUTO,

        controls=[

            ft.Text(
                "Statistics",
                size=26,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Overview of your ByteVault activity.",
                size=14,
                color=TEXT_SECONDARY,
            ),

            ft.Container(height=5),



            ft.Row(
                spacing=12,
                controls=[
                    stat_card(
                        "Total Snippets",
                        str(total_snippets),
                        ft.Icons.CODE,
                    ),

                    stat_card(
                        "Total Views",
                        str(total_views),
                        ft.Icons.VISIBILITY,
                    ),

                    stat_card(
                        "Languages",
                        str(total_languages),
                        ft.Icons.LANGUAGE,
                    ),

                    stat_card(
                        "Favorites",
                        str(total_favorites),
                        ft.Icons.FAVORITE,
                    ),
                ],
            ),

            ft.Container(height=5),



            ft.Text(
                "Language Distribution",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                f"{most_used_language} is your most used language.",
                size=13,
                color=TEXT_SECONDARY,
            ),

            ft.Container(
                bgcolor=SURFACE,
                border_radius=12,
                padding=20,
                height=320,

                content=ft.Row(
                    spacing=25,

                    controls=[
                        ft.Container(
                            width=280,
                            height=280,
                            content=language_pie_chart,
                        ),

                        ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12,
                            controls=language_legend,
                        ),
                    ],
                ),
            ),

            ft.Container(height=5),



            ft.Text(
                "Language Comparison",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Compare the number of snippets "
                "written in each language.",
                size=13,
                color=TEXT_SECONDARY,
            ),

            ft.Container(
                bgcolor=SURFACE,
                border_radius=12,
                padding=20,
                height=360,
                content=language_bar_chart,
            ),

            ft.Container(height=5),


            ft.Text(
                "Most Viewed Snippets",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Your most visited snippets.",
                size=13,
                color=TEXT_SECONDARY,
            ),

            ft.Column(
                spacing=8,
                controls=viewed_controls,
            ),
        ],
    )