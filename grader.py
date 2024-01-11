#! /usr/bin/env python3

from pico import Pico
from prettytable import PrettyTable
import argparse

def print_classrooms_table(classrooms: list):
	table = PrettyTable()
	table.field_names = ["Name", "ID", "Admin"]

	for classroom in classrooms:
		admin_status = "Yes" if classroom['leader'] else "No"
		table.add_row([classroom['name'], classroom['id'], admin_status])

	print(table)

def print_assignments_table(assignments: list):
	table = PrettyTable()
	table.field_names = ["Name", "ID", "Active", "Challenges", "Points Worth", "Due Date"]

	for assignment in assignments:
		active_status = "Active" if assignment['active'] else "Inactive"
		amount_of_challenges = len(assignment['challenges'])
		possible_points = sum(challenge['points'] for challenge in assignment['challenges'])
		due_date = assignment['due_date'] if assignment['due_date'] else "N/A"
		table.add_row([assignment['name'], assignment['id'], active_status, amount_of_challenges, possible_points, due_date])

	print(table)

def print_results_table(results: dict, penalty: int):
	table = PrettyTable()
	field_names = ["Username", "Earned", "Max", "Percentage", "Suspicious Count"]

	if penalty > 0:
		field_names.insert(2, "Penalty")
	table.field_names = field_names

	for result in results.get('results', []):
		possible_points = sum(challenge['points'] for challenge in result['challenges'])
		earned_points = sum(challenge['points'] for challenge in result['challenges'] if challenge['solved_by_due_date'])

		suspicious_submissions_count = sum(len(challenge['suspicious_submissions']) for challenge in result['challenges'])
		penalty_points = suspicious_submissions_count * penalty

		adjusted_points = max(earned_points - penalty_points, 0)
		percentage = (adjusted_points / possible_points * 100) if possible_points > 0 else 0

		row = [
			result['username'],
			earned_points,
			possible_points,
			f"{percentage:.2f}%",
			suspicious_submissions_count
		]

		if penalty > 0:
			row.insert(2, penalty_points)
		table.add_row(row)

	print(table)

def setup_argparse():
	parser = argparse.ArgumentParser(description="PicoCTF classroom grader.")

	parser.add_argument("-u", "--username", required=True, help="Your PicoCTF username")
	parser.add_argument("-p", "--password", required=True, help="Your PicoCTF password")

	subparsers = parser.add_subparsers(dest="command", help="Choose a command")

	subparsers.add_parser("classrooms", help="Prints classrooms you have access to (name, ID, admin status)")

	assignments_parser = subparsers.add_parser("assignments", help="Prints PicoCTF assignments for a specific classroom (name, ID, active status, max points, due date)")
	assignments_parser.add_argument("--classroom-id", type=int, required=True, help="ID of the PicoCTF classroom")

	results_parser = subparsers.add_parser("results", help="Prints results for a specific assignment (username, earned points, max points, percentage, suspicious submissions count.)")
	results_parser.add_argument("--assignment-id", type=int, required=True, help="ID of the assignment")
	results_parser.add_argument("--penalty", type=int, default=0, help="Penalty for each suspicious submission (default: 0)")

	return parser

if __name__ == "__main__":
	parser = setup_argparse()
	args = parser.parse_args()

	pico = Pico.login(args.username, args.password)

	command_functions = {
		"classrooms": lambda: print_classrooms_table(pico.get_classrooms()),
		"assignments": lambda: print_assignments_table(pico.access_assignments(args.classroom_id)),
		"results": lambda: print_results_table(pico.get_results_by_assignment(args.assignment_id), args.penalty)
	}

	if args.command in command_functions:
		command_functions[args.command]()
