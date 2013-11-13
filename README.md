# jshint-external TextMate Bundle

Integrates the [JSHint](http://www.jshint.com/) JavaScript validator with [TextMate 2](https://github.com/textmate/textmate).

![Screenshot](https://raw.github.com/natesilva/jshint-external.tmbundle/master/jshint-external-looks-good.png)

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

Next, install the bundle:

1. [Download the .zip file](https://github.com/natesilva/jshint-external.tmbundle/archive/master.zip).
2. Extract it.
3. Rename the extracted folder to `jshint-external.tmbundle`.
4. Double-click to install it in TextMate.

## Configuration

In most cases no configuration is required. However, in some cases you may wish to customize the following:

* **Use `jshint` that is not on your `PATH`:** If `jshint` is not on your `PATH`, set the `TM_JSHINT` variable to point to it. Set in *TextMate* > *Preferences…* > *Variables*.
* **Don’t validate on save:** If you don’t want to validate your JavaScript automatically whenever you press <kbd>⌘S</kbd>:
     1. Open the Bundle Editor (*Bundles* > *Edit Bundles…*).
     2. Navigate to *JSHint (External)* > *Menu Actions* > *Save & Validate with JSHint*.
     3. In the drawer that appears delete they “Key Equivalent” of <kbd>⌘S</kbd>.
 * **Use a project-specific JSHint configuration:**
     * In a Node.js project, add a key called `jsonHintConfig` to the `package.json` file. This key should contain the filename of your JSHint configuration file ([same syntax as `.jshintrc`](http://www.jshint.com/docs/)).
     * If you are not using Node.js, this still works. Create a file called `package.json` in your source directory or any directory above it. In this file, add a key called `jsonHintConfig` which contains the filename of your JSHint configuration file.
