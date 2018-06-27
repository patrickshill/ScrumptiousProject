from django.conf.urls import url
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^register_user$', views.registerUser),
    url(r'^login$', views.login),
    url(r'^login_user$', views.loginUser),
    url(r'^logout$', views.logout),
    url(r'^projects$', views.projects),
    url(r'^board/(?P<boardID>\d+)$', views.board),
    url(r'^create_board$', views.createBoard),
    url(r'^add_list$', views.addList),
    url(r'^add_task$', views.addTask),
]
