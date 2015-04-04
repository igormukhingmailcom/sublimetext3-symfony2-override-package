# Symfony2 Override

Sublime Text 3 Package for easy overriding files from Symfony2 bundles.

It greatly simplifies the work with bundles, that have files with a high level of nesting.

## Features

At this time, package can only do basic operations like:
- Copy Twig templates from `vendor/BundleName/Resources/views/High/Nesting/Level/template.html.twig` repository to `app/Resources/BundleName/views/High/Nesting/Level/template.html.twig`.
- Copy `.php` files from `vendor/BundleName/High/Nesting/Level/Whatever.php` repository to `src/AppBundle/High/Nesting/Level/Whatever.php`.

and then open it in editor. Another functions that will be implemented collected in TODO.md

## Installation

### Manual

```bash
cd ~/.config/sublime-text-3/Packages
git clone https://github.com/igormukhingmailcom/sublimetext3-symfony2-override-package.git "Symfony2 Override"
```

## Usage

### Override current file

Press `ctrl+shift+o` on Linux.

Also `Override...` menu item available at Context Menu, Side Bar Menu and Main Menu -> File.

If file already overriden, it will be just opened.

## License

MIT
