def write_file(self, content):
    with open("../dataset/.txt", "w") as text_file:
        text_file.write(content)
