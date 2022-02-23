"""Module for generating events by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all events along with the eventr first name, last name, and id
            db_cursor.execute("""
            SELECT event.id, game.title as game_name, event.description, event.date, event.time, organizer.id as gamer_id, organizer.first_name || " " || organizer.last_name as full_name from levelupapi_event as event
            JOIN levelupapi_game as game on game.id = event.game_id
            JOIN levelupapi_gamer as gamer on gamer.id = event.organizer_id
            JOIN auth_user as organizer on organizer.id = gamer.user_id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each eventr.
            # This will be the structure of the events_by_user list:
            #
            # [
            # {
            #     "gamer_id": 1,
            #     "full_name": "Molly Ringwald",
            #     "events": [
            #       {
            #         "id": 5,
            #         "game_name": "Fortress America",
            #         "description": "fun game night with friends",
            #         "date": "2020-12-23",
            #         "time": "19:00"
            #       }
            #     ]
            # }
            # ]

            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called event that includes 
                # the game_name, description, date,
                # and time from the row dictionary
                event = {
                    "id": row['id'],
                    "game_name": row['game_name'],
                    "description": row['description'],
                    "date": row['date'],
                    "time": row['time'],
                }
                
                # This is using a generator comprehension to find the user_dict in the events_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_event in events_by_user:
                #     if user_event['gamer_id'] == row['gamer_id']:
                #         user_dict = user_event
                
                user_dict = next(
                    (
                        user_event for user_event in events_by_user
                        if user_event['gamer_id'] == row['gamer_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the events_by_user list, append the event to the events list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the events_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
