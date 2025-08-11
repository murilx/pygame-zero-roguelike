from enemy import Orc, Shooter

# TODO: Criar um gerador de mapa procedural
rooms = {
    "start_room": {
        "doors": {"north": "room5", "east": "room3", "west": "room2", "south": "room4"},
        "enemies": [],
        "goal": False,
    },
    "room2": {
        "doors": {"north": None, "east": "start_room", "west": None, "south": None},
        "enemies": [Orc((48, 48)), Orc((48, 208)), Orc((208, 48))],
        "goal": False,
    },
    "room3": {
        "doors": {
            "north": None,
            "east": "final_room",
            "west": "start_room",
            "south": None,
        },
        "enemies": [Orc((48, 48)), Shooter((48, 208)), Orc((208, 48))],
        "goal": False,
    },
    "room4": {
        "doors": {"north": "start_room", "east": None, "west": None, "south": None},
        "enemies": [Shooter((48, 48)), Shooter((208, 208))],
        "goal": False,
    },
    "room5": {
        "doors": {"north": None, "east": None, "west": None, "south": "start_room"},
        "enemies": [Shooter((48, 48)), Orc((208, 208))],
        "goal": False,
    },
    "final_room": {
        "doors": {"north": None, "east": None, "west": "room3", "south": None},
        "enemies": [],
        "goal": True,
    },
}
