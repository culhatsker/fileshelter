from os.path import join, abspath, isdir
from pytest import fixture, mark, raises

from ..file_access import FileAccess, FileAccessError


@fixture
def filestorage_mock(mocker):
    def make_mock(filename, filecontent):
        mock = mocker.Mock()
        mock.filename = filename
        mock.save = lambda path: open(path, "w").write(filecontent)
        return mock
    return make_mock

@fixture
def file_api(test_dir, filestorage_mock):
    fa = FileAccess(test_dir)
    fa.make_dir("subdir/sub2dir")
    fa.make_dir("subdir/sub2dir2")
    fa.make_dir("subdir2")
    fa.save_file("", filestorage_mock("alpha.txt", "alpha_content"))
    fa.save_file("", filestorage_mock("beta.txt", "beta_content"))
    fa.save_file("", filestorage_mock("gamma.txt", "gamma_content"))
    fa.save_file("subdir", filestorage_mock("file1.txt", "file1_content"))
    fa.save_file("subdir", filestorage_mock("file2.txt", "file2_content"))
    fa.save_file("subdir/sub2dir", filestorage_mock("file3.txt", "file3_content"))
    return fa


# TESTS


def test_fa_init_creates_dir(test_dir):
    root_path = join(test_dir, "subdir")
    fa = FileAccess(root_path)
    assert fa.root_dir == root_path
    assert isdir(root_path)


@mark.parametrize("path,expected", [
    ("", ""),
    ("blabla", "/blabla"),
    ("a/b/c/../../d/e", "/a/d/e"),
    ("a/b/././c", "/a/b/c"),
])
def test_fa_abspath_checked(test_dir, path, expected):
    fa = FileAccess(test_dir)
    assert fa._abspath_checked(path) == (test_dir + expected)


def test_fa_abspath_checked_raises(test_dir):
    fa = FileAccess(test_dir)
    with raises(FileAccessError):
        fa._abspath_checked("..")


@mark.parametrize("workdir,path,expected", [
    ("", "", ""),
    ("a", "b", "a/b"),
    ("a", "/b", "b")
])
def test_fa_join_to_workdir(test_dir, workdir, path, expected):
    fa = FileAccess(test_dir)
    assert fa._join_to_workdir(workdir, path) == expected


@mark.parametrize("path,expected", [
    (
        "",
        [
            {"name": "subdir", "directory": True},
            {"name": "subdir2", "directory": True},
            {"name": "alpha.txt", "directory": False},
            {"name": "beta.txt", "directory": False},
            {"name": "gamma.txt", "directory": False}
        ]
    ), (
        "subdir",
        [
            {"name": "sub2dir", "directory": True},
            {"name": "sub2dir2", "directory": True},
            {"name": "file1.txt", "directory": False},
            {"name": "file2.txt", "directory": False}
        ]
    ), (
        "subdir/sub2dir",
        [{"name": "file3.txt", "directory": False}]
    ), (
        "subdir/sub2dir2",
        []
    ), (
        "subdir2",
        []
    ),
])
def test_fa_list_directory(file_api: FileAccess, path, expected):
    def make_set(list_of_dicts):
        return set([
            tuple([
                (key, dict_item[key])
                for key in sorted(dict_item.keys())
            ])
            for dict_item in list_of_dicts
        ])

    assert make_set(file_api.list_directory(path)) == make_set(expected)

def test_fa_list_directory_raises(test_dir):
    fa = FileAccess(test_dir)
    with raises(FileAccessError):
        fa.list_directory("..")


def test_fa_save_file(test_dir, filestorage_mock):
    fa = FileAccess(test_dir)
    assert fa.list_directory("") == []
    fa.save_file("", filestorage_mock("file1.txt", "file1_content"))
    fa.make_dir("subdir")
    fa.save_file("subdir", filestorage_mock("file2.txt", "file2_content"))
    assert open(fa._abspath_checked("file1.txt")).read() == "file1_content"
    assert open(fa._abspath_checked("subdir/file2.txt")).read() == "file2_content"


def test_fa_save_file_raises(test_dir, filestorage_mock):
    fa = FileAccess(test_dir)
    with raises(FileAccessError):
        fa.save_file("..", filestorage_mock("file1.txt", "file1_content"))


@mark.parametrize("path,content", [
    ("alpha.txt", "alpha_content"),
    ("beta.txt", "beta_content"),
    ("gamma.txt", "gamma_content"),
    ("subdir/file1.txt", "file1_content"),
    ("subdir/file2.txt", "file2_content"),
    ("subdir/sub2dir/file3.txt", "file3_content")
])
def test_fa_get_file(file_api: FileAccess, path, content):
    assert open(file_api.get_file(path)).read() == content


def test_fa_get_file_raises(test_dir):
    fa = FileAccess(test_dir)
    with raises(FileAccessError):
        fa.get_file("../file1.txt")


@mark.parametrize("frompath,topath,workdir,expectdir,expectname", [
    ("alpha.txt", "subdir", "", "subdir", "alpha.txt"),
    ("alpha.txt", "alpha_new.txt", "", "", "alpha_new.txt"),
    ("../alpha.txt", "", "subdir", "subdir", "alpha.txt"),
])
def test_fa_move_file_simple_case(file_api: FileAccess, frompath, topath, workdir, expectdir, expectname):
    file_api.move_file(frompath, topath, workdir)
    assert {"name": expectname, "directory": False} in file_api.list_directory(expectdir)


@mark.parametrize("frompath,topath", [
    ("../file1.txt", ""),
    ("file1.txt", ".."),
    ("subdir", "")
])
def test_fa_move_file_raises(file_api, frompath, topath):
    with raises(FileAccessError):
        file_api.move_file(frompath, topath, "")
