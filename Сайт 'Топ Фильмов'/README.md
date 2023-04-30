# Сайт "Топ Фильмов"

###### Проект реализован 15.03.2022

<picture><img src="https://img.shields.io/badge/Flask-025E8C?style=for-the-badge&logo=python&logoColor=white"></picture>
<picture><img src="https://img.shields.io/badge/SQLALCHEMY-025E8C?style=for-the-badge&logo=python&logoColor=white"></picture>
<picture><img src="https://img.shields.io/badge/SQLite-fd5b4a?style=for-the-badge&logo=databricks&logoColor=white"></picture>
<picture><img src="https://img.shields.io/badge/Кинопоиск API-fd5b4a?style=for-the-badge&logo=databricks&logoColor=white"></picture>
<picture><img src="https://img.shields.io/badge/bootstrap-797979?style=for-the-badge&logo=addthis&logoColor=white"></picture>
<picture><img src="https://img.shields.io/badge/Jinja2-797979?style=for-the-badge&logo=addthis&logoColor=white"></picture>

- [x] Добавление фильма происходит из вариантов кинопоиска по ключевому слову;
- [x] При добавлении фильма описание и плакат подтягиваются с того же кинопоиска;
- [x] Возможность изменять оценку и своё мнение по фильму;
- [x] Перерасчёт мест в топе фильмов будет происходить при добавлении фильмов или изменении оценки;
- [x] Хоть сайт и называется "Мой топ-10 фильмов", но он поддерживает и больше

<!-- Toggle -->
<details>
<summary>
<code>Видео</code>: использование сайта
</summary>
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/84059957/215088292-cf50a16b-422b-43cc-a211-c4169553ca62.png">
    <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/84059957/210322548-b635bad5-c53d-4209-a73e-fb0adcc437bf.png">
    <img height="0.8">
</picture>

<video src='https://user-images.githubusercontent.com/84059957/235369615-5ddb179e-64ff-4e22-9c38-a4adb7666487.mp4'>

<!-- Окончание -->
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/84059957/215088776-b06bbe95-42fd-4d78-bcae-70cdbeebbbd3.png">
    <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/84059957/210319906-4f1e79cb-1a45-4e5c-93e9-ae21e197e0b9.png">
    <img>
</picture>
</details>

p.s. подробнее про кинопоиск-api здесь: https://api.kinopoisk.dev/v1/documentation

p.s.s. <kbd>pip install python-dotenv</kbd> для работы с <kbd>secrets.env</kbd> (внутри <kbd>TOKEN=...</kbd>)

<!-- ------------------------ -->
<picture> <img width="100%" src="https://user-images.githubusercontent.com/84059957/202753342-fd2ddfa9-2939-43a2-976a-b19a9f32905f.png"> </picture>

Идеи для улучшения:
- [ ] Заполнить фильмом даже если вдруг кинопоиск такого не предложил;
- [ ] Обработка случая когда название введено неправильно (сейчас просто ничего не выводится, <sub>ибо было западло</sub>);
- [ ] Возможность изменить/дополнить запрос из раздела с выбором фильма, а не только с главной страницы;
- [ ] Превью добавляемого фильма;
- [ ] Менять порядок(верх-низ/низ-верх);
- [ ] Хоть и не даёт один и тот же фильм добавлять несколько раз, но не хватает уведомляющего сообщения об этом :)


