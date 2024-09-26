import tarfile
import configparser
import time

class ShellEmulator:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.hostname = self.config['hostname']
        self.virtual_files = self.load_tar(self.config['tar_file'])
        self.log_file = self.config['log_file']
        self.start_script = self.config['start_script']
        self.current_dir = "/"
        self.log = []
        self.start_time = time.time()

    def load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        return {
            'hostname': config['settings']['hostname'],
            'tar_file': config['settings']['tar_file'],
            'log_file': config['settings']['log_file'],
            'start_script': config['settings']['start_script']
        }

    def load_tar(self, tar_path):
        tar = tarfile.open(tar_path, "r")
        return {member.name[13:]: member for member in tar.getmembers()}

if __name__ == "__main__":
    emulator = ShellEmulator("config.ini")
    print(emulator.hostname)
    print(emulator.virtual_files)
    print(emulator.log_file)
    print(emulator.start_script)