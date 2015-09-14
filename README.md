# EF Science Analytics

## Installation

Create a virtualenv directory:

    virtualenv venv

Activate virtualenv:

    source venv/bin/activate

Install dependencies

    pip install -r requirements.txt

### OS X specific

Mac users may need to uninstall lxml by

    pip uninstall lxml

and install it again using

    STATIC_DEPS=true pip install lxml
