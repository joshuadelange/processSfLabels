import sublime, sublime_plugin, re

class processSfLabelsCommand(sublime_plugin.TextCommand):

	edit = {}
	view_size = 0

	opening_tag = '{_"'
	ending_tag = '"_}'

	vf_opening_tag = '{!$Label.'
	vf_ending_tag = '}'

	labels = []

	def log(self, msg):

		self.view.insert(self.edit, self.view_size, "\n" + msg)


	def processNextLabel(self, unchecked_buffer):

		start_of_label_region = unchecked_buffer.find(self.opening_tag)
		end_of_label_region = unchecked_buffer.find(self.ending_tag)

		label_region = sublime.Region(start_of_label_region + len(self.opening_tag), end_of_label_region)
		label_text = unchecked_buffer[start_of_label_region + len(self.opening_tag):end_of_label_region]
		label_camel_case = re.sub(r'\W+', '', ''.join(x for x in label_text.title() if not x.isspace()))

		self.log("FOUND: '" + label_text + "'")
		self.log("Camelcase: '" + label_camel_case + "'")
		self.log("---------------------")

		unchecked_buffer = unchecked_buffer[end_of_label_region + len(self.ending_tag):]

		if (unchecked_buffer.find(self.opening_tag) > 0):

			self.processNextLabel(unchecked_buffer)


	def run(self, edit):

		self.edit = edit
		self.view_size = self.view.size()

		self.view.replace(edit, sublime.Region(0, self.view_size), '<p>{_"Label text here!"_}</p>\n<p>{_"Second label!"_}</p>\n<div>{_"Another label here!"_}</div>\n\n')

		unchecked_buffer = self.view.substr(sublime.Region(0, self.view_size))
		self.processNextLabel(unchecked_buffer)
