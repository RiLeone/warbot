#!/usr/bin/env python3
"""
    State Object Source
    ===================


"""

import json
import numpy as np



class State:
    """State Object

    A state is a player in this game/simulation.
    """

    def __init__(self, properties: dict):
        self._id = properties["id"]
        self._name = properties["name"]
        self._pretty_name = properties["name"].replace("_", " ").title()
        self._area = properties["area"]
        self._pop = properties["pop"]
        self._growth_rate = properties["growth_rate"]


    def grow(self) -> int:
        """Apply growth to state.

        delta_pop is returned as it is needed for statistics computation
        """

        delta_pop = self.compute_population_growth_delta()
        self._pop += delta_pop

        return delta_pop


    def compute_population_growth_delta(self) -> int:
        """Compute population growth based on state's growth-rate

        This function computes a population difference, the return value needs
        to be added to the previous population to get the updated value.
        """

        return int(round(self._pop * self._growth_rate, 0))


    def update_population_after_battle(self, pop_loss: int):
        NotImplemented


    def compute_battle_strength(self, method: str):
        NotImplemented


    def merge_with(self, other_state):
        NotImplemented


    def clean_neighborhood(self, valid_neighbors: list):
        NotImplemented


    def get_population(self) -> int:
        NotImplemented


    def get_neighbors(self) -> list:
        NotImplemented



def load_states_from_json_file(json_file):
    NotImplemented



if __name__ == "__main__":
    print(__doc__)
    print()

    state_props = {
        "pop": 10000,
        "area": 2000,
        "id": 1,
        "neighbors": ["B", "C"],
        "growth_rate": 0.01,
    }
    state_props["name"] = "A"

    state = State(state_props)

    print(state.__dict__)
