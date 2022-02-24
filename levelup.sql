CREATE VIEW GAMES_BY_USER AS
SELECT
    g.*,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN
    levelupapi_gamer gr ON g.gamer_id = gr.id
JOIN
    auth_user u ON gr.user_id = u.id
;

CREATE VIEW EVENTS_BY_USER AS
SELECT event.id, game.title as game_name, event.description, event.date, event.time, organizer.id as gamer_id, organizer.first_name || " " || organizer.last_name as full_name 
FROM levelupapi_event as event
JOIN levelupapi_game as game on game.id = event.game_id
JOIN levelupapi_gamer as gamer on gamer.id = event.organizer_id
JOIN auth_user as organizer on organizer.id = gamer.user_id
;