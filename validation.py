class Validation(object):
    SplitHeader = ":param:"
    SplitKey = "|"
    SplitNum = 2
    TypeList = ["str", "int", "float", "dict"]
    RequiredKey = "required"

    def __init__(self, func, *args, **kwargs):
        if not hasattr(func, '__call__'):
            raise TypeError("Function is error")
        self.func = func
        self.line = self.msg = ""
        self.param_name = ""
        self.validate_pass = True

    def validate_format(self, validated, *args, **kwargs):
        param_str = self.line.replace(self.SplitHeader, "")
        separator_num = param_str.count(self.SplitKey)
        if separator_num < self.SplitNum:
            raise TypeError("Doc format is error")
        validator = param_str.split(self.SplitKey)
        param_type = ''.join(validator[2].split())
        param = ''.join(validator[0].split())
        self.param_name = param
        if separator_num >= 3:
            self.param_name = ''.join(validator[3].split())
        if param_type not in self.TypeList:
            raise TypeError("Param type not in {}".format(self.TypeList))
        if not isinstance(validated.get(param), eval(param_type)):
            self.msg += "{} type is error\n".format(self.param_name)
            return
        if self.RequiredKey in ''.join(validator[1].split()):
            if not validated.get(param):
                self.msg += "{} is empty\n".format(self.param_name)
                self.validate_pass = False

    def validation(self, validated, *args, **kwargs):
        if not isinstance(validated, dict):
            raise TypeError("validated is error")
        for line in self.func.__doc__.splitlines():
            if self.SplitHeader in line:
                self.line = line
                self.validate_format(validated)


if __name__ == '__main__':
    def test_fuc():
        """
        :param:user_name|required|str
        :param:password||int
        :return:
        """


    v = Validation(test_fuc)
    v.validation({
        "user_name": "",
        "password": 0
    })
    print(v.msg)
