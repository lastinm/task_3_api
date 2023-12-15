from sre_parse import Tokenizer
from fastapi import FastAPI                 # Библиотека для создания веб-приложения
#from transformers import pipeline           # Пайплайн модели машинного обучения
from pydantic import BaseModel              # Класс для интерфейса веб-приложения
#import re                                   # Библиотека регулярных выражений
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Создадим класс Item ('элемент') содержаний свойство text типа строка на основе класса BaseModel библиотеки pydantic
class Item(BaseModel):
    text: str

# Сохраним объект веб-приложения в переменной app
app = FastAPI()

model_checkpoint = 'cointegrated/rubert-tiny-toxicity'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
if torch.cuda.is_available():
    model.cuda()

# Создадим функцию вызова пайплайна
# def load_model(model_checkpoint):
#     model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
#     if torch.cuda.is_available():
#         model.cuda()
#     return model_checkpoint, model

# Загружаем предварительно обученную модель в переменную model
#model = load_model(model_checkpoint)

# Для корневой страницы сайта выдадим предупреждение.
@app.get("/")
async def root():
    """Для получения результата от модели используйте в адресе /predict/"""
    return {"msg": "Для получения результата от модели используйте в адресе /predict/"}

# Основная функция приложения, вызываемая по адресу: http://....../predict/
# Получаем из запроса POST объект item созданного нами класса Item
@app.post("/predict/")
async def predict(item: Item):
    u"""Сформулируйте строку для определения вероятности содержания в ней негативного подтекста."""
    with torch.no_grad():
        inputs = tokenizer(item.text, return_tensors='pt', truncation=True, padding=True).to(model.device)
        proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()
    if isinstance(item.text, str):
        proba = proba[0]
    #if aggregate:
    return 1 - proba.T[0] * (1 - proba.T[-1])
    #return proba





