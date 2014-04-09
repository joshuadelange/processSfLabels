import sublime, sublime_plugin, re

class processSfLabelsCommand(sublime_plugin.TextCommand):

	edit = {}
	view_size = 0
	entire_buffer_region = sublime.Region(0, 0)

	opening_tag = '{_"'
	ending_tag = '"_}'

	vf_opening_tag = '{!$Label.'
	vf_ending_tag = '}'

	labels = []

	def log(self, msg):

		self.view.insert(self.edit, self.view_size, "\n" + msg)


	def processNextLabel(self):

		start_of_label = self.view.substr(self.entire_buffer_region).find(self.opening_tag)
		end_of_label = self.view.substr(self.entire_buffer_region).find(self.ending_tag)

		self.log("start of label: '" + str(start_of_label) + "'")
		self.log("end of label: '" + str(end_of_label) + "'")

		label_region = sublime.Region(start_of_label + len(self.opening_tag), end_of_label)
		label_region_to_be_replaced = sublime.Region(start_of_label, end_of_label + len(self.ending_tag))

		label_text = self.view.substr(label_region)
		label_camel_case = re.sub(r'\W+', '', ''.join(x for x in label_text.title() if not x.isspace()))

		self.log("FOUND: '" + label_text + "'")
		self.log("Camelcase: '" + label_camel_case + "'")
		self.log("---------------------")

		self.view.replace(self.edit, label_region_to_be_replaced, self.vf_opening_tag + label_camel_case + self.vf_ending_tag)

		self.log("for next time: " + str(self.view.substr(self.entire_buffer_region).find(self.opening_tag)))

		if (self.view.substr(self.entire_buffer_region).find(self.opening_tag) > 0):

			self.processNextLabel()


	def run(self, edit):

		self.edit = edit
		self.view_size = self.view.size()

		self.entire_buffer_region = sublime.Region(0, self.view_size)

		self.view.replace(edit, sublime.Region(0, self.view_size), '<p>{_"Label text here!"_}</p>\n<p>{_"Second label!"_}</p>\n<div>{_"Another label here!"_}</div>\n\n')

		self.processNextLabel()
