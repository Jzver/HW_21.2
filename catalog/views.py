from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(name, phone, message)
        return super().get(request, *args, **kwargs)


class ProductListView(ListView):
    """Класс для вывода страницы со всеми продуктами"""
    model = Product

    def get_context_data(self, *args, **kwargs):
        """Метод для получения версий Продукта и вывода только активной версии"""
        context = super().get_context_data(*args, **kwargs)
        products = self.get_queryset()
        for product in products:
            product.version = product.versions.filter(is_current=True).first()

        # Данная строчка нужна, чтобы в contex добавились новые данные о Продуктах
        context["object_list"] = products

        return context


class ProductDetailView(DetailView):
    """Класс для вывода страницы с одним продуктом по pk"""
    model = Product

    def get_object(self, queryset=None):
        """Метод для настройки работы счетчика просмотра продукта"""
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    # Добавляем формы. Заменяем fields на form_class
    # fields = ('name', 'description', 'preview', 'category', 'price')
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def get_context_data(self, **kwargs):
        """Метод для создания Формсета и настройки его работы"""
        context_data = super().get_context_data(**kwargs)

        # Создаем ФОРМСЕТ
        # В агрументах прописывается только форма для модели Версия,
        # так как в этом классе form_class = ProductForm уже был указан выше
        # Количество экземпляров, выводимое на страницу
        # instance говорит о том, откуда мы получаем информацию, нужен только для редактирования объекта,
        # для создания не обязателен,
        # extra=1 - означает, что будет выводиться только новая форма для заполнения
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)

        else:
            context_data['formset'] = VersionFormset()

        return context_data

    def form_valid(self, form):
        """Метод для проверки валидации формы и формсета"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        # Задаем условие, при котором д.б. валидными и форма и формсет
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            # save() данная функция сохраняет внесенные изменения
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductUpdateView(UpdateView):
    model = Product

    form_class = ProductForm

    def get_success_url(self):
        """ Метод для определения пути, куда будет совершен переход после редактирования продкута"""
        return reverse('catalog:product_detail', args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        """Метод для создания Формсета и настройки его работы"""
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)

        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """Метод для проверки валидации формы и формсета"""
        context_data = self.get_context_data()
        formset = context_data['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')
