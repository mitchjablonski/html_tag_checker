class HtmlTagMatcher(object):
    def __init__(self,
                file_name: str):
        self.file_name = file_name
        self.html_begin_tags = []
    
    def clean_string(self, to_clean: str) -> bool:
        return to_clean.replace("<", "").replace(">", "").replace("/", "")
    
    def check_end_tag(self, to_check: str) -> bool:
        return to_check.startswith('</')
    
    def check_begin_tag(self, to_check: str) -> bool:
        return to_check.startswith('<')

    def remove_matching_begin_tag(self, tag_to_check: str):
        for idx, current_begin_tag in enumerate(self.html_begin_tags):
            if tag_to_check == current_begin_tag:
                self.html_begin_tags.pop(idx)
                return True
        return False

    def check_valid_file(self) -> bool:
        file_contents = self.read_file()
        for line in file_contents:
            cleaned_string = self.clean_string(line)
            if self.check_end_tag(line):
                if not self.remove_matching_begin_tag(cleaned_string):
                    return False
            elif self.check_begin_tag(line):
                self.html_begin_tags.append(cleaned_string)
        if self.html_begin_tags:
            return False
        return True

    def read_file(self):
        with open(self.file_name) as f:
            f_contents = f.readlines()
        return f_contents

def _main():
    current_file = 'index.html'
    tag_matcher = HtmlTagMatcher('index.html')
    result = tag_matcher.check_valid_file()
    print(f"{current_file} {result}")
    assert(result== True)
    current_file = 'index_missing_begin.html'
    tag_matcher = HtmlTagMatcher(current_file)
    result = tag_matcher.check_valid_file()
    print(f"{current_file} {result}")
    assert(result == False)
    current_file = 'index_missing_end.html'
    tag_matcher = HtmlTagMatcher(current_file)
    result = tag_matcher.check_valid_file()
    print(f"{current_file} {result}")
    assert(tag_matcher.check_valid_file() == False)

if __name__ == "__main__":
    _main()