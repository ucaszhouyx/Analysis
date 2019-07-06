import argparse

def prepare(year,channel):
    print('year is =={}'.format(year))
    print('channel is =={}'.format(channel))

def parse_args():
    parser = argparse.ArgumentParser()

    # create the parser for training a classifier
    parser.add_argument('--year', default='2016')
    parser.add_argument('--channel', default='Xicc')
    args = parser.parse_args() 
    prepare(args.year,args.channel)

   # return parser

if __name__ == '__main__':
    parse_args()
#    args = parser.parse_args()
#    year = args.year
#    channel = args.channel
#    prepare(args.year,args.channel)
		    

