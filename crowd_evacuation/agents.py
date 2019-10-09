from enum import Enum

from mesa import Agent
import random
import numpy as np


class Reasons(Enum):
    SAVED = 1
    KILLED_BY_FIRE = 2


class StewardAgent(Agent):
    def __init__(self, unique_id, model, known_exits):
        super().__init__(unique_id, model)

        self._known_exits = known_exits


class WallAgent(Agent):
    """ A wall agent."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class ExitAgent(Agent):
    """ An emergency exit agent."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class FireAgent(Agent):
    """ Fire Agent """

    def __init__(self, pos, model):
        """
        Create a new fire agent

        Args:
            pos: The tree's coordinates on the grid. Also it is the unique_id
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "On Fire"
        self.burned_delay = 5  # How many iter. steps will a fire agent wait until infecting neighboring squares
        self.delay_counter = 0

    def step(self):
        """
        Fire agents "On Fire" will spread after a certain delay with a certain probability.
        This probability makes it seem more realistic (less square-like).
        """
        if (self.condition == "On Fire") and (self.delay_counter >= self.burned_delay):
            # Once we've reached the minimum delay, fire will spread eventually, depending on some probability
            p_spread = np.random.choice(4)  # Spread prob. 1/4
            if p_spread < 1:
                self.model.spread_fire(self)
                self.condition = "Burned Out"
                self.model.schedule.remove(self)  # Once it's burned, we don't need it in the scheduler
        elif self.condition == "On Fire":
            self.delay_counter += 1

    def get_pos(self):
        return self.pos
