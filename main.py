import slumber
import requests
import os

show_objs = True
api = slumber.API(base_url='http://readthedocs.org/api/v1/')


def download_epub(libraries):
    for library in libraries:
        print(library.lower())
        if '==' in library:
            name, version = library.split('==')
        else:
            name, version = library.lower().strip(), 'latest'

        project = api.project.get(slug=name)
        print(project)
        if project['objects']:
            epub_url = project['objects'][0]['downloads']['epub']
            epub = requests.get('http:' + epub_url).content
            with open('%s-%s.epub' % (name, version), 'wb') as out:
                out.write(epub)


if 'requirements.txt' in os.listdir():
    with open('requirements.txt') as installed:
        libraries = installed.readlines()
        download_epub(libraries)
else:
    print('Please enter a list of libraries seperated by a comma')
    print('If you need to specify a version, please do so by:')
    print('"name==version"')
    libraries = str(input(':')).split(',')
    if libraries:
        download_epub(libraries)
    else:
        print('You did not type anything or did not use the right format.')

