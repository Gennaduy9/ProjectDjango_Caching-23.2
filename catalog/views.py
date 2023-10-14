from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, ProductCuttedForm, VersionForm
from catalog.models import Category, Product, Version
from catalog.services import get_cache_categories


class IndexView(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Автомобильный салон - Главная',
        'lending': 'Кредитование - Мечтайте смелее',
        'Online': 'Покупка онлайн',
        'description': 'Cведения, представленные на сайте, носят информационный характер и не являются публичной офертой',
        'Search': 'Поиск'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:0]
        return context_data


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'description': 'Машина должна быть частью тебя, а ты — её составной частью. Только так можно стать единственным в своем роде. Лучшая машина — новая машина!'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        active_versions = Version.objects.filter(activ_ver=True)
        context_data['active_versions'] = active_versions
        context_data['categories'] = get_cache_categories()
        return context_data


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))[:4]

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data =super().get_context_data(*args, **kwargs)

        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.get(pk=self.kwargs.get('pk'))
            cache.set(key, category_list)
        else:
            category_list = Category.objects.get(pk=self.kwargs.get('pk'))

        category_item =  category_list
        context_data['title'] = f'Модель автомобиля - {category_item.name}'

        return context_data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/includes/inc_product.html'
    context_object_name = 'object'
    pk_url_kwarg = 'pk'


class ContactView(TemplateView):
     template_name = 'catalog/contacts.html'
     extra_context = {
         'title': 'Контакты'
     }


class ConnectionView(TemplateView):
    template_name = 'catalog/connection.html'
    extra_context = {
        'title': 'Обратная связь'
    }

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            print(f'You have new message from {name}({email}): {message}')
        return super().get_context_data(**kwargs)


class StoreView(TemplateView):
    template_name = 'catalog/store.html'


class PrivacyView(TemplateView):
    template_name = 'catalog/privacy.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_create', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'

    def get_success_url(self):
        return reverse('catalog:product_update', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='Модераторы').exists():
            self.form_class = ProductCuttedForm
            return self.object
        if self.request.user.is_superuser:
            return self.object
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        active_version_id = self.request.POST.get('active_version')
        if active_version_id:
            active_version = Version.objects.get(id=active_version_id)
            active_version.is_active = True
            active_version.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.change_product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name='Модераторы').exists():
            self.form_class = ProductCuttedForm
            return self.object
        if self.request.user.is_superuser:
            return self.object
        if self.object.owner != self.request.user:
            raise Http404
        return self.object
