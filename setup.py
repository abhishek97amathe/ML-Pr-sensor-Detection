def get_requirements(file_path:str)->list[str]:
    requirements = []
    with open(file_path)as file_obj:
        requirements = file_obj.readlines()
        requirements=[req.replace('\n','') for req in requirements]
    return requirements

from setuptools import setup, find_packages
from typing import List
setup(
    name ='Fault Detection',
    version = '0.1',
    packages = find_packages(),
    author = 'Abhishek Amathe',
    author_email = 'abhishekamathe@gmail.com',
    install_requires = get_requirements('requirements.txt')
)
    
