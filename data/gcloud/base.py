# coding: utf-8
from __future__ import absolute_import
from datetime import date
from pydash import _
import re
try:
    from google.appengine.ext import ndb
except ImportError:
    print('Please make sure the App Engine SDK is in your PYTHONPATH.')
    raise


class BaseValidator(object):
    """Base factory class for creating validators for ndb.Model properties
    To be able to create validator for some property, extending class has to
    define attribute which has to be one of these:
        list - with 2 elements, determining min and max length of string
        regex - which will be validated agains string
        function - validation function

    After defining attributes we will be able to create respective validator functions.

    Examples:
        Let's say we want to create validator factory for our new model
        class MySuperValidator(BaseValidator):
            short_name = [2, 4]

        Now if we call MySuperValidator.create('short_name') it returns
         function, which will throw error of string is not between 2-4 chars
         The same goes with if short_name was regex, and if it was function,
         the function itself is returned as validator

     Creating validation functions this way is useful for passing it as
     'validator' argument to ndb.Property constructor and also passing it as 'type'
     argument to reqparse.RequestParser, when adding argument via add_argument
    """

    @staticmethod
    def create_validator(lengths=None, regex='', required=True):
        """This is factory function, which creates validator functions, which
        will then validate passed strings according to lengths or regex set at creation time

        Args:
            lengths (list): list of exact length 2. e.g [3, 7]
                indicates that string should be between 3 and 7 charactes
            regex (string): Regular expression
            required (bool): Wheter empty value '' should be accepted as valid,
                ignoring other constrains

        Returns:
            function: Function, which will be used for validating input
        """

        def constrain_string(string, minlen, maxlen):
            if len(string) < minlen:
                raise ValueError('Input need to be at least %s characters long' % minlen)
            elif len(string) > maxlen:
                raise ValueError('Input need to be maximum %s characters long' % maxlen)
            return string

        def constrain_regex(string, regex):
            regex_email = re.compile(regex, re.IGNORECASE)
            if not regex_email.match(string):
                raise ValueError('Incorrect regex format')
            return string

        def validator_function(value, prop):
            """Function validates input against constraints given from closure function
            These functions are primarily used as ndb.Property validators

            Args:
                value (string): input value to be validated
                prop (string): ndb.Property name, which is validated

            Returns:
                string: Returns original string, if valid

            Raises:
                ValueError: If input isn't valid

            """
            # when we compare ndb.Property with equal operator e.g User.name == 'abc' it
            # passes arguments to validator in different order than as when e.g putting data,
            # hence the following parameters switch
            if isinstance(value, ndb.Property):
                value = prop
            if not required and value == '':
                return ''
            if regex:
                return constrain_regex(value, regex)
            return constrain_string(value, lengths[0], lengths[1])

        return validator_function


    @classmethod
    def create(cls, name, required=True):
        """Creates validation function from given attribute name

        Args:
            name (string): Name of attribute
            required (bool, optional) If false, empty string will be always accepted as valid

        Returns:
            function: validation function
        """
        attr = getattr(cls, name)
        if _.is_list(attr):
            return cls.create_validator(lengths=attr, required=required)
        elif _.is_string(attr):
            return cls.create_validator(regex=attr, required=required)
        elif _.is_function(attr):
            return attr

    @classmethod
    def to_dict(cls):
        """Creates dict out of list and regex attributes, so it can be passed to angular
            for frontend validation

            Returns:
                dict:
        """
        result = {}
        for attr_name in _.reject(set(dir(cls)), lambda x: x.startswith('_')):
            attr = getattr(cls, attr_name)
            if _.is_list(attr) or _.is_string(attr):
                result[attr_name] = attr
        return result


class Base(ndb.Model):
    """Base model class, it should always be extended

    Attributes:
        created (ndb.DateTimeProperty): DateTime when model instance was created
        modified (ndb.DateTimeProperty): DateTime when model instance was last time modified
        version (ndb.IntegerProperty): Version of app

        PUBLIC_PROPERTIES (list): list of properties, which are accessible for public, meaning non-logged
            users. Every extending class should define public properties, if there are some
        PRIVATE_PROPERTIES (list): list of properties accessible by admin or authrorized user
    """
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    version = ndb.IntegerProperty(default=1)  # TODO change version by versioning

    PUBLIC_PROPERTIES = ['key', 'version', 'created', 'modified']
    PRIVATE_PROPERTIES = []

    def to_dict(self, include=None):
        """Return a dict containing the entity's property values, so it can be passed to client

        Args:
            include (list, optional): Set of property names to include, default all properties
        """
        repr_dict = {}
        if include is None:
            return super(Base, self).to_dict(include=include)

        for name in include:
            attr = getattr(self, name)
            if isinstance(attr, date):
                repr_dict[name] = attr.isoformat()
            elif isinstance(attr, ndb.Key):
                repr_dict[name] = self.key.urlsafe()
                repr_dict['id'] = self.key.id()
            else:
                repr_dict[name] = attr

        return repr_dict

    def populate(self, **kwargs):
        """Extended ndb.Model populate method, so it can ignore properties, which are not
        defined in model class without throwing error
        """
        kwargs = _.omit(kwargs, Base.PUBLIC_PROPERTIES + ['key', 'id'])  # We don't want to populate those properties
        kwargs = _.pick(kwargs, _.keys(self._properties))  # We want to populate only real model properties
        super(Base, self).populate(**kwargs)

    @classmethod
    def get_by(cls, name, value):
        """Gets model instance by given property name and value"""
        return cls.query(getattr(cls, name) == value).get()

    @classmethod
    def get_public_properties(cls):
        """Public properties consist of this class public properties
        plus extending class public properties"""
        return cls.PUBLIC_PROPERTIES + Base.PUBLIC_PROPERTIES

    @classmethod
    def get_private_properties(cls):
        """Gets private properties defined by extending class"""
        return cls.PRIVATE_PROPERTIES + Base.PRIVATE_PROPERTIES + cls.get_public_properties()

    @classmethod
    def get_all_properties(cls):
        """Gets all model's ndb properties"""
        return ['key', 'id'] + _.keys(cls._properties)


