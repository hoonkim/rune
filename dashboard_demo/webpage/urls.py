from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user_signup$', views.userSignup, name='user_signup'),
    url(r'^login_proc/$', views.loginProc, name='login_proc'),
    url(r'^user_signup_proc/$', views.addUser, name='user_signup_proc'),
    url(r'^project_list$', views.projectList, name='project_list'),
    url(r'^add_project_proc$', views.addProjectProc, name='add_proejct_proc'),
    url(r'^code_list$', views.codeList, name='code_list'),
    url(r'^set_code$', views.setCode, name='set_code'),
    url(r'^set_code_proc$', views.setCodeProc, name='set_code_proc'),

]
