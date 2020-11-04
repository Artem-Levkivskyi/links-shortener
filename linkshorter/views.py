from django.shortcuts import render
from django.http import HttpResponseRedirect
from linkshorter.forms import ShorterForm
from linkshorter.models import WebSite
from shorter import settings
from random import choice
from string import ascii_letters
import validators


# Рендеринг главной страницы
def main_page(request):
    return render(request, 'main_page.html', {})


# Рендеринг после отправки формы сокращения ссылки
def result_page(request):
    full_link = None

    if request.method == "GET":
        full_link_container = ShorterForm(request.GET)

        if full_link_container.is_valid():
            full_link = full_link_container.cleaned_data['full_link']

    # Проверяем, является ли введенное значение ссылкой.
    # Если да - обрабатываем полученное значение. Иначе - рендерим страницу с сообщением об ошибке.
    if validators.url(full_link):
        # Проверяем наличие введенной для сокращения ссылки в базе данных
        try:
            key = WebSite.objects.get(full_link=full_link)

        # Если в базе данных отсутствует ссылка, которую необходимо сократить
        # 1. Создаем key для короткой ссылки
        # 2. Размещаем в базе данных запись с полной ссылкой и созданным key для короткой ссылки
        # 3. Готовим к рендерингу короткую ссылку, содержащую сгенерированный key
        except WebSite.DoesNotExist:

            while True:
                # Генерируем уникальный key для ссылки
                key = ''.join(choice(ascii_letters) for i in range(10))
                # Проверяем сгенерированный key на дубликаты в базе данных
                try:
                    duplicate = WebSite.objects.get(short_link=key)
                # Если в базе данных отсутствует дубликат key выходим из цикла
                except WebSite.DoesNotExist:
                    break

            # Создаем в базе данных запись с полной ссылкой и key-значением
            WebSite.objects.create(full_link=full_link, short_link=key)

            # Если в конфигурации сайта присутствует доменное имя, используем для генерации короткой ссылки его.
            if settings.ALLOWED_HOSTS:
                short_link = settings.ALLOWED_HOSTS[0] + key
            # Иначе - локальный адрес
            else:
                short_link = f'http://127.0.0.1:8000/{key}'

        # Если в базе данных присутствует ссылка, которую необходимо сократить
        # Готовим к рендерингу короткую ссылку, содержащую изъятый из базы данных key
        else:
            # Если в конфигурации сайта присутствует доменное имя, используем для генерации короткой ссылки его.
            if settings.ALLOWED_HOSTS:
                short_link = settings.ALLOWED_HOSTS[0] + key
            # Иначе - локальный адрес
            else:
                short_link = f'http://127.0.0.1:8000/{key}'

        # Рендерим шаблон с результатом сокращения ссылки, передавая в него короткую ссылку
        finally:
            return render(request, 'result_page.html', {'result': short_link})
    else:
        return render(request, 'result_page.html', {'result': 'Value is not URL'})


# Обработка редиректа при переходе по короткой ссылке
def redirect(request, key):
    # Проверяем наличие key из короткой ссылки в базе данных
    try:
        full_link = WebSite.objects.filter(short_link=key)[0].full_link
    # Если key отсутствует - открываем страницу с сообщением об ошибке
    except WebSite.DoesNotExist:
        return render(request, 'result_page.html', {'result': 'Short URL is not valid'})
    # Если key присутствует - редиректим пользователя на нужный сайт
    else:
        return HttpResponseRedirect(full_link)
