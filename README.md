# Symfony2 Override

[![Join the chat at https://gitter.im/igormukhingmailcom/sublimetext3-symfony2-override-package](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/igormukhingmailcom/sublimetext3-symfony2-override-package?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![See package at https://packagecontrol.io/](https://packagecontrol.herokuapp.com/downloads/Symfony2%20Override.svg)](https://packagecontrol.io/packages/Symfony2%20Override)

Sublime Text 3 Package for easy overriding files from Symfony2 bundles.

It greatly simplifies the work with bundles, that have files with a high level of nesting.

## Features

At this time, package can override php files, twig templates, translations in any format and any file from `Resources/public` folder.

For example, it can:
- Copy Twig templates from `vendor/Vendor/BundleName/Resources/views/High/Nesting/Level/template.html.twig` to `app/Resources/VendorBundleName/views/High/Nesting/Level/template.html.twig` or `src/SelectedBundleName/Resources/views/High/Nesting/Level/template.html.twig`.
- Copy `.xliff`, `.yml`, `.php` or whatever files from `vendor/Vendor/BundleName/Resources/translations/whatever.yml` to `src/SelectedBundleName/Resources/translations/whatever.yml` or `app/Resources/VendorBundleName/translations/whatever.yml`.
- Copy `.php` files from `vendor/Vendor/BundleName/High/Nesting/Level/Whatever.php` to `src/SelectedBundleName/High/Nesting/Level/Whatever.php`.
  - Replace old namespace to new one
  - Paste `use Vendor\BundleName\High\Nesting\Level\Whatever as BaseWhatever` statement with source class namespace
  - Replace `class Whatever` or `class Whatever extends SomeBaseClass` to `class Whatever extends BaseWhatever`
- Copy files from `public` folder to selected bundle (css, js, etc)

After file have been copied, it automatically opens in editor.

## Limitations

- Package work only in Sublime Text 3. Not tested in Sublime Text 2.
- Package tested only on Ubuntu environment.
- At that moment package supports overriding only PSR-0 libraries from `vendors` directory

## TODO

Functions that will be implemented in future collected in
[TODO.md](https://github.com/igormukhingmailcom/sublimetext3-symfony2-override-package/blob/master/TODO.md).

## Installation

### Manual

```bash
cd ~/.config/sublime-text-3/Packages
git clone https://github.com/igormukhingmailcom/sublimetext3-symfony2-override-package.git "Symfony2 Override"
```

### Via Package Control

Install [Package Control](https://packagecontrol.io/installation) in your Sublime Text.

Press `Ctrl+Shift+P`, type `Install Package`, press `Enter`, type `Symfony2 Override`, press `Enter`.

## Usage

### Override current file

Press `ctrl+shift+o` on Linux and select a bundle to copy current file to.

Also `Override...` menu item available at Context Menu, Side Bar Menu and Main Menu -> File.

If file already overriden, it will be just opened.

## License

MIT
