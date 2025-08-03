from django.core.management.base import BaseCommand
from auth_app.models import User, Role, Permission, UserRole, RolePermission

class Command(BaseCommand):
    help = 'Заполнить базу тестовыми ролями, пользователями и правами с удалением старых данных'

    def handle(self, *args, **kwargs):
        self.stdout.write("Удаляем старые данные...")
        UserRole.objects.all().delete()
        RolePermission.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()
        Permission.objects.all().delete()

        self.stdout.write("Создаем роли...")
        admin_role = Role.objects.create(name="admin")
        user_role = Role.objects.create(name="user")

        self.stdout.write("Создаем права...")
        perm_read = Permission.objects.create(action="read", resource="/documents/")
        perm_write = Permission.objects.create(action="write", resource="/documents/")
        perm_delete = Permission.objects.create(action="delete", resource="/documents/")

        self.stdout.write("Связываем роли и права...")
        RolePermission.objects.create(role=admin_role, permission=perm_read)
        RolePermission.objects.create(role=admin_role, permission=perm_write)
        RolePermission.objects.create(role=admin_role, permission=perm_delete)
        RolePermission.objects.create(role=user_role, permission=perm_read)

        self.stdout.write("Создаем пользователей...")
        admin = User.objects.create(email="admin@example.com", first_name="Admin", last_name="Adminov", is_active=True, is_staff=True, is_superuser=True)
        admin.set_password("adminpass")
        admin.save()

        user = User.objects.create(email="user@example.com", first_name="User", last_name="Userov", is_active=True)
        user.set_password("userpass")
        user.save()

        self.stdout.write("Назначаем роли пользователям...")
        UserRole.objects.create(user=admin, role=admin_role)
        UserRole.objects.create(user=user, role=user_role)

        self.stdout.write("Тестовые данные успешно созданы!")
