import sublime
import sublime_plugin


class HandyllmInsertFrontmatterCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.view.sel().clear()
		# move to top
		self.view.sel().add(0)
		# insert snippet
		self.view.run_command('insert_snippet', {'name': 'Packages/HandyLLM/Snippets/frontmatter.sublime-snippet'})
