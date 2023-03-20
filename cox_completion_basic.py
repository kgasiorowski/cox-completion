import random as r
import statistics
import time

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

mega_rares = [key for key, value in unique_weights.items() if value == 2]
anc_and_others = [key for key, value in unique_weights.items() if value == 3]
buckler_crossbow = [key for key, value in unique_weights.items() if value == 4]
scrolls = [key for key, value in unique_weights.items() if value == 20]
ancestral = [i for i in unique_weights.keys() if "Ancestral" in i]

unique_table = []
for unique, quantity in unique_weights.items():
    for i in range(quantity):
        unique_table.append(unique)

completion_kc = []
megarare_counts = []
ancestral_counts = []
scrolls_counts = []
buckler_crossbow_counts = []
anc_and_others_counts = []
pet_counts = []
got_tbow_by_kc_count = 0

for _ in range(num_iterations):
    drops = set()
    kc = 0
    megarare_count = 0
    ancestral_count = 0
    scrolls_count = 0
    buckler_crossbow_count = 0
    anc_and_others_count = 0
    pet_count = 0
    got_tbow_by_kc = False
    while len(drops) < (len(unique_weights) if not pet else len(unique_weights) + 1):
        if kc == tbow_testing_kc:
            got_tbow_by_kc_count += 1 if "Twisted Bow" in drops else 0
        kc += 1
        if r.random() < ((points_per_raid/8676)/100):
            if pet and r.random() < (1/53):
                drops.add("Olmlet")
                pet_count += 1
            drop = r.choice(unique_table)
            megarare_count += 1 if drop in mega_rares else 0
            ancestral_count += 1 if drop in ancestral else 0
            scrolls_count += 1 if drop in scrolls else 0
            buckler_crossbow_count += 1 if drop in buckler_crossbow else 0
            anc_and_others_count += 1 if drop in anc_and_others else 0
            drops.add(drop)
    got_tbow_by_kc_count += 1 if kc < tbow_testing_kc else 0
    completion_kc.append(kc)
    megarare_counts.append(megarare_count)
    ancestral_counts.append(ancestral_count)
    scrolls_counts.append(scrolls_count)
    anc_and_others_counts.append(anc_and_others_count)
    buckler_crossbow_counts.append(buckler_crossbow_count)
    pet_counts.append(pet_count)

end_time = time.time()

print('Sim iterations: ', num_iterations)
print('Mean: ', round(statistics.mean(completion_kc), 2))
print('stdev: ', round(statistics.stdev(completion_kc), 2))
print('Median: ', round(statistics.median(completion_kc), 2))
print('Avg megarares: ', round(statistics.mean(megarare_counts), 2))
print('Avg anc: ', round(statistics.mean(ancestral_counts), 2))
print('Avg scrolls: ', round(statistics.mean(scrolls_counts), 2))
print('Avg anc+others: ', round(statistics.mean(anc_and_others_counts), 2))
print('Avg crossbow + bucklers: ', round(statistics.mean(buckler_crossbow_counts), 2))
print('Avg pets: ', round(statistics.mean(pet_counts), 2))
print(f'Number of accounts that got tbow by {tbow_testing_kc}:', got_tbow_by_kc_count, f'({round(got_tbow_by_kc_count/num_iterations*100,2)}%)')
print(f'Time elapsed: {round(end_time-start_time,2)} seconds')