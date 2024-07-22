import argparse
import json
import sys

from .plate_model import PlateModel


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(1)


def main():
    parser = ArgParser()

    subparser = parser.add_subparsers(dest="command")
    ls_cmd = subparser.add_parser("ls")
    get_cmd = subparser.add_parser("get")

    ls_cmd.add_argument("-m", "--rotation-model", type=str, dest="rotation_model")

    get_cmd.add_argument("-m", "--rotation-model", type=str, dest="rotation_model")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "ls":
        if args.rotation_model == None:
            print("Listing all the rotation models....")
            models = PlateModel.list_models()
            print(json.dumps(models))
        else:
            print(f"Listing all the layers in rotation model {args.rotation_model}")
            model_details = PlateModel(args.rotation_model).get_cfg()
            print(json.dumps(model_details, indent=4))

    elif args.command == "get":
        if args.rotation_model:
            model_details = PlateModel(args.rotation_model).get_cfg()
            print(json.dumps(model_details, indent=4))
        else:
            print(f"get something")


if __name__ == "__main__":
    main()
