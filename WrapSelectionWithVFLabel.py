import sublime, sublime_plugin

class WrapSelectionWithVfLabelCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# we might have multiple regions 
		for region in self.view.sel():

			self.view.replace(edit, region, '{_"' + self.view.substr(region) + '"_}')

			pass