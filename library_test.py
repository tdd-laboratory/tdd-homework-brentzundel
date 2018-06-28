import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Test to find a iso8601 date in text.
    def test_extract_date_iso8601(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    #Test to make sure iso8601 date has a month between 1 and 12
    def test_extract_date_iso8601_proper_month(self):
        self.assert_extract('I was born on 2015-00-25.', library.dates_iso8601)
        self.assert_extract('I was born on 2015-13-25.', library.dates_iso8601)

    #Test to make sure iso8601 date has a day between 1 and 31
    def test_extract_date_iso8601_proper_day(self):
        self.assert_extract('I was born on 2015-07-00.', library.dates_iso8601)
        self.assert_extract('I was born on 2015-07-32.', library.dates_iso8601)

    #Test to extract 'dd Mon Year' date
    def test_extract_date_no_hyphens(self):
        self.assert_extract('I was born on 25 Jan 2017', library.dates_ddMonYear)

    #Test to make sure 'dd Mon Year' date has a month between 1 and 12
    def test_extract_date_no_hyphens_proper_month(self):
        self.assert_extract('I was born on 25 Man 2017.', library.dates_ddMonYear)
        self.assert_extract('I was born on 25 Der 2017.', library.dates_ddMonYear)

    #Test to make sure 'dd Mon Year' date has a day between 1 and 31
    def test_extract_date_no_hyphens_proper_day(self):
        self.assert_extract('I was born on 0 Jan 2017.', library.dates_ddMonYear)
        self.assert_extract('I was born on 32 Jan 2017.', library.dates_ddMonYear)

    #Test to extract iso8601 dates with a timestamp separated by a space
    def test_extract_date_iso8601_with_timestamp(self):
        self.assert_extract('I was born on 2015-07-25 18:22:19.123', library.dates_iso8601, '2015-07-25 18:22:19.123')

    #Test to extract iso8601 date with a timestamp separated by a tab
    def test_extract_date_iso8601_with_timestamp_tab(self):
        self.assert_extract('I was born on 2015-07-25   18:22:19.123', library.dates_iso8601, '2015-07-25   18:22:19.123')

    #Test to extract iso8601 date with a timestamp with minute precision
    def test_extract_date_iso8601_timestamp_minutes(self):
        self.assert_extract('I was born on 2015-07-25 18:22', library.dates_iso8601, '2015-07-25 18:22')

    #Test to prove iso8601 date with a timestamp has minute precision between 00-59
    def test_extract_date_iso8601_timestamp_proper_minutes(self):
        self.assert_extract('I was born on 2015-07-25 18:65', library.dates_iso8601)

    #Test to extract iso8601 date with a timestamp with second precision
    def test_extract_date_iso8601_timestamp_seconds(self):
        self.assert_extract('I was born on 2015-07-25 18:22:19', library.dates_iso8601, '2015-07-25 18:22:19')

    #Test to prove iso8601 date with a timestamp has second precision between 00-59
    def test_extract_date_iso8601_timestamp_proper_seconds(self):
        self.assert_extract('I was born on 2015-07-25 18:22:69', library.dates_iso8601)

    #Test to extract iso8601 date with a timestamp with a 3-letter timezone specifier
    def test_extract_date_iso8601_with_timezone(self):
        self.assert_extract('I was born on 2015-07-25 18:22:19.123 MDT', library.dates_iso8601, '2015-07-25 18:22:19.123 MDT')

    #Test to extract iso8601 date with a timestamp with a 'Z' timezone specifier
    def test_extract_date_iso8601_with_Z_UTC(self):
        self.assert_extract('I was born on 2015-07-25 18:22:19.123 Z', library.dates_iso8601, '2015-07-25 18:22:19.123 Z')

    #Test to extract iso8601 date with a timestamp with an offset timezone specifier
    def test_extract_date_iso8601_with_offset_timezone(self):
        self.assert_extract('I was born on 2015-07-25 18:22:19.123 -0800', library.dates_iso8601, '2015-07-25 18:22:19.123 -0800')

    #Test to prove iso8601 date has an offset timezone specifier with the first two digits between 00-24
    def test_extract_date_iso8601_proper_timezone_offset_hours(self):
        self.assert_extract('I was born on 2015-07-25 18:22:19.123 -2700', library.dates_iso8601)

    #Test to prove iso8601 date has an offset timezone specifier with the second two digits between 00-59
    def test_extract_date_iso8601_proper_timezone_offset_minutes(self):
        self.assert_extract('I was born on 2015-07-25 18:22:19.123 -0877', library.dates_iso8601)

    #Test to extract 'dd Mon, Year' date    #Test to extract 'dd Mon Year' date
    def test_extract_date_no_hyphens_with_comma(self):
        self.assert_extract('I was born on 25 Jan, 2017', library.dates_ddMonYear)

    #Test to prove we can find numbers delimited with a comma '1,234,567'
    def test_integers_with_commas_one_digit_prefix(self):
        self.assert_extract('I have $1,234,567', library._integer_pat, '1,234,567')

    #Test to prove we can find numbers delimited with a comma '12,345,678'
    def test_integers_with_commas_two_digit_prefix(self):
        self.assert_extract('I have $12,345,678', library._integer_pat, '12,345,678')

    #Test to prove we can find numbers delimited with a comma '123,456,789'
    def test_integers_with_commas_three_digit_prefix(self):
        self.assert_extract('I have $123,456,789', library._integer_pat, '123,456,789')

if __name__ == '__main__':
    unittest.main()
