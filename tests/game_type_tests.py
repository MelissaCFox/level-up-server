from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import GameType

class GameTypeTests(APITestCase):
    def setUp(self):
        """create a new Gamer and collect the auth Token
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


    def test_create_game_type(self):
        """Ensure we can create (POST) a new game_type
        """

        # Define the URL path for creating a new game_type
        url = "/gametypes"

        # Define the Game_type properties
        game_type = {
            "label": "Board Game"
        }

        # Initiate the POST request and capture the response
        response = self.client.post(url, game_type, format='json')

        # Assert that the response status code is 201 (CREATED)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the values are correct
        self.assertEqual(response.data['label'], game_type['label'])


    def test_get_game_type(self):
        """ Ensure we can GET an existing game_type"""

        # Create a new instance of a game_type
        game_type = GameType()
        game_type.label = "Board Game"

        # Save te game_type to the testing database
        game_type.save()

        # Define the url path for getting a single game_type
        url = f'/gametypes/{game_type.id}'

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['label'], game_type.label)


    def test_change_game_type(self):
        """ Ensure we can change an existing game_type"""

        # Create a new instance of a game_type
        game_type = GameType()
        game_type.label = "Board Game"

        # Save te game_type to the testing database
        game_type.save()

        # Define the url path for updating an existing game_type
        url = f'/gametypes/{game_type.id}'

        # Define NEW game_type properties
        new_game_type = {
            "label": "RPG"
        }

        # Initiate PUT request and capture the response
        response = self.client.put(url, new_game_type, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture that response
        response = self.client.get(url)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['label'], new_game_type['label'])


    def test_delete_game_type(self):
        """ Ensure we can delete an existing game_type
        """

        # Create a new instance of a game_type
        game_type = GameType()
        game_type.label = "Board Game"

        # Sve the game_type to the testing database
        game_type.save()

        # define the URL path for deleting an existing game_type
        url = f'/gametypes/{game_type.id}'

        # Initiate the DELETE request and capture the response
        response = self.client.delete(url)

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Initiate GET request and capture the response
        response = self.client.get(url)

        # Assert that the response status code is 404 (NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
