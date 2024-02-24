from fastapi import FastAPI                 # Библиотека для создания веб-приложения
from transformers import pipeline           # Пайплайн модели машинного обучения
from pydantic import BaseModel              # Класс для интерфейса веб-приложения
import re                                   # Библиотека регулярных выражений


# Создадим класс Item ('элемент') содержаний свойство text типа строка на основе класса BaseModel библиотеки pydantic
class Item(BaseModel):
    text: str


# Сохраним объект веб-приложения в переменной app
app = FastAPI()


# Создадим функцию вызова пайплайна
def load_model():
    return pipeline('fill-mask', model='xlm-roberta-base')


# Загружаем предварительно обученную модель в переменную model
model = load_model()


# Для корневой страницы сайта выдадим предупреждение.
@app.post("/")
async def root():
    """Для получения результата от модели используйте в адресе /predict/"""
    return "Для получения результата от модели используйте в адресе /predict/"


# Основная функция приложения, вызываемая по адресу: http://....../predict/
# Получаем из запроса POST объект item созданного нами класса Item
@app.post("/predict/")
async def predict(item: Item):
    u"""Напишите предложение, указав вместо подбираемого слова шаблон <mask>: 'Этот <mask> стол здесь не стоял'."""
    # Проверим строку на наличие в ней нужного шаблона
    all_ok = re.search("<mask>", item.text)
    if all_ok:
        # Шаблон найден, тогда вернем результат работы модели
        return model(item.text)
    else:
        # Шаблон не найден, тогда предупредим пользователя
        return "В строке не найден шаблон <mask>."
