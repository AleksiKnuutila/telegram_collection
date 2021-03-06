from loguru import logger
import yaml
from docopt import docopt
import sys

# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
# logging.getLogger("telethon").setLevel(logging.WARNING)
#
# logger = logging.getLogger("default")

with open("config.yaml", "r") as conf, open("secret.yaml", "r") as secr:
    config = yaml.safe_load(conf)
    secret_config = yaml.safe_load(secr)
cli_args = {}
if (
    sys.modules["__main__"].__package__ is None
    or "pytest" not in sys.modules["__main__"].__package__
):
    cli_args = docopt(
        sys.modules["__main__"].__doc__, version="telegram_collection 0.1"
    )
    cli_args = {k.replace("--", ""): v for k, v in cli_args.items() if "--" in k and v}
    if "tracked-telegram-channels" in cli_args:
        cli_args["tracked-telegram-channels"] = cli_args[
            "tracked-telegram-channels"
        ].split(",")
config = {**config, **secret_config, **cli_args}
