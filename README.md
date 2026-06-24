# image-processor-app
Educational practice

## Запуск приложения

1. Клонируйте репозиторий:
git clone https://github.com/NataliaSte/image-processor-app.git
cd image-processor-app

2. Создайте виртуальное окружение (Windows):
python -m venv venv-app
venv-app\Scripts\activate

3. Установите зависимости:
pip install -r requirements.txt

4. Запустите приложение:
python src/main.py

## Использование

- **Загрузить изображение** — выбор файла PNG или JPG
- **Снимок с камеры** — ПРОБЕЛ для снимка, ESC для отмены
- **Каналы** — Красный / Зелёный / Синий
- **Негатив** — инверсия цветов
- **Границы** — ввод толщины в пикселях
- **Линия** — ввод координат и толщины
- **Сброс** — возврат к оригиналу
- **Сохранить** — экспорт в PNG или JPG

## Ссылка на репозиторий

[https://github.com/NataliaSte/image-processor-app] (https://github.com/NataliaSte/image-processor-app)