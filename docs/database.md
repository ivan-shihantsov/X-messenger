
визуализация схемы по ссылке `https://dbdiagram.io/d`

```
Table messages {
  msg_id integer [primary key]
  chat_id integer
  text varchar
  datetime timestamp
  from_user integer
}

Table users {
  user_id integer [primary key]
  username varchar
  chats varchar
  created_at timestamp
}

Table chats {
  chat_id integer [primary key]
  chat_name varchar
  color varchar
  created_at timestamp
  users varchar
  admin integer
}

Table userKeys {
  key_id integer [primary key]
  user_id integer
  passHash varchar
  created_at timestamp
}

Table usersInChats {
  link_id integer [primary key]
  user_id integer
  chat_id integer
}

Ref user_keys: userKeys.user_id > users.user_id
Ref chat_admins: chats.admin > users.user_id
Ref UIC_users: usersInChats.user_id > users.user_id
Ref UIC_chats: usersInChats.chat_id > chats.chat_id
Ref user_messages: messages.from_user > users.user_id
Ref msgs_in_chats: messages.chat_id > chats.chat_id
```
