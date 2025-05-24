from datetime import datetime, timedelta
import random

# Sample database for 911 calls
calls_db = {}


def generate_sample_data():
    sample_data = [
        {
            "id": "1",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {"role": "assistant", "content": "9-1-1, what's your emergency?"},
                {"role": "user", "content": "There's a fire in my apartment building!"},
                {
                    "role": "assistant",
                    "content": "I understand there's a fire. What's your location?",
                },
                {"role": "user", "content": "123 Main Street, Apartment 4B"},
            ],
            "emotions": [
                {"emotion": "fear", "intensity": 0.8},
                {"emotion": "stress", "intensity": 0.9},
                {"emotion": "urgency", "intensity": 0.95},
            ],
            "phone": "555-123-4567",
            "recommendation": "Evacuate immediately. Do not use elevators.",
            "severity": "MODERATE",
            "type": "fire",
            "name": "John Doe",
            "title": "Apartment Fire on Main Street",
            "summary": "Caller reported a fire in their apartment building. Immediate evacuation required.",
            "location": "123 Main Street, Apartment 4B",
        },
        {
            "id": "2",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {"role": "assistant", "content": "9-1-1, what's your emergency?"},
                {
                    "role": "user",
                    "content": "I think my neighbor is having a heart attack!",
                },
                {
                    "role": "assistant",
                    "content": "I understand it's a medical emergency. What's the address?",
                },
                {"role": "user", "content": "456 Oak Avenue, House number 7"},
            ],
            "emotions": [
                {"emotion": "panic", "intensity": 0.9},
                {"emotion": "concern", "intensity": 0.95},
                {"emotion": "helplessness", "intensity": 0.7},
            ],
            "phone": "555-987-6543",
            "recommendation": "Begin CPR if trained. Keep the patient still and calm.",
            "severity": "CRITICAL",
            "type": "hospital",
            "name": "Jane Smith",
            "title": "Suspected Heart Attack on Oak Avenue",
            "summary": "Caller reported a suspected heart attack for their neighbor. Immediate medical assistance required.",
            "location": "456 Oak Avenue, House number 7",
        },
        {
            "id": "3",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {"role": "assistant", "content": "9-1-1, what's your emergency?"},
                {
                    "role": "user",
                    "content": "There's a break-in happening at the store across the street!",
                },
                {
                    "role": "assistant",
                    "content": "I understand there's a break-in. Can you give me the store's address?",
                },
                {
                    "role": "user",
                    "content": "789 Pine Street, it's the convenience store on the corner",
                },
            ],
            "emotions": [
                {"emotion": "fear", "intensity": 0.7},
                {"emotion": "alertness", "intensity": 0.8},
                {"emotion": "anxiety", "intensity": 0.6},
            ],
            "phone": "555-246-8135",
            "recommendation": "Do not approach or confront the suspects. Stay in a safe location.",
            "severity": "MODERATE",
            "type": "police",
            "name": "Mike Johnson",
            "title": "Break-in at Convenience Store on Pine Street",
            "summary": "Caller reported an ongoing break-in at a convenience store. Police assistance required immediately.",
            "location": "789 Pine Street",
        },
        {
            "id": "4",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {"role": "assistant", "content": "9-1-1, what's your emergency?"},
                {
                    "role": "user",
                    "content": "There's been a car accident on the highway!",
                },
                {
                    "role": "assistant",
                    "content": "I understand there's been a car accident. Can you tell me which highway and the nearest mile marker?",
                },
                {
                    "role": "user",
                    "content": "It's on Highway 101, near mile marker 25. Multiple cars involved.",
                },
            ],
            "emotions": [
                {"emotion": "shock", "intensity": 0.8},
                {"emotion": "concern", "intensity": 0.9},
                {"emotion": "distress", "intensity": 0.7},
            ],
            "phone": "555-369-2580",
            "recommendation": "Do not move injured persons unless in immediate danger. Turn on hazard lights and stay clear of traffic.",
            "severity": "MODERATE",
            "type": "hospital",
            "name": "Sarah Lee",
            "title": "Multi-car Accident on Highway 101",
            "summary": "Caller reported a multi-car accident on Highway 101. Emergency services dispatched for potential injuries and traffic control.",
            "location": "Highway 101, Mile Marker 25",
        },
        {
            "id": "5",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {"role": "assistant", "content": "9-1-1, what's your emergency?"},
                {"role": "user", "content": "I smell gas in my house!"},
                {
                    "role": "assistant",
                    "content": "I understand you smell gas. What's your address?",
                },
                {"role": "user", "content": "1010 Elm Street"},
            ],
            "emotions": [
                {"emotion": "worry", "intensity": 0.7},
                {"emotion": "uncertainty", "intensity": 0.6},
                {"emotion": "alertness", "intensity": 0.8},
            ],
            "phone": "555-147-2589",
            "recommendation": "Evacuate immediately. Do not turn on/off any electrical devices or create sparks.",
            "severity": "MODERATE",
            "type": "fire",
            "name": "Tom Brown",
            "title": "Gas Leak Reported on Elm Street",
            "summary": "Caller reported smelling gas in their house. Evacuation and fire department response required.",
            "location": "1010 Elm Street",
        },
        {
            "id": "6",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {"role": "assistant", "content": "9-1-1, what's your emergency?"},
                {
                    "role": "user",
                    "content": "There's a suspicious person lurking around the school!",
                },
                {
                    "role": "assistant",
                    "content": "I understand your concern. Can you tell me which school and where exactly you see this person?",
                },
                {
                    "role": "user",
                    "content": "It's at Central Elementary School, near the playground on the east side.",
                },
            ],
            "emotions": [
                {"emotion": "suspicion", "intensity": 0.8},
                {"emotion": "concern", "intensity": 0.9},
                {"emotion": "unease", "intensity": 0.7},
            ],
            "phone": "555-951-7532",
            "recommendation": "Do not approach the individual. Keep observing from a safe distance if possible.",
            "severity": "MODERATE",
            "type": "police",
            "name": "Emily Chen",
            "title": "Suspicious Person Near Central Elementary",
            "summary": "Caller reported a suspicious person near a school playground. Police dispatched to investigate.",
            "location": "Central Elementary School, East side playground",
        },
        {
            "id": "7",
            "time": (
                datetime.now() - timedelta(minutes=random.randint(0, 120))
            ).isoformat(),
            "transcript": [
                {"role": "assistant", "content": "9-1-1, what's your emergency?"},
                {"role": "user", "content": "My child is choking on food!"},
                {
                    "role": "assistant",
                    "content": "I understand your child is choking. What's your location?",
                },
                {"role": "user", "content": "2020 Maple Drive, we're in the kitchen!"},
            ],
            "emotions": [
                {"emotion": "panic", "intensity": 0.95},
                {"emotion": "fear", "intensity": 0.9},
                {"emotion": "desperation", "intensity": 0.85},
            ],
            "phone": "555-753-9514",
            "recommendation": "Perform the Heimlich maneuver if the child is over 1 year old. For infants, use back blows and chest thrusts.",
            "severity": "SAFE",
            "type": "hospital",
            "name": "Alex Rodriguez",
            "title": "Child Choking Emergency on Maple Drive",
            "summary": "Caller reported their child choking on food. Immediate medical assistance and guidance provided.",
            "location": "2020 Maple Drive",
        },
    ]

    for call in sample_data:
        calls_db[call["id"]] = call


# Generate sample data
generate_sample_data()


def get_all_calls():
    """
    Accessor function to get all calls in the database.
    """
    return calls_db


def get_call(call_id):
    """
    Accessor function to get a specific call by its ID.
    """
    return calls_db.get(call_id, {})


def update_call(call_id, updated_data):
    """
    Modification function to update or insert a specific call's data.
    """
    if call_id in calls_db:
        calls_db[call_id].update(updated_data)
    else:
        calls_db[call_id] = updated_data
    return True


def delete_call(call_id):
    """
    Function to delete a call from the database.
    """
    if call_id in calls_db:
        del calls_db[call_id]
        return True
    return False
