'use strict';

// Minimal JSHint reporter that returns the errors as a JSON array.

module.exports = {
  reporter: function(res) {
    var report = res.map(function(r) { return r.error; });
    process.stdout.write(JSON.stringify(report) + '\n');
  }
};
