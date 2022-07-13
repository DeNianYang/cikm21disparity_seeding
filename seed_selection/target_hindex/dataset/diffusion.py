import pandas as pd
import networkx as nx
import numpy as np

# load the graph
g = nx.read_gpickle("../../../../facebook-graph.pkl")
# get user gender dictionary
genders = nx.get_node_attributes(g, "gender")

# define the independent cascade diffusion
def IC_graph_gendered(G, S, mc, genders):
    """
    Performs Independent Cascade diffusion.
    Adapted from https://hautahi.com/im_greedycelf and https://hautahi.com/im_ris, read the blog posts for a more detailed explanation.

    Args:
        G: A networkX graph (directed, weighted).
        S: List of seed nodes used to start the diffusion (set as active before diffusion begins).
        mc: Number of Monte Carlo simulations - the higher the number, the more accurate the spread value, but the slower the execution.
        genders: the gender dictionary mapping each node_id to a gender ("f" or "m").

    Return: Four spread values corresponding to the average number of I: all influenced nodes, II: male influenced nodes,
    III: female influenced nodes when starting the diffusion from given seed.
    """
    spread, spread_m, spread_f = [], [], []
    probabilities = nx.get_edge_attributes(G, "prob")
    for i in range(mc):

        # Simulate propagation process
        new_active, A = S[:], S[:]

        while new_active:

            # 1. Find out-neighbors for each newly active node
            targets = []
            probas = []

            for node in new_active:
                neighbors = list(G[node].keys())
                targets += neighbors
                probas += [probabilities[(node, target)] for target in neighbors]

            # 2. Determine newly activated neighbors (set seed and sort for consistency)
            np.random.seed(i)
            success = np.random.uniform(0, 1, len(targets)) < np.array(probas)
            new_ones = list(np.extract(success, sorted(targets)))

            # 3. Find newly activated nodes and add to the set of activated nodes
            new_active = list(set(new_ones) - set(A))
            A += new_active

        # get total, male and female spread
        spread.append(len(A))
        female_spread = (np.array([genders[a] for a in A]) == "f").sum()
        male_spread = (np.array([genders[a] for a in A]) == "m").sum()
        spread_m.append(male_spread)
        spread_f.append(female_spread)

    return np.mean(spread), np.mean(spread_m), np.mean(spread_f)

def read_nodes(female, seed_num):
    ratio = female/seed_num
    with open("./target_hindex-25-{}.csv".format(ratio), "r") as f: 
        seed_list = [int(l.replace("\n","")) for l in f.readlines()]
    return seed_list

def print_info(target_ratio, spread_f, spread_total):
    # estimate the spreads
    print("Target ratio: {}".format(target_ratio))
    print("Female ratio: {}".format(spread_f/spread_total))
    print("Spread: {}".format(spread_total))

seed_num = 25
agnostic_females = 20
agnostic_ratio = agnostic_females/seed_num
for f in range(seed_num+1):
    target_ratio = f/seed_num
    """
    if target_ratio == agnostic_ratio:
        seed = read_nodes(agnostic_females, seed_num)
        spread_total, spread_m, spread_f = IC_graph_gendered(g, seed, mc=1000, genders=genders)
        best_spread_total = spread_total
        best_spread_f = spread_f
    elif target_ratio < agnostic_ratio:
        best_spread_total, best_spread_f = 0, 0
        for i in range(f, agnostic_females+1):
            seed = read_nodes(i, seed_num)
            spread_total, spread_m, spread_f = IC_graph_gendered(g, seed, mc=1000, genders=genders)
            if spread_total > best_spread_total:
                best_spread_total = spread_total
                best_spread_f = spread_f
    else:
        best_spread_total, best_spread_f = 0, 0
        for i in range(agnostic_females, f+1):
            seed = read_nodes(i, seed_num)
            spread_total, spread_m, spread_f = IC_graph_gendered(g, seed, mc=1000, genders=genders)
            if spread_total > best_spread_total:
                best_spread_total = spread_total
                best_spread_f = spread_f
    """

    seed = read_nodes(f, seed_num)
    best_spread_total, best_spread_m, best_spread_f = IC_graph_gendered(g, seed, mc=1000, genders=genders)
    print_info(target_ratio, best_spread_f, best_spread_total)



