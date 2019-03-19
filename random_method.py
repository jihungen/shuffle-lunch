import random

from common import generate_indexes_from_list, build_indexes_with_score, \
	chunk_it, evaluate_grouping


RANDOM_METHOD_ITERATIONS = 10000


def use_random_method(records, nums_to_divide):
	indexes = generate_indexes_from_list(records)
	
	best_grouping = build_indexes_with_score(None, 100000)
	
	for repeats in range(RANDOM_METHOD_ITERATIONS):
		random.shuffle(indexes)
		grouping_indexes = chunk_it(indexes, nums_to_divide)
		
		grouping_score = evaluate_grouping(records, grouping_indexes)
		new_grouping = build_indexes_with_score(grouping_indexes, grouping_score)
		
		if new_grouping['score'] < best_grouping['score']:
			best_grouping = new_grouping
			
		if best_grouping['score'] <= 0:
			break
			
	return best_grouping
