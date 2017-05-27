'use strict';

describe('loginApp.version module', function() {
  beforeEach(module('loginApp.version'));

  describe('version service', function() {
    it('should return current version', inject(function(version) {
      expect(version).toEqual('0.1');
    }));
  });
});
