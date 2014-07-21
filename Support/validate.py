#!/usr/bin/env python
# encoding: utf-8

"""
Validate a JavaScript file using jshint. Uses an EXTERNAL,
user-installed copy of jshint, rather than an embedded copy.

Author: Nate Silva
Copyright 2013, 2014 Nate Silva
License: MIT
"""

from __future__ import print_function
import sys
import os
import re
import time
import json
import subprocess
import tempfile
import hashlib
from minify_json import json_minify


def find_up_the_tree(dir_name, filename, max_depth=30):
    """
    Search for the named file in the dir_name or any of its parent
    directories, up to the root directory.
    """

    while True:
        if max_depth <= 0:
            return None

        full_path = os.path.abspath(os.path.join(dir_name, filename))
        if os.path.isfile(full_path):
            return full_path

        (drive, path) = os.path.splitdrive(dir_name)
        is_root = (path == os.sep or path == os.altsep)
        if is_root:
            return None

        max_depth -= 1
        dir_name = os.path.abspath(os.path.join(dir_name, os.pardir))


def find_jshintrc(start_dir):
    """
    Locates the most relevant .jshintrc file. Of the following
    locations, the first to be found will be used:

        1. The file referenced by a jsonHintConfig value in a
           package.json file. The package.json file is found in the
           start_dir or any of its parents.
        2. A .jshintrc file in the start_dir or any of its parents.
        3. ~/.jshintrc

    start_dir is normally set to the directory of the file being
    validated.

    When start_dir is not provided (which happens with files that
    are not saved yet), the first two locations will not be
    available, so ~/.jshintrc is the only candidate that is
    considered.

    If no relevant .jshintrc is found, the return value is None.
    """

    if start_dir:
        # locate the nearest package.json
        pj = find_up_the_tree(start_dir, 'package.json')
        if pj:
            # does it have a jsonHintConfig setting?
            try:
                pkg = json.loads(json_minify(open(pj, 'r').read()))
                if 'jsonHintConfig' in pkg:
                    # does it point to a file that exists?
                    pj_dir = os.path.dirname(pj)
                    full_path = os.path.join(pj_dir, pkg['jsonHintConfig'])
                    full_path = os.path.abspath(full_path)
                    if os.path.isfile(full_path):
                        # success
                        return full_path
            except ValueError:
                # package.json file is invalid JSON! Skip it.
                pass

        # locate the nearest .jshintrc
        jshrc = find_up_the_tree(start_dir, '.jshintrc')
        if jshrc:
            return jshrc

    # last ditch: look for .jshintrc in the user’s home directory
    home_jshrc = os.path.expanduser('~/.jshintrc')
    if os.path.isfile(home_jshrc):
        return home_jshrc

    return None


def show_error_message(message):
    context = {
        'message': message,
        'timestamp': time.strftime('%c')
    }

    my_dir = os.path.abspath(os.path.dirname(__file__))

    error_ejs_path = os.path.join(my_dir, 'error.ejs')
    error_ejs = open(error_ejs_path, 'r').read()

    template_path = os.path.join(my_dir, 'template.html')
    template = open(template_path, 'r').read()
    template = template.replace('{{ TM_BUNDLE_SUPPORT }}',
        os.environ['TM_BUNDLE_SUPPORT'])
    template = template.replace('{{ EJS_TEMPLATE }}', json.dumps(error_ejs))
    template = template.replace('{{ CONTEXT }}', json.dumps(context))

    print(template)


def get_marker_directory():
    """
    Create the directory that will hold "marker" files that we use
    to detect which files have a validation window open. Used to
    implement the following feature:

    Normally, when you hit Cmd-S, the validation window appears
    only if there is a warning or error.

    Assume you had previously validated a file, and the validation
    window showing its errors is still open. Now you fix the
    errors and press Cmd-S. We want that validation window to
    update to show no errors.

    In order to do this, we have to somehow detect if TextMate has
    a validation window open for the current file. It’s not easy.
    We use marker files.

    This script creates a marker file before returning the HTML
    document that will be shown in the validation window.

    When the HTML document detects that it is being hidden (closed),
    it runs a TextMate.system command to delete its marker file.
    """
    baseDir = os.path.join(tempfile.gettempdir(), 'jshint-external-tmbundle')
    if not os.path.isdir(baseDir):
        os.makedirs(baseDir)

    today = time.strftime('%Y-%m-%d')
    markerDir = os.path.join(baseDir, today)
    if not os.path.isdir(markerDir):
        os.makedirs(markerDir)

    # Deletion should happen automatically, but to be clean(er),
    # delete any previous-day marker dirs.
    children = os.listdir(baseDir)
    children = [_ for _ in children if _ != today]
    children = [os.path.join(baseDir, _) for _ in children]
    children = [_ for _ in children if os.path.isdir(_)]
    [shutil.rmtree(_, True) for _ in children]

    return markerDir


def validate(quiet=False):
    # locate the .jshintrc to use
    jshintrc = find_jshintrc(os.environ.get('TM_DIRECTORY', None))
    jshintrc_valid = False
    if jshintrc:
        try:
            json.loads(json_minify(open(jshintrc, 'r').read()))
            jshintrc_valid = True
        except ValueError:
            jshintrc_valid = False

    # path to our custom jshint reporter
    reporter_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        'reporter.js')

    # build jshint args
    args = [
        os.environ.get('TM_JSHINT_EXTERNAL_JSHINT', 'jshint'),
        '--reporter="' + reporter_path + '"'
    ]

    if jshintrc and jshintrc_valid:
        args.append('--config="%s"' % jshintrc)
    args.append('-')

    # Build env for our command: JSHint (and Node) are often
    # installed to /usr/local/bin, which may not be on the
    # bundle’s PATH in a default install of TextMate.
    env = os.environ.copy()
    path_parts = env['PATH'].split(':')
    if '/bin' not in path_parts:
        path_parts.append('/bin')
    if '/usr/bin' not in path_parts:
        path_parts.append('/usr/bin')
    if '/usr/local/bin' not in path_parts:
        path_parts.append('/usr/local/bin')
    env['PATH'] = ':'.join(path_parts)

    try:
        jshint = subprocess.Popen(args, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, env=env)
    except OSError as e:
        msg = [
            'Hi there. This is the “JavaScript JSHint (External)” bundle for ' +
                'TextMate. I validate your code using JSHint.',
            '',
            'I had the following problem running <code>jshint</code>:',
            '',
            '<code>%s</code>' % e,
            '',
            '<h4>How to fix it</h4>',
            'Make sure the <code>jshint</code> and <code>node</code> ' +
                'commands are on the <code>PATH</code>.',
            '',
            '<ol>' +
                '<li>Go to <i>TextMate</i> > <i>Preferences…</i> > ' +
                    '<i>Variables</i></li>' +
                '<li>Ensure the <code>PATH</code> is enabled there and that ' +
                    'it includes the location of your <code>jshint</code> ' +
                    'and <code>node</code> commands.</li>'
            '</ol>',
            'The path currently used by TextMate bundles is:',
            '',
            '<div style="overflow:auto"><code>%s</code></div>' % env['PATH'],
            '<h4>How to disable validation</h4>',
            'If you mistakenly installed this validation tool and want to ' +
                'disable it, you can do so in TextMate:',
            '',
            '<ol>' +
                '<li>On the TextMate menu, choose ' +
                '<i>Bundles</i> > <i>Edit Bundles…</i></li>' +
                '<li>Locate “JavaScript JSHint (External)”</li>' +
                '<li>Uncheck “Enable this item”</li>' +
                '<li>Close the Bundle Editor and choose “Save”</li>' +
            '</ol>'
        ]
        show_error_message('<br>'.join(msg))
        sys.exit()

    # Pipe stdin to the subprocess; if we are validating an HTML
    # file with embedded JavaScript, only pipe content within the
    # <script>…</script> tags to the subprocess.
    if os.environ['TM_SCOPE'].startswith('source.js'):
        for line in sys.stdin:
            jshint.stdin.write(line)
    else:
        start_tag = re.compile('(\<\s*script)[\s\>]', re.IGNORECASE)
        end_tag = re.compile('\<\/\s*script[\s\>]', re.IGNORECASE)
        state = 'IGNORE'
        for line in sys.stdin:
            while line:
                if state == 'IGNORE':
                    match = start_tag.search(line)
                    if match:
                        # found a script tag
                        line = ' ' * match.end(1) + line[match.end(1):]
                        state = 'LOOK_FOR_END_OF_OPENING_TAG'
                    else:
                        jshint.stdin.write('\n')
                        line = None

                elif state == 'LOOK_FOR_END_OF_OPENING_TAG':
                    gt_pos = line.find('>')
                    if gt_pos != -1:
                        line = ' ' * (gt_pos + 1) + line[gt_pos + 1:]
                        state = 'PIPE_TO_OUTPUT'
                    else:
                        jshint.stdin.write('\n')
                        line = None

                elif state == 'PIPE_TO_OUTPUT':
                    match = end_tag.search(line)
                    if match:
                        # found closing </script> tag
                        jshint.stdin.write(line[:match.start()])
                        line = line[match.end():]
                        state = 'IGNORE'
                    else:
                        jshint.stdin.write(line)
                        line = None

    jshint.stdin.close()

    # parse the results
    try:
        issues = json.loads(json_minify(jshint.stdout.read()))
    except ValueError:
        print('could not parse data returned from jshint')
        sys.exit(1)

    # normalize line numbers
    input_start_line = int(os.environ['TM_INPUT_START_LINE']) - 1
    for issue in issues:
        issue['line'] += input_start_line

    # add URLs to the issues
    if 'TM_FILEPATH' in os.environ:
        url_maker = lambda x: \
            'txmt://open?url=file://%s&amp;line=%d&amp;column=%d' % \
            (os.environ['TM_FILEPATH'], x['line'], x['character'])
    else:
        url_maker = lambda x: \
            'txmt://open?line=%d&amp;column=%d' % (x['line'], x['character'])

    for issue in issues:
        issue['url'] = url_maker(issue)

    # context data we will send to JavaScript
    context = {
        'jshintrc': jshintrc,
        'jshintrcValid': jshintrc_valid,
        'issues': issues,
        'timestamp': time.strftime('%c')
    }

    if 'TM_FILEPATH' in os.environ:
        context['fileUrl'] = \
            'txmt://open?url=file://%s' % os.environ['TM_FILEPATH']
        context['targetFilename'] = os.path.basename(os.environ['TM_FILEPATH'])
    else:
        context['fileUrl'] = 'txmt://open?line=1&amp;column=0'
        context['targetFilename'] = '(current unsaved file)'

    # Identify the marker file that we will use to indicate the
    # TM_FILEPATH of the file currently shown in the validation
    # window.
    markerDir = get_marker_directory()
    hash = hashlib.sha224(context['fileUrl']).hexdigest()
    context['markerFile'] = os.path.join(markerDir, hash + '.marker')

    context['errorCount'] = \
        len([_ for _ in context['issues'] if _['code'][0] == 'E'])
    context['warningCount'] = \
        len([_ for _ in context['issues'] if _['code'][0] == 'W'])

    if context['errorCount'] == 0 and context['warningCount'] == 0:
        # There are no errors or warnings. We can bail out if all of
        # the following are True:
        #
        #     * There is no validation window currently open for
        #       this document.
        #     * quiet is True.
        if not os.path.exists(context['markerFile']):
            if quiet:
                return

    # create the marker file
    markerFile = open(context['markerFile'], 'w+')
    markerFile.close()

    # read and prepare the template
    my_dir = os.path.abspath(os.path.dirname(__file__))

    content_ejs_path = os.path.join(my_dir, 'content.ejs')
    content_ejs = open(content_ejs_path, 'r').read()

    template_path = os.path.join(my_dir, 'template.html')
    template = open(template_path, 'r').read()
    template = template.replace('{{ TM_BUNDLE_SUPPORT }}',
        os.environ['TM_BUNDLE_SUPPORT'])
    template = template.replace('{{ EJS_TEMPLATE }}', json.dumps(content_ejs))
    template = template.replace('{{ CONTEXT }}', json.dumps(context))

    print(template)


if __name__ == '__main__':
    quiet = ('-q' in sys.argv or '--quiet' in sys.argv)
    validate(quiet)
