from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='harditools',
      version='0.1',
      description='Tools for processing HARDI diffusion MRI data',
      long_description=readme(),
      url='https://github.com/scott-trinkle/hardi',
      author='Scott Trinkle',
      author_email='tscott.trinkle@gmail.com',
      license='MIT',
      packages=['harditools'],
      package_dir={'harditools': 'harditools'},
      package_data={'harditools': ['data/*']},
      install_requires=['numpy', 'dipy', 'nibabel'],
      zip_safe=False)
