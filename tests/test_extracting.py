# Copyright (c) 2015-2016, Activision Publishing, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from assertpy import assert_that,fail

class TestExtracting(object):

    def setup(self):
        fred = Person('Fred', 'Smith', 12)
        john = Person('John', 'Jones', 9.5)
        self.people = [fred, john]

    def test_extracting_property(self):
        assert_that(self.people).extracting('first_name').contains('Fred','John')

    def test_extracting_multiple_properties(self):
        assert_that(self.people).extracting('first_name', 'last_name', 'shoe_size').contains(('Fred','Smith',12), ('John','Jones',9.5))

    def test_extracting_zero_arg_method(self):
        assert_that(self.people).extracting('full_name').contains('Fred Smith', 'John Jones')

    def test_extracting_property_and_method(self):
        assert_that(self.people).extracting('first_name', 'full_name').contains(('Fred','Fred Smith'), ('John', 'John Jones'))

    def test_extracting_dict(self):
        people_as_dicts = [{'first_name': p.first_name, 'last_name': p.last_name} for p in self.people]
        assert_that(people_as_dicts).extracting('first_name').contains('Fred','John')
        assert_that(people_as_dicts).extracting('last_name').contains('Smith','Jones')

    def test_extracting_bad_val_failure(self):
        try:
            assert_that(123).extracting('bar')
            fail('should have raised error')
        except TypeError as ex:
            assert_that(str(ex)).is_equal_to('val is not iterable')

    def test_extracting_bad_val_str_failure(self):
        try:
            assert_that('foo').extracting('bar')
            fail('should have raised error')
        except TypeError as ex:
            assert_that(str(ex)).is_equal_to('val must not be string')

    def test_extracting_empty_args_failure(self):
        try:
            assert_that(self.people).extracting()
            fail('should have raised error')
        except ValueError as ex:
            assert_that(str(ex)).is_equal_to('one or more name args must be given')

    def test_extracting_bad_property_failure(self):
        try:
            assert_that(self.people).extracting('foo')
            fail('should have raised error')
        except ValueError as ex:
            assert_that(str(ex)).is_equal_to('val does not have property or zero-arg method <foo>')

    def test_extracting_too_many_args_method_failure(self):
        try:
            assert_that(self.people).extracting('say_hello')
            fail('should have raised error')
        except ValueError as ex:
            assert_that(str(ex)).is_equal_to('val method <say_hello()> exists, but is not zero-arg method')

    def test_extracting_dict_missing_key_failure(self):
        people_as_dicts = [{'first_name': p.first_name, 'last_name': p.last_name} for p in self.people]
        try:
            assert_that(people_as_dicts).extracting('foo')
            fail('should have raised error')
        except ValueError as ex:
            assert_that(str(ex)).matches(r'item keys \[.*\] did not contain key <foo>')

    def test_described_as_with_extracting(self):
        try:
            assert_that(self.people).described_as('extra msg').extracting('first_name').contains('Fred','Bob')
            fail('should have raised error')
        except AssertionError as ex:
            assert_that(str(ex)).is_equal_to("[extra msg] Expected <['Fred', 'John']> to contain items ('Fred', 'Bob'), but did not contain <Bob>.")

    def test_described_as_with_double_extracting(self):
        try:
            assert_that(self.people).described_as('extra msg').extracting('first_name').described_as('other msg').contains('Fred','Bob')
            fail('should have raised error')
        except AssertionError as ex:
            assert_that(str(ex)).is_equal_to("[other msg] Expected <['Fred', 'John']> to contain items ('Fred', 'Bob'), but did not contain <Bob>.")

class Person(object):
    def __init__(self, first_name, last_name, shoe_size):
        self.first_name = first_name
        self.last_name = last_name
        self.shoe_size = shoe_size

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def say_hello(self, name):
        return 'Hello, %s!' % name
