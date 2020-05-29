"""omms_telegram_collection.

Usage:
omms_telegram_collection -h | --help
omms_telegram_collection --version

Options:

 -h --help    Show this screen.
 --version    Show the version.
"""

import sys
from omms_telegram_collection.from_docopt import from_docopt

from omms_telegram_collection.telegram import SyncTelegramClient


def main(inputargs=None):
    """Main entry point of omms_telegram_collection"""
    if inputargs is None:
        inputargs = sys.argv[1:] if len(sys.argv) > 1 else ""
    #    args = from_docopt(argv=inputargs, docstring=__doc__)

    test = SyncTelegramClient()
    msgs = test.fetch_messages("pjwnews", 100, 0)
    print("moi")


if __name__ == "__main__":
    main()
