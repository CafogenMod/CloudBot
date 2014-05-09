import json

from util import hook, textgen


def get_generator(_json, variables):
    data = json.loads(_json)
    return textgen.TextGenerator(data["templates"],
                                 data["parts"], variables=variables)


@hook.command
def slap(inp, action=None, nick=None, conn=None, notice=None, bot=None):
    """slap <user> -- Makes the bot slap <user>."""
    target = inp.strip()

    # if the user is trying to make the bot slap itself, slap them
    if target.lower() == conn.nick.lower() or target.lower() in ["itself", "yourself"]:
        target = nick

    masters = bot.config.get("masters", [])
    if masters:
        if target.lower() in masters:   
            target = nick
    print masters

    variables = {
        "user": target
    }

    with open("plugins/data/slaps.json") as f:
        generator = get_generator(f.read(), variables)

    # act out the message
    action(generator.generate_string())
