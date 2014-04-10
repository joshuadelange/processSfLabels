import sublime, sublime_plugin, re, os.path

class processSfLabelsCommand(sublime_plugin.TextCommand):

    edit = {}
    view_size = 0
    entire_buffer_region = sublime.Region(0, 0)

    opening_tag = '{_"'
    ending_tag = '"_}'

    vf_opening_tag = '{!$Label.'
    vf_ending_tag = '}'

    labels_file = ''
    fcontents = ''

    def processNextLabel(self):

        if (self.view.substr(self.entire_buffer_region).find(self.opening_tag) > 0):

            start_of_label = self.view.substr(self.entire_buffer_region).find(self.opening_tag)
            end_of_label = self.view.substr(self.entire_buffer_region).find(self.ending_tag)

            print("start of label: '" + str(start_of_label) + "'")
            print("end of label: '" + str(end_of_label) + "'")

            label_region = sublime.Region(start_of_label + len(self.opening_tag), end_of_label)
            label_region_to_be_replaced = sublime.Region(start_of_label, end_of_label + len(self.ending_tag))

            label_text = self.view.substr(label_region)
            label_camel_case = re.sub(r'\W+', '', ''.join(x for x in label_text.title() if not x.isspace()))[:80]

            print("FOUND: '" + label_text + "'")
            print("Camelcase: '" + label_camel_case + "'")

            if(self.fcontents.find("<fullName>" + label_camel_case + "</fullName>") < 0):

                # write to xml!
                print("writing to XML")

                xml = """
    <labels>
        <fullName>""" + label_camel_case + """</fullName>
        <language>en_US</language>
        <protected>false</protected>
        <shortDescription>""" + label_camel_case + """</shortDescription>
        <value>""" + label_text + """</value>
    </labels>"""

                f = open(self.labels_file, 'a', encoding='utf-8')
                f.write(xml)
                f.close()

                print("Wrote to xml")

            else:
                print("Already in XML")


            self.view.replace(self.edit, label_region_to_be_replaced, self.vf_opening_tag + label_camel_case + self.vf_ending_tag)

            self.processNextLabel()

        else:

            print("done processing")


    def run(self, edit):

        settings = sublime.load_settings('mavensmate.sublime-settings')

        workspace = settings.get('mm_workspace')
        # hacky, but sorta works?
        project_name = sublime.active_window().project_file_name().replace('.sublime-project', '').replace(workspace, '').split('/')[0]
        self.labels_file = workspace + project_name + '/src/labels/CustomLabels.labels'

        if(os.path.isfile(self.labels_file) == False):
            # should probably error more verbose here
            print("FILE NOT FOUND")
        else:

            f = open(self.labels_file, 'r', encoding='utf-8')
            self.fcontents = f.read()
            f.close()

        print(sublime.active_window().active_view())

        print(settings.get('mm_workspace'))
        print(project_name)

        self.edit = edit
        self.view_size = self.view.size()

        self.entire_buffer_region = sublime.Region(0, self.view_size)

        self.processNextLabel()

        # horribly inefficient, but works for now ! :D
        f = open(self.labels_file, 'r', encoding='utf-8')
        data = f.read()
        f.close()

        f = open(self.labels_file, 'w', encoding='utf-8')
        f.write(data.replace('</CustomLabels>', '') + "</CustomLabels>")
        f.close()
