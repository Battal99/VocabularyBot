after_start = []


def after_start_views(func: callable):
    """
    Регистрация функции как event.
    :param func: регистрируемая функция
    :return: func
    """
    if callable(func):
        after_start.append(func)
        return func


def process_after_register_views(*args):
    """
    Действия после регистрации пользователя.
    :param username: имя
    :param user_name: никнейм
    :param user_id: id
    :return: None
    """
    for func in after_start:
        if callable(func):
            func(*args)

