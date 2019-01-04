use myusers;

SELECT * FROM users;

SELECT * FROM messages;

SELECT users.first_name, friend.first_name as friend_first_name, messages.content, messages.friend_id
FROM users
LEFT JOIN messages
ON users.user_id = messages.user_id
LEFT JOIN users as friend
ON messages.friend_id = friend.user_id
WHERE messages.friend_id = 7; #7 is the current logged in user session['user_id'];  {{ friend_first_name }}  wrote {{content}}

SELECT users.first_name, friend.first_name as friend_first_name, messages.content, messages.friend_id, users.user_id, messages.msg_id
FROM users
LEFT JOIN messages
ON users.user_id = messages.user_id
LEFT JOIN users as friend
ON messages.friend_id = friend.user_id
WHERE messages.friend_id = 8; 