from enum import Enum
import random

class Position(Enum):
    GK = 1
    DF = 2
    MF = 3
    FW = 4

class Player:
    def __init__(self, name, position, rating):
        self.name = name
        self.position = position
        self.rating = rating
        self.age = random.randint(16, 35)
        self.value = self.calculate_value()

    def calculate_value(self):
        # Base value from rating
        base_value = self.rating * 1_000_000

        # Position multiplier
        position_multiplier = {
            Position.GK: 0.8,
            Position.DF: 1.0,
            Position.MF: 1.2,
            Position.FW: 1.5
        }[self.position]

        # Age factor (decreases as age increases)
        age_factor = max(0, (35 - self.age) / 19)  # 19 is the range of possible ages (35 - 16)

        # Calculate final value
        value = base_value * position_multiplier * (0.5 + 0.5 * age_factor)

        # Reduce the value by 60%
        value *= 0.4

        # Ensure value is between 0 and 40 million (adjusted from 100 million)
        return min(max(int(value), 0), 40_000_000)

    @classmethod
    def generate_player(cls, position):
        first_names = ["John", "David", "Michael", "James", "William", "Robert", "Richard", "Thomas", "Charles", "Daniel",
                       "Paul", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                      "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        rating = random.randint(60, 90)
        return cls(name, position, rating)

    def __str__(self):
        return f"{self.name} ({self.position.name}, Rating: {self.rating}, Age: {self.age}, Value: £{self.value:,})"

# ... (rest of the file remains unchanged)
