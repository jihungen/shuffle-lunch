HISTORY_SCORE = 100


def chunk_it(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0
	
	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg
		
	return out


def generate_indexes_from_list(target_list):
	return list(range(0, len(target_list)))


def build_indexes_with_score(indexes, score):
	return {
		'indexes': indexes,
		'score': score
	}


def build_history_cnts(records, indexes):
	history_cnts = {}
	
	for index in indexes:
		for history in records[index]['history']:
			if history not in history_cnts:
				history_cnts[history] = 0
			else:
				history_cnts[history] += 1
				
	return history_cnts


def evaluate_group(records, indexes):
	history_cnts = build_history_cnts(records, indexes)
				
	score = 0
	for history in history_cnts.keys():
		score = score + history_cnts[history] * int(history / HISTORY_SCORE)
		
	return score


def print_issue_history(records, indexes):
	history_cnts = build_history_cnts(records, indexes)
	
	for history in history_cnts.keys():
		if history_cnts[history] > 0:
			issue_names = []
			for index in indexes:
				if history in records[index]['history']:
					issue_names.append(records[index]['name'])
					
			print(str(history) + ' : ' + ', '.join(issue_names))


def evaluate_grouping(records, grouping_indexes):
	grouping_score = 0
	for curr_index in grouping_indexes:
		curr_score = evaluate_group(records, curr_index)
		grouping_score = grouping_score + curr_score
		
	return grouping_score


def calculate_month_diff(date_1, date_2):
	date_before = date_1
	date_after = date_2
	
	if date_1 > date_2:
		date_after = date_1
		date_before = date_2
		
	return (date_after.year - date_before.year) * 12 + date_after.month - date_before.month
