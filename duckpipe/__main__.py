"""Command-line entry point: python -m duckpipe pipeline.toml

Keep this file thin. It only parses arguments, loads settings and hands off;
all real behaviour lives in the classes, where it can be tested.
"""

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    """Run the pipeline described by the given config file. Return an exit code."""
    parser = argparse.ArgumentParser(prog="duckpipe", description=__doc__)
    parser.add_argument("config", type=Path, help="path to pipeline.toml")
    args = parser.parse_args(argv)

    # TODO:
    # 1. load_dotenv() so secrets in .env become environment variables.
    # 2. config = load_config(args.config)
    # 3. with open_database(config.database) as connection:
    #        build_pipeline(config, connection).run()
    # 4. Catch PipelineError: print the message to sys.stderr and return 1.
    #    Let any other exception crash loudly; that's a bug, not bad input.
    # 5. Return 0 on success.
    print(f"duckpipe is not implemented yet (config: {args.config})", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
