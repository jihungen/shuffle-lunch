import random


from common import build_indexes_with_score, evaluate_group, \
	generate_indexes_from_list, chunk_it, evaluate_grouping


def identify_index_to_add(records, indexes, group_indexes):
	random.shuffle(indexes)
	
	best_indexes_to_add = build_indexes_with_score([], 100000)
	
	for index in indexes:
		new_index_added = group_indexes + [index]
		curr_group_score = evaluate_group(records, new_index_added)
		new_indexes_to_add = build_indexes_with_score([index], curr_group_score)
		
		if new_indexes_to_add['score'] < best_indexes_to_add['score']:
			best_indexes_to_add = new_indexes_to_add
		elif new_indexes_to_add['score'] == best_indexes_to_add['score']:
			best_indexes_to_add['indexes'].extend(new_indexes_to_add['indexes'])

	random.shuffle(best_indexes_to_add['indexes'])
	
	return best_indexes_to_add['indexes'][0]


def use_greedy_method(records, nums_to_divide):
	indexes = generate_indexes_from_list(records)
	
	sizes_of_groups = [len(group) for group in chunk_it(indexes, nums_to_divide)]
	curr_group_index = 0
	
	grouping_indexes = []
	curr_group = []
	
	while len(indexes) > 0:
		random.shuffle(indexes)
		
		index_to_add = identify_index_to_add(records, indexes, curr_group)
		curr_group.append(index_to_add)
		
		if len(curr_group) >= sizes_of_groups[curr_group_index]:
			grouping_indexes.extend(curr_group)
			curr_group = []
			curr_group_index += 1
		
		new_indexes = [index for index in indexes if index != index_to_add]
		indexes = new_indexes
		
	indexes_to_calculate = chunk_it(grouping_indexes, nums_to_divide)
	grouping_score = evaluate_grouping(records, indexes_to_calculate)
	
	return build_indexes_with_score(indexes_to_calculate, grouping_score)
