import argparse


def get():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name',default='AAAAA')
		

    return parser


if __name__ == '__main__':
    parser = get()
    args = parser.parse_args()
    name = args.name
    print('XXX {}'.format(name))
