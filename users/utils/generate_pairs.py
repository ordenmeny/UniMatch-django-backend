from collections import defaultdict
from itertools import combinations, permutations
import heapq

def get_user_hobbies(user):
    return set(h.name for h in user.hobby.all())

def compute_similarity(user1, user2):
    return len(get_user_hobbies(user1) & get_user_hobbies(user2))

def compute_triple_similarity(u1, u2, u3):
    hobbies = [get_user_hobbies(u) for u in (u1, u2, u3)]
    return len(hobbies[0] & hobbies[1]) + len(hobbies[0] & hobbies[2]) + len(hobbies[1] & hobbies[2])

def generate_weekly_pairs(all_users, past_pairs):
    users = list(all_users)
    used_users = set()
    result = []

    # Построим кучу из всех возможных пар с приоритетом по количеству общих интересов
    pair_heap = []
    for u1, u2 in combinations(users, 2):
        pair_set = frozenset([u1, u2])
        if pair_set in past_pairs:
            continue
        score = compute_similarity(u1, u2)
        if score > 0:
            # Вставляем в кучу с id как tie-breaker
            heapq.heappush(pair_heap, (-score, u1.id, u2.id, u1, u2))

    # Формируем пары с максимальной похожестью
    while pair_heap:
        _, _, _, u1, u2 = heapq.heappop(pair_heap)
        if u1 in used_users or u2 in used_users:
            continue
        used_users.update([u1, u2])
        result.append((u1, u2))

    # Остались неиспользованные
    remaining = [u for u in users if u not in used_users]

    if len(remaining) == 3:
        # Пытаемся найти лучшую тройку из трёх оставшихся
        best_score = -1
        best_triplet = None
        for trio in permutations(remaining, 3):
            trio_set = frozenset(trio)
            if trio_set in past_pairs:
                continue
            score = compute_triple_similarity(*trio)
            if score > best_score:
                best_score = score
                best_triplet = trio
        if best_triplet and best_score > 0:
            result.append(best_triplet)
            used_users.update(best_triplet)

    return result
