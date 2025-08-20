from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_initial_data(apps, schema_editor):
    User = apps.get_model("users", "User")
    Role = apps.get_model("users", "Role")
    Permission = apps.get_model("users", "Permission")
    AccessRule = apps.get_model("users", "AccessRule")

    # роли
    admin_role, _ = Role.objects.get_or_create(name="admin")
    user_role = Role.objects.create(name="user")

    # права
    p_create = Permission.objects.create(name="create")
    p_read = Permission.objects.create(name="read")
    p_edit = Permission.objects.create(name="edit")
    p_delete = Permission.objects.create(name="delete")

    # базовые правила
    AccessRule.objects.create(role=admin_role, permission=p_create, resource="documents")
    AccessRule.objects.create(role=admin_role, permission=p_read, resource="documents")
    AccessRule.objects.create(role=admin_role, permission=p_edit, resource="documents")
    AccessRule.objects.create(role=admin_role, permission=p_delete, resource="documents")
    AccessRule.objects.create(role=admin_role, permission=p_create, resource="projects")
    AccessRule.objects.create(role=admin_role, permission=p_read, resource="projects")
    AccessRule.objects.create(role=admin_role, permission=p_edit, resource="projects")
    AccessRule.objects.create(role=admin_role, permission=p_delete, resource="projects")

    AccessRule.objects.create(role=user_role, permission=p_read, resource="documents")
    AccessRule.objects.create(role=user_role, permission=p_read, resource="projects")

    # тестовый админ (с захэшированным паролем)
    User.objects.create(
        email="admin@admin.com",
        first_name="Admin",
        password=make_password("123456"),
        role=admin_role,
    )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_func),
    ]
