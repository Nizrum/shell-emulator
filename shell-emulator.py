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

    def execute_command(self, command):
        if command.startswith("cd"):
            self.change_directory(command.split(" ")[1])
        elif command == "ls":
            self.list_directory()
        elif command == "exit":
            self.exit_shell()
        elif command.startswith("find"):
            self.find_file(command.split(" ")[1])
        else:
            print(f"{command}: command not found")

    def change_directory(self, path):
        if path == "/":
            self.current_dir = "/"
        elif path == "..":
            self.current_dir = '/'.join(self.current_dir.split('/')[:-2]) + '/'
        elif (self.current_dir + path) in self.virtual_files:
            self.current_dir = self.current_dir + path + "/"
        else:
            print(f"cd: {path}: No such file or directory")

    def list_directory(self):
        dir_content = filter(lambda name: len(name.split('/')) == 1, [name[len(self.current_dir):] for name in self.virtual_files if name.startswith(self.current_dir)])
        print("\n".join(dir_content))

    def find_file(self, filename):
        found_files = [name[len(self.current_dir):] for name in self.virtual_files if name.startswith(self.current_dir) and (name.find(filename) >= len(self.current_dir))]
        print("\n".join(found_files) if len(found_files) != 0 else f"find: '{filename}': No such file or directory")

    def exit_shell(self):
        print("Exiting shell...")
        exit()

    def run(self):
        while True:
            command = input(f"{self.hostname}:{self.current_dir}$ ")
            self.execute_command(command)

if __name__ == "__main__":
    emulator = ShellEmulator("config.ini")
    emulator.run()