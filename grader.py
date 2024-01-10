#! /usr/bin/env python3

from pico import Pico

from prettytable import PrettyTable
import json, argparse

def print_classrooms_table(classrooms: list):
	table = PrettyTable()
	table.field_names = ["Name", "ID", "Admin"]

	for classroom in classrooms:
		admin_status = "Yes" if classroom['leader'] else "No"
		table.add_row([classroom['name'], classroom['id'], admin_status])

	print(table)

def print_assignments_table(assignments: list):
	table = PrettyTable()
	table.field_names = ["Name", "ID", "Active", "Due Date"]

	for assignment in assignments:
		active_status = "Active" if assignment['active'] else "Inactive"
		due_date = assignment['due_date'] if assignment['due_date'] else "N/A"
		table.add_row([assignment['name'], assignment['id'], active_status, due_date])

	print(table)

def print_results_table(results: dict):
	table = PrettyTable()
	table.field_names = ["Username", "Earned", "Max", "Percentage", "Suspicious Count"]

	for result in results.get('results', []):
		total_points = sum(challenge['points'] for challenge in result['challenges'] if challenge['solved_by_due_date'])
		possible_points = sum(challenge['points'] for challenge in result['challenges'])
		percentage = (total_points / possible_points * 100) if possible_points > 0 else 0
		suspicious_submissions_count = sum(len(challenge['suspicious_submissions']) for challenge in result['challenges'])

		table.add_row([
			result['username'],
			total_points,
			possible_points,
			f"{percentage:.2f}%",
			suspicious_submissions_count
		])

	print(table)

