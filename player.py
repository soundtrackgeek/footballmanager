from enum import Enum
import random
import csv

class Position(Enum):
    GK = 1
    DF = 2
    MF = 3
    FW = 4

class Player:
    # Load names from CSV file
    with open('playernames.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        names = list(reader)

    def __init__(self, name, position, rating):
        self.name = name
        self.position = position
        self.rating = rating
        self.age = random.randint(16, 35)
        self.value = self.calculate_value()
        self.injured = False
        self.injury_weeks_left = 0

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
        # Choose a random first name and last name from the loaded names
        first_name, last_name = random.choice(cls.names)
        name = f"{first_name} {last_name}"
        rating = random.randint(60, 90)
        return cls(name, Position[position], rating)

    def __str__(self):
        return f"{self.name} ({self.position.name}, Rating: {self.rating}, Age: {self.age}, Value: £{self.value:,})"

# ... (rest of the file remains unchanged)
