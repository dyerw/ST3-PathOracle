import sublime, sublime_plugin
import os


class PathOracle(sublime_plugin.EventListener):

    def get_path_completions(self, view, prefix):
        # Gets path completions based on the location of
        # the current file and the preceding text

        # Gets the file location of the current file
        current_file = view.file_name()

        # Unsaved files will not have a file location
        if current_file != None:
            # Get the current directory of this file
            current_dir = os.path.dirname(current_file)

            # Return a list of tuples of each file in the directory
            # to populate the completions list
            return [(file, file) for file in os.listdir(current_dir)]
        else:
            # If we can't get the current view's file location, return
            # no completions
            return []

    def valid_scope(self, scope):
        # Receives a scope and returns whether or not we
        # should auto-complete for paths.
        # We only want to auto-complete paths inside
        # of strings. 
        
        # Our scope will contain the string "string" if we are in
        # a string (say that ten times fast)
        return "string" in scope

    def on_query_completions(self, view, prefix, locations):
        # Fires whenever the autocomplete looks for a list of
        # completions.

        # Get the current cursor position, we grab the selections
        # from the view and take the first selection, then take
        # its beginning coordinate.
        cursor_pos = view.sel()[0].begin()

        # Get our current scope based on the cursor position
        current_scope = view.scope_name(cursor_pos)

        # We only want to populate the autocomplete if we are
        # in a context where a path would be appropriate
        if self.valid_scope(current_scope):
            return self.get_path_completions(view, prefix)
