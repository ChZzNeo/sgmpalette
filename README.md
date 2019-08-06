# Skullgirls Mobile Palette Editor

A palette editor for the static sprites of Skullgirls Mobile.

<img src="sample.png">

Don't expect to be able to perfectly recreate the more complex official palettes, such as Doublicious or Tomb & Gloom. The detail layer and color layer are blended with linear burn; the game likely uses more complex and multiple other blend modes.

Also, unlike my previous Skullgirls Mobile projects, I did not take any steps to make this website mobile-friendly. The color picker on most mobile browsers is too limited anyway.

## Features

### Menu

To load sprites, you must choose a character from the menu.
You can also toggle visibility of the background layer, linework layer, and detail layer here.

### Spritesheet

The spritesheet contains all in-game static sprites of the chosen character.
You can click within any sprite to select a color area to edit.

### Palette

The palette contains all colors present in the chosen character's spritesheet.
Some characters have sprites with noisy edges and thus have extraneous rows of color.

The leftmost button in a row indicates whether the color area is opaque (detail layer applies shadows) or transparent (detail layer is an alpha channel).
The other options in the row indicate color and uniform opacity.

## Download

To download a single sprite, right-click (or control-click) a sprite and select `Save Image As...`.

To download a zipped folder of all sprites in the current spritesheet, click the `Download` button at the very bottom of the page.

Thanks to the following:

* [Stuk/jszip](https://github.com/Stuk/jszip) for making it easy to create zip files
* [eligrey/FileSaver.js](https://github.com/eligrey/FileSaver.js) for making it easy to download those zip files
