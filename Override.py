import sublime
import sublime_plugin
import os
import re
import sys
import shutil
import functools
import fileinput

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

    def is_views_file_path(self, file_path):
        return file_path[:15] == 'Resources/views'

    def is_translations_file_path(self, file_path):
        return file_path[:22] == 'Resources/translations'

    def is_public_file_path(self, file_path):
        return file_path[:16] == 'Resources/public'

    def is_app_destination(self, destination_root):
        return '/app' == destination_root[-4:]

    def can_override_to_app(self, file_path):
        return self.is_views_file_path(file_path) or self.is_translations_file_path(file_path)

    def get_project_paths(self, path, root_path = 'vendor', namespace_include_file=False):
        file_path = os.path.basename(path)
        project_root = os.path.dirname(path)
        bundle_root = ''
        bundle_name = ''
        bundle_namespace = ''

        i = 0
        while i < 20:
            i+=1
            project_root, tail = os.path.split(project_root)

            if bundle_root == '':
                file_path = os.path.join(tail, file_path)

                if 'Bundle' == project_root[-6:]:
                    bundle_root = project_root
                    bundle_name = os.path.basename(bundle_root)

                    # Get vendor name
                    vendor_root, _ = os.path.split(project_root)
                    vendor_name = os.path.basename(vendor_root)
                    bundle_namespace = os.path.join(bundle_name, file_path)

                    if 'Bundle' == vendor_name:
                        vendor_root, _ = os.path.split(vendor_root)
                        vendor_name = os.path.basename(vendor_root)
                        bundle_namespace = os.path.join(vendor_name, 'Bundle', bundle_namespace)
                    else:
                        bundle_namespace = os.path.join(vendor_name, bundle_namespace)

                    bundle_namespace = self.extract_namespace_from_path(bundle_namespace, namespace_include_file)

            if tail in [root_path, 'vendor']:
                break;

            if '/' == project_root:
                raise NotSf2BundleError('This path is not inside vendors directory')

        file_name = os.path.basename(file_path)
        _, ext = os.path.splitext(file_name)

        if '' == bundle_name:
            raise NotSf2BundleError('This path is in vendors, but not inside PSR-0 Symfony2 Bundle directory')

        return project_root, bundle_root, vendor_name, bundle_namespace, bundle_name, file_path, file_name, ext[1:]

    def extract_namespace_from_path(self, bundle_namespace, include_filename=False):
        bundle_filename = ''

        if include_filename:
            # Extract filename without extension
            bundle_filename = os.path.basename(bundle_namespace)
            bundle_filename, ext = os.path.splitext(bundle_filename)
            bundle_filename = '/' + bundle_filename

        bundle_namespace = os.path.dirname(bundle_namespace)
        bundle_namespace = bundle_namespace + bundle_filename
        bundle_namespace = bundle_namespace.replace('/', '\\')
        return bundle_namespace

    # Replace old namespace to new one
    # Paste `use` statement with source class as base class
    # Replace extended class to base class
    def namespace_convert_in_file(self, source_namespace, dest_namespace, dest_filename):

        _, tail = os.path.split(dest_filename)
        class_name, ext = os.path.splitext(tail)

        file_descriptor = open(dest_filename,'r')
        file_content = file_descriptor.read()
        file_descriptor.close()

        # Replace old namespace to new
        dest_namespace = dest_namespace + ";\n\nuse " + source_namespace + "\\" + class_name + " as Base" + class_name
        new_content = file_content.replace(source_namespace, dest_namespace)

        # Add or replace extended class name
        find_extended = "class " + class_name + " extends"
        find_simple = "class " + class_name
        replace = "class " + class_name + " extends Base" + class_name


        if new_content.find(find_extended) > -1:
            new_content = re.sub(find_extended + "\s(.+)", replace, new_content)
        else:
            new_content = re.sub(find_simple, replace, new_content)

        file_descriptor = open(dest_filename,'w')
        file_descriptor.write(new_content)
        file_descriptor.close()

    def override_to_path(self, path, destination_root):
        try:
            project_root, bundle_root, vendor_name, bundle_namespace, bundle_name, file_path, file_name, file_ext = self.get_project_paths(path)

            if self.is_app_destination(destination_root):
                if self.is_views_file_path(file_path):
                    dest_filename = os.path.join(destination_root, file_path.replace('Resources/views', 'Resources/' + vendor_name + bundle_name + '/views'))
                elif self.is_translations_file_path(file_path):
                    dest_filename = os.path.join(destination_root, file_path.replace('Resources/translations', 'Resources/' + vendor_name + bundle_name + '/translations'))
                else:
                    raise UnsupportedFileTypeError("You can't override files with " + file_ext + " extension to " + destination_root + " folder")
            elif self.is_public_file_path(file_path) or file_ext in ['php', 'twig', 'yml', 'xliff']:
                dest_filename = os.path.join(destination_root, file_path);
            else:
                raise UnsupportedFileTypeError('Unsupported File Type')

            dest_dirname = os.path.dirname(dest_filename)
            if not os.path.isdir(dest_dirname):
                os.makedirs(dest_dirname)

            if os.path.exists(dest_filename):
                print('File', dest_filename, 'already exists.')
            else:
                shutil.copy(path, dest_filename)

                if not self.is_app_destination(destination_root) and file_ext in ['php']:
                    # Get new namespace
                    _, _, _, dest_namespace, _, _, _, _ = self.get_project_paths(dest_filename, 'src')
                    self.namespace_convert_in_file(bundle_namespace, dest_namespace, dest_filename)

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

        destination_root = self.bundles[index];
        self.override_to_path(path, destination_root)

    def is_src_bundle_directory(self, directory):
        return 'Bundle' == directory[-6:] and os.path.isdir(directory)

    def is_src_vendor_directory(self, directory):
        return 'Bundle' != directory[-6:] and os.path.isdir(directory)

    def get_bundles(self, path):
        project_root, bundle_root, vendor_name, bundle_namespace, bundle_name, file_path, file_name, file_ext = self.get_project_paths(path)
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

        # We can override views and translations in app/ directory
        if self.can_override_to_app(file_path):
            self.bundles.append(os.path.join(project_root, 'app'))
            bundles.append('app')

        return bundles

    def run(self, paths=[], parameters=None):
        path = self.get_path(paths)
        if not path:
            return

        try:
            bundles = self.get_bundles(path)
            self.window.show_quick_panel(bundles, functools.partial(self.override_to_bundle, path), 0)
        except Exception as e:
            sublime.error_message(str(e))
