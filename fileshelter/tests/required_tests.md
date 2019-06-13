
# Required tests

## file access

### init

* creates root dir if doesn't exist
* unfolds relative path into absolute path (can't test in current configuration)

### abspath checked

* makes path that is relative to `root_dir` absolute
* raises if path isn't in the `root_dir`

### join to workdir

* joins the given path to the given workdir
* if path starts with "/" ignores workdir and returns the given path (withot the slash)

### list directory

* returns list of dictionaries, each represent a file in the given directory
* dict fields:
 * name - file name
 * directory - true if entry is directory, false otherwise
* raises if directory is outside of the root dir

### save file

* accepts a FileStorage object (won't test for it for now, only mocks)
* saves filestorage content to the given directory under the name that is specified in the storage
* raises if resulting filename is inaccessible, i.e. is outside of the root dir

### get file

* returns the absolute path to the given file path
* raises if the file is outside of the root dir

### move file

* accepts two paths, each is relative either to workdir or to the root dir
* moves the file and returns the path to the directory of the moved file relative to the root path
* raises if trying to move a directory
* raises if either path is outside of the root path

### make directory

* creates directories in the given workdir
* can create multiple directories if they are nested
* raises if the resulting directory is outside of the root dir

## flask app

### root view

* redirects to the files list view (root path)

### files list view

* can be accessed through `/files`, `/files/` or `/files/<dir>`
* shows the list of files in the given directory (workdir)
* `/files` and `/files/` show the root dir

# Testing hints or ideas

To test that file list view only shows filenames of the given directory we can create some unique files in every directory and check that each filename of the testing directory is a substring of the rendered html code and all the other filenames aren't

To test file api we can create and prepare a temporary directory for every test. This will allow running tests imdependently