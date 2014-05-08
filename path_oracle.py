import sublime, sublime_plugin
import os


class PathOracle(sublime_plugin.EventListener):

    def get_preceding_str(self, view, cursor_pos, scope):
        # Determine if we are in a double or single quoted string
        if "double" in scope:
            quote_char = "\""
        else:
            quote_char = "\'"

        prec_str = ""

        # Add all the letters to our result until we hit 
        # the quote char
        while view.substr(cursor_pos - 1) != quote_char:
            prec_str = prec_str + view.substr(cursor_pos - 1)
            cursor_pos -= 1

        # Reverse the string because we built it backwards
        return prec_str[::-1]

    def get_path_completions(self, view, context):
        # Gets path completions based on the location of
        # the current file and the preceding text

        # Get the current directory of the file being
        # edited
        current_file = view.file_name()
        current_dir = os.path.dirname(current_file)


        # If there is a file separator in the preceding string
        # we should check if a valid directory precedes it
        # otherwise try and populate completions from the current
        # directory
        if os.sep in context:

            # Strip everything trailing past the last separator
            split_path = context.split(os.sep)
            context_dir = os.sep.join(split_path[:-1])

            # If the path begins with . or .. we need to prepend
            # the current directory or they refer to the Sublime
            # installation directory
            if split_path[0] == "." or split_path[0] == "..":

                # Check to make sure we can find the current file
                if current_file != None:
                    context_dir = current_dir + os.sep + context_dir
                    print(context_dir)
                else:
                    return []

            # If it's an existing directory this is the one
            # we should search for completions
            # Otherwise don't return any completions
            if os.path.isdir(context_dir):
                print(context_dir)
                search_dir = context_dir
            else:
                return []
        else: 
            # Unsaved files will not have a file location
            if current_file != None:
                search_dir = current_dir
            else:
                # If we can't get the current view's file location, return
                # no completions
                # TODO: Check for project folder
                return []

        #print("SEARCHING: " + search_dir)
        #print(os.listdir(search_dir))
        # Return a list of tuples of each file in the directory
        # to populate the completions list
        return [(file, file) for file in os.listdir(search_dir)]

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
            # Get the preceding contents of the string we are in
            context = self.get_preceding_str(view, cursor_pos, current_scope)

            return self.get_path_completions(view, context)
