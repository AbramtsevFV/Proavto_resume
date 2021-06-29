from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,  DetailView, FormView, CreateView
from django.views.generic.list import MultipleObjectMixin

from .models import *
from .forms import Search, FeedbackForm


class HomePage(TemplateView):
    template_name = "proauto/index.html"
    allow_empty = False

    def get_context_data(self, **kwargs):
        # добавляем форму поиска в контекст
        context = super().get_context_data(**kwargs)
        context['search'] = Search
        return context


class Country(DetailView):
    model = Country
    template_name = 'proauto/countru.html'
    slug_url_kwarg = 'country_slug'
    context_object_name = "country"
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = Search
        return context



class Brend_auto(DetailView, MultipleObjectMixin ):
    model = Brend
    paginate_by = 7
    template_name = 'proauto/brend.html'
    slug_url_kwarg = 'brend_slug'
    context_object_name = "brend"
    allow_empty = False

    def get_context_data(self, **kwargs):
        """
        Добавляем в контексту выборку из моделей определённого бренда, по
        параметру slug_url_kwarg.
        """
        object_list = Auto.objects.filter(cat__slug=self.kwargs['brend_slug'])
        context = super(Brend_auto, self).get_context_data(object_list=object_list, **kwargs)
        context['search'] = Search
        return context


class Car_model(DetailView):
    model = Auto
    template_name = 'proauto/car_model.html'
    slug_url_kwarg = 'auto_slug'
    context_object_name = 'car'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(Car_model, self).get_context_data( **kwargs)
        context['title'] = context['car']
        context['search'] = Search
        return context


class SearchCar(TemplateView, FormView):
    template_name = 'proauto/search_page.html'
    form_class = Search
    success_url = '/search/'


    def get(self, request, *args,  **kwargs):
        """
        Получаем список из модели Auto, согласно данных полученых GET запросом.
        """
        form = self.form_class(request.GET)
        if form.is_valid():
            object_list = Auto.objects.filter(title__icontains=form.cleaned_data['search'])
            return render(request, self.template_name, {'form': form, 'object_list': object_list})

        return render(request, self.template_name, {'form': form})


class Feedback(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'proauto/feedback_page.html'
    success_url = reverse_lazy('glavnaya')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = Search
        return context

    def form_valid(self, form):
        """
        Отправка емаил пользователю и админу(вопрос пользователя).

        """
        content = f"Добрый день {form.data['name']}! Благодарим за обращение в Службу поддержки пользователей сайта проавто! Данное сообщение не требует ответа! Мы Вам ответим в течении 48 часов. C уважением служба технической поддержки!"
        subject = "Техподдержка сайта proproauto"
        send_mail(subject, content,
                  'support@proproauto.ru',
                  [form.data['email']]
                  )
        content = f"Текст вопроса: {form.data['massage']}  Отправитель {form.data['email']} "
        send_mail(subject, content,
                  'support@proproauto.ru',
                  ['support@proproauto.ru']
                  )
        # сохранение в бд
        return super().form_valid(form)




