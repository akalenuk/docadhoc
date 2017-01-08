import web
import os
        
urls = (
    '/(.*)', 'serve_doc'
)
app = web.application(urls, globals())

class serve_doc:        
    def GET(self, path):
	path.replace('.', '')
	if path:
		path += '/'
        full_path = './static/docadhoc/' + path
	page = ''

	page += '<h1>'
	subpath_place = [('/', '~')]
	subpath = ''
	for place in path.split('/')[:-1]:
		subpath += '/' + place
		subpath_place += [(subpath, place)] 
	for (subpath, place) in subpath_place[:-1]:
		page += '<a href="' + subpath + '">' + place + '</a> / '
	(subpath, place) = subpath_place[-1]
	page += place + '</h1>'
	
	files_and_dirs = sorted(os.listdir(full_path))

	page += '<ul>'
	for file_or_dir in files_and_dirs:
		print full_path + file_or_dir
		if os.path.isdir(full_path + file_or_dir):
			page += '<li><a href="/' + path + file_or_dir + '">' + file_or_dir + '</a></li>'
	page += '</ul>'

	page += '<ol>'
	for file_or_dir in files_and_dirs:
		if os.path.isfile(full_path + file_or_dir):
			page += '<li><a href="/static/docadhoc/' + path + file_or_dir + '">' + file_or_dir + '</a>'
			if file_or_dir.endswith('.dah'):
				page += '<br /><pre>' + open(full_path + file_or_dir, 'r').read() + '</pre>'
			if file_or_dir.endswith('.jpg') or file_or_dir.endswith('.png') or file_or_dir.endswith('.gif'):
				page += '<br /><img src="' + full_path + file_or_dir + '" />'
			page += '</li>'
	page += '</ol>'

        return page

if __name__ == "__main__":
    app.run()
