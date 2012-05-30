from django.dispatch import Signal
from mock_django.signals import mock_signal_receiver
from unittest2 import TestCase


class MockSignalTestCase(TestCase):
    def test_mock_receiver(self):
        signal = Signal()
        with mock_signal_receiver(signal) as receiver:
            signal.send(sender=None)
            self.assertEqual(receiver.call_count, 1)

        sentinel = {}
        def side_effect(*args, **kwargs):
            return sentinel

        with mock_signal_receiver(signal, wraps=side_effect) as receiver:
            responses = signal.send(sender=None)
            self.assertEqual(receiver.call_count, 1)

            # Signals respond with a list of tuple pairs [(receiver, response), ...]
            self.assertIs(responses[0][1], sentinel)
