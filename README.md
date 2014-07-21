# jshint-external TextMate Bundle

The best way to run the [JSHint](http://www.jshint.com/) JavaScript validator in [TextMate 2](https://github.com/textmate/textmate).

<small>Want to use ESLint instead? Try the [javascript-eslint.tmbundle](https://github.com/natesilva/javascript-eslint.tmbundle).</small>

<img src="http://natesilva.github.io/jshint-external.tmbundle/images/no-errors-1.1.1.png" style="width:560px;" width="560" alt="Screenshot 1">

## Features

* Validate automatically when you save your file, and on-demand.
* Intelligently uses `.jshintrc` settings, whether stored in the same directory tree as your source file, in your home directory, or referenced from a `package.json` file.
* Uses a separately-installed copy of `jshint`.
    * Does not include a bundled (possibly outdated) copy of JSHint.
    * Fewer dependency problems.
* Common error codes include a link to the relevant explanation on [jslinterrors.com](http://jslinterrors.com/).

<img src="http://natesilva.github.io/jshint-external.tmbundle/images/with-errors-1.1.1.png" style="width:560px;" width="560" alt="Screenshot 2">

## Install

If you don’t have JSHint, install it:

1. Install [Node.js](http://nodejs.org/).
2. `[sudo] npm install -g jshint`

Now install the bundle:

1. [Download the latest release .zip file](https://github.com/natesilva/jshint-external.tmbundle/releases/latest).
2. Extract it and double-click to install.

## Release Notes

View the [release notes](https://github.com/natesilva/jshint-external.tmbundle/releases).

## Configuration

In most cases no configuration is required. However, in some cases you may want to customize the following:

* **Use `jshint` that is not on your `PATH`:** If `jshint` is not on your `PATH`, set the `TM_JSHINT_EXTERNAL_JSHINT` variable to point to it. Set in *TextMate* > *Preferences…* > *Variables*.
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
