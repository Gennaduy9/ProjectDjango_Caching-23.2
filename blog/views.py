from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'body',)
    extra_context = {
        'title': 'Добавить статью'
    }
    success_url = reverse_lazy('blog:list')

    def get_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()

            return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    permission_required = 'blog.change_article'
    extra_context = {
        'title': 'Изменить или редактировать статью'
    }

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='Модераторы').exists():
            return self.object
        if self.request.user.is_superuser:
            return self.object
        if self.request.user.groups.filter(name='Контент-менеджера').exists():
            return self.object
        return self.object

    def get_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()

            return super().form_valid(form)


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    extra_context = {
        'title': 'Cтатьи'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    model = Article
    extra_context = {
        'title': 'Cтатьи'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:list')

# def toggle_activity(request, pk):
#     article_item = get_object_or_404(Article, pk=pk)
#     if article_item.is_published:
#         article_item.is_published = False
#     else:
#         article_item.is_published = True
#
#     article_item.save()
#
#     return redirect(reverse('blog:list'))