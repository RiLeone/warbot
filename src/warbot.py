#!/usr/bin/env python3
"""
    WarBot Source
"""

import json
import pprint
import numpy as np
import matplotlib.pyplot as pltlib

class WarBot:
    def __init__(self, data_file):
        self._players = self.load_players(data_file)
        self._players_names = [pn.replace("_", " ").capitalize() for pn in self._players.keys()]
        self._history = [{"players": self._players_names.copy(),
                          "n_of_players": len(self._players_names)},]
        self._n_of_rounds = 0
        self._max_rounds = 10

        self._pop_weight = 0.5
        self._area_weight = 0.1
        self._losers = []

    def load_players(self, data_file):
        return json.load(open(data_file, "r"))["states"]

    def compute_round(self):
        battle_pairs = self.get_pairs()
        self.compute_battles(battle_pairs)
        self._n_of_rounds += 1

    def get_pairs(self):
        pairs = []
        available_players = list(self._players.keys())
        busy_players = []

        for ii in range(20):
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

    def compute_battles(self, battle_pairs):
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

        self._losers += losers
        self.clean_neighborhoods(losers, winners)

    def clean_neighborhoods(self, losers, winners):
        # TODO: We have to remove conquered territories from list of available neighbors,
        # but also add conquering territory as new neighbor! This somehow not working yet
        for p in self._players.keys():
            for l, w in zip(losers, winners):
                try:
                    self._players[p]["neighbors"].remove(l)
                    if p != w:
                        self._players[p]["neighbors"].append(w)
                except:
                    pass

    def merge_players(self, winner, loser):
        for k in self._players[winner].keys():
            if k != "id":
                self._players[winner][k] += self._players[loser][k]

        self._players[winner]["neighbors"] = list(set(self._players[winner]["neighbors"]))

        del self._players[loser]

    def run(self):
        counter = 0
        while self._n_of_rounds < self._max_rounds and len(self._players_names) > 1:
            counter += 1
            print("HISTORY INFO :: Number of remaining states {:d}".format(len(list(self._players.keys()))))
            print("HISTORY INFO :: Round {:d} being computed...".format(counter))
            self.compute_round()
            self._history.append({"players": self._players_names.copy(),
                                  "n_of_players": len(self._players_names)})

    def print_players(self):
        print("Surviving regions are:")
        for p in self._players.keys():
            print("\t{:s}: Population {:d}, Area {:d} km2, Neighbors: {}".format(p.capitalize(), self._players[p]["pop"], self._players[p]["area"], self._players[p]["neighbors"]))







if __name__ == "__main__":
    print("\033c")
    print(__doc__)
    print()

    data = "../Switzerland/states.json"
    wb = WarBot(data)
    # pprint.pprint(wb._players)
    # pprint.pprint(wb._players_names)
    pprint.pprint(wb.get_pairs())
    wb.run()
    wb.print_players()
