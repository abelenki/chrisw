chrisw = {};

chrisw.render = Mustache.to_html;

chrisw.raty = function(selector, parameters){
  
  var defaults = {
    path: '/images/common/'
  };
  
  var options = $.extend(parameters, defaults)

  $(selector).raty(
    options
  );
};

chrisw.reload = function(){
  location.reload()
}
