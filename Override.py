import sublime
import sublime_plugin
import os
import shutil

class NotSf2BundleError(Exception):
    pass

class UnsupportedFileTypeError(Exception):
    pass

class SymfonyOverrideCommand():
    def get_path(self, paths):
        if paths:
            return paths[0]
        elif self.window.active_view():
            return self.window.active_view().file_name()
        # elif self.window.folders():
        #     return self.window.folders()[0]
        else:
            sublime.error_message('Symfony Override: No file to override')
            return False

    def get_project_paths(self, path):
        file_path = os.path.basename(path)
        project_root = os.path.dirname(path)
        bundle_root = ''
        bundle_name = ''

        while True:
            (project_root, tail) = os.path.split(project_root)

            if bundle_root == '':
                file_path = os.path.join(tail, file_path)
                if 'Bundle' == project_root[-6:]:
                    bundle_root = project_root
                    bundle_name = os.path.basename(bundle_root)

                    # Get vendor name
                    (vendor_root, tail) = os.path.split(project_root)
                    vendor_name = os.path.basename(vendor_root)

                    if ('Bundle' == vendor_name):
                        (vendor_root, tail) = os.path.split(vendor_root)
                        vendor_name = os.path.basename(vendor_root)

            if 'vendor' == tail:
                break;

            if '/' == project_root:
                raise NotSf2BundleError('This path is not inside vendors directory')

        (_, ext) = os.path.splitext(file_path)

        if '' == bundle_name:
            raise NotSf2BundleError('This path is in vendors, but not inside PSR-0 Symfony2 Bundle directory')

        return project_root, bundle_root, vendor_name, bundle_name, file_path, ext[1:]

    def do_override(self, path, to):
        try:
            (project_root, bundle_root, vendor_name, bundle_name, file_path, file_ext) = self.get_project_paths(path)
            print (to, project_root, bundle_root, vendor_name, bundle_name, file_path, file_ext)
            if '/app' == to[-4:]:
                if file_ext in ['twig']:
                    dest_filename = os.path.join(to, file_path.replace('Resources/views', 'Resources/' + vendor_name + bundle_name + '/views'));
                else:
                    raise UnsupportedFileTypeError("You can't override files with " + file_ext + " extension to " + to + " folder")
            elif file_ext in ['php', 'twig']:
                dest_filename = os.path.join(to, file_path);
            else:
                raise UnsupportedFileTypeError('Unsupported File Type')

            dest_dirname = os.path.dirname(dest_filename)
            if not os.path.isdir(dest_dirname):
                os.makedirs(dest_dirname)

            if os.path.exists(dest_filename):
                print('File', dest_filename, 'already exists.')
            else:
                shutil.copy(path, dest_filename)

                if os.path.isfile (dest_filename):
                    print('File', dest_filename, 'successfully created!')

            self.window.open_file(dest_filename)
        except Exception as e:
            sublime.error_message(str(e))
            return False


class SymfonyOverrideFileCommand(sublime_plugin.WindowCommand, SymfonyOverrideCommand):
    bundles = []

    def override_to_bundle(self, path, index):
        if index == -1:
            return

        to = self.bundles[index];
        self.do_override(path, to)

    def is_src_bundle_directory(self, directory):
        return 'Bundle' == directory[-6:] and os.path.isdir(directory)

    def is_src_vendor_directory(self, directory):
        return 'Bundle' != directory[-6:] and os.path.isdir(directory)

    def get_bundles(self, path):
        project_root, bundle_root, vendor_name, bundle_name, file_path, file_ext = self.get_project_paths(path)
        src_root = os.path.join(project_root, 'src')

        bundles = []

        # Scan src/ directory
        bundles += [f for f in os.listdir(src_root) if self.is_src_bundle_directory(src_root + '/' + f)]

        # Scan src/Vendor directories
        vendors = [f for f in os.listdir(src_root) if self.is_src_vendor_directory(src_root + '/' + f)]
        for vendor in vendors:
            vendor_root = src_root + '/' + vendor
            bundles += [vendor + '/' + f for f in os.listdir(vendor_root) if self.is_src_bundle_directory(vendor_root + '/' + f)]
        bundles.sort()

        self.bundles = [src_root + '/' + str(f) for f in bundles]

        # We can override templates in app/ directory
        if file_ext in ['twig']:
            self.bundles.append(os.path.join(project_root, 'app'))
            bundles.append('app')

        return bundles

    def run(self, paths=[], parameters=None):
        import functools

        path = self.get_path(paths)
        if not path:
            return

        try:
            bundles = self.get_bundles(path)
            self.window.show_quick_panel(bundles, functools.partial(self.override_to_bundle, path), 0)

        except Exception as e:
            sublime.error_message(str(e))
