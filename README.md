# Whatsapp uploader images to Google Drive and Google Sheets

Ссылка на скачивание - https://github.com/plaksherie/whatsappSalesGoogleSheets/archive/refs/heads/master.zip

### Запуск
```sh
python -m bot --mode=dev
```

Запуск в двух режимах:
- `dev`
- `prod`

Docker в `prod` режиме

### Config
Конфиг в зависимости от режима создается локально из `config.sample.toml` в `config.{mode}.toml`

#### Параметры
Секция selenium:

- `path_profiles` - папка где chrome хранит все профили
- `profile_name` - название профиля(папка профиля)
- `user_agent` - User Agent для браузера чтобы пропускал Whatsapp при headless режиме(у других версий просит обновления)
- `browser_version` - версия браузера(не задействовано, устанавливает ласт версию)
- `timeout_get_messages` - как часто проверять новые сообщения
- `timeout_loading_first_messages` - сколько ожидать загрузки первых сообщений при входе в чат 
- `headless` - headless режим для браузера, без его окна(для ubuntu в prod)

Секция whatsapp:

- `chat_name` - чат который будет прослушивать

Секция google_sheets:

- `config_url_sheet` - ссылка на таблицу с конфигом, в котором прописаны правила обработки сообщений
- `config_worksheet_name` - название листа с конфигом

конфиг в формате:

коммент	| сокращение(hashtag) | ссылка на таблицу | лист | столбец номера | столбец для ссылки

Секция google_drive:

- `folder_id_uploads` - id папки в которую грузить изображения(нужно создать папку на google drive, можно ей выставить общий доступ, id будет в ссылке - https://drive.google.com/drive/folders/ТУТ_ID)

### Профили Chrome

Профили должны быть в папке `profiles`. По сути это должна папка браузера `User Data`, которая обычно в Windows по пути `C:\Users\User\AppData\Local\Google\Chrome\User Data`(т.е. ее всю нужно копировать). А сама папка с профилем в `C:\Users\User\AppData\Local\Google\Chrome\User Data\Profile 2`

На сервер ubuntu это все копируется долго, поэтому папку `User Data` можно запаковать в .zip и распаковать на сервере командой:
```shell
unzip profiles.zip
```
Если не установлен распаковщик, то сначала:
```shell
apt install unzip
```

### Остальные папки
- `bot` - исполняемый модуль с ботом
- `screens` - скрины браузера, `before.png` перед поиском чата, `enter_chat.png` - после поиска и входа в чат. Сделал для большего контроля, что происходит в скрытом режиме
- `temp` - временные скачиваемые файлы с whatsapp

### Google Api

Для использования Google Sheets & Google Drive нужен файл json с доступом к API.

Назвать его нужно будет `service_account.json`

Как получить - https://telegra.ph/Poluchit-json-token-dlya-Google-Sheets-Api-07-10

Он же будет работать и для Google Drive, главное включить его аналогично с Google Sheets здесь https://console.cloud.google.com/apis/library/drive.googleapis.com и выбрать нужный проект слева вверху

Так же в инструкции создается Service account, если гугл таблица или папка с приватным доступ, то нужно добавлять email этого сервисного аккаунта(https://console.cloud.google.com/apis/credentials выбрать нужный проект) в редакторы, в настройках доступа