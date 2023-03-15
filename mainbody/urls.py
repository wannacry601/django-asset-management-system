from django.urls import path
from mainbody import views

urlpatterns = [
    path("change_password/",views.passwordchange),
    path("",views.homepage),
    path("logout/",views.logout),
    path("manage_inf/",views.manageinf),
    # path("admin/",views.admin_page)
]
