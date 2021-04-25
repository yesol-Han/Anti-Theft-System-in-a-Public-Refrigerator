import requests


class mobius():
    def __init__(self):
        self.url = "http://114.71.221.47:7579/Mobius/"
        self.headers = {'Content-Type': 'text/plain', 'X-M2M-RI':'12345', 'X-M2M-Origin':'SS'}
        self.headers_get = self.headers
        self.headers_post = self.headers
        self.headers_delete = self.headers

        self.payload_get = {}
        self.payload_delete = {}

    #post
    def response_post_cin(self, url_post, con, origin):		#con type은 String 또는 str()
        self.headers_post['Content-Type'] = 'application/vnd.onem2m-res+json;ty=4'
        self.headers_delete['X-M2M-Origin'] = origin
        self.payload_post_make = "{\n    \"m2m:cin\": {\n        \"con\": \""+ con + "\"\n    }\n}"
        self.response = requests.request("POST", url_post, headers = self.headers_post, data = self.payload_post_make)
        print(self.response.text.encode('utf8'))
        return self.response.status_code, self.response.json()

    def response_post_cnt(self, url_post, rn, origin):
        self.headers_post['Content-Type'] = 'application/vnd.onem2m-res+json; ty=3'
        self.headers_delete['X-M2M-Origin'] = origin
        self.payload_post_make = "{\n  \"m2m:cnt\": {\n    \"rn\": "+ rn + "\n  }\n}"
        self.response = requests.request("POST", url_post, headers = self.headers_post, data = self.payload_post_make)
        print(self.response.text.encode('utf8'))
        return self.response.status_code, self.response.json()

    #get
    def response_get_cin(self, url_get, origin, Content_type = 'application/json'):
        self.headers_get['Content-Type'] = Content_type
        self.headers_get['X-M2M-Origin'] = origin
        self.response = requests.request("GET", url_get, headers = self.headers_get, data = self.payload_get)
#        print (self.response.text.encode('utf8'))
        return self.response.status_code, self.response.json()

    def response_get_cnt(self, url_get, origin, Content_type = 'application/json'):
        self.headers_get['Content-Type'] = Content_type
        self.headers_get['X-M2M-Origin'] = origin
        self.response = requests.request("GET", url_get, headers = self.headers_get, data = self.payload_get)
#        print (self.response.text.encode('utf8'))
        return self.response.status_code, self.response.json()

    #delete
    def response_delete_cnt(self, url_delete, origin, Content_type = 'application/json'):
        self.headers_delete['Content-Type'] = Content_type
        self.headers_delete['X-M2M-Origin'] = origin
        self.response = requests.request("DELETE", url_delete, headers = self.headers_delete, data = self.payload_delete)
#        print (self.response.text.encode('utf8'))
        return self.response.status_code, self.response.json()

    def response_delete_cin(self, url_delete, origin, Content_type = 'application/json'):
        self.headers_delete['Content-Type'] = Content_type
        self.headers_delete['X-M2M-Origin'] = origin
        self.response = requests.request("DELETE", url_delete, headers = self.headers_delete, data = self.payload_delete)
#        print (self.response.text.encode('utf8'))
        return self.response.status_code, self.response.json()
