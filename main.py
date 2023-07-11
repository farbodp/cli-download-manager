import time
from tqdm import tqdm
import argparse
import requests
from threading import Thread


class URLDownloader:
    def __init__(self, destination):
        self.urls = []
        self.threads = []
        self.destination = destination

    def add_url(self, url):
        self.urls.append(url)

    def _download_url(self, url, save_path):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(save_path, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    progress_bar.update(len(data))

    def start(self):
        """
        Start the scheduler and run the jobs.
        """
        for url in self.urls:
            filename = url.split('/')[-1]
            file_path = f"{self.destination}/{filename}"
            thread = Thread(target=self._download_url, args=(url, file_path))
            self.threads.append(thread)
            thread.start()

    def stop(self):
        for thread in self.threads:
            thread.join()





def main():
    parser = argparse.ArgumentParser(description='Download multiple URLs')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='URLs to download')
    parser.add_argument('-d', '--destination', metavar='PATH', type=str,
                        help='Destination path to save the files')
    args = parser.parse_args()

    destination = args.destination or './'
    url_downloader = URLDownloader(destination=destination)

    for url in args.urls:
        url_downloader.add_url(url)

    url_downloader.start()
    url_downloader.stop()

if __name__ == "__main__":
    main()