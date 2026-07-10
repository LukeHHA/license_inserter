import os
import sys
import pathlib
import argparse


def create_license(filename, name, project):
    name_offset = 58 - len(name)
    filename_offset = 72 - len(filename)
    project_offset = 45 - len(project)

    for _ in range(name_offset - 2):
        name += " "
    name += "*/"

    for _ in range(filename_offset - 2):
        filename += " "
    filename += "*/"

    for _ in range(project_offset - 2):
        project += " "
    project += "*/"

    license = f""" 
/**************************************************************************/
/*  {filename}                                                            
/**************************************************************************/
/*                         This file is part of:                          */
/*                             {project}                                  
/**************************************************************************/
/* Copyright (c)  {name}                                                  
/*                                                                        */
/* Permission is hereby granted, free of charge, to any person obtaining  */
/* a copy of this software and associated documentation files (the        */
/* "Software"), to deal in the Software without restriction, including    */
/* without limitation the rights to use, copy, modify, merge, publish,    */
/* distribute, sublicense, and/or sell copies of the Software, and to     */
/* permit persons to whom the Software is furnished to do so, subject to  */
/* the following conditions:                                              */
/*                                                                        */
/* The above copyright notice and this permission notice shall be         */
/* included in all copies or substantial portions of the Software.        */
/*                                                                        */
/* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,        */
/* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF     */
/* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. */
/* IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY   */
/* CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,   */
/* TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE      */
/* SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                 */
/**************************************************************************/

"""
    return license


def prepend_license(rootdir, name, project, exclude_dirs, include_file_type):
    exclude = set(exclude_dirs)
    for folder, subdirs, files in os.walk(rootdir, topdown=True):
        subdirs[:] = [
            d for d in subdirs if pathlib.Path(folder, d).resolve() not in exclude
        ]
        print(subdirs)

        for file in files:
            if file == __file__:
                continue
            if pathlib.Path(file).suffix not in include_file_type:
                continue

            path = os.path.join(folder, file)
            contents = []

            try:
                with open(os.path.join(folder, file), "r") as f:
                    contents = f.readlines()
                    contents.insert(0, create_license(file, name, project))

                with open(path, "w") as f:
                    f.writelines(contents)

            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(e)


def main():
    parser = argparse.ArgumentParser(
        prog="license-inserter.py",
        description="CLI tool to insert MIT license into files of a project directory",
    )

    parser.add_argument("path", help="Path pointing at project to scan")

    parser.add_argument("name", help="Full name of the license holder")

    parser.add_argument("project", help="Full name of the project")

    parser.add_argument(
        "-f",
        "--include-file-type",
        action="append",
        default=[],
        help="Specify which file extensions a license should be inserted into",
    )

    parser.add_argument(
        "-e",
        "--exclude-dirs",
        action="append",
        default=[],
        help="Directories to exclude",
    )

    args = parser.parse_args()

    proceed = input("Ensure you have a BACKUP! Do you wish to proceed (Y/n): ")

    if proceed.lower() == "n":
        print("exiting")
        sys.exit()

    elif proceed.lower() != "y":
        print("exiting")
        sys.exit()

    for i in range(len(args.exclude_dirs)):
        args.exclude_dirs[i] = pathlib.Path(args.exclude_dirs[i]).resolve()

    prepend_license(
        args.path, args.name, args.project, args.exclude_dirs, args.include_file_type
    )


if __name__ == "__main__":
    raise SystemExit(main())
