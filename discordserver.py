from collections import deque
import discord

class discordserver:
    def __init__(self, client):
        self.queue = deque()
        self.current_player = None
        self.client = client

    def play(self, player):
        if self.current_player is None:
            self.current_player = player
            player.start()
        else:
            self.queue.append(player)

    def queue_complete(self):
        if not self.queue:
            print("Queue is empty")
            self.current_player = None
            return True
        else:
            print("Queue has songs")
            player = self.queue.popleft()
            self.current_player = player
            player.start()
        return False

    def skip_song(self):
        print(self.current_player)
        self.current_player.stop()
        print(self.current_player)
