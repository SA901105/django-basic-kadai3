from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

class PaidMemberRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is a paid member."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_paid_member:
            return HttpResponseForbidden("この機能は有料会員のみ利用可能です。")
        return super().dispatch(request, *args, **kwargs)
