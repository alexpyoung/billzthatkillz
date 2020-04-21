from django.utils.html import format_html


def link(url: str, text: str) -> str:
    return format_html(
        f'<a href="{{url}}" target="_blank">{{text}}</a>', url=url, text=text,
    )
