#!/usr/bin/env python3
"""
    WarBot Main Object Source
    =========================


"""

import json
import pprint
import numpy as np
import matplotlib.pyplot as pltlib



class WarBot:
    """WarBot Object

    This is the main object in the game: it loads start properties of the world
    of interest, computes rounds and saves the history. The bare minimum code to
    let it run is the following

    wb = WarBot(<path_to_json_file>)
    wb.run()

    where <path_to_json_file> is a string indicating the path to a JSON file
    with the structure

    {
        "source": str,
        "states": {
            "state1": {
                "pop": int,
                "area": int or float,
                "id": int (unique),
                "neighbors": [str]
            },
            ...
        }
    }

    see for example <prj_root>/Switzerland/states.json.

    """

    def __init__(self, data_file: str) -> "WarBot Object":
        self._players = self.load_players(data_file)
        self._players_names = [pn.replace("_", " ").capitalize() for pn in self._players.keys()]
        self._history = [{"players": self._players_names.copy(),
                          "n_of_players": len(self._players_names)},]
        self._n_of_rounds = 0
        self._max_rounds = len(self._players.keys())

        self._pop_weight = 0.5
        self._area_weight = 0.1
        self._losers = []


    def load_players(self, data_file: str) -> dict:
        """Load the players from the datafile.

        Returns the initial states with their properties in a dictionary. It
        loads the JSON file and only returns the "states" entry thereof.
        """

        return json.load(open(data_file, "r"))["states"]


    def compute_round(self):
        """Compute/simulate a single round of the game.

        This involves getting a list of pairs of battling states (have to be
        neighboring states) and computing the outcomes of the battles.
        """

        battle_pairs = self.get_pairs()
        self.compute_battles(battle_pairs)
        self._players_names = list(self._players.keys())
        self._n_of_rounds += 1


    def get_pairs(self) -> list:
        """Get battling pairs.

        From the current state of the world, pick neighboring states which will
        have a fight in this round. This method returns a list of lists of
        neighboring states (randomly selected).

        NOTE: so far only one pair is selected at each round. Also, it was
        thought that a state can only have one adversary at the time. This
        mechanic might as well be dropped/changed for more 'interesting' plots
        of the world history.
        """

        pairs = []
        available_players = list(self._players.keys())
        busy_players = []

        for ii in [1,]: # range(20): # TODO parallel version still bugged (not reaching an end because of wrong neighborhood handling)
            if len(available_players) > 0:
                idx = np.random.randint(0, len(available_players))

            else:
                break

            p1 = available_players[idx]
            if p1 in busy_players:
                continue

            else:
                available_players.remove(p1)
                busy_players.append(p1)

            available_neighbors = self._players[p1]["neighbors"]

            for bp in busy_players:
                try:
                    available_neighbors.remove(bp)

                except:
                    pass

            if len(available_neighbors) > 0:
                p2 = available_neighbors[np.random.randint(0, len(available_neighbors))]
                busy_players.append(p2)
                pairs.append([p1, p2])

            else:
                busy_players.remove(p1)

        return pairs


    def compute_battles(self, battle_pairs: list):
        """Compute the outcome of all battles specified by the battle_pairs.

        One way of getting battle pairs is to call the get_pairs() method.
        """

        winners = []
        losers = []
        for pp in battle_pairs:
            strengths = [self._players[p]["area"] * self._area_weight + self._players[p]["pop"] * self._pop_weight for p in pp]
            tot_s = np.sum(strengths)

            for ii in range(len(strengths)):
                strengths[ii] /= tot_s

            result = np.random.rand(1)

            if result > strengths[0]:
                winner = pp[0]
                loser = pp[1]

            else:
                winner = pp[1]
                loser = pp[0]

            losers.append(loser)
            winners.append(winner)

            print("BATLLE INFO :: Battle between {:s} and {:s} was won by {:s}".format(pp[0], pp[1], winner))

        for w, l in zip(winners, losers):
            self.merge_players(w, l)

        self.clean_neighborhoods(losers, winners)
        self._losers += losers


    def clean_neighborhoods(self, losers: list, winners: list):
        """Update the world after the battles are over in terms of neighborhoods."""
        for p in self._players.keys():
            for l, w in zip(losers, winners):
                while l in self._players[p]["neighbors"]:
                    self._players[p]["neighbors"].remove(l)
                    if p != w and not w in self._players[p]["neighbors"]:
                        self._players[p]["neighbors"].append(w)

        for p in self._players.keys():
            self._players[p]["neighbors"] = list(set(self._players[p]["neighbors"]))


    def merge_players(self, winner: list, loser: list):
        """Merge losers into winners for each battle."""
        for k in self._players[winner].keys():
            if k != "id":
                self._players[winner][k] += self._players[loser][k]

        self._players[winner]["neighbors"] = list(set(self._players[winner]["neighbors"]))
        while winner in self._players[winner]["neighbors"]:
            self._players[winner]["neighbors"].remove(winner) # Avoid having oneself as a neighbor

        while loser in self._players[winner]["neighbors"]:
            self._players[winner]["neighbors"].remove(loser) # no longer in the game

        del self._players[loser]


    def run(self):
        """Run a game.

        This is the one method to call them all. It simulates the full game
        until there is either only one state left or the max number of
        iterations has been reached.
        """
        counter = 0
        while self._n_of_rounds < self._max_rounds and len(self._players.keys()) > 1:
            counter += 1
            print("HISTORY INFO :: Number of remaining states {:d}".format(len(list(self._players.keys()))))
            print("HISTORY INFO :: Round {:d} being computed...".format(counter))
            self.compute_round()
            self._history.append(
                {
                    "players": self._players_names.copy(),
                    "n_of_players": len(self._players_names)
                }
            )
            self.print_players()


    def print_players(self):
        """Auxilizry method for (pretty) printing the remaining states."""
        print("Surviving regions are:")
        for p in self._players.keys():
            print("\t{:s}: Population {:d}, Area {:d} km2, Neighbors: {}".format(
                p.capitalize(),
                self._players[p]["pop"],
                self._players[p]["area"],
                self._players[p]["neighbors"]
                )
            )



if __name__ == "__main__":
    print("\033c")
    print(__doc__)
    print()

    data = "../Switzerland/states.json"
    wb = WarBot(data)
    wb.run()
