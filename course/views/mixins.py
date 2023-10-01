from django.views.generic import DetailView
from django.views.generic.edit import FormMixin


class AddTitleFormMixin(FormMixin):
    title = None
    editing = False

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.title or "Нет названия"
        kwargs['editing'] = self.editing
        return super().get_context_data(**kwargs)


class ProDetailView(DetailView):
    def title(self):
        return self.object.title

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.title or "Нет названия"
        can_edit = False
        if self.request.user.is_authenticated:
            can_edit = self.request.user.pk == self.object.creator_id or self.request.user.is_superuser
        kwargs['can_edit'] = can_edit
        return super().get_context_data(**kwargs)
