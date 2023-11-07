from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyCreatorMixin(UserPassesTestMixin):
    def test_func(self):

        if self.request.user.id == self.model.objects.get(pk=int(self.kwargs['pk'])).creator_id or \
                self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False
