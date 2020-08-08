import curl
help(curl)
def call(data):
    print(data)
a=curl.get('https://www.w3schools.com',caller=call)
