import random as r
import statistics
import time
import concurrent.futures

start_time = time.time()

num_iterations = 100000
points_per_raid = 31950
tbow_testing_kc = 2409
pet = True
unique_weights = {
    "Arcane Prayer Scroll": 20,
    "Dexterous Prayer Scroll": 20,
    "Twisted Buckler": 4,
    "Dragon Hunter Crossbow": 4,
    "Dinh's Bulwark": 3,
    "Ancestral Hat": 3,
    "Ancestral Robe Top": 3,
    "Ancestral Robe Bottom": 3,
    "Dragon Claws": 3,
    "Elder Maul": 2,
    "Kodai Insignia": 2,
    "Twisted Bow": 2
}

MEGARARES = [key for key, value in unique_weights.items() if value == 2]
ANC_AND_OTHERS = [key for key, value in unique_weights.items() if value == 3]
BUCKLER_CROSSBOW = [key for key, value in unique_weights.items() if value == 4]
SCROLLS = [key for key, value in unique_weights.items() if value == 20]
ANCESTRAL = [i for i in unique_weights.keys() if "Ancestral" in i]

unique_table = []
for unique, quantity in unique_weights.items():
    for i in range(quantity):
        unique_table.append(unique)

completion_kcs = []
megarare_counts = []
ancestral_counts = []
scrolls_counts = []
buckler_crossbow_counts = []
anc_and_others_counts = []
pet_counts = []
got_tbow_by_kc_count = 0

def filter_result_dict(result, valid_keys) -> list[int]:
    return [value for key, value in result.items() if key in valid_keys]

def simulate_collection_log() -> (dict, bool, int):
    result = {}
    got_tbow_by_kc = False
    kc = 0
    while len(result.keys()) < (len(unique_weights) if not pet else len(unique_weights) + 1):
        if kc == tbow_testing_kc:
            got_tbow_by_kc = "Twisted Bow" in result.keys()
        kc += 1
        if r.random() < ((points_per_raid/8676)/100):
            if pet and r.random() < (1/53):
                result.setdefault("Olmlet", 0)
                result["Olmlet"] += 1
            drop = r.choice(unique_table)
            result.setdefault(drop, 0)
            result[drop] += 1

    return result, got_tbow_by_kc, kc


for _ in range(num_iterations):
    drops, got_tbow_by_kc, completion_kc = simulate_collection_log()
    completion_kcs.append(completion_kc)
    got_tbow_by_kc += 1 if got_tbow_by_kc else 0
    megarare_counts.append(sum(filter_result_dict(drops, MEGARARES)))
    ancestral_counts.append(sum(filter_result_dict(drops, ANCESTRAL)))
    scrolls_counts.append(sum(filter_result_dict(drops, SCROLLS)))
    anc_and_others_counts.append(sum(filter_result_dict(drops, ANC_AND_OTHERS)))
    buckler_crossbow_counts.append(sum(filter_result_dict(drops, BUCKLER_CROSSBOW)))
    pet_counts.append(drops["Olmlet"])

end_time = time.time()

print('Sim iterations: ', num_iterations)
print('Mean: ', round(statistics.mean(completion_kcs), 2))
print('stdev: ', round(statistics.stdev(completion_kcs), 2))
print('Median: ', round(statistics.median(completion_kcs), 2))
print('Avg megarares: ', round(statistics.mean(megarare_counts), 2))
print('Avg anc: ', round(statistics.mean(ancestral_counts), 2))
print('Avg scrolls: ', round(statistics.mean(scrolls_counts), 2))
print('Avg anc+others: ', round(statistics.mean(anc_and_others_counts), 2))
print('Avg crossbow + bucklers: ', round(statistics.mean(buckler_crossbow_counts), 2))
print('Avg pets: ', round(statistics.mean(pet_counts), 2))
print(f'Number of accounts that got tbow by {tbow_testing_kc}:', got_tbow_by_kc_count, f'({round(got_tbow_by_kc_count/num_iterations*100,2)}%)')
print(f'Time elapsed: {round(end_time-start_time,2)} seconds')