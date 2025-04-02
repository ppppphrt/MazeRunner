
class Player:
    def __init__(self,name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.collected_keys = set()  # Use a set to track which keys have been collected

    def move(self, dx, dy, maze):
        new_x, new_y = self.x + dx, self.y + dy
        if maze.is_valid_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            return True
        return False

    def check_key_collection(self, maze):
        """Check if player is on a key position and collect it if so"""
        for i, key_pos in enumerate(maze.key_positions):
            if (self.x, self.y) == key_pos and i not in self.collected_keys:
                self.collected_keys.add(i)
                return i  # Return the index of the collected key
        return None

    def get_key_count(self, maze):
        """Check if player has collected all keys"""
        return len(self.collected_keys)

    def reached_end(self, end_pos):
        """Check if player has reached the end position"""
        return (self.x, self.y) == end_pos

    def respawn(self):
        """Reset player position to (0,0) without resetting keys."""
        self.x, self.y = 0, 0