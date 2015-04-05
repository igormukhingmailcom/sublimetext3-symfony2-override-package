# Symfony2 Override

Sublime Text 3 Package for easy overriding files from Symfony2 bundles.

It greatly simplifies the work with bundles, that have files with a high level of nesting.

## Features

At this time, package can override php files, twig templates and translations in any format.

For example, it can:
- Copy Twig templates from `vendor/Vendor/BundleName/Resources/views/High/Nesting/Level/template.html.twig` to `app/Resources/VendorBundleName/views/High/Nesting/Level/template.html.twig` or `src/SelectedBundleName/Resources/views/High/Nesting/Level/template.html.twig`.
- Copy `.xliff`, `.yml`, `.php` or whatever files from `vendor/Vendor/BundleName/Resources/translations/whatever.yml` to `src/SelectedBundleName/Resources/translations/whatever.yml` or `app/Resources/SelectedBundleName/translations/whatever.yml`.
- Copy `.php` files from `vendor/Vendor/BundleName/High/Nesting/Level/Whatever.php` to `src/SelectedBundleName/High/Nesting/Level/Whatever.php`.

After file have been copied, it automatically opens in editor.

## TODO

Another functions that will be implemented collected in
[TODO.md](https://github.com/igormukhingmailcom/sublimetext3-symfony2-override-package/TODO.md).

## Installation

### Manual

```bash
cd ~/.config/sublime-text-3/Packages
git clone https://github.com/igormukhingmailcom/sublimetext3-symfony2-override-package.git "Symfony2 Override"
```

## Usage

### Override current file

Press `ctrl+shift+o` on Linux and select a bundle to copy current file to.

Also `Override...` menu item available at Context Menu, Side Bar Menu and Main Menu -> File.

If file already overriden, it will be just opened.

## License

MIT
