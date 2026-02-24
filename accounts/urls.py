from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [   
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path("subscribe/", views.subscribe_email, name="subscribe_email"),
    
      # Password reset request
    path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.txt',   # TEXT
        html_email_template_name='password_reset_email.html',  # HTML
        subject_template_name='password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done')
    ),
    name='password_reset'
),


    # After submitting email
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Link in email
path(
    'password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')  # use name, not hardcoded URL
    ),
    name='password_reset_confirm'
),


    # After resetting password
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    
    path('notifications/', views.notifications, name='notifications'),
    path("notifications/count/", views.get_notification_count, name="notification_count"),
    path("account/", views.account_dashboard, name="account_dashboard"),
    path('profile/', views.profile, name='profile'),
    path('addresses/', views.address_list, name='address_list'),
    path('custom-cake-orders/', views.custom_cake_orders, name='custom_cake_orders'),
    path('change-password/', views.change_password, name='change_password'),

]