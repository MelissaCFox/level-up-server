from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from levelupapi.models import Event, Game, GameType

class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new Gamer, collect the auth Token, and create a sample Game
        """

        # Define the URL path for registering a Gamer
        url = '/register'

        # Define the Gamer properties
        gamer = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, gamer, format='json')

        # Store the TOKEN from the response data
        self.token = Token.objects.get(pk=response.data['token'])

        # Use the TOKEN to authenticate the requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED THE DATABASE WITH A GAME AND A GAMETYPE
        # This is necessary because the API does not
        # expose a /games or/gametypes URL paths for creating Games and Game Types

        # Create a new instance of GameType
        game_type=GameType()
        game_type.label = "Board Game"
        
        # Save the GameType to the testing database
        game_type.save()
        
        # Create a new instance of Game
        game = Game()
        game.title = "Sorry"
        game.maker = "Hasbro"
        game.skill_level = 2
        game.number_of_players = 4
        game.game_type_id = 1
        game.description = "Is it too late now to say sorry?"
        game.gamer_id = self.token.user_id

        # Save the Game to the testing database
        game.save()

    def test_create_event(self):
        """
        Ensure we can create (POST) a new Event.
        """

        # Define the URL path for creating a new Event
        url = "/events"

        # Define the Event properties
        event = {
            "gameId": 1,
            "description": "Let's play sorry!",
            "date": "2022-02-22",
            "time": "12:00:00",
        }

        # Initiate POST request and capture the response
        response = self.client.post(url, event, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        self.assertEqual(response.data["game"]["id"], event['gameId'])
        self.assertEqual(response.data["description"], event['description'])
        self.assertEqual(response.data["date"], event['date'])
        self.assertEqual(response.data["time"], event['time'])
        self.assertEqual(response.data["organizer"]['id'], self.token.user_id)


    def test_get_event(self):
        """
        Ensure we can GET an existing event.
        """

        # Create a new instance of Event
        event = Event()
        event.game_id = 1
        event.description = "Let's play sorry!"
        event.date = "2022-02-22"
        event.time = "12:00:00"
        event.organizer_id = 1

        # Save the Event to the testing database
        event.save()

        # Define the URL path for getting a single Event
        url = f'/events/{event.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["game"]["id"], event.game_id)
        self.assertEqual(response.data["description"], event.description)
        self.assertEqual(response.data["date"], event.date)
        self.assertEqual(response.data["time"], event.time)
        self.assertEqual(response.data["organizer"]['id'], event.organizer_id)


    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """

        # Create a new instance of Event
        event = Event()
        event.game_id = 1
        event.description = "Let's play sorry!"
        event.date = "2022-02-22"
        event.time = "12:00:00"
        event.organizer_id = 1

        # Save the Event to the testing database
        event.save()

        # Define the URL path for updating an existing Event
        url = f'/events/{event.id}'

        # Define NEW Event properties
        new_event = {
            "gameId": 1,
            "description": "Let's play sorry! I'm gonna totally crush you and THEN you'll be sorry",
            "date": "2022-02-22",
            "time": "13:30:00",
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_event, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["game"]["id"], new_event['gameId'])
        self.assertEqual(response.data["description"], new_event['description'])
        self.assertEqual(response.data["date"], new_event['date'])
        self.assertEqual(response.data["time"], new_event['time'])



    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """

        # Create a new instance of Event
        event = Event()
        event.game_id = 1
        event.description = "Let's play sorry!"
        event.date = "2022-02-22"
        event.time = "12:00:00"
        event.organizer_id = 1

        # Save the Event to the testing database
        event.save()

        # Define the URL path for deleting an existing Event
        url = f'/events/{event.id}'

        # Initiate DELETE request and capture the response
        response = self.client.delete(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


