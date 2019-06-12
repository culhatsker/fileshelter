import os

class FileAccessError(Exception):
    pass

class FileAccess:
    def __init__(self, root_directory):
        self.root_dir = os.path.abspath(root_directory)
        if not os.path.isdir(self.root_dir):
            os.makedirs(self.root_dir)

    def _abspath_checked(self, path):
        abs_norm_path = os.path.normpath(os.path.join(self.root_dir, path))
        if not abs_norm_path.startswith(self.root_dir):
            raise FileAccessError(path)
        return abs_norm_path

    @staticmethod
    def _join_to_workdir(workdir, path):
        new_path = os.path.join(workdir, path)
        if path.startswith("/"):
            return new_path[1:]
        return new_path

    def list_directory(self, directory):
        absdirectory = self._abspath_checked(directory)
        return [
            {
                "name": name,
                "directory": os.path.isdir(os.path.join(absdirectory, name))
            }
            for name in os.listdir(absdirectory)
        ]

    def save_file(self, directory, filestorage):
        save_to = self._abspath_checked(os.path.join(directory, filestorage.filename))
        filestorage.save(save_to)

    def get_file(self, filepath):
        return self._abspath_checked(filepath)

    def move_file(self, from_path, to_path, workdir="/"):
        to_path = self._join_to_workdir(workdir, to_path)
        from_path = self._join_to_workdir(workdir, from_path)
        if os.path.isdir(self._abspath_checked(from_path)):
            raise FileAccessError("Can't move directory (for now)")
        if os.path.isdir(self._abspath_checked(to_path)):
            to_path = os.path.join(to_path, os.path.basename(from_path))
        os.rename(
            self._abspath_checked(from_path),
            self._abspath_checked(to_path)
        )
        return os.path.dirname(to_path)

    def make_dir(self, directory, workdir="/"):
        directory = self._join_to_workdir(workdir, directory)
        os.makedirs(self._abspath_checked(directory))
        return directory

