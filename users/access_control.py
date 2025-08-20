from .models import AccessRule, Role, Permission


def check_access(user, resource: str, action: str) -> bool:
    """
    Проверка, есть ли у пользователя доступ к ресурсу
    :param user: объект User
    :param resource: название ресурса (например "documents")
    :param action: действие (например "view_documents")
    """
    if not user.is_active:
        return False

    # 2. роль должна быть назначена
    if not user.role:
        return False

    perm = Permission.objects.filter(name=action).first()
    if not perm:
        return False

    have_access = AccessRule.objects.filter(
        role=user.role,
        permission=perm,
        resource=resource,
        allowed=True,
    ).exists()

    return have_access
