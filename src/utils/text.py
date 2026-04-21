def get_cm_word(count: int) -> str:
    """Возвращает правильное склонение слова 'сантиметр'."""
    count = abs(count)
    rem10 = count % 10
    rem100 = count % 100

    if 11 <= rem100 <= 14:
        return "сантиметров"
    if rem10 == 1:
        return "сантиметр"
    if 2 <= rem10 <= 4:
        return "сантиметра"
    return "сантиметров"

def mention(vk_id: int, first_name: str, last_name: str) -> str:
    """Создает кликабельное упоминание пользователя ВК."""
    return f"[id{vk_id}|{first_name} {last_name}]"

def tag_mention(vk_id: int, text: str) -> str:
    """Создает тег пользователя ВК."""
    return f"@id{vk_id} ({text})"

def tag_mention(domain: str, text: str) -> str:
    """Создает тег пользователя ВК."""
    return f"@{domain} ({text})"