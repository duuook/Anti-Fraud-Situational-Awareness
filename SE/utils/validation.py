import re


# 电话号码校验
def is_all_digits(s):
    return s.isdigit()


# 邮箱号校验
def is_valid_email(email):
    pattern = r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    if re.match(pattern, email):
        return True
    else:
        return False


# 网址校验
def is_valid_url(url):
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    if re.match(pattern, url):
        return True
    else:
        return False
