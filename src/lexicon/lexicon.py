class Messages:
    @staticmethod
    def link(link: str) -> str:
        return f"👤 Ссылка на чат:\n\n{link}"


class System:
    name_link = "Ссылка бота"


class Errors: ...


class MainMenu:
    start = "Перезапустить бота"
    help = "Помощь"


class Buttons:
    refresh_link = "Обновить ссылку"
    