from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]

setup(
    name = 'pyclimb',
    version = '0.0.1',
    description = 'A package to scrape, clean, and vizualize data from mountainproject.com',
    author = 'Hayden Crofts and Riley Wilkinson',
    author_email = 'rileyw@byu.edu',
    install_requires = parse_requirements('requirements.txt'),
    url = 'https://github.com/quintbro/Climbing_and_Climate',
    packages=find_packages(exclude=['tests', 'Presentation', 'In_Progess_Files']),
)