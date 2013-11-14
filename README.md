# jshint-external TextMate Bundle

Integrates the [JSHint](http://www.jshint.com/) JavaScript validator with [TextMate 2](https://github.com/textmate/textmate).

![Screenshot](https://raw.github.com/natesilva/jshint-external.tmbundle/master/screenshot.png)

## Features

* Validate automatically when you save your file, and on-demand.
* Intelligently uses `.jshintrc` settings, whether stored in the same directory tree as your source file, in your home directory, or referenced from a `package.json` file.
* Uses a *separately-installed* copy of `jshint`.
    * Does not include a bundled (possibly outdated) copy of JSHint.
    * Fewer dependency problems.

## Install

First, install JSHint if you have not done so already:

1. Install [Node.js](https://nodejs.org/).
2. `[sudo] npm install -g jshint`

Now install the bundle:

1. [Download the latest release .zip file](https://github.com/natesilva/jshint-external.tmbundle/releases/latest).
2. Extract it.
3. Rename the extracted folder to `jshint-external.tmbundle`.
4. Double-click to install it in TextMate.

## Configuration

In most cases no configuration is required. However, in some cases you may wish to customize the following:

* **Use `jshint` that is not on your `PATH`:** If `jshint` is not on your `PATH`, set the `TM_JSHINT` variable to point to it. Set in *TextMate* > *Preferences…* > *Variables*.
* **Don’t validate on save:** If you don’t want to validate your JavaScript automatically whenever you press `⌘S`:
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
5. If there is a file called `JSHint (External).tmbundle`, trash it.
6. You may need to clear TextMate’s cache by trashing `~/Library/Caches/com.macromates.TextMate.preview`.
