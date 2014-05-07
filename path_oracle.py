import sublime, sublime_plugin
import os


class PathOracle(sublime_plugin.EventListener):

    def valid_scope(self, scope):
        # Receives a scope and returns whether or not we
        # should auto-complete for paths.
        # For now, we only want to auto-complete paths inside
        # of strings. 
        
        return "string" in scope

    def on_query_completions(self, view, prefix, locations):
        cursor_pos = view.sel()[0].begin()
        current_scope = view.scope_name(cursor_pos)

        if self.valid_scope(current_scope):
            return [("zoobooks", "zoobooks")]
