from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_tenant", views.add_tenant, name="add_tenant"),
    path("messages", views.messages, name="messages"),
    path("issues", views.issues, name="issues"),
    path("profile", views.profile, name="profile"),
    path("add_property", views.add_property, name="add_property"),
    path("report_issue", views.report_issue, name="report_issue"),
    path("send_message", views.send_message, name="send_message"),
    path("unit/<int:unit_id>", views.unit, name="unit"),
    path("unit_messages/<int:unit_id>", views.unit_messages, name="unit_messages"),
    path("unit_issues/<int:unit_id>", views.unit_issues, name="unit_issues"),
    path("change_resolved/<int:issue_id>", views.change_resolved, name="change_resolved"),
    path("add_profile_picture", views.add_profile_picture, name="add_profile_picture"),


    # API Routes
    path("edit_issue/<int:issue_id>", views.edit_issue, name="edit_issue"),
    path("unit_messages/delete_message/<int:message_id>", views.delete_message, name="delete_message"),
    path("mark_as_read/<int:unit_id>", views.mark_as_read, name="mark_as_read")
]