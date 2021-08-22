# flask_trace
tldr: flask webapp that returns info about incoming request like headers and ip.  


This flask webapp echos information about incoming requests in different formats.  It returns the headers of incoming connections in plain text and json.  It also 
returns the seen ip of incoming connections in plain text.  It supports 'GET', 'POST', 'OPTIONS', 'TRACE' methods.  There isnt really any reason it cant support others,
just didnt think they would be used as much.  On reciving an unsupported method it returns an error message showing allowed methods.
