import asyncio
import os

from dotenv import find_dotenv, load_dotenv
from spond import spond

load_dotenv(find_dotenv())

# Fetch variables from the .env file.
username = os.getenv("SPOND_USERNAME")
password = os.getenv("SPOND_PASSWORD")

trough_fc_id = "7A150EBDCE804330B67A83721745F645"


def clean_name(name: str) -> str:
    """
    Tidy up some names to match the Google Sheet
    """

    name_map = {
        "JithinA": "JithinAreepuzha",
        "Ethan 'The Danger'Webb": "Ethan Webb",
    }
    return name_map.get(name, name)


async def main():
    s = spond.Spond(username=username, password=password)

    events = await s.get_events(group_id=trough_fc_id)

    # grab the next event
    event = events[0]

    player_ids = event["responses"]["acceptedIds"]
    users = event["recipients"]["group"]["members"]
    names = [
        clean_name(user["firstName"] + user["lastName"])
        for user in users
        if user["id"] in player_ids
    ]

    print(names)

    await s.clientsession.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
