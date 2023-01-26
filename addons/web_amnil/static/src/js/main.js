odoo.define('web_amnil.ListRenderer', function (require) {
    "use strict";
    var ListRenderer = require('web.ListRenderer');
  
    ListRenderer.include({
  
      /**
       * @override
       * @returns {jQueryElement} a jquery element <tbody>
       */
      _renderBody: function () {
        var self = this;
        var $rows = this._renderRows();
        while ($rows.length < 1) {
          $rows.push(self._renderEmptyRow());
        }
        return $('<tbody>').append($rows);
      },
  
    });
  
    return ListRenderer;
  });
  