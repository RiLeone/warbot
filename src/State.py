#!/usr/bin/env python3
"""
    State Object Source
    ===================


"""

import copy
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
        self._neighbors = properties["neighbors"]

        self._history = {
            "pop": [self._pop, ],
        }


    def update_history(self):
        """Update history."""

        self._history["pop"].append(self._pop)


    def grow(self) -> int:
        """Apply growth to state.

        delta_pop is returned as it is needed for statistics computation
        """

        delta_pop = self.compute_population_growth_delta()
        self._pop += delta_pop
        self._pop = max([1, self._pop])
        self.update_history()

        return delta_pop


    def compute_population_growth_delta(self) -> int:
        """Compute population growth based on state's growth-rate

        This function computes a population difference, the return value needs
        to be added to the previous population to get the updated value.
        """

        return int(round(self._pop * self._growth_rate, 0))


    def update_population_after_battle(self, pop_loss: int):
        """Update population after battle"""

        self._pop -= pop_loss
        self._pop = max([1, self._pop])
        self.update_history()


    def compute_battle_strength(self, method: str) -> float:
        """Given a battle pair compute the relative strenghts of the contestants
        and return them in a list of floats.

        <method> is a string in ("poparea", ). If an invalid <method> is
        provided, "poparea" is used. Default method is "poparea".
        """

        VALID_METHODS = ("poparea", )

        if method not in VALID_METHODS:
            method = VALID_METHODS[0]

        if method == VALID_METHODS[0]:
            AREA_WEIGHT = 1.
            POP_WEIGHT = 0.5
            strength = self._area * AREA_WEIGHT + self._pop * POP_WEIGHT

        return strength


    def merge_with(self, other_state):
        """Merge <other_state> into self"""

        attributes_to_be_summed = ("_pop", "_area", "_neighbors")
        for atbs in attributes_to_be_summed:
            setattr(self, atbs, getattr(self, atbs) + getattr(other_state, atbs))

        self._neighbors = list(set(self._neighbors))

        invalid_neighbors = (self.get_name(), other_state.get_name())
        self.clean_neighborhood(invalid_neighbors)


    def clean_neighborhood(self, invalid_neighbors: list):
        """Remove invalid entries from neighbors"""

        for inv_neigh in invalid_neighbors:
            while inv_neigh in self._neighbors:
                self._neighbors.remove(inv_neigh)


    def get_name(self) -> str:
        """Get state name"""

        return self._name


    def get_population(self) -> int:
        """Get state population"""

        return self._pop


    def get_area(self) -> float:
        """Get state area"""

        return self._area


    def get_history(self) -> dict:
        """Get history of state"""

        return copy.deepcopy(self._history)


    def get_neighbors(self) -> list:
        """Get state neighbors"""

        return self._neighbors.copy()


    def add_neighbor(self, new_neighbor: str):
        """Add a neighbor"""

        self._neighbors.append(new_neighbor)
        self._neighbors = list(set(self._neighbors)) # enforce absence of duplicates


    def __str__(self):
        """Representation of self when calling print()"""

        return "State Object :: name: {}".format(self._name)



def load_states_from_json_file(json_file):
    """Load states from a states.json file"""

    states = {}

    with open(json_file, "r") as fp:
        state_dicts = copy.deepcopy(json.load(fp))["states"]

    for state_name, state_props in state_dicts.items():
        state_props["name"] = state_name
        states[state_name] = State(state_props)

    return states




if __name__ == "__main__":
    print(__doc__)
    print()

    filename = "test/worlds/Testland/states.json"
    states = load_states_from_json_file(filename)

    for state_name, state in states.items():
        print("* Name: {}; Pop: {}; Neighbors: {}.".format(
            state_name,
            state.get_population(),
            state.get_neighbors()
            )
        )
