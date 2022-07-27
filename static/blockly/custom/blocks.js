var jsonBlocks = [{
  "type": "vzletni",
  "message0": "Vzlétnout dron",
  "previousStatement": null,
  "nextStatement": null,
  "colour": 0,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "pristan",
  "message0": "Přistát dron",
  "previousStatement": null,
  "nextStatement": null,
  "colour": 0,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "letet_manualne",
  "message0": "Letět (páčky na ovladači) %1 Výška: %2 Otáčení: %3 Vpřed / vzad: %4 Vpravo / vlevo: %5",
  "args0": [
    {
      "type": "input_dummy"
    },
    {
      "type": "input_value",
      "name": "p1",
      "check": "Number"
    },
    {
      "type": "input_value",
      "name": "p2",
      "check": "Number"
    },
    {
      "type": "input_value",
      "name": "p3",
      "check": "Number"
    },
    {
      "type": "input_value",
      "name": "p4",
      "check": "Number"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "Rozsah -1 až 1",
  "helpUrl": ""
},
{
  "type": "uhel",
  "message0": "Směr %1",
  "args0": [
    {
      "type": "field_angle",
      "name": "uhel",
      "angle": 0
    }
  ],
  "output": "Number",
  "colour": 225,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "playsound",
  "message0": "Přehrát zvuk (na počítači) %1",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "sound",
      "options": [
        [
          "varování",
          "0"
        ],
        [
          "mise dokončena",
          "1"
        ],
        [
          "airhorn",
          "2"
        ]
      ]
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 90,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "delay",
  "message0": "Počkat %1 sekund",
  "args0": [
    {
      "type": "input_value",
      "name": "time",
      "check": "Number"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "move",
  "message0": "Letět %1 %2 [cm]",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "dir",
      "options": [
        [
          "nahoru",
          "0"
        ],
        [
          "dolů",
          "1"
        ],
        [
          "dopředu",
          "2"
        ],
        [
          "dozadu",
          "3"
        ],
        [
          "doprava",
          "4"
        ],
        [
          "doleva",
          "5"
        ]
      ]
    },
    {
      "type": "input_value",
      "name": "range",
      "check": "Number"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "rotate",
  "message0": "Otočit dron %1  o %2 %3",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "dir",
      "options": [
        [
          "vpravo",
          "1"
        ],
        [
          "vlevo",
          "-1"
        ]
      ]
    },
    {
      "type": "input_value",
      "name": "angle",
      "check": "Number"
    },
    {
      "type": "input_dummy"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "set_speed",
  "message0": "Nastavit rychlost dronu %1 %%",
  "args0": [
    {
      "type": "input_value",
      "name": "speed",
      "check": "Number"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "stisknuta_klavesa",
  "message0": "stisknuta klávesa %1 (kód)",
  "args0": [
    {
      "type": "field_number",
      "name": "key",
      "value": 0,
      "precision": 1
    }
  ],
  "output": "Boolean",
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "stisknuta_klavesa_jednoduse",
  "message0": "stisknuta klávesa %1",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "key",
      "options": [
        [
          "mezera",
          "32"
        ],
        [
          "enter",
          "13"
        ],
        [
          "šipka dopředu",
          "38"
        ],
        [
          "šipka dozadu",
          "40"
        ],
        [
          "šipka doprava",
          "39"
        ],
        [
          "šipka doleva",
          "37"
        ],
        [
          "levý shift",
          "16"
        ],
        [
          "levý ctrl",
          "17"
        ]
      ]
    }
  ],
  "output": "Boolean",
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "save_img",
  "message0": "Uložit obrázek %1 do souboru %2 .jpg",
  "args0": [
    {
      "type": "input_value",
      "name": "image",
      "check": "image"
    },
    {
      "type": "input_value",
      "name": "file",
      "check": "String"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "take_img",
  "message0": "vyfotit obrázek z kamery dronu",
  "output": "image",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "objects_img",
  "message0": "Rozpoznej %1 z obrázku %2 %3",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "obj",
      "options": [
        [
          "libovolný nejbližší objekt",
          "0"
        ],
        [
          "nejbližšího člověka",
          "1"
        ],
        [
          "nejbližší židli",
          "2"
        ],
        [
          "nejbližší stůl",
          "3"
        ],
        [
          "nejbližší vozidlo",
          "4"
        ],
        [
          "nejbližší domácí zvíře",
          "5"
        ]
      ]
    },
    {
      "type": "input_value",
      "name": "img",
      "check": "image"
    },
    {
      "type": "input_dummy"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "set_speed_jednoduse",
  "message0": "Nastavit rychlost dronu na %1",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "speed",
      "options": [
        [
          "nejrychleji",
          "100"
        ],
        [
          "rychle",
          "60"
        ],
        [
          "pomalu",
          "30"
        ]
      ]
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "salto",
  "message0": "Salto %1",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "dir",
      "options": [
        [
          "vpřed",
          "0"
        ],
        [
          "vzad",
          "1"
        ],
        [
          "vpravo",
          "2"
        ],
        [
          "vlevo",
          "3"
        ]
      ]
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "drone_parameters",
  "message0": "získat parametr dronu %1",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "param",
      "options": [
        [
          "baterie",
          "0"
        ],
        [
          "teplota",
          "1"
        ],
        [
          "(tof) vzdálenost od země",
          "2"
        ],
        [
          "čas letu [s]",
          "3"
        ],
        [
          "směr dronu",
          "4"
        ],
        [
          "náklon vpřed/vzad",
          "5"
        ],
        [
          "náklon vpravo/vlevo",
          "6"
        ],
        [
          "výška dronu",
          "7"
        ]
      ]
    }
  ],
  "output": "Number",
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "take_img_webcam",
  "message0": "Vyfotit obrázek z kamery %1",
  "args0": [
    {
      "type": "input_value",
      "name": "NAME",
      "check": "camera"
    }
  ],
  "output": "image",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "cv2_imshow",
  "message0": "Vykreslit obrázek %1 %2 Nadpis okna %3",
  "args0": [
    {
      "type": "input_value",
      "name": "inputImg",
      "check": "image"
    },
    {
      "type": "input_dummy"
    },
    {
      "type": "input_value",
      "name": "headline",
      "check": "String"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "log",
  "message0": "Vypiš na konzoli %1",
  "args0": [
    {
      "type": "input_value",
      "name": "param",
      "check": "String"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 90,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "hands_detect",
  "message0": "Detekuj ruce na obrázku %1 %2",
  "args0": [
    {
      "type": "input_value",
      "name": "NAME",
      "check": "image"
    },
    {
      "type": "input_dummy"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "hands_distance",
  "message0": "Vzdálenost %1 ruky od dronu",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "handchoice",
      "options": [
        [
          "pravé",
          "0"
        ],
        [
          "levé",
          "1"
        ],
        [
          "libovolné",
          "2"
        ]
      ]
    }
  ],
  "output": "Number",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "exit_program",
  "message0": "Ukončit program hláškou %1",
  "args0": [
    {
      "type": "input_value",
      "name": "time"
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "object_distance",
  "message0": "Vzdálenost sledovaného objektu",
  "output": "Number",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "object_angle",
  "message0": "Ůhel sledovaného objektu",
  "output": "Number",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "gesture_tpose",
  "message0": "detekuji rozpaženého člověka",
  "output": "Boolean",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "gesture_hands",
  "message0": "Detekuji %1 ruku před dronem",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "handchoice",
      "options": [
        [
          "pravou",
          "0"
        ],
        [
          "levou",
          "1"
        ],
        [
          "libovolnou",
          "2"
        ]
      ]
    }
  ],
  "output": "Boolean",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "create_webcam",
  "message0": "Vytvořit kameru %1",
  "args0": [
    {
      "type": "input_value",
      "name": "NAME",
      "check": "Number"
    }
  ],
  "output": "camera",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "programrunningflag",
  "message0": "Je program spuštěný",
  "output": "Boolean",
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "cv2_destroyallwindows",
  "message0": "Zavřít všechna okna",
  "previousStatement": null,
  "nextStatement": null,
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "hands_x",
  "message0": "Pozice X %1 ruky od dronu",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "handchoice",
      "options": [
        [
          "pravé",
          "0"
        ],
        [
          "levé",
          "1"
        ],
        [
          "libovolné",
          "2"
        ]
      ]
    }
  ],
  "output": "Number",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "hands_y",
  "message0": "Pozice Y %1 ruky od dronu",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "handchoice",
      "options": [
        [
          "pravé",
          "0"
        ],
        [
          "levé",
          "1"
        ],
        [
          "libovolné",
          "2"
        ]
      ]
    }
  ],
  "output": "Number",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "gesture_hands_detect_gesture",
  "message0": "Detekuj gesto rukou %1",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "gesture",
      "options": [
        [
          "nahoru",
          "0"
        ],
        [
          "dolů",
          "1"
        ],
        [
          "doprava",
          "2"
        ],
        [
          "doleva",
          "3"
        ]
      ]
    }
  ],
  "output": "Boolean",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
},
{
  "type": "gesture_hands_count",
  "message0": "Počet detekovaných rukou",
  "output": "Number",
  "colour": 45,
  "tooltip": "",
  "helpUrl": ""
}];