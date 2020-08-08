# cURL-light
python library for transferring data specified with URL syntax using cURL.
Curl is a python library and a command line tool for transferring data 
specified with URLsyntax. Find out how to use curl by reading the curl  
help page or the [api](https://github.com/Ksengine/cURL-light/blob/master/api.md)

libcurl is the library curl is using to do its job. its heavy for python
*so I made this for you**

## Example

```python
import curl
s, data = curl.get('https://w3schools.com')
print(s)
print(data)
```

## NOTICE

Curl contains pieces of source code that is Copyright (c) 1998, 1999
Kungliga Tekniska Högskolan. This notice is included here to comply with the
distribution terms.
cURL-light is licensed under MIT.
