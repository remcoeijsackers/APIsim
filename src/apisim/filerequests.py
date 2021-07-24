from unit import request_unit

class filehandler:
    def __init__(self) -> None:
        pass

        def from_file(self, input_file, mode, url=None):
            urls_to_call = []
            data_to_push = []
            if mode == "get":
                try:
                    with open(input_file, "r") as reader:
                        for line in reader.readlines():
                            urls_to_call.append(line)
                        x = request_unit(urls_to_call, mode)
                        self.multi_request(x)

                except TypeError:
                    print("file does not exist")
                    return
            if mode == "post":
                try:
                    with open(input_file, "r") as reader:
                        for line in reader.readlines():
                            data_to_push.append(line)
                        self.multi_request(url, mode, body=data_to_push)

                except TypeError:
                    print("file does not exist")