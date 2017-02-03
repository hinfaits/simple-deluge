import os, sys

try:
    sys.path.index(sys.path.append(os.path.join(os.path.dirname(__file__), "pip")))
except ValueError:
    sys.path.append(sys.path.append(os.path.join(os.path.dirname(__file__), "pip")))

from deluge_client import DelugeRPCClient

class DelugeClient():
    def __init__(self):
        import config
        self.client = DelugeRPCClient(
            host=config.DELUGE['host'],
            port=config.DELUGE['port'],
            username=config.DELUGE['uname'],
            password=config.DELUGE['pword']
        )
        self.client.connect()
        self.torrent_status_data = None

    def connected(self):
        return self.client.connected

    def all_torrent_id(self):
        return self.client.call('core.get_session_state')

    def torrent_status(self, torrent_id):
        return self.client.call('core.get_torrent_status', torrent_id, [])

    def all_torrent_status(self, refresh=False):
        if refresh or self.torrent_status_data is None:
            self.torrent_status_data = [self.torrent_status(t_id) for t_id in self.all_torrent_id()]
        return self.torrent_status_data

    def torrent_exists(self, torrent_name):
        res = self.all_torrent_status()
        for torrent in res:
            if torrent[b'name'].decode('ascii') == torrent_name:
                return torrent
        return None

    def recheck_torrent(self, torrent_id):
        return self.client.call('core.force_recheck', [torrent_id])

    def resume_torrent(self, torrent_id):
        return self.client.call('core.resume_torrent', [torrent_id])
    
    def remove_torrent(self, torrent_id, remove_data=False):
        return self.client.call('core.remove_torrent', torrent_id, remove_data)

    def set_do_not_download(self, torrent_id):
        res = self.torrent_status(torrent_id)
        if res:
            new_file_priorities = [0 for _ in res[b'file_priorities']]
            self.client.call('core.set_torrent_file_priorities', torrent_id, new_file_priorities)
        else:
            return None
