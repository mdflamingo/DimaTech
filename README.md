### Запуск через docker-compose

 - создать `.env` файл в корне проекта по примеру `.env.example`
 - запустить командой `docker compose up -d` из корня
 - после успешного выполнения команды в системе должны быть запущены 2 контейнера (postgres, app)
 - к базе применится init.sql файл для создания пользователя, админа и счета

### Запуск в режиме разработки
- запустить postgres в контейнере командой
```docker run -d \
  --name my-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \       
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -v $(pwd)/migrations:/docker-entrypoint-initdb.d \
  -v pg_data:/var/lib/postgresql/data \
  postgres:16-alpine
```
- запустить приложения через терминал
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


### User
```{
  "email": "user@example.com",
  "password": "qwe123",
  "full_name": "Test User"
}
```

### Admin
```{
  "email": "user@example.com",
  "password": "qwe123",
  "full_name": "Test User"
}
```

### Тело запроса для тестирования /api/v1/payment
```{
  "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
  "user_id": 1,
  "account_id": 1,
  "amount": 100,
  "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
}
```
