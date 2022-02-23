SELECT * FROM levelupapi_gametype;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;

SELECT *, user.first_name || " " || user.last_name as full_name FROM levelupapi_game as game
JOIN levelupapi_gamer as gamer on gamer.id = game.gamer_id
JOIN auth_user as user on user.id = gamer.user_id


SELECT event.id, game.title as game_name, event.description, event.date, event.time, organizer.id as gamer_id, organizer.first_name || " " || organizer.last_name as full_name from levelupapi_event as event
JOIN levelupapi_game as game on game.id = event.game_id
JOIN levelupapi_gamer as gamer on gamer.id = event.organizer_id
JOIN auth_user as organizer on organizer.id = gamer.user_id