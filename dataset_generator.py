import argparse
from image_grabber import image_downloader

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('image_keyword', nargs=1, help='keyword to search')
    parser.add_argument('-dest', help='Folder destination (default: "images"). A sub folder is created for each keyword')
    parser.add_argument('-limit', help='Number of files to download (default: 50)')

    args = parser.parse_args()

    print args

    downloader = image_downloader.ImageDownloader()
    print args.limit

    if args.dest is not None:
        downloader.destination = args.dest

    if args.limit is not None:
        downloader.limit = int(args.limit)

    keyword = args.image_keyword[0]
    downloader.download_images(keyword)




