import flet
from tag import Tag
from tag_color import TagColor


def get_tag_widget(tag: Tag, enlarged: bool = False) -> flet.Container:
    if tag.color in [TagColor.YELLOW, TagColor.PINK]:  # TODO
        text_color = flet.colors.BLACK
    else:
        text_color = flet.colors.WHITE

    text_size = 16 if enlarged else 12

    return flet.Container(
        padding=flet.padding.symmetric(horizontal=5, vertical=2.5),
        content=flet.Text(tag.label, size=text_size, color=text_color),
        bgcolor=tag.color,
        border_radius=flet.border_radius.all(5)
    )
