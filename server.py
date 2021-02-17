
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from compound import compound


class Post(BaseHTTPRequestHandler):
    def print_response(self, message, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf-8"))

    def print_error(self, message):
        self.print_response(message, 400)

    def print_result(self, message):
        self.print_response(message, 200)

    def do_POST(self):

        content_len = int(self.headers.get('Content-Length'))
        try:
            content = json.loads(self.rfile.read(content_len))
        except:
            self.print_error('Json object must be POSTed')
            return

        if not 'principal' in content.keys():
            self.print_error('Principal must be specified for interest calculation')
            return

        elif not (isinstance(content['principal'], int) or isinstance(content['principal'], float)):
            self.print_error('Principal must be a number')
            return
        else:
            principal = content['principal']

        if not 'annual_rate' in content.keys():
            self.print_error('Annual rate must be specified for interest calculation')
            return
        elif not (isinstance(content['annual_rate'], int) or isinstance(content['annual_rate'], float)):
            self.print_error('Annual rate must be a number')
            return
        else:
            annual_rate = content['annual_rate']

        if not 'years' in content.keys():
            self.print_error('Period in years must be specified for interest calculation')
            return
        elif not (isinstance(content['years'], int) or  isinstance(content['years'], float)):
            self.print_error('Years must be specified as a number')
            return
        else:
            years = content['years']

        compounds_per_year = 1
        if 'compounds_per_year' in content.keys():
            if not (isinstance(content['compounds_per_year'], int) or isinstance(content['compounds_per_year'], float)):
                self.print_error('Compounds per year must be a number')
                return
            else:
                compounds_per_year = content['compounds_per_year']


        compound_interest = compound(principal, annual_rate, years, compounds_per_year)

        self.print_result('Cumulative interest for {} loan with {}% annual rate and {} compounds per year for {} year(s) duration is {}. Deposit amount with interest is {}'\
                          .format(principal, annual_rate, compounds_per_year, years, compound_interest, principal+compound_interest))





def run(server_class=HTTPServer, handler_class=Post):
    server_address = ('0.0.0.0', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
