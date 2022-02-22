"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = GameType.objects.all()
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game type instance
        """
        # Create a new Python instance of the GameType class
        # and set its properties from what was sent in the
        # body of the request from the client.
        game_type = GameType.objects.create(
            label = request.data["label"],
        )

        # Try to save the new game_type to the database, then
        # serialize the game_type instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game_type.save()
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, pk=None):
        """Handle PUT requests for a game type

        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game type, get the game type record
        # from the database whose primary key is `pk`
        try:
            game_type = GameType.objects.get(pk=pk)
            game_type.label = request.data["label"]
       
            game_type.save()
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            # 204 status code means everything worked but the
            # server is not sending back any data in the response
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game_type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = GameType.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = GameType
        fields = ('id', 'label')
