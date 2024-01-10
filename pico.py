import requests

BASE_URL = "https://play.picoctf.org/api"
USER_AGENT = "PicoGrader"

class Pico:
	def __init__(self, session, csrf_token, session_id):
		self.session = session
		self.csrf_token = csrf_token
		self.session_id = session_id
		self.session.headers.update({'User-Agent': USER_AGENT})

	@classmethod
	def login(cls, username: str, password: str):
		'''
			Attempts to login to PicoCTF with the given credentials.
			Returns a Pico object if successful, otherwise None.
		'''
		login_url = f"{BASE_URL}/user/login/"
		login_payload = {"username": username, "password": password}
		session = requests.Session()
		session.headers.update({'User-Agent': USER_AGENT})

		try:
			response = session.post(login_url, data=login_payload)
			response.raise_for_status()

			csrf_token = response.cookies.get('csrftoken')
			session_id = response.cookies.get('sessionid')
			session.cookies.set('csrftoken', csrf_token)
			session.cookies.set('sessionid', session_id)

			return cls(session, csrf_token, session_id)
		except requests.RequestException as e:
			print(f"Error logging in: {e}")
			return None

	def get_classrooms(self):
		'''
			Retrieves and returns raw JSON data of all classrooms the user is enrolled in.
			JSON format returned:
			[
				{
					'id': int,                  # Unique identifier for the classroom
					'name': str,                # Name of the classroom
					'invite_code': str,         # Invitation code for the classroom
					'pending': bool,            # Indicates if the user's membership is pending
					'leader': bool,             # Indicates if the user is a leader in the classroom
					'include_leaders_in_scoring': bool  # Indicates if leaders are included in scoring
				},
				... # Additional classroom objects in the same format
			]
		'''
		classrooms_url = f"{BASE_URL}/classrooms/?page=1"

		try:
			response = self.session.get(classrooms_url)
			response.raise_for_status()

			return response.json().get("results", [])
		except requests.RequestException as e:
			print(f"Error getting classrooms: {e}")
			return []

	def access_assignments(self, classroom_id: int):
		'''
			Retrieves and returns raw JSON data of all assignments associated with a specific classroom.
			JSON format returned:
			[
				{
					'id': int,          # Unique identifier for the assignment
					'classroom': {
						'id': int,      # Unique identifier of the classroom
						'name': str     # Name of the classroom
					},
					'name': str,        # Name of the assignment
					'due_date': str,    # Due date of the assignment in ISO 8601 format
					'active': bool,     # Indicates if the assignment is currently active
					'created': bool,    # Indicates if the assignment has been created
					'challenges': [     # List of challenges associated with the assignment
						{
							'id': int,               # Unique identifier for the challenge
							'name': str,             # Name of the challenge
							'points': int,           # Points awarded for the challenge
							'solved_by_due_date': bool,  # Indicates if the challenge was solved by due date
							'solve_time': str or None    # Time at which the challenge was solved, in ISO 8601 format or None if not solved
						},
						... # Additional challenge objects in the same format
					]
				},
				... # Additional assignment objects in the same format
			]
		'''
		assignments_url = f"{BASE_URL}/assignments/?classroom={classroom_id}&created=true&page=1&page_size=10000"

		try:
			response = self.session.get(assignments_url)
			response.raise_for_status()

			return response.json().get("results", [])
		except requests.RequestException as e:
			print(f"Error accessing assignments: {e}")
			return []

	def get_results_by_assignment(self, assignment_id: int):
		'''
			Retrieves and returns raw JSON data of all assignments associated with a specific classroom.
			JSON format returned:
			{
				'results': [
					{
						'user_id': int,                   # Unique identifier for the user
						'username': str,                  # Username of the user
						'challenges': [                   # List of challenges associated with the assignment for this user
							{
								'id': int,                           # Unique identifier for the challenge
								'name': str,                         # Name of the challenge
								'points': int,                       # Points awarded for the challenge
								'solved_by_due_date': bool,          # Indicates if the challenge was solved by the due date
								'solve_time': str or None,           # Time at which the challenge was solved, in ISO 8601 format or None if not solved
								'suspicious_submissions': [str],     # List of timestamps for suspicious submissions, in ISO 8601 format
							},
							... # Additional challenge objects in the same format
						],
						'completed': bool,                # Indicates if the assignment is completed by the user
					},
					... # Additional result objects for other users in the same format
				]
			}
		'''
		results_url = f"{BASE_URL}/assignments/{assignment_id}/results/"

		try:
			response = self.session.get(results_url)
			response.raise_for_status()

			return response.json()
		except requests.RequestException as e:
			print(f"Error getting results by assignment: {e}")
			return {}


