import mechanize
import zipfile
import re
import sys
import argparse

DOWNLOADS_URL = "https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html"
ZIP_URL = "http://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_%s.zip"
CHUNK_SIZE= 1000
LINK_PATTERN = re.compile("download.nlm.nih.gov.*full")

def download_rxnorm(args):

    br = mechanize.Browser()
    br.set_handle_robots(False)

    if args.release:
        url = ZIP_URL%args.release
    else:
        br.open(DOWNLOADS_URL)
        url = br.links(url_regex=LINK_PATTERN).next().url

    print("Signing in to download %s"%(url))
    br.open(url)

    br.select_form(nr=0)
    br["username"] = args.username
    br["password"] = args.password
    zip_request = br.submit()

    try:
        bytes = int(zip_request.info().getheader('Content-Length'))
    except:
        print "Failed to download file. Check your credentials."
        sys.exit(1)

    with open(args.file, "wb") as outfile:
        while zip_request.tell() < bytes:
            outfile.write(zip_request.read(size=CHUNK_SIZE))
            read = zip_request.tell()
            print "\rDownload:  %.2f%% of %sMB"%(
                    read * 100.0 / bytes,
                    bytes / 1000000),

    print("Extracting zip")
    with zipfile.ZipFile(args.file) as zf:
        zf.extractall()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download RxNorm Release')

    parser.add_argument('--username',  help='UMLS username', required=True)
    parser.add_argument('--password',  help='UMLS password', required=True)
    parser.add_argument(
            "--release",
            help="specify release version (e.g. '10052015'). Default: latest.",
            default=None)
    parser.add_argument(
            '--file',
            help='Where to save .zip download. Default: "rxnorm-download.zip"',
            default="rxnorm-download.zip")

    args = parser.parse_args()
    download_rxnorm(args)
