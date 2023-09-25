from django.views.generic.edit import FormMixin


class AddTitleFormMixin(FormMixin):
    def get_context_data(self, **kwargs):
        kwargs['title'] = self.title or "Нет названия"
        return super().get_context_data(**kwargs)
