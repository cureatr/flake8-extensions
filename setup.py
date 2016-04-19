from setuptools import setup, find_packages

install_requires = ['flake8', 'setuptools']

setup(
    name='cureatr-flake8-print',
    description="cureatr print statement and print functionn checker plugin for flake8",
    version='1.0',
    author='Levi McDonough',
    author_email='levi@cureatr.com',
    py_modules=['cureatr_flake8_print.cureatr_print_linter'],
    zip_safe=False,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'flake8.extension': [
            'cureatr_flake8_print = cureatr_flake8_print.cureatr_print_linter:CureatrPrintLinter',
        ],
    },
)
