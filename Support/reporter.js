'use strict';

// Minimal JSHint reporter that returns the errors as a JSON array.

module.exports = {
  reporter: function(res) {
    var report = res.map(function(r) { return r.error; });
    report.sort(function(a, b) {
      if (a.line === b.line && a.character === b.character) { return 0; }

      if (a.line < b.line) { return -1; }
      if (a.line === b.line && a.character < b.character) { return -1; }

      return 1;
    });
    process.stdout.write(JSON.stringify(report) + '\n');
  }
};
