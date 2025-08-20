# Проект Django авторизации

Проект на **Django** с коробочной авторизацией через JWT и кастомной системой ролей.  
Написано с помощью ChatGPT с последующей доработкой. Убирать ИИ-комментарии и писать свои не стал из экономии времени.

---

## 📌 Возможности
- ✅ Регистрация и аутентификация пользователей по email + паролю (JWT).   
- ✅ Роли пользователей.
- ✅ Права (permissions) на ресурсы.  
- ✅ Таблица правил доступа, которая связывает роли, права и ресурсы.  
- ✅ Админский доступ для управления ролями и правами.  
- ✅ Замоканные ресурсы.

---

## О ролях подробнее

Стандартная система:  
Все возможные роли пользователей лежат в таблице `Role`.  
Все пермишины (виды действий) лежат в таблице `Permission`.  
Связи ролей и пермишинов лежат в таблице `AccessRule`.  

**Формат связи:**  
`id роли <-> id пермишина <-> текстовое название ресурса`

- Дефолтные роли: `admin (id=1)` и `user (id=2)`  
- Дефолтные пермишины: создание (id=1), чтение (id=2), редактирование (id=3), удаление (id=4) (CRUD).  
- Дефолтные ресурсы: `documents` и `projects` (они же и замоканы в качестве бизнес-логики).  
- Дефолтные права ролей: админ может делать всё с любыми ресурсами, юзер может читать все ресурсы.  

**Пример:** первая запись в таблице `AccessRule` — это разрешение админу читать из `documents`:  
`id роли(1) <-> id пермишина(1) <-> "documents"`

---

## О замоканных ресурсах

Замоканы два типа ресурсов: `documents` и `projects`.  
Для каждого из них применимы CRUD-операции в соответствии с правами доступа пользователя.  
Возвращает текстовый ответ в случае успешного запроса к ресурсу.

---

## 🛠️ Установка и запуск
```bash
git clone https://github.com/clawermachine/em_auth.git
cd em_auth

docker-compose build
docker-compose up -d db
docker-compose up -d web

docker-compose down -v
```

---

После запуска автоматически создаётся админ:
```
Email: admin@admin.com
Пароль: 123456
```

---

## 📖 Инструкция по пользованию эндпоинтами

### 1. Авторизация

#### 1.1 Авторизация (получение JWT токенов)
**[POST]** `http://localhost:8080/users/token/`  

**Body JSON:**
```json
{
  "email": "admin@admin.com",
  "password": "123456"
}
```

**Response JSON:**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

#### 1.2 Обновление access-токена (refresh)
**[POST]** `http://localhost:8080/users/token/refresh/`  

**Body JSON:**
```json
{
  "refresh": "<refresh_token>"
}
```

**Response JSON:**
```json
{
  "access": "<new_access_token>"
}
```

---

### 2. Админские действия

#### 2.1 Чтение списка ролей
**[GET]** `http://localhost:8080/users/admin/roles/`  
**Headers:** `Authorization: Bearer <access_token>`

**Response JSON:**
```json
[
  {
    "id": 1,
    "name": "admin"
  },
  {
    "id": 2,
    "name": "user"
  }
]
```

#### 2.2 Чтение списка пермишинов
**[GET]** `http://localhost:8080/users/admin/permissions/`  
**Headers:** `Authorization: Bearer <access_token>`

**Response JSON:**
```json
[
  {
    "id": 1,
    "name": "create"
  },
  {
    "id": 2,
    "name": "read"
  },
  {
    "id": 3,
    "name": "edit"
  },
  {
    "id": 4,
    "name": "delete"
  }
]
```

#### 2.3 Чтение списка правил доступа
**[GET]** `http://localhost:8080/users/admin/accessrules/`  
**Headers:** `Authorization: Bearer <access_token>`

**Response JSON:**
```json
[
  {
    "id": 1,
    "resource": "documents",
    "role_id": 1,
    "permission_id": 1
  },
  {
    "id": 2,
    "resource": "documents",
    "role_id": 1,
    "permission_id": 2
  },
  ...
]
```

#### 2.4 Создание правила доступа
**[POST]** `http://localhost:8080/users/admin/roles/<int:role_id>/permissions/`  
**Headers:** `Authorization: Bearer <access_token>`

**Body JSON:**
```json
{
  "permission_id": 1,
  "resource": "documents"
}
```

#### 2.5 Удаление правила доступа
**[DELETE]** `http://localhost:8080/users/admin/roles/<int:role_id>/permissions/`  
**Headers:** `Authorization: Bearer <access_token>`

**Body JSON:**
```json
{
  "permission_id": 1,
  "resource": "documents"
}
```

---

### 3. Пользовательские действия

#### 3.1 Регистрация
**[POST]** `http://localhost:8080/users/register/`  

**Body JSON:**
```json
{
  "first_name": "name",
  "last_name": "surname",
  "middle_name": "midname",
  "email": "user@user.com",
  "password": "123456",
  "password_2": "123456"
}
```

**Response JSON:**
```json
{
  "id": 2,
  "first_name": "name",
  "last_name": "surname",
  "middle_name": "midname",
  "email": "user@user.com"
}
```

#### 3.2 Чтение данных профиля
**[GET]** `http://localhost:8080/users/profile/`  
**Headers:** `Authorization: Bearer <access_token>`

**Response JSON:**
```json
{
  "id": 1,
  "last_login": null,
  "email": "admin@admin.com",
  "first_name": "Admin",
  "last_name": null,
  "middle_name": null,
  "is_active": true,
  "role": 1
}
```

#### 3.3 Обновление данных профиля
**[PUT]** `http://localhost:8080/users/profile/`  
**Headers:** `Authorization: Bearer <access_token>`

**Body JSON:**
```json
{
  "email": "admin2@example.com",
  "first_name": "Admin_name",
  "last_name": "Admin_surname",
  "middle_name": "Admin_midname"
}
```

**Response JSON:**
```json
{
  "id": 1,
  "last_login": null,
  "email": "admin2@example.com",
  "first_name": "Admin_name",
  "last_name": "Admin_surname",
  "middle_name": "Admin_midname",
  "is_active": true,
  "role": 1
}
```

#### 3.4 Мягкое удаление профиля
**[DELETE]** `http://localhost:8080/users/profile/`  
**Headers:** `Authorization: Bearer <access_token>`


---

### 4. Замоканная бизнес-логика

**[GET/POST/PUT/DELETE]** `http://localhost:8080/resources/documents/`  
**[GET/POST/PUT/DELETE]** `http://localhost:8080/resources/projects/`  
**Headers:** `Authorization: Bearer <access_token>`


**Response JSON:**
```json
{
    "resource": "documents"/"projects",
    "action": "create"/"read"/"edit"/"delete",
    "data": [
        "documents1_read"/"projects1_read"/...,
        "documents2_read"/"projects2_read"/...
    ]
}
```

---
