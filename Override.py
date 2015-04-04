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
            raise NotSf2BundleError('This path is in vendors, but not inside Symfony2 Bundle directory')

        return project_root, bundle_root, vendor_name, bundle_name, file_path, ext[1:]

    def do_override(self, path):
        try:
            (project_root, bundle_root, vendor_name, bundle_name, file_path, file_ext) = self.get_project_paths(path)
            if 'twig' == file_ext:
                dest_filename = os.path.join(project_root, 'app', file_path.replace('Resources/views', 'Resources/' + vendor_name + bundle_name + '/views'));
            elif 'php' == file_ext:
                dest_filename = os.path.join(project_root, 'src/AppBundle', file_path);
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

    def run(self, paths=[], parameters=None):
        path = self.get_path(paths)
        if not path:
            return

        self.do_override(path)
