import argparse
import os

from ui import demo


def parse_args():
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('--server_port', type=int, default=80)
    parser.add_argument('--server_name', type=str, default="0.0.0.0")
    return parser.parse_args()

if __name__ == '__main__':
    
    if not os.environ.get("OPENAI_API_KEY"):
        raise Exception("Please set OPENAI_API_KEY")

    args = parse_args()
    demo.queue()
    demo.launch(server_name=args.server_name, server_port=args.server_port)
