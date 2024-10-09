import unittest
from datetime import datetime
from shell_emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.emulator = ShellEmulator('config.ini')

    def test_cd(self):
        self.emulator.change_directory('invalid-dir')
        self.assertNotEqual(self.emulator.current_dir, '/invalid-dir/')
        
        self.emulator.change_directory('example-folder-1')
        self.assertEqual(self.emulator.current_dir, '/example-folder-1/')

        self.emulator.change_directory('example-folder-2')
        self.assertEqual(self.emulator.current_dir, '/example-folder-1/example-folder-2/')

        self.emulator.change_directory('/')
        self.assertEqual(self.emulator.current_dir, '/')

    def test_ls(self):
        result = self.emulator.list_directory('')
        self.assertEqual(['example1.txt', 'example2.txt', 'example-folder-1'], result)

        result = self.emulator.list_directory('example-folder-1')
        self.assertEqual(['example3.txt', 'example-folder-2'], result)

        result = self.emulator.list_directory('example-folder-3')
        self.assertEqual([], result)

    def test_find(self):
        self.emulator.change_directory('/')

        result = self.emulator.find_file('example1.txt')
        self.assertEqual(['example1.txt'], result)

        result = self.emulator.find_file('example-folder-1')
        self.assertEqual(['example-folder-1', 'example-folder-1/example3.txt', 'example-folder-1/example-folder-2', 'example-folder-1/example-folder-2/example4.txt'], result)

        self.emulator.change_directory('/example-folder-1')

        result = self.emulator.find_file('example4.txt')
        self.assertEqual(['example-folder-1/example-folder-2/example4.txt'], result)

    def test_uptime(self):
        now = datetime.now()
        uptime = now - self.emulator.start_time
        self.assertEqual(f"{now.strftime('%H:%M:%S')} up {round(uptime.total_seconds() / 60)} min,  1 user", self.emulator.show_uptime())

if __name__ == "__main__":
    unittest.main()