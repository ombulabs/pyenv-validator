# Pyenv Validator

This package validates `.env` variables. You can configure validation rules by 
adding the appropriate comments to the `.env.example` file.

# Installation

Install the package in the desired environment:

```
pip install pyenv-validator
```

Add the package to your `requirements.txt` file:

```txt
pyenv_validator~=0.2.0
```

In your pipeline, add:

```python
from pyenv_validator import PyenvValidator
PyenvValidator.check()
```

## Updating

Simply run:

```
pip install pyenv-validator --update
```

# Configuring env variable

In your `.env.example` file, you can add comments to tell PyenvValidator how to validate the variable:

```
MY_REQUIRED_VAR=value #required
THIS_IS_AN_OPTIONAL_INT=123 #format=int
THIS_IS_A_REQUIRED_EMAIL=123 #required,format=email
```

## Formats

- `str` or `string` or `String` (accepts anything)
- `email` (checks value against `/[\w@]+@[\w@]+\.[\w@]+/`)
- `url` (checks value against `/https?:\/\/.+/`)
- `bool` or `boolean` or `Boolean` (checks value against `true` or `false`, case sensitive)
- `uuid` or `UUID` (checks value against `/\A[\da-f]{32}\z/i` or `/\A[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}\z/i`)
