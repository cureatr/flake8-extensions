from setuptools import setup, find_packages

setup(
    name='cureatr-flake8-print',
    description="cureatr print statement and print functionn checker plugin for flake8",
    version='1.0',
    author='Levi McDonough',
    author_email='levi@cureatr.com',
    py_modules=['cureatr_flake8_extensions.cureatr_print_linter'],
    zip_safe=False,
    packages=find_packages(exclude=['tests*']),
    install_requires=['flake8', 'setuptools'],
    entry_points={
        'flake8.extension': [
            'cureatr_flake8_print = cureatr_flake8_extensions.cureatr_print_linter:CureatrPrintLinter',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
        ],
)
