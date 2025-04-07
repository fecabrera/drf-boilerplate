from django_fsm import can_proceed
from rest_framework import status
from rest_framework.response import Response


class StateTransitionMixin:
    def _handle_state_transition(self, request, transition_name, error_message, success_message):
        obj = self.get_object()
        transition_method = getattr(obj, transition_name)

        if not can_proceed(transition_method):
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        transition_method(request.user)
        obj.save()

        return Response({'message': success_message}, status=status.HTTP_200_OK)
