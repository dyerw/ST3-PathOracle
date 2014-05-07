import sublime, sublime_plugin
import os


class PathOracle(sublime_plugin.EventListener):

    def valid_scope(self, scope):
        # Receives a scope and returns whether or not we
        # should auto-complete for paths.
        # We only want to auto-complete paths inside
        # of strings. 
        
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
            return [("zoobooks", "zoobooks")]
