from domain.primary_port import PrimaryPort

import argparse

class LoggingConfigCli(PrimaryPort):

    """
    A PrimaryPort that configures logging the command line.
    """
    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 0

    async def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Catches logging flags from the command line"
        )
        parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
        parser.add_argument('-vv', '--trace', action='store_true', help="Enable tracing mode")
        parser.add_argument('-q', '--quiet', action='store_true', help="Enable quiet mode")
        args, unknown_args = parser.parse_known_args()
        await app.accept_configure_logging({ "verbose": args.verbose, "trace": args.trace, "quiet": args.quiet })
