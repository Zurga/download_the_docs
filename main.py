import slumber
import requests
import os
import sys
import getopt


api = slumber.API(base_url='http://readthedocs.org/api/v1/')


def download_epub(libraries):
    for library in libraries:
        print(library.lower())
        if '==' in library:
            name, version = library.split('==')
        else:
            name, version = library.lower().strip(), ''

        project = api.project(name).get()
        if project['objects']:
            downloads = project['objects'][0]['downloads']
            if downloads.get('epub'):
                print('Downloading %s docs for %s' % (version, name))
                doc = requests.get('http:' + downloads.get('epub')).content
                with open('%s-%s.epub' % (name, version), 'wb') as out:
                    out.write(doc)
                print('Docs saved!')
            else:
                print('Downloading %s docs for %s' % (version, name))
                doc = requests.get('http://' + downloads.get('htmlzip'))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h")
    except:
        pass
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

if __name__ == '__main__':
    main(sys.argv[1:])
