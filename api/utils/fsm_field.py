from django_fsm import can_proceed
from rest_framework import status
from rest_framework.response import Response


def handle_state_transition(obj, transition_name: str, error_message: str, success_message: str, args: list = None,
                            kwargs: dict = None):
    """
    Handles state transitions for an object by invoking a specific transition method.

    This function executes a state transition on the provided object by calling the transition
    method specified by the transition_name parameter. If the transition cannot proceed, it
    returns an error response. If successful, it saves the object and returns a success response.

    Parameters:
        obj: The target object on which the state transition will be performed.
        transition_name (str): The name of the transition method to invoke.
        error_message (str): The error message to return if the transition cannot proceed.
        success_message (str): The success message to return if the transition is successful.
        args (list, optional): Positional arguments to pass to the transition method. Defaults to None.
        kwargs (dict, optional): Keyword arguments to pass to the transition method. Defaults to None.

    Returns:
        Response: An HTTP response with either a success or error message, along with the corresponding
        HTTP status code.
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    transition_method = getattr(obj, transition_name)

    if not can_proceed(transition_method):
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

    transition_method(*args, **kwargs)
    obj.save()

    return Response({'message': success_message}, status=status.HTTP_200_OK)