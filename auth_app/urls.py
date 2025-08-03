from django.urls import path

from auth_app.views import LoginView, LogoutView, RegisterView, protected_view, read_reports, view_documents, \
    create_document, delete_document

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path('protected/', protected_view), # тестовый url для проверки распознавания пользователя
    path('reports/', read_reports), # тестовый url для проверки разрешений и ролей
    path('documents/', view_documents), # тестовый url для проверки разрешений и ролей
    path('documents/create/', create_document), # тестовый url для проверки разрешений и ролей
    path('documents/delete/', delete_document), # тестовый url для проверки разрешений и ролей
]
