import urllib.request
import socket
import urllib.error

def is_bad_proxy(pip):    
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req=urllib.request.Request('http://google.com')  # change the URL to test here
        sock=urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    return False

def main():
    socket.setdefaulttimeout(120)

    f = "proxylist.txt"
    with open(f) as fp:
        for currentProxy in fp:
            if is_bad_proxy(currentProxy):
                print("Bad Proxy %s" % (currentProxy))
            else:
                print("%s is working" % (currentProxy))
                e = open("proxies.txt", "a")
                e.write(currentProxy)

if __name__ == '__main__':
    main() 