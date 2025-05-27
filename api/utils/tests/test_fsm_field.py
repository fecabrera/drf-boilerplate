from unittest import mock
from unittest.mock import Mock
from django.test import TestCase
from api.utils.fsm_field import handle_state_transition
from rest_framework import status


class TestHandleStateTransition(TestCase):
    @mock.patch('api.utils.fsm_field.can_proceed', return_value=True)
    def test_handle_state_transition_success(self, mock_can_proceed):
        mock_obj = Mock()
        mock_obj.transition_method = Mock()
        mock_obj.save = Mock()

        response = handle_state_transition(
            obj=mock_obj,
            transition_name='transition_method',
            error_message="Transition failed.",
            success_message="Transition succeeded."
        )

        mock_obj.transition_method.assert_called_once_with()
        mock_obj.save.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': "Transition succeeded."})

    @mock.patch('api.utils.fsm_field.can_proceed', return_value=False)
    def test_handle_state_transition_failure(self, mock_can_proceed):
        mock_obj = Mock()
        mock_obj.transition_method = Mock()

        response = handle_state_transition(
            obj=mock_obj,
            transition_name='transition_method',
            error_message="Transition failed.",
            success_message="Transition succeeded."
        )

        mock_obj.transition_method.assert_not_called()
        mock_obj.save.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': "Transition failed."})

    @mock.patch('api.utils.fsm_field.can_proceed', return_value=True)
    def test_handle_state_transition_with_args_and_kwargs(self, mock_can_proceed):
        mock_obj = Mock()
        mock_obj.transition_method = Mock()
        mock_obj.save = Mock()

        response = handle_state_transition(
            obj=mock_obj,
            transition_name='transition_method',
            error_message="Transition failed.",
            success_message="Transition succeeded.",
            args=[1, 2],
            kwargs={"key": "value"}
        )

        mock_obj.transition_method.assert_called_once_with(1, 2, key="value")
        mock_obj.save.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': "Transition succeeded."})
