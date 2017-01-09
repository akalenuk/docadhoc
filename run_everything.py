import web
import os
import re
        
urls = ('/(.*)', 'serve_doc')
app = web.application(urls, globals())

header = '<!DOCTYPE html><html><head><link rel="icon" href="/static/favicon.ico" type="image/x-icon"><link rel="stylesheet" href="/static/default.css"></head><body>'
footer = '<form action="/" method="POST"><input type="text" name="search" /><input type="submit" value="?" /></form></body></html>'
texts = ['dah', 'txt', 'h', 'cpp', 'hxx', 'txx']
images = ['jpg', 'png', 'gif', 'bmp', 'tif']

class serve_doc:        
    def GET(self, path):
	if not path:
		raise web.redirect('/docadhoc')
	path.replace('.', '')
        full_path = './static/' + path
	files_and_dirs = sorted(os.listdir(full_path))
	page = header
	page += '<h1>' # breadcrumbs
	subpath = ''
	for place in path.split('/')[:-1]:
		subpath += '/' + place
		page += '<a href="' + subpath + '">' + place + '</a> / '
	page += path.split('/')[-1] + '</h1>'
	page += '<ul>' # directories
	for file_or_dir in files_and_dirs:
		if os.path.isdir(full_path + '/' + file_or_dir):
			page += '<li><a href="/' + path + '/' + file_or_dir + '">' + file_or_dir + '</a></li>'
	page += '</ul>'
	page += '<ol>' # files
	no = 0
	for file_or_dir in files_and_dirs:
		if os.path.isfile(full_path + '/' + file_or_dir):
			no += 1
			page += '<li><a name="' + str(no) + '"></a>'
			page += '<a href="/static/' + path + '/' + file_or_dir + '">' + file_or_dir + '</a>'
			if file_or_dir.split('.')[-1] in texts:
				page += '<br /><pre>' + open(full_path + '/' + file_or_dir, 'r').read() + '</pre>'
			if file_or_dir.split('.')[-1] in images:
				page += '<br /><img src="/static/' + path + '/' + file_or_dir + '" />'
			page += '</li>'
	page += '</ol>'
	return page + footer

    def POST(self, _):
	search_for = web.data().split('search=')[1]
	page = header
	page += '<h1><a href="/">docadhoc</a> ? ' + search_for + '</h1>'
	page += '<ul>' # search results
	for path, dirs, files in os.walk('./static/docadhoc'):
		for file_name, no in zip(sorted(files), range(1, len(files) + 1)):
			if re.search(search_for, file_name) or (file_name.split('.')[-1] in texts and re.search(search_for, open(path + '/' + file_name, 'r').read())):
				short_path = path[len('./static'):]
				page += '<li><a href="' + short_path + '#' + str(no) + '">' + short_path + '/' + file_name + '</a></li>'
	page += '</ul>'
        return page + footer


if __name__ == "__main__":
    app.run()
