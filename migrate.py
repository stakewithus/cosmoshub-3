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
        export_output = subprocess.check_output(docker_cmd, shell=True)
        return export_output
    except subprocess.CalledProcessError as err:
        print(err)


def checksum_exported(settings):
    source_dir = settings["default"]["SourceDirectory"]
    arrange_proc = subprocess.Popen(
        "jq -S -c -M '' exported.json",
        shell=True,
        cwd=source_dir,
        stdout=subprocess.PIPE,
    )
    output = subprocess.check_output(
        ("shasum", "-a", "256"),
        stdin=arrange_proc.stdout,
    )
    arrange_proc.wait()
    checksum = str(output, "utf-8")
    print(f"Verify SHASUM: {checksum}")


def migrate_exported(settings):
    source_dir = settings["default"]["SourceDirectory"]
    if settings["migration"]["SourceIncludesNetwork"] == "yes":
        source_dir += "/" + settings["migration"]["FromNetwork"]
    to_image = settings["migration"]["ToImage"]
    to_network = settings["migration"]["ToNetwork"]

    docker_cmd = f"""docker run \
--mount type=bind,src={source_dir},dst=/opt/chain \
-w /opt/chain \
--rm -it {to_image} \
migrate \
v0.36 \
exported.json \
--chain-id={to_network} \
--genesis-time=2019-09-24T13:38:19Z \
> {to_network}-genesis.json
"""
    try:
        export_output = subprocess.check_output(docker_cmd, shell=True)
        return export_output
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
    # export_for_height(settings)
    # Check SHA256 SUM
    checksum_exported(settings)

    migrate_exported(settings)


if __name__ == "__main__":
    main()
