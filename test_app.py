import pytest

from main import compute_inside_parentheses, handle_parentheses


def run_from_string(input_string):
    inputs = input_string.split()

    opened_parentheses_counter = None
    parentheses_content_concatenation = ""
    digit_concatenation = ""
    previous_character = None
    operator = None
    previous_result = None
    result = None
    previous_digit_concatenation = None
    previous_term = None
    previous_operator = None
    term = None
    previous_factor = None

    for user_input in inputs:
        (
            opened_parentheses_counter,
            parentheses_content_concatenation,
            digit_concatenation,
            previous_character,
            operator,
            previous_result,
            result,
            previous_digit_concatenation,
            previous_term,
            previous_operator,
            term,
            previous_factor,
        ) = handle_parentheses(
            user_input,
            opened_parentheses_counter,
            parentheses_content_concatenation,
            digit_concatenation,
            previous_character,
            operator,
            previous_result,
            result,
            previous_digit_concatenation,
            previous_term,
            previous_operator,
            term,
            previous_factor
        )

    return result


def test_concatenation():
    input_string = "1 1 ?"
    assert run_from_string(input_string) == 11


def test_addition():
    input_string = "1 + 20 + 30 ?"
    assert run_from_string(input_string) == 51


def test_subtraction():
    input_string = "1 0 - 2 - 1 1 ?"
    assert run_from_string(input_string) == -3


def test_concatenation_multiplication():
    input_string = "1 1 * 2 ?"
    assert run_from_string(input_string) == 22


def test_concatenation_multiplication2():
    input_string = "1 1 * 2 * 3 1 ?"
    assert run_from_string(input_string) == 682


def test_concatenation_multiplication_concatenation():
    input_string = "1 1 * 2 ? 1 ?"
    assert run_from_string(input_string) == 231


def test_concatenation_multiplication_concatenation_addition():
    input_string = "1 1 * 2 ? 1 + 3 ?"
    assert run_from_string(input_string) == 234


def test_concatenation_multiplication_division():
    input_string = "1 2 * 2 / 3 ?"
    assert run_from_string(input_string) == 8


def test_multiplication_priority():
    input_string = "1 1 * 2 ? 1 + 3 ? * 7 ? "
    assert run_from_string(input_string) == 252


def test_division_priority():
    input_string = "1 1 * 2 ? 1 + 3 ? * 7 ? + 10 / 5 ?"
    assert run_from_string(input_string) == 254


def test_double_operator_error():
    input_string = "1 1 * 2 ? 1 + 3 ? * 7 ? + + 8 7 9 ?"
    with pytest.raises(Exception):
        run_from_string(input_string)


def test_parentheses():
    input_string = "3 * ( 2 + 5 ) ?"
    assert run_from_string(input_string) == 21


def test_parentheses2():
    input_string = "3 + ( 2 + 5 ) * 1 0 ?"
    assert run_from_string(input_string) == 73


def test_parentheses3():
    input_string = "( 2 + 5 ) * 1 0 ?"
    assert run_from_string(input_string) == 70


def test_opened_parentheses_error():
    input_string = "1 0 + (2 ?"
    with pytest.raises(Exception):
        run_from_string(input_string)


def test_starting_with_close_parentheses_error():
    input_string = ")"
    with pytest.raises(Exception):
        run_from_string(input_string)


def test_unmatched_close_parentheses_error():
    input_string = "3 * ( 2 + 5 )) ?"
    with pytest.raises(Exception):
        run_from_string(input_string)


def test_parentheses_priority():
    input_string = "1 0 + ( 2 + 3 ) * 5 + 2 ?"
    assert run_from_string(input_string) == 37


def test_negative_parentheses():
    input_string = "3 + 4 * ( 2 - 6 ) ?"
    assert run_from_string(input_string) == -13


def test_negative_parentheses2():
    input_string = "3 + 4 + ( 2 - 6 ) ?"
    assert run_from_string(input_string) == 3


def test_negative_parentheses3():
    input_string = "( 2 - 6 ) * 1 0 ?"
    assert run_from_string(input_string) == -40


def test_negative_parentheses4():  # todo: fix
    input_string = "3 + 4 * ( 2 - 6 ) * 1 0 ?"
    assert run_from_string(input_string) == -157


def test_double_parentheses_priority():  # todo: fix
    input_string = "3 * ( 9 + ( 7 + 4 ) * 2 ) ?"
    assert run_from_string(input_string) == 93


def test_triple_parentheses_priority():  # todo: fix
    input_string = "1 0 + ( 2 + 3 * ( 9 + ( 7 + 4 ) * 2 ) ) * 5 ?"
    assert run_from_string(input_string) == 485
