import os
import shutil
from torrentp import TorrentDownloader

from torrent.models import DownloadedFile


async def download_file_magnet(magnet_link: str, download_id: str) -> DownloadedFile:
    source_path = os.path.join(os.getcwd(), f'torrent/files/{download_id}/source')
    zip_path = os.path.join(os.getcwd(), f'torrent/files/{download_id}/')
    delete_path = os.path.join(os.getcwd(), f'torrent/files/{download_id}')

    torrent_file = TorrentDownloader(magnet_link, source_path)
    await torrent_file.start_download()

    downloaded_files = os.listdir(source_path)
    file_name = downloaded_files[0] if len(downloaded_files) == 1 else 'yourfile'
    zip_path = os.path.join(zip_path, file_name)
    shutil.make_archive(zip_path, 'zip', source_path)

    zip_file = DownloadedFile(
        file_name=f'{file_name}.zip',
        file_path=f'{zip_path}.zip',
        delete_path=delete_path
        )
    return zip_file


if __name__ == '__main__':
    delete_path = os.path.join(os.getcwd(), f'/torrent/files/507541585_354')
    print(delete_path)
    shutil.rmtree(delete_path)