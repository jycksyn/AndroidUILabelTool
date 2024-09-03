# Android UI Dump Labeling Tool

## How to run:
#### Arguments:
* `--input_dir`: The directory where the XML dumps and unannotated PNG files are stored. Defaults to the current working directory.
* `--output_dir`: The directory where the annotated PNG files will placed. Defaults to the input directory.
* `--overwrite`: Add this flag if the program should overwrite existing files in the output directory. False by default.

#### Run Source Code:
1. Clone this repository and ensure that [Poetry](https://python-poetry.org/) and `pip` are installed on your system.
2. `cd` into the `android_ui_label_tool` directory
3. Execute the program with `poetry run python android_ui_label_tool/__main__.py` followed by your arguments

#### Install From Wheel:
1. Clone this repository and ensure that `pip` is installed on your system.
3. Run the command `pip install android_ui_label_tool/dist/android_ui_label_tool-0.1.0-py3-none-any.whl` to install the utility and its dependencies.
4. Execute the program with `python -m android_ui_label_tool` followed by your arguments

## Design

The sample source data is contained in the `Programming-Assignment-Data` folder. The annotated screenshots are contained in its subfolder `output`. All libraries are included in the `pyproject.toml` file created by Poetry.

The solution allows a user to point to an input directory of screenshots and corresponding UI dumps. The program then annotates each screenshot with the bounds of the most nested UI elements, or leaf XML nodes. The user can point to a specific directory where the annotated screenshots are deposited and can specify whether or not existing files should be overwritten.

The logic for the solution is grouped together into functions which each has responsibility for working with a specific library or module to accomplish a particular subtask.

Error handling is done in a way that removes the stack trace and returns a clean error to the user that they can quickly address and points to the specific XML dump related to the error. The logic for drawing UI bounds is extracted into its own class to encapsulate the logic of working with bounds, parsing the regex, and drawing rectangles on the screenshots.