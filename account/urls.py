from django.conf.urls import url

from .views import SignUpFormView
from .views import ProfileSearch
from .views import NewUserLandingView
from .views import UpdateProfileFormView
from .views import UpdateProfileAvatarForm
from .views import UpdateProfileDescriptionForm
from .views import AdminNotificationAcceptView
from .views import AdminNotificationRejectView
from .views import AdminNotificationResendView
from .views import ProfessionalProfileCategoryView
from .views import UserMessageFormView

from .views import LoadNotificationModal
from .views import LoadMessageModal
from .views import InboxView
from .views import NotificationsView

urlpatterns = [
    url(
        r'^$',
        SignUpFormView.as_view(),
        name='signup_form_submit',
    ),

    # API Userprofile
    url(
        r'^profile-search/$',
        ProfileSearch.as_view(),
        name='profile-search',
    ),

    url(
        r'^landing/$',
        NewUserLandingView.as_view(),
        name='signup_landing',
    ),

    url(
        r'^update/$',
        UpdateProfileFormView.as_view(),
        name='profile_update',
    ),

    url(
        r'^ax_update_professional_profile_category/$',
        ProfessionalProfileCategoryView.as_view(),
        name='ax_update_professional_profile_category',
    ),

    url(
        r'^ax_account/update_description/$',
        UpdateProfileDescriptionForm.as_view(),
        name='update_profile_description_form',
    ),

    url(
        r'^ax-post-notification-load/(?P<pk>\d+)/$',
        LoadNotificationModal.as_view(),
        name='ajax_post_notification_load',
    ),

    url(
        r'^admin_notification_accept/(?P<pk>\d+)/$',
        AdminNotificationAcceptView.as_view(),
        name='admin_notification_accept',
    ),

    url(
        r'^admin_notification_reject/(?P<pk>\d+)/$',
        AdminNotificationRejectView.as_view(),
        name='admin_notification_reject',
    ),

    url(
        r'^ax_admin_notification_resend/(?P<pk>\d+)/$',
        AdminNotificationResendView.as_view(),
        name='admin_notification_resend',
    ),

    url(
        r'^ax_send_user_mesasge/$',
        UserMessageFormView.as_view(),
        name='send_user_mesasge',
    ),

    url(
        r'^ax-post-message-load/(?P<pk>\d+)/$',
        LoadMessageModal.as_view(),
        name='ajax_post_message_load',
    ),

    url(
        r'^inbox/$',
        InboxView.as_view(),
        name='inbox_view',
    ),

    url(
        r'^notifications/$',
        NotificationsView.as_view(),
        name='notifications_view',
    ),

    url(
        r'^ax_profile_avatar/$',
        UpdateProfileAvatarForm.as_view(),
        name='update_profile_avatar_form',
    ),
]
