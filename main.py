import sys
import json
import math
from datetime import datetime, timedelta

from common import chunk_it, generate_indexes_from_list, \
	build_indexes_with_score, calculate_month_diff, print_issue_history
from random_method import use_random_method
from greedy_method import use_greedy_method

NUM_PEOPLE_IN_GROUP = 6
MAX_MONTHS_TO_CONSIDER = 3


GREEDY_METHOD_ITERATIONS = 100



def build_record(name, history):
	return {
		'name': name,
		'history': [result for result in history],
	}


def build_output(name, group, date):
	return {
		'name': name,
		'group': group,
		'date': date
	}


def calculate_result_score(date_now, date_result, max_month_diff):
	month_diff = calculate_month_diff(date_now, date_result)
	if month_diff > MAX_MONTHS_TO_CONSIDER:
		return None

	return (max_month_diff - month_diff + 1) * 100


def calculate_team_score(max_month_diff):
	return (max_month_diff + 1) * 100


def count_people(team_info):
	return len(team_info)


def transform_team_info_to_records(team_info, max_month_diff):
	team_with_number = {}
	curr_team_number = 0

	records = []

	for person in team_info:
		curr_team = person['team']
		if curr_team not in team_with_number:
			team_with_number[curr_team] = curr_team_number
			curr_team_number += 1

		team_to_history = calculate_team_score(max_month_diff) + team_with_number[curr_team]
		new_record = build_record(person['name'], [team_to_history])

		records.append(new_record)

	return records


def add_results_to_records(records, result_dict, date_now, max_month_diff):
	records_by_name = {}

	for person in records:
		records_by_name[person['name']] = build_record(person['name'], person['history'])

	for result_date in result_dict.keys():
		for person in result_dict[result_date]:
			date_result = datetime.strptime(person['date'], '%Y-%m-%d')
			score = calculate_result_score(date_now, date_result, max_month_diff)

			if score is not None:
				records_by_name[person['name']]['history'].append(score + person['group'])

	return [records_by_name[name] for name in records_by_name.keys()]


def use_greedy_method_with_iterations(records, nums_to_divide):
	best_grouping = build_indexes_with_score(None, 100000)

	for repeats in range(GREEDY_METHOD_ITERATIONS):
		new_grouping = use_greedy_method(records, nums_to_divide)

		if new_grouping['score'] < best_grouping['score']:
			best_grouping = new_grouping

		if best_grouping['score'] <= 0:
			break

	return best_grouping


def generate_output(records, grouping, datetime):
	date_str = datetime.strftime('%Y-%m-%d')

	outputs = []
	curr_group = 0

	for indexes in grouping['indexes']:
		for index in indexes:
			curr_output = build_output(records[index]['name'], curr_group, date_str)
			outputs.append(curr_output)

		curr_group += 1

	return {
		date_str: outputs
	}


def identify_best_grouping(records, nums_to_divide, method_to_run):
	target_method = {
		'random': use_random_method,
		'greedy': use_greedy_method_with_iterations
	}

	return target_method[method_to_run](records, nums_to_divide)


def print_grouping(records, grouping):
	print('Score: ' + str(grouping['score']))

	curr_group = 0
	for indexes in grouping['indexes']:
		names = [records[index]['name'] for index in indexes]
		print(str(curr_group) + ': ' + str(names))

		curr_group += 1


def identify_issue(records_result_added, grouping):
	for indexes in grouping['indexes']:
		print_issue_history(records_result_added, indexes)


def identify_max_month_diff(output_dict, date_curr):
	max_month_diff = 0

	for date_str in output_dict.keys():
		date_output = datetime.strptime(date_str, '%Y-%m-%d')
		month_diff = calculate_month_diff(date_curr, date_output)

		if month_diff > max_month_diff:
			max_month_diff = month_diff

	if max_month_diff > MAX_MONTHS_TO_CONSIDER:
		return MAX_MONTHS_TO_CONSIDER

	return max_month_diff


method_to_run = sys.argv[1]
simulation_months = int(sys.argv[2])


output_dict = {}
with open('./resources/team_info.json', encoding='utf-8') as json_file:
	team_info = json.load(json_file)['team_info']

	num_people = count_people(team_info)
	nums_to_divide = int(math.ceil(num_people / NUM_PEOPLE_IN_GROUP))

	date_curr = datetime(2019, 1, 1)
	for repeats in range(simulation_months):
		max_month_diff = identify_max_month_diff(output_dict, date_curr)

		records = transform_team_info_to_records(team_info, max_month_diff)
		records_result_added = add_results_to_records(records, output_dict, date_curr, max_month_diff)
		best_grouping = identify_best_grouping(records_result_added, nums_to_divide, method_to_run)

		print('Best grouping at', str(date_curr))
		print_grouping(records, best_grouping)

		print('Identify goinmul issues:')
		identify_issue(records_result_added, best_grouping)

		curr_output_dict = generate_output(records, best_grouping, date_curr)
		output_dict.update(curr_output_dict)

		date_new = datetime(date_curr.year, date_curr.month + 1, date_curr.day)
		date_curr = date_new
