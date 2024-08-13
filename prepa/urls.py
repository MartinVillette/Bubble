from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from english import views as english_views
from french import views as french_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', english_views.home, name='home'),

    path('english/createlesson', english_views.create_lesson, name='create-lesson-english'),
    path('<username>/english', english_views.user_lessons, name='user-lessons-english'),
    path('english/<lesson_id>', english_views.lesson, name='lesson-english'),
    path('english/<lesson_id>/cards', english_views.lesson_cards, name='lesson-english-cards'),
    path('english/<lesson_id>/edit', english_views.edit_lesson, name='edit-lesson-english'),
    path('english/<lesson_id>/copy', english_views.copy_lesson, name='copy-lesson-english'),
    path('english/<lesson_id>/delete', english_views.delete_lesson, name='delete-lesson-english'),
    path('english/<lesson_id>/quizz', english_views.quizz, name='lesson-quizz-english'),
    path('english/<lesson_id>/training', english_views.training, name='lesson-training-english'),
    path('english/<lesson_id>/share/<share_id>', english_views.lesson_share, name='lesson-share-english'),


    # path('createlesson/french', french_views.create_lesson, name='create-lesson-french'),
    path('french', french_views.lesson, name='lesson-french'),
    path('french/quotes', french_views.quotes, name='french-quotes'),
    path('french/addquote', french_views.add_quote, name='add-quote'),
    path('french/typing', french_views.typing, name='lesson-typing-french'),
    path('french/learning', french_views.learning, name='lesson-learning-french'),
    path('french/share/<quote_id>', french_views.quote_share, name='quote-share'),


    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),


    path('groups/', users_views.groups, name='groups'),
    path('creategroup/', users_views.create_group, name='create-group'),
    path('groups/<group_id>', users_views.group_page, name='group-page'),
    path('groups/<group_id>/delete', users_views.delete_group, name='delete-group'),
    path('groups/<group_id>/members', users_views.group_members, name='group-members'),
    path('groups/<group_id>/quit', users_views.quit_group, name='quit-group'),
    path('groups/<group_id>/edit', users_views.edit_group, name='edit-group'),
    path('groups/<group_id>/edit_users', users_views.edit_group_users, name='edit-group-users'),
    path('groups/<group_id>/share/<share_id>', users_views.group_share, name='group-share'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('login/redirect', users_views.login_redirect, name='login-redirect'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
