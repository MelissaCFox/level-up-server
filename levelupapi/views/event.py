from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """

        # Uses the token passed in the `Authorization` header
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])


        # Create a new Python instance of the Event class
        # and set its properties from what was sent in the
        # body of the request from the client.
        event = Event.objects.create(
            game = game,
            description = request.data["description"],
            date = request.data["date"],
            time = request.data["time"],
            organizer = gamer
        )

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            event.save()
            serializer = EventSerializer(event)
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for a event

        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Event, get the event record
        # from the database whose primary key is `pk`
        try:
            event = Event.objects.get(pk=pk)
            event.description = request.data["description"]
            event.date = request.data["date"]
            event.time = request.data["time"]

            game = Game.objects.get(pk=request.data["gameId"])
            event.game = game
            event.save()

            # 204 status code means everything worked but the
            # server is not sending back any data in the response
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response ({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for event types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer', 'attendees')
        depth = 2
