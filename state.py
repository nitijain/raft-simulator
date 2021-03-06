import time
import random
from message import Message

class State(object):
    def set_server(self, server):
        self._server = server

    def on_message(self, message):
        _type = message.type

        if message.term > self._server._currentTerm:
            self._server._currentTerm = message.term
        elif(message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if _type == Message.AppendEntries:
            return self.on_append_entries(message)
        elif _type == Message.RequestVote:
            a = self.on_vote_request(message)
            return a
        elif _type == Message.RequestVoteResponse:
            return self.on_vote_received(message)
        elif _type == Message.Response:
            return self.on_response_received(message)
        elif _type == Message.ClientCommand:
            return self.run_client_command(message)

    def on_leader_timeout(self, message):
        """This is called when the leader timeout is reached."""

    def on_vote_request(self, message):
        """This is called when there is a vote request."""

    def on_vote_received(self, message):
        """This is called when this node recieves a vote."""

    def on_append_entries(self, message):
        """This is called when there is a request to
        append an entry to the log.

        """
    def on_response_received(self, message):
        """This is called when a response is sent back to the Leader"""

    def _nextTimeout(self):
        self._currentTime = time.time()
        return self._currentTime + self._timeout

    def _send_response_message(self, msg, yes=True):
        response = Message(self._server._name, msg.sender, msg.term, {
            "response": yes,
            "currentTerm": self._server._currentTerm,
        }, Message.Response)
        self._server.send_message_response(response)
