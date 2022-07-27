/**
 * @license
 * Copyright 2012 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview JavaScript for Blockly's Code demo, thank you for the code its eazy to
 * @author fraser@google.com (Neil Fraser)
 */
'use strict';

/**
 * Create a namespace for the application.
 */
var Code = {};

/**
 * Lookup for names of supported languages.  Keys should be in ISO 639 format.
 */
Code.LANGUAGE_NAME = {
  'cs': 'Česky',
  'en': 'English'
};

/**
 * List of RTL languages.
 */
Code.LANGUAGE_RTL = ['ar', 'fa', 'he', 'lki'];

/**
 * Blockly's main workspace.
 * @type {Blockly.WorkspaceSvg}
 */
Code.workspace = null;

/**
 * Extracts a parameter from the URL.
 * If the parameter is absent default_value is returned.
 * @param {string} name The name of the parameter.
 * @param {string} defaultValue Value to return if parameter not found.
 * @return {string} The parameter value or the default value if not found.
 */
Code.getStringParamFromUrl = function(name, defaultValue) {
  var val = location.search.match(new RegExp('[?&]' + name + '=([^&]+)'));
  return val ? decodeURIComponent(val[1].replace(/\+/g, '%20')) : defaultValue;
};

/**
 * Get the language of this user from the URL.
 * @return {string} User's language.
 */
Code.getLang = function() {
  var lang = Code.getStringParamFromUrl('lang', '');
  if (Code.LANGUAGE_NAME[lang] === undefined) {
    // Default to English.
    lang = 'en';
  }
  return lang;
};

/**
 * Is the current language (Code.LANG) an RTL language?
 * @return {boolean} True if RTL, false if LTR.
 */
Code.isRtl = function() {
  return Code.LANGUAGE_RTL.indexOf(Code.LANG) != -1;
};

/**
 * Load blocks saved on App Engine Storage or in session/local storage.
 * @param {string} defaultXml Text representation of default blocks.
 */
Code.loadBlocks = function(defaultXml) {
  try {
    var loadOnce = window.sessionStorage.loadOnceBlocks;
  } catch(e) {
    // Firefox sometimes throws a SecurityError when accessing sessionStorage.
    // Restarting Firefox fixes this, so it looks like a bug.
    var loadOnce = null;
  }
  if ('BlocklyStorage' in window && window.location.hash.length > 1) {
    // An href with #key trigers an AJAX call to retrieve saved blocks.
    BlocklyStorage.retrieveXml(window.location.hash.substring(1));
  } else if (loadOnce) {
    // Language switching stores the blocks during the reload.
    delete window.sessionStorage.loadOnceBlocks;
    var xml = Blockly.Xml.textToDom(loadOnce);
    Blockly.Xml.domToWorkspace(xml, Code.workspace);
  } else if (defaultXml) {
    // Load the editor with default starting blocks.
    var xml = Blockly.Xml.textToDom(defaultXml);
    Blockly.Xml.domToWorkspace(xml, Code.workspace);
  } else if ('BlocklyStorage' in window) {
    // Restore saved blocks in a separate thread so that subsequent
    // initialization is not affected from a failed load.
    window.setTimeout(BlocklyStorage.restoreBlocks, 0);
  }
};

function loadCustomBlocks(){
	Blockly.defineBlocksWithJsonArray(jsonBlocks);

	Blockly.Python['vzletni'] = function(block) {
		return 'tello.takeoff()\n';
	};
	Blockly.Python['pristan'] = function(block) {
		return 'tello.land()\n';
	};
	Blockly.Python['letet_manualne'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "p1", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		var b = Blockly.Python.valueToCode(block, "p2", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		var c = Blockly.Python.valueToCode(block, "p3", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		var d = Blockly.Python.valueToCode(block, "p4", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		return "tello.send_rc_control(int(" + String(d) + "), int(" + String(c) + "), int(" + String(a) + "), int(" + String(b) + "))\n"
	};
	Blockly.Python['zastav'] = function(block) {
		return 'tello.move(0, 0)\n';
	};
	Blockly.Python['uhel'] = function(block) {
		var a = Number(block.getFieldValue("uhel"));
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};
	Blockly.Python['playsound'] = function(block) {
		var a = block.getField("sound").value_;
		return 'playsound(' + a + ')\n';
	};
	Blockly.Python['delay'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "time", Blockly.Python.ORDER_UNARY_SIGN) || "1";
		return 'time.sleep(' + a + ')\n';
	};
	Blockly.Python['move'] = function(block) {
		var a = block.getField("dir").value_;
    var preklad = ["up", "down", "forward", "back", "right", "left"];
		var b = Blockly.Python.valueToCode(block, "range", Blockly.Python.ORDER_UNARY_SIGN) || "50";
		return 'tello.move("' + preklad[a] + '", ' + b + ')\n';
	};
	Blockly.Python['rotate'] = function(block) {
		var a = block.getField("dir").value_;
		var b = Blockly.Python.valueToCode(block, "angle", Blockly.Python.ORDER_UNARY_SIGN) || "50";
    if (a == 1) var command = "rotate_clockwise"; else var command = "rotate_counter_clockwise";
		return 'tello.' + command + '(' + b + ')\n';
	};
	Blockly.Python['set_speed'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "speed", Blockly.Python.ORDER_UNARY_SIGN) || "1";
		return 'tello.set_speed(' + a + ')\n';
	};
	Blockly.Python['go_xyz_speed'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "x", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		var b = Blockly.Python.valueToCode(block, "y", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		var c = Blockly.Python.valueToCode(block, "z", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		return "tello.go_xyz_speed(" + String(a) + ", " + String(b) + ", " + String(c) + ", 100)\n"
	}; //win32api.GetAsyncKeyState(win32con.VK_CAPITAL)
	Blockly.Python['stisknuta_klavesa'] = function(block) {
		var a = Number(block.getFieldValue("key"));
		a = "win32api.GetAsyncKeyState(" + String(a) + ")";
    var b = Blockly.Python.ORDER_FUNCTION_CALL;
    return [a, b];
	};
	Blockly.Python['stisknuta_klavesa_jednoduse'] = function(block) {
		var a = block.getField("key").value_;
		a = "win32api.GetAsyncKeyState(" + String(a) + ")";
    var b = Blockly.Python.ORDER_FUNCTION_CALL;
    return [a, b];
	};
	Blockly.Python['programrunningflag'] = function(block) {
		var a = "programRunningFlag";
    var b = Blockly.Python.ORDER_FUNCTION_CALL;
    return [a, b];
	};
	Blockly.Python['cv2_destroyallwindows'] = function(block) {
		var a = "cv2.destroyAllWindows()";
    return a;
	};
  

	Blockly.Python['create_webcam'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "NAME", Blockly.Python.ORDER_UNARY_SIGN) || "1";
    var b = Blockly.Python.ORDER_MEMBER;
		return ['cv2.VideoCapture(' + a + ')\n', b];
	};
	Blockly.Python['take_img_webcam'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "NAME", Blockly.Python.ORDER_UNARY_SIGN) || "1";
    var b = a + ".read()[1]";
    var c = Blockly.Python.ORDER_MEMBER;
		return [b, c];
	};
	Blockly.Python['cv2_imshow'] = function(block) {
		var a = (String(Blockly.Python.valueToCode(block, "headline", Blockly.Python.ORDER_UNARY_SIGN)) || "image");
    a = a.substring(1, a.length - 1);
		var b = Blockly.Python.valueToCode(block, "inputImg", Blockly.Python.ORDER_UNARY_SIGN) || "None";
		return 'cv2.imshow("' + a + '", ' + b + ')\ncv2.waitKey(1)\n';
	};  
	Blockly.Python['save_img'] = function(block) {
		var a = (String(Blockly.Python.valueToCode(block, "file", Blockly.Python.ORDER_UNARY_SIGN)) || "image");
    a = a.substring(1, a.length - 1) + ".jpg";
		var b = Blockly.Python.valueToCode(block, "image", Blockly.Python.ORDER_UNARY_SIGN) || "None";
		return 'cv2.imwrite("' + a + '", ' + b + ')\n';
	};
	Blockly.Python['take_img'] = function(block) {
    var a = "readDroneImage()";
    var b = Blockly.Python.ORDER_MEMBER;
		return [a, b];
	};
	Blockly.Python['aruco_img'] = function(block) {
		var a = Number(block.getFieldValue("value"));
		var b = Blockly.Python.valueToCode(block, "img", Blockly.Python.ORDER_UNARY_SIGN) || "None";
    var c = Blockly.Python.ORDER_MEMBER;
		return ['aruco.detect(' + a + ', ' + b + ')', c];
	};
	Blockly.Python['letet'] = function(block) {
		var a = block.getField("smer").value_;
    var preklad = ["up", "down", "forward", "back", "right", "left"];
		var b = 50;
		return 'tello.move("' + preklad[a] + '", ' + b + ')\n';
	};
	Blockly.Python['set_speed_jednoduse'] = function(block) {
		var a = block.getField("speed").value_;
		return 'tello.set_speed(' + a + ')\n';
	};
	Blockly.Python['salto'] = function(block) {
		var a = block.getField("dir").value_;
    var preklad = ["f", "b", "r", "l"];
		return 'tello.flip("' + preklad[a] + '")\n';
	};
	Blockly.Python['drone_parameters'] = function(block) {
		var a = block.getField("param").value_;
    var preklad = ["battery", "temperature", "tof", "time", "yaw", "pitch", "roll", "height"];
    
    var b = Blockly.Python.ORDER_FUNCTION_CALL;
		return ['getDroneData("' + preklad[a] + '")', b];
	};




	Blockly.Python['letet'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "p1", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		var b = Blockly.Python.valueToCode(block, "p2", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		return "dron.letet(" + String(a) + ", " + String(b) + ")\n"
	};
	Blockly.Python['letet_2'] = function(block) {
    var a = block.getField("smer");
		var b = block.getField("rychlost");
		//var aa = parseInt(a.menuGenerator_.flat().indexOf(a.value_)/2);
		//var bb = parseInt(b.menuGenerator_.flat().indexOf(a.value_)/2);
		return 'dron.letet("' + String(a.value_) + '", "' + String(b.value_) + '")\n';
	};
	Blockly.Python['otocit'] = function(block) {
		var a = block.getField("rychlost");
		var b = Blockly.Python.valueToCode(block, "NAME", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		//var aa = parseInt(a.menuGenerator_.flat().indexOf(a.value_)/2);
		//var bb = parseInt(b.menuGenerator_.flat().indexOf(a.value_)/2);
		return 'dron.otocit("' + String(a.value_) + '", ' + String(b) + ')\n';
	};
	Blockly.Python['hledej_aruco_symbol'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "NAME", Blockly.Python.ORDER_UNARY_SIGN) || "0";
		a = "kamera.hledejAruco(" + String(a) + ")";
        var b = Blockly.Python.ORDER_FUNCTION_CALL;
		return [a, b];
	};


	Blockly.Python['stisknuta__klavesa'] = function(block) {
		var a = "klavesaZmacknuta(" + String(Number(block.getFieldValue("key")) + ")");
        var b = Blockly.Python.ORDER_FUNCTION_CALL
		return [a, b]
	};

	Blockly.Python['log'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "param", Blockly.Python.ORDER_UNARY_SIGN) || "None";
		return "log(" + String(a) + ")\n"
	};

  /*
	Blockly.Python['follow'] = function(block) {
		var a = (String(Blockly.Python.valueToCode(block, "NAME", Blockly.Python.ORDER_UNARY_SIGN)) || "None");
		return 'follow(' + a + ')\n';
	};*/



  // Hand detector
	Blockly.Python['hands_detect'] = function(block) {
		var param = Blockly.Python.valueToCode(block, "NAME", Blockly.Python.ORDER_UNARY_SIGN) || "None";
		var a = "handDetector.detect(" + String(param) + ")\n";
		return a;
	};
	Blockly.Python['hands_distance'] = function(block) {
		    var a = block.getField("handchoice").value_;
        a = "handDetector.distance(" + String(a) + ")";
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};
	Blockly.Python['hands_x'] = function(block) {
		    var a = block.getField("handchoice").value_;
        a = "handDetector.posX(" + String(a) + ")";
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};
	Blockly.Python['hands_y'] = function(block) {
		    var a = block.getField("handchoice").value_;
        a = "handDetector.posY(" + String(a) + ")";
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};
	Blockly.Python['gesture_hands'] = function(block) {
		    var a = block.getField("handchoice").value_;
        var dst = "handDetector.distance(" + String(a) + ")";
        a = "(" + dst + " != -1 and " + dst + " < 70)";
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};

  //Object and people detector
	Blockly.Python['objects_img'] = function(block) {
		var a = block.getField("obj").value_;
		var b = Blockly.Python.valueToCode(block, "img", Blockly.Python.ORDER_UNARY_SIGN) || "None";
    var c = 'objectDetector.detect(' + a + ', ' + b + ')\n';
		return c;
	};
	Blockly.Python['object_distance'] = function(block) {
        var a = "objectDetector.distance()";
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};
	Blockly.Python['object_angle'] = function(block) {
        var a = "objectDetector.angle()";
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};
	Blockly.Python['gesture_tpose'] = function(block) {
        var a = "objectDetector.gesture('tpose')";
        var b = Blockly.Python.ORDER_MEMBER;
		return [a, b]
	};


  
	
	Blockly.Python['exit_program'] = function(block) {
		var a = Blockly.Python.valueToCode(block, "time", Blockly.Python.ORDER_UNARY_SIGN) || "'UNDEFINED EXIT CODE'";
		return "sys.exit(" + String(a) + ")\n"
	};





};

/**
 * Save the blocks and reload with a different language.
 */
Code.changeLanguage = function() {
  // Store the blocks for the duration of the reload.
  // MSIE 11 does not support sessionStorage on file:// URLs.
  if (window.sessionStorage) {
    var xml = Blockly.Xml.workspaceToDom(Code.workspace);
    var text = Blockly.Xml.domToText(xml);
    window.sessionStorage.loadOnceBlocks = text;
  }

  var languageMenu = document.getElementById('languageMenu');
  var newLang = encodeURIComponent(
      languageMenu.options[languageMenu.selectedIndex].value);
  var search = window.location.search;
  if (search.length <= 1) {
    search = '?lang=' + newLang;
  } else if (search.match(/[?&]lang=[^&]*/)) {
    search = search.replace(/([?&]lang=)[^&]*/, '$1' + newLang);
  } else {
    search = search.replace(/\?/, '?lang=' + newLang + '&');
  }

  window.location = window.location.protocol + '//' +
      window.location.host + window.location.pathname + search;
};

/**
 * Changes the output language by clicking the tab matching
 * the selected language in the codeMenu.
 */
Code.changeCodingLanguage = function() {
  var codeMenu = document.getElementById('code_menu');
  Code.tabClick(codeMenu.options[codeMenu.selectedIndex].value);
}

/**
 * Bind a function to a button's click event.
 * On touch enabled browsers, ontouchend is treated as equivalent to onclick.
 * @param {!Element|string} el Button element or ID thereof.
 * @param {!Function} func Event handler to bind.
 */
Code.bindClick = function(el, func) {
  if (typeof el == 'string') {
    el = document.getElementById(el);
  }
  el.addEventListener('click', func, true);
  el.addEventListener('touchend', func, true);
};	

/**
 * Compute the absolute coordinates and dimensions of an HTML element.
 * @param {!Element} element Element to match.
 * @return {!Object} Contains height, width, x, and y properties.
 * @private
 */
Code.getBBox_ = function(element) {
  var height = element.offsetHeight;
  var width = element.offsetWidth;
  var x = 0;
  var y = 0;
  do {
    x += element.offsetLeft;
    y += element.offsetTop;
    element = element.offsetParent;
  } while (element);
  return {
    height: height,
    width: width,
    x: x,
    y: y
  };
};

/**
 * User's language (e.g. "en").
 * @type {string}
 */
Code.LANG = Code.getLang();

/**
 * List of tab names.
 * @private
 */
Code.TABS_ = ['blocks', 'python'];

/**
 * List of tab names with casing, for display in the UI.
 * @private
 */
Code.TABS_DISPLAY_ = [
  'Blocks', 'Python'
];

Code.selected = 'blocks';

/**
 * Switch the visible pane when a tab is clicked.
 * @param {string} clickedName Name of tab clicked.
 */
Code.tabClick = function(clickedName) {
  // If the XML tab was open, save and render the content.
  

  if (document.getElementById('tab_blocks').classList.contains('tabon')) {
    Code.workspace.setVisible(false);
  }
  // Deselect all tabs and hide all panes.
  for (var i = 0; i < Code.TABS_.length; i++) {
    var name = Code.TABS_[i];
    var tab = document.getElementById('tab_' + name);
    tab.classList.add('taboff');
    tab.classList.remove('tabon');
    document.getElementById('content_' + name).style.visibility = 'hidden';
  }

  // Select the active tab.
  Code.selected = clickedName;
  var selectedTab = document.getElementById('tab_' + clickedName);
  selectedTab.classList.remove('taboff');
  selectedTab.classList.add('tabon');
  // Show the selected pane.
  document.getElementById('content_' + clickedName).style.visibility =
      'visible';
  Code.renderContent();
  // The code menu tab is on if the blocks tab is off.
  var codeMenuTab = document.getElementById('tab_code');
  if (clickedName == 'blocks') {
    Code.workspace.setVisible(true);
    codeMenuTab.className = 'taboff';
  } else {
    codeMenuTab.className = 'tabon';
  }
  // Sync the menu's value with the clicked tab value if needed.
  var codeMenu = document.getElementById('code_menu');
  for (var i = 0; i < codeMenu.options.length; i++) {
    if (codeMenu.options[i].value == clickedName) {
      codeMenu.selectedIndex = i;
      break;
    }
  }
  Blockly.svgResize(Code.workspace);
};

/**
 * Populate the currently selected pane with content generated from the blocks.
 */
Code.renderContent = function() {
  var content = document.getElementById('content_' + Code.selected);
  // Initialize the pane.
  if (content.id == 'content_xml') {
    var xmlTextarea = document.getElementById('content_xml');
    var xmlDom = Blockly.Xml.workspaceToDom(Code.workspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);
    xmlTextarea.value = xmlText;
    xmlTextarea.focus();
  } else if (content.id == 'content_python') {
    Code.attemptCodeGeneration(Blockly.Python);
  }
  if (typeof PR == 'object') {
    PR.prettyPrint();
  }
};

/**
 * Attempt to generate the code and display it in the UI, pretty printed.
 * @param generator {!Blockly.Generator} The generator to use.
 */

function generatePythonCode(){
	var code = Blockly.Python.workspaceToCode(Code.workspace);
	code = "" + code;
	return code;
};
 
Code.attemptCodeGeneration = function(generator) {
  var content = document.getElementById('content_' + Code.selected);
  content.textContent = '';
  if (Code.checkAllGeneratorFunctionsDefined(generator)) {
    var code = generatePythonCode();
    content.textContent = code;
    // Remove the 'prettyprinted' class, so that Prettify will recalculate.
    content.className = content.className.replace('prettyprinted', '');
  }
};

/**
 * Check whether all blocks in use have generator functions.
 * @param generator {!Blockly.Generator} The generator to use.
 */
Code.checkAllGeneratorFunctionsDefined = function(generator) {
  var blocks = Code.workspace.getAllBlocks(false);
  var missingBlockGenerators = [];
  for (var i = 0; i < blocks.length; i++) {
    var blockType = blocks[i].type;
    if (!generator[blockType]) {
      if (missingBlockGenerators.indexOf(blockType) == -1) {
        missingBlockGenerators.push(blockType);
      }
    }
  }

  var valid = missingBlockGenerators.length == 0;
  if (!valid) {
    var msg = 'The generator code for the following blocks not specified for ' +
        generator.name_ + ':\n - ' + missingBlockGenerators.join('\n - ');
    Blockly.alert(msg);  // Assuming synchronous. No callback.
  }
  return valid;
};

/**
 * Initialize Blockly.  Called on page load.
 */
Code.init = function() {
  Code.initLanguage();
  
  loadCustomBlocks();

  var rtl = Code.isRtl();
  var container = document.getElementById('content_area');
  var onresize = function(e) {
    var bBox = Code.getBBox_(container);
    for (var i = 0; i < Code.TABS_.length; i++) {
      var el = document.getElementById('content_' + Code.TABS_[i]);
      el.style.top = bBox.y + 'px';
      el.style.left = bBox.x + 'px';
      // Height and width need to be set, read back, then set again to
      // compensate for scrollbars.
      el.style.height = bBox.height + 'px';
      el.style.height = (2 * bBox.height - el.offsetHeight) + 'px';
      el.style.width = bBox.width + 'px';
      el.style.width = (2 * bBox.width - el.offsetWidth) + 'px';
    }
    // Make the 'Blocks' tab line up with the toolbox.
    if (Code.workspace && Code.workspace.getToolbox().width) {
      document.getElementById('tab_blocks').style.minWidth =
          (Code.workspace.getToolbox().width - 38) + 'px';
          // Account for the 19 pixel margin and on each side.
    }
  };
  window.addEventListener('resize', onresize, false);

  // The toolbox XML specifies each category name using Blockly's messaging
  // format (eg. `<category name="%{BKY_CATLOGIC}">`).
  // These message keys need to be defined in `Blockly.Msg` in order to
  // be decoded by the library. Therefore, we'll use the `MSG` dictionary that's
  // been defined for each language to import each category name message
  // into `Blockly.Msg`.
  // TODO: Clean up the message files so this is done explicitly instead of
  // through this for-loop.
  for (var messageKey in MSG) {
    if (messageKey.indexOf('cat') == 0) {
      Blockly.Msg[messageKey.toUpperCase()] = MSG[messageKey];
    }
  }

  // Construct the toolbox XML, replacing translated variable names.
  var toolboxText = document.getElementById('toolbox').outerHTML;
  toolboxText = toolboxText.replace(/(^|[^%]){(\w+)}/g,
      function(m, p1, p2) {return p1 + MSG[p2];});
  var toolboxXml = Blockly.Xml.textToDom(toolboxText);

  Code.workspace = Blockly.inject('content_blocks',
      {grid:
          {spacing: 25,
           length: 3,
           colour: '#ccc',
           snap: true},
       media: 'media/',
       rtl: rtl,
       toolbox: toolboxXml,
       zoom:
           {controls: true,
            wheel: true}
      });

  // Add to reserved word list: Local variables in execution environment (runJS)
  // and the infinite loop detection function.
  //Blockly.JavaScript.addReservedWords('code,timeouts,checkTimeout');

  Code.loadBlocks('');

  if ('BlocklyStorage' in window) {
    // Hook a save function onto unload.
    BlocklyStorage.backupOnUnload(Code.workspace);
  }

  Code.tabClick(Code.selected);

  Code.bindClick('saveButton', function() {
        var xml = Blockly.Xml.workspaceToDom(Code.workspace);
        var xmlText = new XMLSerializer().serializeToString(xml);
        console.log(xml);
        var blob = new Blob([xmlText], {type: "text/xml"});
        saveAs(blob, "program.xml");
  });
  
  var fileChooser = document.getElementById('file');
  Code.bindClick('loadButton', function(){
    fileChooser.value = "";
    fileChooser.click();
  })

  function parseTextAsXml(text) {
      var parser = new DOMParser(),
      xmlDom = parser.parseFromString(text, "text/xml");
      Code.discard();
      Blockly.Xml.domToWorkspace(xmlDom.firstChild, Code.workspace);
      //now, extract items from xmlDom and assign to appropriate text input fields
  }

  function waitForTextReadComplete(reader) {
    reader.onloadend = function(event) {
        var text = event.target.result;

        parseTextAsXml(text);
    }
  }

  function handleFileSelection() {
    var file = fileChooser.files[0],
        reader = new FileReader();

    waitForTextReadComplete(reader);
    reader.readAsText(file);
  }
  fileChooser.addEventListener('change', handleFileSelection, false);

  Code.bindClick('samplesButton', function(){
    //alert("Dobrá práce, objevil jsi nedoprogramovanou funkci :) ... toto otevře dialog s pár ukázkovýma prográmkama pro okamžité nahrání na dron.");
  
    document.getElementById('mySizeChartModal').style.display = "block";  
  })

  Code.bindClick('trashButton',
      function() {Code.discard(); Code.renderContent();});
  Code.bindClick('runButton', Code.runJS);
  // Disable the link button if page isn't backed by App Engine storage.
  var linkButton = document.getElementById('linkButton');
  if ('BlocklyStorage' in window) {
    BlocklyStorage['HTTPREQUEST_ERROR'] = MSG['httpRequestError'];
    BlocklyStorage['LINK_ALERT'] = MSG['linkAlert'];
    BlocklyStorage['HASH_ERROR'] = MSG['hashError'];
    BlocklyStorage['XML_ERROR'] = MSG['xmlError'];
    Code.bindClick(linkButton,
        function() {BlocklyStorage.link(Code.workspace);});
  } else if (linkButton) {
    linkButton.className = 'disabled';
  }

  for (var i = 0; i < Code.TABS_.length; i++) {
    var name = Code.TABS_[i];
    Code.bindClick('tab_' + name,
        function(name_) {return function() {Code.tabClick(name_);};}(name));
  }
  Code.bindClick('tab_code', function(e) {
    if (e.target !== document.getElementById('tab_code')) {
      // Prevent clicks on child codeMenu from triggering a tab click.
      return;
    }
    Code.changeCodingLanguage();
  });

  onresize();
  Blockly.svgResize(Code.workspace);

  // Lazy-load the syntax-highlighting.
  window.setTimeout(Code.importPrettify, 1);
};


/**
 * Initialize the page language.
 */
Code.initLanguage = function() {
  // Set the HTML's language and direction.
  var rtl = Code.isRtl();
  document.dir = rtl ? 'rtl' : 'ltr';
  document.head.parentElement.setAttribute('lang', Code.LANG);

  // Sort languages alphabetically.
  var languages = [];
  for (var lang in Code.LANGUAGE_NAME) {
    languages.push([Code.LANGUAGE_NAME[lang], lang]);
  }
  var comp = function(a, b) {
    // Sort based on first argument ('English', 'Русский', '简体字', etc).
    if (a[0] > b[0]) return 1;
    if (a[0] < b[0]) return -1;
    return 0;
  };
  languages.sort(comp);
  // Populate the language selection menu.
  var languageMenu = document.getElementById('languageMenu');
  languageMenu.options.length = 0;
  for (var i = 0; i < languages.length; i++) {
    var tuple = languages[i];
    var lang = tuple[tuple.length - 1];
    var option = new Option(tuple[0], lang);
    if (lang == Code.LANG) {
      option.selected = true;
    }
    languageMenu.options.add(option);
  }
  languageMenu.addEventListener('change', Code.changeLanguage, true);

  // Populate the coding language selection menu.
  var codeMenu = document.getElementById('code_menu');
  codeMenu.options.length = 0;
  for (var i = 1; i < Code.TABS_.length; i++) {
    codeMenu.options.add(new Option(Code.TABS_DISPLAY_[i], Code.TABS_[i]));
  }
  codeMenu.addEventListener('change', Code.changeCodingLanguage);

  // Inject language strings.
  //document.title += ' ' + MSG['title'];
  //document.getElementById('title').textContent = MSG['title'];
  document.getElementById('tab_blocks').textContent = MSG['blocks'];

  document.getElementById('linkButton').title = MSG['linkTooltip'];
  document.getElementById('runButton').title = MSG['runTooltip'];
  document.getElementById('trashButton').title = MSG['trashTooltip'];
};

/**
 * Execute the user's code.
 * Just a quick and dirty eval.  Catch infinite loops.
 */
Code.runJS = function() {
  var code = generatePythonCode();

  var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function () {
		if (this.readyState != 4) return;
		if (this.status == 200) {
      var data = JSON.parse(this.responseText)["fetch"];
      console.log(data);
    }

		// end of state change: it can be after some time (async)
	};
	xhr.open("POST", "./../../exec", true);   //Replace endpoint url asap ... TBD
	xhr.setRequestHeader('Content-Type', 'application/json');
	var jsonToSend = JSON.stringify({"command": "exec", "exec": code, "priority": 0})
	
	xhr.send(jsonToSend);
};

/**
 * Discard all blocks from the workspace.
 */
Code.discard = function() {
  var count = Code.workspace.getAllBlocks(false).length;
  if (count < 2 ||
      window.confirm(Blockly.Msg['DELETE_ALL_BLOCKS'].replace('%1', count))) {
    Code.workspace.clear();
    if (window.location.hash) {
      window.location.hash = '';
    }
  }
};

// Load the Code demo's language strings.
document.write('<script src="msg/' + Code.LANG + '.js"></script>\n');
// Load Blockly's language strings.
document.write('<script src="msg/js/' + Code.LANG + '.js"></script>\n');

window.addEventListener('load', Code.init);


function loadSample(sample) {
  var xml = Blockly.Xml.textToDom(samplecode[sample]);
  //Clean
  Code.workspace.clear();
  Blockly.Xml.domToWorkspace(xml, Code.workspace);
  var ebModal = document.getElementById('mySizeChartModal');
  ebModal.style.display = "none";
}

var samplecode = ['<xml xmlns="https://developers.google.com/blockly/xml"><variables><variable id="BN#/ReoZT/CA)Li90UJx">obrazek</variable></variables><block type="vzletni" id=";c#JPNf;jQ|1;CfxvUO:" x="238" y="112"><next><block type="move" id="L4]^WmwTXq8Am82`{4MU"><field name="dir">0</field><value name="range"><block type="math_number" id="sy@FJEh^-xyZSLJ];4YU"><field name="NUM">80</field></block></value><next><block type="controls_whileUntil" id="^#$UPuQj#j|gMB;-9bv!"><field name="MODE">WHILE</field><value name="BOOL"><block type="programrunningflag" id=")xNZhi`K|Te_F.s!Udr%"/></value><statement name="DO"><block type="variables_set" id="FU-T#}xL+r:#lmd]tiTc"><field name="VAR" id="BN#/ReoZT/CA)Li90UJx">obrazek</field><value name="VALUE"><block type="take_img" id="GM[N|:`NCk0;nG^7qF*A"/></value><next><block type="hands_detect" id="Da}fB#nL$i`?r3,xuB(!"><value name="NAME"><block type="variables_get" id="2II/PMbF:sIB7OjuHN$V"><field name="VAR" id="BN#/ReoZT/CA)Li90UJx">obrazek</field></block></value><next><block type="controls_if" id="k^X9!xD4y:UA$J*t@YsP"><value name="IF0"><block type="gesture_hands" id="A7py;xbDVO.{h==L?fDW"><field name="handchoice">2</field></block></value><statement name="DO0"><block type="rotate" id="`0HQkgow1*W_ChULc@i?"><field name="dir">1</field><value name="angle"><block type="uhel" id="}XPAvv]A^9KK,#J87oI("><field name="uhel">180</field></block></value><next><block type="move" id="qo%[*5:4|2N=Q`$P4TMc"><field name="dir">2</field><value name="range"><block type="math_number" id="Pb|{-Q#b5^y5SW6Kue1f"><field name="NUM">300</field></block></value></block></next></block></statement><next><block type="controls_if" id="7*WbQT0pU1*W8*LP9-`G"><value name="IF0"><block type="logic_compare" id="q:j130S#8I8l:c11k@9`"><field name="OP">LT</field><value name="A"><block type="drone_parameters" id="MfZ=f$C2P:MC`!:YB0MZ"><field name="param">2</field></block></value><value name="B"><block type="math_number" id="ek(hRs%*LM#Km:N]V:25"><field name="NUM">30</field></block></value></block></value><statement name="DO0"><block type="pristan" id="(Dy:6/q,|DVVdFC$b#iu"><next><block type="controls_flow_statements" id="f5fF|YRHn!vp/QSx`p%@"><field name="FLOW">BREAK</field></block></next></block></statement></block></next></block></next></block></next></block></statement></block></next></block></next></block></xml>',
'<xml xmlns="https://developers.google.com/blockly/xml"><block type="vzletni" id="bcI6+-$gfLe]{3fe!0nS" x="237" y="137"><next><block type="move" id="#f=TS)nEL8yFA7Ayi20W"><field name="dir">0</field><value name="range"><block type="math_number" id="+,ZDHi_10Byr/CGk2p|P"><field name="NUM">50</field></block></value><next><block type="move" id="$HYd{O)6V]aWH=pEDpXJ"><field name="dir">2</field><value name="range"><block type="math_number" id=".H~HOs1Q9C9$/1^(v=/~"><field name="NUM">100</field></block></value><next><block type="rotate" id="c3AD}xd*B6j$I-@mh@zl"><field name="dir">1</field><value name="angle"><block type="uhel" id="W5#|`|-ll_P65Gxs.Ji:"><field name="uhel">90</field></block></value><next><block type="move" id="Op*uvr0y$mgp{W(@)$CN"><field name="dir">2</field><value name="range"><block type="math_number" id="5TFFp(B5bvz:3G6GpC,X"><field name="NUM">100</field></block></value><next><block type="rotate" id="4K85pyr6)C7hyx-SgV?_"><field name="dir">1</field><value name="angle"><block type="uhel" id="eO=L@;E5*c8DG/DE7#,a"><field name="uhel">90</field></block></value><next><block type="move" id="%S[Ma9Fch#7e_qp5RSe)"><field name="dir">2</field><value name="range"><block type="math_number" id="uPPI`-wG^R]6[ef0)MNH"><field name="NUM">100</field></block></value><next><block type="rotate" id="FH?BMC=-.XA{Z6Kuw|=E"><field name="dir">1</field><value name="angle"><block type="uhel" id="AE?(03Nk/1APIXbNJ65I"><field name="uhel">90</field></block></value><next><block type="move" id=",N}tc$`9eJL.8mT-G]jT"><field name="dir">2</field><value name="range"><block type="math_number" id="7J-/)T_PuCEy$Zp/d1GB"><field name="NUM">100</field></block></value><next><block type="rotate" id="YgtbY!sJBb#eN}fe^b.C"><field name="dir">1</field><value name="angle"><block type="uhel" id="V#xlk6Iyo:NKrv#9Vo8R"><field name="uhel">90</field></block></value><next><block type="salto" id="zttnZXnN7_WKoZZ8)=U{"><field name="dir">0</field><next><block type="pristan" id="9+MJ3}8jV(qHSZq6KS}!"/></next></block></next></block></next></block></next></block></next></block></next></block></next></block></next></block></next></block></next></block></next></block></xml>',
'<xml xmlns="https://developers.google.com/blockly/xml"><variables><variable id="[DcggImY+Wib.dxXFVYD">obrazek</variable></variables><block type="vzletni" id="1!!EUGqa{y%a+;=*~K75" x="137" y="138"><next><block type="controls_whileUntil" id="yRrP$4?W{sN1yFy{i0NA"><field name="MODE">WHILE</field><value name="BOOL"><block type="programrunningflag" id="y^N3Z7s!omkt-1@g|_GW"/></value><statement name="DO"><block type="variables_set" id="+D)i9Jkch$V!~K^vT0PJ"><field name="VAR" id="[DcggImY+Wib.dxXFVYD">obrazek</field><value name="VALUE"><block type="take_img" id="jafD,9Zi/Tmjo6A?3}Zi"/></value><next><block type="objects_img" id="YZ!_9=UorZ/.WX``@k+V"><field name="obj">1</field><value name="img"><block type="variables_get" id=".dXDv+%1Yk~PB0UmIUSg"><field name="VAR" id="[DcggImY+Wib.dxXFVYD">obrazek</field></block></value><next><block type="controls_if" id="q]X2u-mjHIA6nfSgoP[5"><mutation else="1"/><value name="IF0"><block type="logic_compare" id="TZvP5Unj3h);8vHoLIB*"><field name="OP">NEQ</field><value name="A"><block type="object_distance" id="myBUOfoF1CwjE]2O[$im"/></value><value name="B"><block type="math_number" id="z2oC(wOC`G1F6haP@)XN"><field name="NUM">-1</field></block></value></block></value><statement name="DO0"><block type="log" id="~Hr.(D,nemO9Kd5(W5e)"><value name="param"><block type="text_join" id="QGW8T5|}lgjt8GABnI*,"><mutation items="3"/><value name="ADD0"><block type="text" id="D9xCk,gm-#J^I7D,CxQS"><field name="TEXT">Angle:</field></block></value><value name="ADD1"><block type="object_angle" id="u+}gZBG*wDx3~HN#fnvd"/></value></block></value><next><block type="letet_manualne" id=";e~OvSqCk4U|S/_O`6e("><value name="p1"><block type="math_number" id="=WsZ{[K3Pr;krnd;-:4$"><field name="NUM">0</field></block></value><value name="p2"><block type="math_arithmetic" id="UbHI*vkaWj|H:m*l:YqF"><field name="OP">MULTIPLY</field><value name="A"><shadow type="math_number" id="vpo8~V3Y2:U=7k-UzO,6"><field name="NUM">0.3</field></shadow></value><value name="B"><shadow type="math_number" id="b6oU0Zi,SjH6m[v=F!5u"><field name="NUM">1</field></shadow><block type="object_angle" id=",CnO$^y~]ZiW`XHKO/E~"/></value></block></value><value name="p3"><block type="math_number" id=":mSrp7_cmGl!6!u%b%fy"><field name="NUM">0</field></block></value><value name="p4"><block type="math_number" id=".e_CiezR;98/5s]Pm?cU"><field name="NUM">0</field></block></value></block></next></block></statement><statement name="ELSE"><block type="letet_manualne" id="-OF6Yg#qK@s8|UqTSD]S"><value name="p1"><block type="math_number" id="b6B{;[h}~p.!V?!S:N.)"><field name="NUM">0</field></block></value><value name="p2"><block type="math_number" id="gwr+CQxitn,53S8./1Sw"><field name="NUM">0</field></block></value><value name="p3"><block type="math_number" id="TD^lWDZ:B(^Q)ZOw%4JK"><field name="NUM">0</field></block></value><value name="p4"><block type="math_number" id=",.I:8=W9cni]c:JDW`/4"><field name="NUM">0</field></block></value></block></statement><next><block type="cv2_imshow" id="gWIcdLz06(=4id7cV$nk"><value name="inputImg"><block type="variables_get" id=":,#$xm2q/2uESP=-UUBb"><field name="VAR" id="[DcggImY+Wib.dxXFVYD">obrazek</field></block></value><value name="headline"><block type="text" id="zWt*iTQ[-k9/vG?s;S!B"><field name="TEXT">test</field></block></value><next><block type="delay" id="h$W*PLCjZ.Zl#wk`KFAZ"><value name="time"><block type="math_number" id="x|+W;R%55]/AEi$Yc|s|"><field name="NUM">0.01</field></block></value></block></next></block></next></block></next></block></next></block></statement><next><block type="pristan" id="1xShm]Ixh|3-L7$OY-oL"><next><block type="cv2_destroyallwindows" id="x*5x=OW4ZvyM7^n_q1!2"/></next></block></next></block></next></block></xml>'];
