# jshint-external TextMate Bundle

Integrates the [JSHint](http://www.jshint.com/) JavaScript validator with [TextMate 2](https://github.com/textmate/textmate).

![Screenshot 1](https://raw.github.com/natesilva/jshint-external.tmbundle/master/no-errors.png)

## Features

* Validate automatically when you save your file, and on-demand.
* Intelligently uses `.jshintrc` settings, whether stored in the same directory tree as your source file, in your home directory, or referenced from a `package.json` file.
* Uses a separately-installed copy of `jshint`.
    * Does not include a bundled (possibly outdated) copy of JSHint.
    * Fewer dependency problems.
* Common error codes include a link to the relevant explanation on [jslinterrors.com](http://jslinterrors.com/).

![Screenshot 2](https://raw.github.com/natesilva/jshint-external.tmbundle/master/with-errors.png)

## Install

First install JSHint:

1. Install [Node.js](http://nodejs.org/).
2. `[sudo] npm install -g jshint`

Now install the bundle:

1. [Download the latest release .zip file](https://github.com/natesilva/jshint-external.tmbundle/releases/latest).
2. Extract it.
3. Rename the extracted folder to `jshint-external.tmbundle`.
4. Double-click to install it in TextMate.

## Release Notes

Release notes are found in the [Releases](https://github.com/natesilva/jshint-external.tmbundle/releases) section of this GitHub repo.

## Configuration

In most cases no configuration is required. However, in some cases you may want to customize the following:

* **Use `jshint` that is not on your `PATH`:** If `jshint` is not on your `PATH`, set the `TM_JSHINT` variable to point to it. Set in *TextMate* > *Preferences…* > *Variables*.
* **Don’t validate on save:** If you don’t want to validate your JavaScript automatically when you press `⌘S`:
    1. Open the Bundle Editor (*Bundles* > *Edit Bundles…*).
    2. Navigate to *JSHint (External)* > *Menu Actions* > *Save & Validate with JSHint*.
    3. In the drawer that appears, delete the “Key Equivalent” of `⌘S`.
* **Use a project-specific JSHint configuration:**
    * **For Node.js:** Add a key called `jsonHintConfig` to the `package.json` file. This key should contain the filename of your JSHint configuration file ([JSHint config syntax](http://www.jshint.com/docs/)).
    * **For any JavaScript project:** Create a `.jshintrc` file ([syntax](http://www.jshint.com/docs/)). Place it in your source directory or any directory above it.

## Uninstall

1. Quit TextMate.
2. Open `~/Library/Application Support/Avian/Pristine Copy/Bundles`.
3. Trash `jshint-external.tmbundle`.
4. Open `~/Library/Application Support/Avian/Bundles`.
5. If there is a file called `JavaScript JSHint (External).tmbundle`, trash it.
6. You may need to clear TextMate’s cache by trashing `~/Library/Caches/com.macromates.TextMate.preview`.
