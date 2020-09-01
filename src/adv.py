"""
Make a new player object that is currently in the 'outside' room.

Write a loop that:
* Prints the current room name
* Prints the current description (the textwrap module might be useful here).
* Waits for user input and decides what to do.

If the user enters a cardinal direction, attempt to move to the room there.
Print an error message if the movement isn't allowed.

If the user enters "q", quit the game.

Now Even More Deadly!

Possible future project: NLP to encode / decode the directions from user input.
"""
from Fortuna import d

from src.player import Player
from src.room import Room


rooms = {
    'outside': Room(
        "Outside Cave Entrance",
        "North of you, the drawbridge of a ruined castle beckons you.",
    ),
    'foyer': Room(
        "Castle Foyer",
        "Dim light filters in from the south. Dusty passages run north and east.",
    ),
    'overlook': Room(
        "Grand Overlook",
        "A steep cliff appears before you, falling into the darkness. Ahead to\n"
        "the north, a light flickers in the distance, there is but a slim \n"
        "chance to cross the chasm without magical aid.",
    ),
    'narrow': Room(
        "Not-so Secret Passage",
        "This narrow passage bends here from west to north. The smell of gold\n"
        "permeates the air.",
    ),
    'treasure': Room(
        "Royal Treasure Chamber",
        "You've found the long-lost treasure chamber! Sadly, it has already\n"
        "been completely plundered by earlier adventurers. The only exit is to\n"
        "the south.",
    ),
    'dragon_lair': Room(
        "Dragon's Lair",
        "You're engulfed in flames as the ancient dragon's breath fills the room."
    )
}

rooms['outside'].n_to = rooms['foyer']
rooms['foyer'].s_to = rooms['outside']
rooms['foyer'].n_to = rooms['overlook']
rooms['foyer'].e_to = rooms['narrow']
rooms['overlook'].s_to = rooms['foyer']
rooms['overlook'].n_to = rooms['dragon_lair']
rooms['dragon_lair'].s_to = rooms['overlook']
rooms['narrow'].w_to = rooms['foyer']
rooms['narrow'].n_to = rooms['treasure']
rooms['treasure'].s_to = rooms['narrow']

player = Player('Pyewacket', location=rooms['outside'])
print(f"\n{player.name}'s starting location: {player.location.name}")
print(f"{player.location.description}")

while True:
    direction_dispatch = {
        'n': lambda x: x.n_to,
        's': lambda x: x.s_to,
        'e': lambda x: x.e_to,
        'w': lambda x: x.w_to,
    }
    user_input = input("\nWhere would you like to go next? ")
    if not user_input:
        continue
    else:
        user_input = user_input[0].lower()
    if user_input == 'q':
        exit()
    if user_input in direction_dispatch.keys():
        target = direction_dispatch[user_input](player.location)
        if target:
            player.location = target
            if target.name != "Dragon's Lair":
                print(f'{player.name} enters the {player.location.name}')
                print(f'{player.location.description}')
            else:
                if d(20) > 15:
                    print(f'{player.name} enters the {player.location.name}')
                    print(f'{player.location.description}')
                    print("You have been incinerated!")
                else:
                    print("You attempt to gain entry to the Dragon's Lair,\n"
                          "but fall to your death crossing the chasm.")
                exit()
        else:
            print('You cannot go that way!')
    else:
        print(f"You cannot go that way, '{user_input}' is not a valid "
              f"direction.\nTry one of these: (n, s, e, w)")
