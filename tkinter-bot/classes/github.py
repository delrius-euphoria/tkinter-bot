import requests


class GitHub:
    """Class that handle github code blobs"""

    def __init__(self):
        self.URL = "https://raw.githubusercontent.com/{}"

    def validate_link(self, url: str) -> bool:
        """Checks if the link is a valid github link"""
        return "github.com" in url

    def get_code_block(self, url: str) -> tuple[list, str]:
        """Function to return the code from the requested github url"""
        code_lst = []

        line = url.split("#L")[1:]
        parts = url.replace("/blob", "")
        data = parts.split("github.com/")[-1]
        code_url = self.URL.format(data)
        info_str = self.get_repo_info(code_url)

        if len(line) > 1:
            n1, n2 = int(line[0].replace("-", "")), int(line[1]) + 1

            if n1 < n2:
                num_range = range(n1, n2)
            else:
                num_range = range(n2 - 1, n1 + 1)

            looper = num_range
        else:
            looper = line

        for i in looper:  # IMPROVE EFFICIENCY
            code = (
                requests.get(code_url).content.decode("utf-8").split("\n")[int(i) - 1]
            )  # NOT FOUND ERROR
            code_lst.append(code)

        return code_lst, info_str

    def get_repo_info(self, url: str) -> tuple[str, str]:
        """Returns info about the github code block"""
        url = url.replace("https://raw.githubusercontent.com/", "")
        parts = url.split("/")[3:]
        file_data = "/".join(parts).split("#")
        file_path = file_data[0]
        lang = file_path.split(".")[-1]
        line = file_data[1:]

        if len(line) > 1:
            line_count = "lines"
        else:
            line_count = "line"

        line_info = f"{line_count} {''.join(''.join(line).split('L'))}"
        data_string = f"`{file_path}` {line_info}"

        return data_string, lang
