import os

class FileAccessError(Exception):
    pass

class FileAccess:
    def __init__(self, root_directory):
        self.root_dir = os.path.abspath(root_directory)
        if not os.path.isdir(self.root_dir):
            os.makedirs(files_dir)

    def _check_path(self, path):
        abs_norm_path = os.path.normpath(os.path.join(self.root_dir, path))
        if not abs_norm_path.startswith(self.root_dir):
            raise FileAccessError(path)
        return abs_norm_path

    def _abspath(self, path):
        return self._check_path(path)

    def list_directory(self, directory):
        absdirectory = self._abspath(directory)
        return [
            {
                "name": name,
                "directory": os.path.isdir(os.path.join(absdirectory, name))
            }
            for name in os.listdir(absdirectory)
        ]

    def save_file(self, directory, filestorage):
        save_to = self._abspath(os.path.join(directory, filestorage.filename))
        filestorage.save(save_to)

    def get_file(self, filepath):
        return self._abspath(filepath)

    def move_file(self, from_path, to_path):
        os.rename(self._abspath(from_path), self._abspath(to_path))

    def make_dir(self, directory):
        os.makedirs(self._abspath(directory))
