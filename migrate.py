# Migration Script for CosmosHub 2 to 3
import argparse
import configparser
import subprocess


def export_for_height(settings):
    export_height = settings["export_height"]
    from_image = settings["migration"]["FromImage"]
    source_dir = settings["default"]["SourceDirectory"]
    if settings["migration"]["SourceIncludesNetwork"] == "yes":
        source_dir += "/" + settings["migration"]["FromNetwork"]

    docker_cmd = f"""docker run \
--mount type=bind,src={source_dir},dst=/opt/chain \
-w /opt/chain \
--rm -it {from_image} \
export \
--for-zero-height \
--height={export_height} \
> exported.json
"""
    try:
        export_output = subprocess.check_output(docker_cmd, shell=True, stderr=None)
    except subprocess.CalledProcessError as err:
        print(err)


def main():
    arg_parser = argparse.ArgumentParser(
        description="Migrate a node from cosmoshub-2 to cosmoshub-3",
    )
    arg_parser.add_argument(
        "height",
        metavar="height",
        type=int,
        help="The height to export state from",
    )

    args = arg_parser.parse_args()
    export_height = args.height

    cfg_parser = configparser.ConfigParser()
    cfg_parser.read("config.ini")

    if "migration" not in cfg_parser.sections():
        raise ValueError("[migration] is missing or config.ini does not exist")

    settings = {
        "default": cfg_parser["DEFAULT"],
        "migration": cfg_parser["migration"],
        "export_height": export_height,
    }

    # Export For Height
    export_for_height(settings)


if __name__ == "__main__":
    main()
