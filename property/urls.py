from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("messages", views.messages, name="messages"),
    path("issues", views.issues, name="issues"),
    path("profile", views.profile, name="profile"),
    path("add_property", views.add_property, name="add_property"),
    path("report_issue", views.report_issue, name="report_issue"),
    path("send_message", views.send_message, name="send_message"),
    path("unit/<int:unit_id>", views.unit, name="unit"),
    path("unit_messages/<int:unit_id>", views.unit_messages, name="unit_messages"),
    path("unit_issues/<int:unit_id>", views.unit_issues, name="unit_issues")


    # API Routes
    #path("edit/<int:post_id>", views.edit, name="edit"),
]